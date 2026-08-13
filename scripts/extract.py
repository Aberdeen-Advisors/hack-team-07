#!/usr/bin/env python3
"""
Bridge ingest — credential-free extraction pass.

Reads every transcript in data/inbox/transcripts/ that meta.json has not recorded as
ingested, pulls candidate register entries out of them, and writes the registers plus
the snapshot the app reads.

No API key, no Slack token, no network. It runs in GitHub Actions on a stock ubuntu
runner with nothing configured, which is the point: the pipeline proves itself.

What it cannot do, and does not pretend to: judge nuance. It finds commitments,
decisions and risks by the shape of the sentence. Anything it is unsure of gets
confidence "low" and still arrives pending, because a human verifies everything anyway.
When an ANTHROPIC_API_KEY exists, scripts/ingest.md replaces this with a real
extraction pass over the same inputs and the same output contract.

Usage:  python3 scripts/extract.py            # ingest anything new
        python3 scripts/extract.py --force    # re-ingest everything
"""
import json, os, re, subprocess, sys, datetime, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(ROOT, 'data', 'inbox', 'transcripts')
FORCE = '--force' in sys.argv
# Pattern extraction is OFF by default. Claude Tag's structured JSON is the input;
# regex over raw dialogue produces plausible-looking rubbish ("Fine", "Thanks", "Me")
# and this product's whole claim is that the record can be trusted.
# Turn it on deliberately with --patterns or BRIDGE_ALLOW_PATTERN=1.
ALLOW_PATTERN = ('--patterns' in sys.argv) or os.environ.get('BRIDGE_ALLOW_PATTERN') == '1'

SPEAKER = re.compile(r'^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s+([A-Z][A-Za-z.\'-]*(?:\s+[A-Z][A-Za-z.\'-]*){0,3}):\s+(.*)$')

# Sentence shapes that mark a commitment, a decision or a risk.
COMMIT = re.compile(r"\b(I(?:'| wi)ll|I am going to|I'm going to|we(?:'| wi)ll)\b", re.I)
ASSIGN = re.compile(r"\b([A-Z][a-z]+)\s+to\s+([a-z]{3,})", re.I)
DECIDE = re.compile(r"\b(I'?m making the call|the call is|we are not|we're not|is descoped|"
                    r"decision is|my position is a decision|we have decided|is confirmed|migrates into)\b", re.I)
RISK   = re.compile(r"\b(is (?:a )?red|is (?:an )?amber|that'?s (?:a|the) risk|that'?s a red|"
                    r"is not booked|unresolved|we don'?t know the size)\b", re.I)
DATE_EXPLICIT = re.compile(r"\b(?:by|before|on)\s+(?:the\s+)?(?:"
                           r"(\d{1,2})(?:st|nd|rd|th)?\s+of\s+(\w+)|"
                           r"(\w+)\s+the\s+(\d{1,2})(?:st|nd|rd|th)?|"
                           r"(\w+)\s+(\d{1,2})(?:st|nd|rd|th)?)\b", re.I)
DATE_WORD     = re.compile(r"\b(?:by|before|on)\s+(\w+day|tomorrow|today|end of week|eow)\b", re.I)
ORDINALS = {'first':1,'second':2,'third':3,'fourth':4,'fifth':5,'sixth':6,'seventh':7,'eighth':8,
            'ninth':9,'tenth':10,'eleventh':11,'twelfth':12,'thirteenth':13,'fourteenth':14,
            'fifteenth':15,'sixteenth':16,'seventeenth':17,'eighteenth':18,'nineteenth':19,
            'twentieth':20,'twenty-first':21,'twenty-second':22,'twenty-third':23,'twenty-fourth':24,
            'twenty-fifth':25,'twenty-sixth':26,'twenty-seventh':27,'twenty-eighth':28,
            'twenty-ninth':29,'thirtieth':30,'thirty-first':31}
ORD_DATE  = re.compile(r"\b(?:by|before|on)\s+(?:the\s+)?([a-z]+(?:-[a-z]+)?)\s+of\s+(\w+)\b", re.I)
# "by Friday the twenty-first" / "by the eighteenth" — a day number with no month
ORD_DAY   = re.compile(r"\b(?:by|before|on)\s+(?:\w+day\s+)?the\s+([a-z]+(?:-[a-z]+)?|\d{1,2})(?:st|nd|rd|th)?\b", re.I)
MONTHS = {m.lower(): i for i, m in enumerate(
    ['January','February','March','April','May','June','July','August',
     'September','October','November','December'], 1)}
