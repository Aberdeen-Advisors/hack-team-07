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


class SlackError(Exception):
    """Slack said no. Loud in the log, but never fatal to the pipeline."""


def call(method, **params):
    url = API + method + ('?' + urllib.parse.urlencode(params) if params else '')
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + TOKEN})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if not data.get('ok'):
        raise SlackError('%s failed: %s' % (method, data.get('error')))
    return data


def download(url):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + TOKEN})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8', 'replace')


def bare_json_objects(text):
    """Find top-level {...} objects in a message that was posted without a code fence.
    Brace matching, string-aware, so braces inside quotes do not throw it off."""
    out, depth, start, in_str, esc = [], 0, None, False, False
    for i, ch in enumerate(text):
        if in_str:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == '"': in_str = False
            continue
        if ch == '"': in_str = True
        elif ch == '{':
            if depth == 0: start = i
            depth += 1
        elif ch == '}':
            if depth:
                depth -= 1
                if depth == 0 and start is not None:
                    out.append(text[start:i + 1]); start = None
    return out


def slug(s, fallback):
    s = re.sub(r'[^a-z0-9]+', '', (s or '').lower())[:24]
    return s or fallback


def main():
    if not TOKEN:
        print('SLACK_BOT_TOKEN not set — skipping the Slack pull.')
        return 0
    try:
        return pull()
    except SlackError as e:
        # Never fail the run: files already in data/inbox/ must still be ingested.
        print('::warning title=Slack pull skipped::%s' % e)
        print('If this says channel_not_found on a private channel, invite the app to it '
              '(/invite @YourApp) and confirm groups:history + groups:read scopes.')
        return 0
    except Exception as e:
        print('::warning title=Slack pull failed::%s: %s' % (type(e).__name__, e))
        return 0


