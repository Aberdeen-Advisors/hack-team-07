#!/usr/bin/env python3
"""
Bridge — apply the app's verification decisions back into the registers.

The page cannot write to disk, so "Export changes" downloads a decisions file. Drop it
into data/inbox/decisions/ and this closes the loop: the same registers the ingest writes
get patched, snapshot.js is regenerated, and the next page load shows the decision as
permanent rather than as browser-local state.

    python3 scripts/apply.py

Standard library only. Idempotent: a decisions file is applied once and recorded in
meta.appliedDecisions, so re-running never double-applies.
"""
import json, os, re, glob, datetime, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEC = os.path.join(ROOT, 'data', 'inbox', 'decisions')
dpath = lambda *p: os.path.join(ROOT, 'data', *p)

# Only fields a human is allowed to settle in the app. Anything else in a decisions file
# is ignored rather than trusted — the file arrives from a browser download.
FIELDS = {'owner', 'due', 'sev', 'severity', 'status', 'title'}


def node_json(js_path, var):
    """Read `window.VAR = {...};` out of a classic script file."""
    src = open(js_path, encoding='utf-8').read()
    i = src.index('window.' + var)
    i = src.index('=', i) + 1
    j = src.rindex(';', i)
    return json.loads(src[i:j].strip())


def main():
    os.makedirs(DEC, exist_ok=True)
    meta = json.load(open(dpath('meta.json'), encoding='utf-8'))
    applied = set(meta.get('appliedDecisions', []))
    files = [f for f in sorted(glob.glob(os.path.join(DEC, '*.json')))
             if os.path.basename(f) not in applied and os.path.getsize(f) > 0]
    if not files:
        print('no new decision files in data/inbox/decisions/')
        return 0

    snap = open(dpath('snapshot.js'), encoding='utf-8').read()
    DATA = node_json(dpath('snapshot.js'), 'BRIDGE_DATA')
    by_id = {it['id']: it for it in DATA['items']}

    verified = rejected = edited = skipped = 0
    log = []
    for path in files:
        name = os.path.basename(path)
        try:
            payload = json.load(open(path, encoding='utf-8'))
        except json.JSONDecodeError as e:
            print('::warning::%s would not parse (%s) — left in place' % (name, e))
            continue
        actor = payload.get('actor') or 'unknown'
        for ch in payload.get('changes', []):
            it = by_id.get(ch.get('registerId'))
            if not it:
                skipped += 1
                continue
            when = ch.get('actedAt') or datetime.datetime.now().isoformat(timespec='seconds')
            who = ch.get('actor') or actor
            act = ch.get('action')
            if act == 'approved':
                it['verification'] = {'status': 'verified', 'decidedBy': who,
                                      'decidedAt': when, 'note': ch.get('note')}
                verified += 1
            elif act == 'rejected':
                it['verification'] = {'status': 'rejected', 'decidedBy': who,
                                      'decidedAt': when, 'note': ch.get('note')}
                rejected += 1
            elif act == 'edited':
                for k, v in (ch.get('fields') or {}).items():
                    if k not in FIELDS:
                        continue
                    key = 'sev' if k == 'severity' else k
                    it[key] = v
                    # a field a person settled is no longer unclear
                    if isinstance(it.get('unclear'), list):
                        it['unclear'] = [u for u in it['unclear'] if u not in (k, key)]
                    edited += 1
            log.append('%s %s%s by %s' % (act, ch.get('registerId'),
                                          (' ' + ','.join((ch.get('fields') or {}).keys())) if act == 'edited' else '',
                                          who))
        applied.add(name)

    meta['appliedDecisions'] = sorted(applied)
    meta['generatedAt'] = datetime.datetime.now().isoformat(timespec='seconds')

    hdr = snap[:snap.index('window.BRIDGE_META')]
    open(dpath('snapshot.js'), 'w', encoding='utf-8').write(
        hdr + 'window.BRIDGE_META = ' + json.dumps(meta, ensure_ascii=False) + ';\n'
        + 'window.BRIDGE_DATA = ' + json.dumps(DATA, ensure_ascii=False) + ';\n')
    json.dump(meta, open(dpath('meta.json'), 'w', encoding='utf-8'), indent=2)
    for f, key, kinds in [('actions.json', 'actions', ['Action']),
                          ('decisions.json', 'decisions', ['Decision']),
                          ('risks.json', 'risks', ['Risk', 'Blocker', 'Issue'])]:
        d = json.load(open(dpath(f), encoding='utf-8'))
        d['meta'] = meta
        d[key] = [i for i in DATA['items'] if i['kind'] in kinds]
        json.dump(d, open(dpath(f), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

    summary = ('%d verified, %d rejected, %d field edit(s) applied from %d file(s)%s'
               % (verified, rejected, edited, len(files),
                  ('; %d change(s) referenced ids not in the register' % skipped) if skipped else ''))
    print(summary)
    for l in log:
        print('  ' + l)
    open(os.path.join(ROOT, 'ingest-report.txt'), 'a', encoding='utf-8').write(summary + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
