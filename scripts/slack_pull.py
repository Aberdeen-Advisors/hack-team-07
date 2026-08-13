#!/usr/bin/env python3
"""
Bridge — pull new Slack messages and posted transcript files into data/inbox/.

Standard library only. No SDK, no pip install. Runs on a stock GitHub runner.
Does nothing at all unless SLACK_BOT_TOKEN is set, so it is safe to leave wired up
before the token exists.

    SLACK_BOT_TOKEN   xoxb-… from a workspace-installed app
    SLACK_CHANNEL_ID  defaults to the team's dev channel

Scopes needed on the app: channels:history, groups:history, channels:read,
groups:read, files:read, users:read.

Output: one file per posted transcript, plus a digest of loose messages, written to
data/inbox/transcripts/. scripts/extract.py then turns those into register entries —
this script never touches the registers itself.
"""
import json, os, re, sys, urllib.request, urllib.parse, datetime

TOKEN = os.environ.get('SLACK_BOT_TOKEN', '').strip()
CHANNEL = os.environ.get('SLACK_CHANNEL_ID', 'C0BPZH0JXD4').strip()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(ROOT, 'data', 'inbox', 'transcripts')
META = os.path.join(ROOT, 'data', 'meta.json')
API = 'https://slack.com/api/'


def call(method, **params):
    url = API + method + ('?' + urllib.parse.urlencode(params) if params else '')
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + TOKEN})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if not data.get('ok'):
        raise SystemExit('slack %s failed: %s' % (method, data.get('error')))
    return data


def download(url):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + TOKEN})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8', 'replace')


def slug(s, fallback):
    s = re.sub(r'[^a-z0-9]+', '', (s or '').lower())[:24]
    return s or fallback


def main():
    if not TOKEN:
        print('SLACK_BOT_TOKEN not set — skipping the Slack pull.')
        return 0

    meta = json.load(open(META, encoding='utf-8')) if os.path.exists(META) else {}
    oldest = meta.get('lastSlackTs', '0')
    os.makedirs(INBOX, exist_ok=True)

    hist = call('conversations.history', channel=CHANNEL, limit=100, oldest=oldest)
    msgs = sorted(hist.get('messages', []), key=lambda m: float(m.get('ts', 0)))
    if not msgs:
        print('no new Slack messages since', oldest)
        return 0

    names, written, loose = {}, [], []

    def who(uid):
        if not uid:
            return 'Unknown'
        if uid not in names:
            try:
                names[uid] = call('users.info', user=uid)['user'].get('real_name', uid)
            except SystemExit:
                names[uid] = uid
        return names[uid]

    for m in msgs:
        if m.get('subtype') in ('channel_join', 'channel_leave'):
            continue
        ts = m.get('ts', '0')
        stamp = datetime.datetime.fromtimestamp(float(ts)).strftime('%H:%M:%S')

        for f in m.get('files', []) or []:
            if not (f.get('mimetype', '').startswith('text/') or
                    f.get('name', '').endswith(('.txt', '.md', '.vtt'))):
                continue
            src = f.get('url_private_download') or f.get('url_private')
            if not src:
                continue
            body = download(src)
            name = slug(f.get('title') or f.get('name'), 'slackfile' + ts.replace('.', ''))
            path = os.path.join(INBOX, name + '.md')
            if os.path.exists(path):
                continue
            open(path, 'w', encoding='utf-8').write(body)
            written.append(os.path.basename(path))

        text = (m.get('text') or '').strip()
        if text and not m.get('files'):
            text = re.sub(r'<@([A-Z0-9]+)(\|[^>]*)?>', lambda x: '@' + who(x.group(1)), text)
            text = re.sub(r'<(https?://[^|>]+)(\|[^>]*)?>', r'\1', text)
            loose.append('[%s] %s: %s' % (stamp, who(m.get('user')), text.replace('\n', ' ')))

    if loose:
        day = datetime.date.today().isoformat()
        path = os.path.join(INBOX, 'slack%s.md' % day.replace('-', ''))
        header = ['# Slack channel digest — %s' % day, '',
                  'Pulled from Slack by scripts/slack_pull.py. Each line is one message.', '']
        existing = open(path, encoding='utf-8').read().split('\n') if os.path.exists(path) else header
        open(path, 'w', encoding='utf-8').write('\n'.join(existing + loose) + '\n')
        written.append(os.path.basename(path))

    meta['lastSlackTs'] = msgs[-1]['ts']
    meta['lastSlackPull'] = datetime.datetime.now().isoformat(timespec='seconds')
    json.dump(meta, open(META, 'w', encoding='utf-8'), indent=2)

    print('pulled %d message(s) from %s; wrote: %s'
          % (len(msgs), CHANNEL, ', '.join(sorted(set(written))) or 'nothing new'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