DOW = {d.lower(): i for i, d in enumerate(
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])}


def iso_from(text, base_iso):
    """Resolve a stated date against the meeting date. Explicit dates beat weekday words,
    because 'by Friday the twenty-first' means the 21st, not the next Friday."""
    base = datetime.date.fromisoformat(base_iso)

    m = ORD_DATE.search(text)                       # "by the twenty-first of August"
    if m and ORDINALS.get(m.group(1).lower()) and MONTHS.get(m.group(2).lower()):
        try:
            return datetime.date(base.year, MONTHS[m.group(2).lower()],
                                 ORDINALS[m.group(1).lower()]).isoformat()
        except ValueError:
            pass

    m = ORD_DAY.search(text)                        # "by Friday the twenty-first"
    if m:
        g = m.group(1).lower()
        day = ORDINALS.get(g) or (int(g) if g.isdigit() else None)
        if day:
            month, year = base.month, base.year
            if day < base.day:                      # already past — it means next month
                month, year = (1, year + 1) if month == 12 else (month + 1, year)
            try:
                return datetime.date(year, month, day).isoformat()
            except ValueError:
                pass

    m = DATE_EXPLICIT.search(text)                  # "by 21 of August" / "by August the 21st"
    if m:
        for day, mon in ((m.group(1), m.group(2)), (m.group(4), m.group(3)), (m.group(6), m.group(5))):
            if day and mon and MONTHS.get((mon or '').lower()):
                try:
                    return datetime.date(base.year, MONTHS[mon.lower()], int(day)).isoformat()
                except ValueError:
                    pass

    m = DATE_WORD.search(text)                      # "by Friday" / "by tomorrow"
    if m:
        w = m.group(1).lower()
        if w == 'today':
            return base.isoformat()
        if w == 'tomorrow':
            return (base + datetime.timedelta(days=1)).isoformat()
        if w in ('end of week', 'eow'):
            return (base + datetime.timedelta(days=(4 - base.weekday()) % 7)).isoformat()
        target = DOW.get(w)
        if target is not None:
            ahead = (target - base.weekday()) % 7 or 7
            return (base + datetime.timedelta(days=ahead)).isoformat()
    return None


FILLER = re.compile(r"^(so|then|right|okay|ok|and|well|look|yes|no|yeah|sure|fine|thanks|"
                    r"thank you|great|agreed|understood|exactly|correct|me|good)\b[\s,.:;-]*", re.I)

def clause_at(text, pos):
    """The sentence containing the match — not the first sentence of the utterance."""
    starts = [0] + [m.end() for m in re.finditer(r'(?<=[.!?])\s+', text)]
    ends = [m.start() for m in re.finditer(r'(?<=[.!?])\s+', text)] + [len(text)]
    for a, b in zip(starts, ends):
        if a <= pos < b:
            return text[a:b].strip()
    return text.strip()


def title_of(text):
    t = text.strip()
    prev = None
    while prev != t:                       # strip stacked fillers: "Yes. Fine. I'll do X"
        prev = t
        t = FILLER.sub('', t).lstrip('.,;: ')
    t = re.sub(r'^(I\'ll|I will|I am going to|I\'m going to)\s+', '', t, flags=re.I)
    t = t[:1].upper() + t[1:] if t else t
    t = t.rstrip('.,;:')
    return (t[:104].rsplit(' ', 1)[0] + '…') if len(t) > 106 else t


def worth_keeping(sentence):
    """A commitment is a clause with substance. 'Fine' and 'Thanks' are not entries."""
    words = re.findall(r"[A-Za-z']+", sentence)
    if len(words) < 6:
        return False
    if FILLER.match(sentence) and len(words) < 9:
        return False
    return True


def header_meta(lines, slug):
    """Title and date from the transcript header, falling back to the filename."""
    head = '\n'.join(lines[:12])
    d = re.search(r'(20\d{2}-\d{2}-\d{2})', head) or re.search(r'(20\d{2}-\d{2}-\d{2})', slug)
    date = d.group(1) if d else None
    if not date:
        m = re.search(r'(\d{1,2})\s+(\w+)\s+(20\d{2})', head)
        if m and MONTHS.get(m.group(2).lower()):
            date = datetime.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1))).isoformat()
    cand = [l.lstrip('# ').strip() for l in lines[:12]
            if l.strip() and not l.startswith('[')
            and not re.match(r'^(meeting id|attendees|date|time|participants|recorded)\b', l.strip(), re.I)
            and len(re.findall(r"[A-Za-z']+", l)) >= 3]
    title = cand[0] if cand else slug
    return title[:90], date or datetime.date.today().isoformat()