def pull():

    meta = json.load(open(META, encoding='utf-8')) if os.path.exists(META) else {}
    oldest = meta.get('lastSlackTs', '0')
    os.makedirs(INBOX, exist_ok=True)

    # Page through the whole history, not just the newest 100.
    msgs, cursor, pages = [], None, 0
    while pages < 20:
        params = dict(channel=CHANNEL, limit=200, oldest=oldest)
        if cursor:
            params['cursor'] = cursor
        page = call('conversations.history', **params)
        msgs.extend(page.get('messages', []))
        cursor = (page.get('response_metadata') or {}).get('next_cursor') or None
        pages += 1
        if not cursor:
            break

    # Threads are the trap. conversations.history with `oldest` returns only PARENTS newer
    # than the watermark — so a new reply on an older thread is invisible. Scan recent
    # parents regardless of the watermark, then take replies newer than it.
    try:
        recent = call('conversations.history', channel=CHANNEL, limit=200)
        parents = recent.get('messages', [])
    except SlackError as e:
        print('::warning::could not scan for threads: %s' % e)
        parents = list(msgs)

    seen_parents = set()
    for parent in parents + list(msgs):
        ts = parent.get('ts')
        if not parent.get('reply_count') or ts in seen_parents:
            continue
        seen_parents.add(ts)
        try:
            rep = call('conversations.replies', channel=CHANNEL, ts=ts, limit=200)
            new_in_thread = 0
            for r in rep.get('messages', []):
                if r.get('ts') != ts and float(r.get('ts', 0)) > float(oldest or 0):
                    msgs.append(r); new_in_thread += 1
            if new_in_thread:
                print('  thread %s: %d new reply(ies)' % (ts, new_in_thread))
        except SlackError as e:
            print('::warning::could not read thread %s: %s' % (ts, e))

    seen_ts = set()
    msgs = [m for m in sorted(msgs, key=lambda m: float(m.get('ts', 0)))
            if not (m.get('ts') in seen_ts or seen_ts.add(m.get('ts')))]
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
            except (SlackError, Exception):
                names[uid] = uid   # a missing users:read scope must not lose the message
        return names[uid]

    CAND = os.path.join(ROOT, 'data', 'inbox', 'candidates')
    os.makedirs(CAND, exist_ok=True)
    JSON_BLOCK = re.compile(r'```(?:json)?\s*(\{.*?\})\s*```', re.S)

    def save_candidates(payload, ts, author):
        """A Claude Tag batch: structured candidates, already judged. This is the good path —
        titles, owners and dates are authored, not guessed."""
        if not isinstance(payload, dict) or not isinstance(payload.get('items'), list):
            return False
        payload.setdefault('capturedAt', ts)
        payload.setdefault('postedBy', author)
        path = os.path.join(CAND, 'tag-%s.json' % ts.replace('.', ''))
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return False
        open(path, 'w', encoding='utf-8').write(json.dumps(payload, indent=2, ensure_ascii=False))
        written.append('candidates/' + os.path.basename(path))
        return True

    BOTS = set()                    # Claude Tag's structured output IS a source; loose bot chat is not
    for m in msgs:
        if m.get('subtype') in ('channel_join', 'channel_leave', 'bot_message'):
            continue
        is_bot = bool(m.get('bot_id')) or m.get('user') in ('U0AB8UM5278',)
        text_raw = m.get('text') or ''
        blocks = JSON_BLOCK.findall(text_raw)
        if not blocks and '"items"' in text_raw:
            blocks = bare_json_objects(text_raw)   # posted without a code fence
        got_json = False
        for b in blocks:
            try:
                got_json = save_candidates(json.loads(b), m.get('ts', '0'), m.get('user') or 'bot') or got_json
            except json.JSONDecodeError as e:
                print('::warning::a JSON block would not parse (%s) — asking for a valid one is better than guessing' % e)
        if is_bot:
            continue                # a bot's prose is never a source; its JSON already landed above
        ts = m.get('ts', '0')
        stamp = datetime.datetime.fromtimestamp(float(ts)).strftime('%H:%M:%S')

        for f in m.get('files', []) or []:
            if f.get('name', '').endswith('.json'):
                src = f.get('url_private_download') or f.get('url_private')
                if src:
                    try:
                        save_candidates(json.loads(download(src)), m.get('ts', '0'), m.get('user') or '')
                    except (json.JSONDecodeError, Exception) as e:
                        print('::warning::could not read %s: %s' % (f.get('name'), e))
                continue
            if not (f.get('mimetype', '').startswith('text/') or
                    f.get('name', '').endswith(('.txt', '.md', '.vtt'))):
                continue
            src = f.get('url_private_download') or f.get('url_private')
            if not src:
                continue
            body = download(src)
            name = slug(f.get('title') or f.get('name'), 'slackfile' + ts.replace('.', ''))
            path = os.path.join(INBOX, name + '.md')
            if os.path.exists(path) and os.path.getsize(path) > 0:
                continue          # an emptied placeholder is a request to re-download
            open(path, 'w', encoding='utf-8').write(body)
            written.append(os.path.basename(path))

        text = (m.get('text') or '').strip()
        if text and not m.get('files'):
            text = re.sub(r'<@([A-Z0-9]+)(\|[^>]*)?>', lambda x: '@' + who(x.group(1)), text)
            text = re.sub(r'<(https?://[^|>]+)(\|[^>]*)?>', r'\1', text)
            text = (text.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&'))
            text = re.sub(r'^\s*>+\s*', '', text)      # Slack blockquote marker
            loose.append('[%s] %s: %s' % (stamp, who(m.get('user')), text.replace('\n', ' ')))

    if loose:
        day = datetime.date.today().isoformat()
        path = os.path.join(INBOX, 'slack%s.md' % day.replace('-', ''))
        header = ['# Slack channel digest — %s' % day, '',
                  'Pulled from Slack by scripts/slack_pull.py. Each line is one message.', '']
        prior = open(path, encoding='utf-8').read().strip() if os.path.exists(path) else ''
        existing = prior.split('\n') if prior else header
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
