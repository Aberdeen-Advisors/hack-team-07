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

SPEAKER = re.compile(r'^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s+([A-Z][A-Za-z.\'-]*(?:\s+[A-Z][A-Za-z.\'-]*){0,3}):\s+(.*)$')

# Sentence shapes that mark a commitment, a decision or a risk.
COMMIT = re.compile(r"\b(I(?:'| wi)ll|I am going to|I'm going to|we(?:'| wi)ll)\b", re.I)
ASSIGN = re.compile(r"\b([A-Z][a-z]+)\s+to\s+([a-z]{3,})", re.I)
DECIDE = re.compile(r"\b(I'?m making the call|the call is|we are not|we're not|is descoped|"
                    r"decision is|my position is a decision|we have decided|is confirmed|migrates into)\b", re.I)
RISK   = re.compile(r"\b(is (?:a )?red|is (?:an )?amber|that'?s (?:a|the) risk|that'?s a red|"
                    r"is not booked|unresolved|we don'?t know the size)\b", re.I)
DATE   = re.compile(r"\bby\s+(?:the\s+)?(?:(\w+day)|(\d{1,2})(?:st|nd|rd|th)?\s+of\s+(\w+)|"
                    r"(\w+)\s+the\s+(\d{1,2})(?:st|nd|rd|th)?)\b", re.I)
MONTHS = {m.lower(): i for i, m in enumerate(
    ['January','February','March','April','May','June','July','August',
     'September','October','November','December'], 1)}
DOW = {d.lower(): i for i, d in enumerate(
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])}


def iso_from(text, base_iso):
    """Resolve 'by the twenty-first of August' / 'by Wednesday' against the meeting date."""
    m = DATE.search(text)
    if not m:
        return None
    base = datetime.date.fromisoformat(base_iso)
    if m.group(1):                                        # by <weekday>
        target = DOW.get(m.group(1).lower())
        if target is None:
            return None
        ahead = (target - base.weekday()) % 7 or 7
        return (base + datetime.timedelta(days=ahead)).isoformat()
    if m.group(2) and m.group(3):                          # by the 21st of August
        mon = MONTHS.get(m.group(3).lower())
        if mon:
            return datetime.date(base.year, mon, int(m.group(2))).isoformat()
    if m.group(4) and m.group(5):                          # by August the 21st
        mon = MONTHS.get(m.group(4).lower())
        if mon:
            return datetime.date(base.year, mon, int(m.group(5))).isoformat()
    return None


def title_of(text):
    t = re.sub(r'^(so|then|right|okay|ok|and|well|look)[,\s]+', '', text.strip(), flags=re.I)
    t = re.split(r'(?<=[a-z])[.?!]\s', t)[0].strip().rstrip('.,;:')
    return (t[:110].rsplit(' ', 1)[0] + '…') if len(t) > 112 else t


def header_meta(lines, slug):
    """Title and date from the transcript header, falling back to the filename."""
    head = '\n'.join(lines[:12])
    d = re.search(r'(20\d{2}-\d{2}-\d{2})', head) or re.search(r'(20\d{2}-\d{2}-\d{2})', slug)
    date = d.group(1) if d else None
    if not date:
        m = re.search(r'(\d{1,2})\s+(\w+)\s+(20\d{2})', head)
        if m and MONTHS.get(m.group(2).lower()):
            date = datetime.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1))).isoformat()
    title = next((l.lstrip('# ').strip() for l in lines[:6] if l.strip() and not l.startswith('[')), slug)
    return title[:90], date or datetime.date.today().isoformat()


def extract(path):
    slug = re.sub(r'[^a-z0-9]', '', os.path.basename(path).lower().replace('.md', '').replace('.txt', ''))[:24]
    lines = open(path, encoding='utf-8').read().split('\n')
    title, date = header_meta(lines, os.path.basename(path))
    out = []
    for n, raw in enumerate(lines, 1):
        m = SPEAKER.match(raw.strip())
        if not m:
            continue
        _, who, said = m.groups()
        if len(said) < 30:
            continue
        register = owner = None
        if DECIDE.search(said):
            register, owner = 'decision', who
        elif RISK.search(said):
            register, owner = 'risk', None
        elif COMMIT.search(said):
            register, owner = 'action', who
        else:
            a = ASSIGN.search(said)
            if a and re.search(r'\bto\s+(publish|deliver|send|confirm|secure|produce|draft|circulate|book|chase|raise)\b', said, re.I):
                register, owner = 'action', a.group(1)
        if not register:
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


def main():
    dpath = lambda *p: os.path.join(ROOT, 'data', *p)
    meta = json.load(open(dpath('meta.json'), encoding='utf-8'))
    done = set() if FORCE else set(meta.get('ingestedFiles', []))

    files = [f for f in sorted(glob.glob(os.path.join(INBOX, '*.md')) + glob.glob(os.path.join(INBOX, '*.txt')))
             if os.path.basename(f) not in done]
    if not files:
        print('nothing new in data/inbox/transcripts/'); return 0

    snap = open(dpath('snapshot.js'), encoding='utf-8').read()
    DATA = node_json(dpath('snapshot.js'), 'BRIDGE_DATA')
    TR = node_json(dpath('transcripts.js'), 'BRIDGE_TRANSCRIPTS')

    nxt = {}
    for pfx in 'adr':
        used = [int(mm.group(1)) for it in DATA['items']
                for mm in [re.match('^%s(\\d+)$' % pfx, it['id'])] if mm]
        nxt[pfx] = (max(used) if used else 0) + 1

    existing_quotes = {(it.get('provenance') or {}).get('quote') for it in DATA['items']}
    KIND = {'action': ('Action', 'a'), 'decision': ('Decision', 'd'), 'risk': ('Risk', 'r')}
    added, report = [], []

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