def extract(path):
    slug = re.sub(r'[^a-z0-9]', '', os.path.basename(path).lower().replace('.md', '').replace('.txt', ''))[:24]
    lines = open(path, encoding='utf-8').read().split('\n')
    title, date = header_meta(lines, os.path.basename(path))

    # Who actually speaks in this transcript. An owner has to be one of them.
    roster = []
    for raw in lines:
        m = SPEAKER.match(raw.strip())
        if m and m.group(2) not in roster:
            roster.append(m.group(2))
    first = {}
    for full in roster:
        first.setdefault(full.split()[0].lower(), full)

    def resolve(name):
        if not name:
            return None
        if name in roster:
            return name
        return first.get(name.split()[0].lower())      # "Tom" -> "Tom Okafor"; unknown -> None

    out = []
    for n, raw in enumerate(lines, 1):
        m = SPEAKER.match(raw.strip())
        if not m:
            continue
        _, who, said = m.groups()
        if len(said) < 30:
            continue
        register = owner = None
        hit = None
        if DECIDE.search(said):
            hit = DECIDE.search(said); register, owner = 'decision', resolve(who) or who
        elif RISK.search(said):
            hit = RISK.search(said); register, owner = 'risk', None
        elif COMMIT.search(said):
            hit = COMMIT.search(said); register, owner = 'action', resolve(who) or who
        else:
            a = ASSIGN.search(said)
            if a and re.search(r'\bto\s+(publish|deliver|send|confirm|secure|produce|draft|circulate|book|chase|raise)\b', said, re.I):
                hit = a
                register = 'action'
                # keep the full name where the transcript gives one
                owner = resolve(a.group(1))
                if not owner:
                    continue        # "the record has to..." is not a person
        if not register:
            continue
        said = clause_at(said, hit.start())
        if not worth_keeping(said):
            continue
        quote = said if len(said) <= 240 else said[:237].rsplit(' ', 1)[0] + '…'
        assert quote.split('…')[0] in raw, 'quote must be verbatim'
        out.append({
            'register': register, 'title': title_of(said), 'detail': said[:400],
            'owner': owner, 'due': iso_from(said, date) if register == 'action' else None,
            'severity': ('R' if re.search(r'is (?:a )?red|that\'?s a red', said, re.I) else 'Y') if register == 'risk' else None,
            'docId': slug, 'line': n, 'author': who, 'quote': quote,
            'confidence': 'medium' if register != 'risk' else 'low',
        })
    # one entry per line, and cap what a single transcript can add
    seen, dedup = set(), []
    for c in out:
        k = c['quote'][:80]
        if k in seen:
            continue
        seen.add(k); dedup.append(c)
    return slug, title, date, lines, dedup[:12]


def node_json(js_path, var):
    # The file may assign several window.* globals; shim window rather than rewriting them.
    src = 'var window = {};\n' + open(js_path, encoding='utf-8').read() \
          + '\nmodule.exports = window.%s;' % var
    tmp = '/tmp/_bridge_%s.cjs' % var
    open(tmp, 'w', encoding='utf-8').write(src)
    r = subprocess.run(['node', '-e', 'console.log(JSON.stringify(require("%s")))' % tmp],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit('could not parse %s: %s' % (js_path, r.stderr[:300]))
    return json.loads(r.stdout)


def ingest_candidates(DATA, meta, seq, existing_quotes):
    """Claude Tag batches: structured candidates that were already judged by a model.

    This is the preferred path. Titles, owners and dates are taken exactly as authored —
    nothing is inferred here. Pattern extraction only ever runs on raw transcripts that
    arrived with no structured counterpart.
    """
    CAND = os.path.join(ROOT, 'data', 'inbox', 'candidates')
    if not os.path.isdir(CAND):
        return [], []
    done = set(meta.get('ingestedFiles', []))
    added, report = [], []
    KIND = {'action': ('Action', 'a'), 'decision': ('Decision', 'd'), 'risk': ('Risk', 'r'),
            'blocker': ('Blocker', 'r'), 'issue': ('Issue', 'r'),
            'deliverable': ('Action', 'a'), 'stakeholder': ('Action', 'a')}
    for path in sorted(glob.glob(os.path.join(CAND, '*.json'))):
        key = 'candidates/' + os.path.basename(path)
        if (key in done and not FORCE) or os.path.getsize(path) == 0:
            continue          # zero-length is an emptied placeholder, not a failure
        try:
            batch = json.load(open(path, encoding='utf-8'))
        except Exception as e:
            print('::warning::unreadable candidate batch %s: %s' % (key, e)); continue
        n = 0
        for c in batch.get('items', []):
            prov = c.get('provenance') or {}
            quote = (prov.get('quote') or '').strip()
            title = (c.get('title') or '').strip()
            if not title:
                continue                      # a candidate with no title is not an entry
            if quote and quote in existing_quotes:
                continue
            kind, pfx = KIND.get((c.get('register') or 'action').lower(), ('Action', 'a'))
            iid = '%s%d' % (pfx, seq[pfx]); seq[pfx] += 1
            unclear = c.get('unclear') or []
            it = {'id': iid, 'kind': kind,
                  'urg': 'High' if (c.get('severity') == 'R' or c.get('priority') == 'high') else 'Med',
                  'title': title, 'owner': c.get('owner') or 'Unassigned',
                  'note': c.get('detail') or '',
                  'ws': c.get('ws'), 'meetingId': c.get('meetingId'), 'relatedTo': c.get('relatedTo'),
                  'provenance': {'sourceSystem': prov.get('sourceSystem') or 'slack',
                                 'channel': prov.get('channel'), 'docId': prov.get('docId'),
                                 'line': prov.get('line'), 'author': prov.get('author'),
                                 'messageTs': prov.get('messageTs'), 'permalink': prov.get('permalink'),
                                 'quote': quote or None,
                                 'confidence': prov.get('confidence') or 'medium'},
                  'verification': {'status': 'pending', 'decidedBy': None, 'decidedAt': None,
                                   'note': 'Proposed by Claude Tag. No person has checked it.'}}
            if kind == 'Action':
                it['due'] = c.get('due'); it['status'] = 'open'
            if kind == 'Decision':
                it['date'] = c.get('decidedOn') or (prov.get('messageTs') or '')[:10]
            if kind in ('Risk', 'Blocker', 'Issue'):
                it['sev'] = c.get('severity') or 'Y'; it['status'] = 'open'
                it['reviewed'] = None; it['due'] = c.get('due')
            if unclear:
                it['unclear'] = unclear        # the app blocks verification until these are filled
            DATA['items'].append(it); added.append(it)
            if quote:
                existing_quotes.add(quote)
            n += 1
        report.append('%s: %d from Claude Tag' % (key, n))
        done.add(key)
    meta['ingestedFiles'] = sorted(done)
    return added, report


def main():
    dpath = lambda *p: os.path.join(ROOT, 'data', *p)
    meta = json.load(open(dpath('meta.json'), encoding='utf-8'))
    done = set() if FORCE else set(meta.get('ingestedFiles', []))

    files = [f for f in sorted(glob.glob(os.path.join(INBOX, '*.md')) + glob.glob(os.path.join(INBOX, '*.txt')))
             if os.path.basename(f) not in done and os.path.getsize(f) > 0]
    cand_files = [f for f in glob.glob(os.path.join(ROOT, 'data', 'inbox', 'candidates', '*.json'))
                  if ('candidates/' + os.path.basename(f)) not in done]
    all_transcripts = [f for f in sorted(glob.glob(os.path.join(INBOX, '*.md')) + glob.glob(os.path.join(INBOX, '*.txt')))
                       if os.path.getsize(f) > 0]
    if not files and not cand_files:
        print('nothing new in data/inbox/'); return 0
    if not ALLOW_PATTERN:
        print('pattern extraction disabled — only Claude Tag JSON batches create entries')

    snap = open(dpath('snapshot.js'), encoding='utf-8').read()
    DATA = node_json(dpath('snapshot.js'), 'BRIDGE_DATA')
    TR = node_json(dpath('transcripts.js'), 'BRIDGE_TRANSCRIPTS')

    nxt = {}
    for pfx in 'adr':
        used = [int(mm.group(1)) for it in DATA['items']
                for mm in [re.match('^%s(\\d+)$' % pfx, it['id'])] if mm]
        nxt[pfx] = (max(used) if used else 0) + 1

    existing_quotes = {(it.get('provenance') or {}).get('quote') for it in DATA['items']}
    # Structured batches first — they win over anything the pattern pass would guess.
    tag_added, tag_report = ingest_candidates(DATA, meta, nxt, existing_quotes)
    done = set(meta.get('ingestedFiles', []))
    KIND = {'action': ('Action', 'a'), 'decision': ('Decision', 'd'), 'risk': ('Risk', 'r')}
    added, report = [], []

    if not ALLOW_PATTERN:
        files = []          # transcripts still get indexed for citations, just not mined
    for path in files:
        slug, title, date, lines, cands = extract(path)
        TR[slug] = {'title': title, 'date': date, 'channel': 'data/inbox/transcripts',
                    'lines': [{'n': i + 1, 'text': l} for i, l in enumerate(lines)]}
        new_here = 0
        for c in cands:
            if c['quote'] in existing_quotes:
                continue
            kind, pfx = KIND[c['register']]
            iid = '%s%d' % (pfx, nxt[pfx]); nxt[pfx] += 1
            it = {'id': iid, 'kind': kind,
                  'urg': 'High' if c['severity'] == 'R' else 'Med',
                  'title': c['title'], 'owner': c['owner'] or 'Unassigned', 'note': c['detail'],
                  'provenance': {'sourceSystem': 'transcript', 'docId': c['docId'], 'line': c['line'],
                                 'author': c['author'], 'messageTs': date, 'permalink': None,
                                 'quote': c['quote'], 'confidence': c['confidence']},
                  'verification': {'status': 'pending', 'decidedBy': None, 'decidedAt': None,
                                   'note': 'Extracted from a transcript by Bridge. No person has checked it.'}}
            if kind == 'Action':
                it['due'] = c['due']; it['status'] = 'open'
            if kind == 'Decision':
                it['date'] = date
            if kind == 'Risk':
                it['sev'] = c['severity']; it['status'] = 'open'; it['reviewed'] = None; it['due'] = None
            DATA['items'].append(it); added.append(it); existing_quotes.add(c['quote']); new_here += 1
        report.append('%s: %d new' % (os.path.basename(path), new_here))
        done.add(os.path.basename(path))

    added = tag_added + added
    report = tag_report + report
    if not added:
        print('no new candidates'); return 0

    meta['generatedAt'] = datetime.datetime.now().isoformat(timespec='seconds')
    meta['ingestedFiles'] = sorted(done)
    meta['source'] = 'scripts/extract.py over data/inbox/transcripts'

    hdr = snap[:snap.index('window.BRIDGE_META')]
    open(dpath('snapshot.js'), 'w', encoding='utf-8').write(
        hdr + 'window.BRIDGE_META = ' + json.dumps(meta, ensure_ascii=False) + ';\n'
        + 'window.BRIDGE_DATA = ' + json.dumps(DATA, ensure_ascii=False) + ';\n')
    tj = open(dpath('transcripts.js'), encoding='utf-8').read()
    open(dpath('transcripts.js'), 'w', encoding='utf-8').write(
        tj[:tj.index('window.BRIDGE_TRANSCRIPTS')]
        + 'window.BRIDGE_TRANSCRIPTS = ' + json.dumps(TR, ensure_ascii=False) + ';\n')
    json.dump(meta, open(dpath('meta.json'), 'w', encoding='utf-8'), indent=2)
    for f, key, kinds in [('actions.json', 'actions', ['Action']),
                          ('decisions.json', 'decisions', ['Decision']),
                          ('risks.json', 'risks', ['Risk', 'Blocker', 'Issue'])]:
        d = json.load(open(dpath(f), encoding='utf-8')); d['meta'] = meta
        d[key] = [i for i in DATA['items'] if i['kind'] in kinds]
        json.dump(d, open(dpath(f), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

    noown = sum(1 for i in added if i['owner'] == 'Unassigned')
    nodate = sum(1 for i in added if i['kind'] == 'Action' and not i.get('due'))
    summary = ('%d candidates extracted, all pending. %d with no owner, %d with no date. %s'
               % (len(added), noown, nodate, '; '.join(report)))
    open(os.path.join(ROOT, 'ingest-report.txt'), 'w', encoding='utf-8').write(
        summary + '\nnew ids: ' + ', '.join(i['id'] for i in added) + '\n')
    print(summary)
    print('new ids:', ', '.join(i['id'] for i in added))
    return 0


if __name__ == '__main__':
    sys.exit(main())
