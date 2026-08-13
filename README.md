# Bridge — an AI Engagement Associate

**Team 07 · Aberdeen Advisors**

A consulting team decides things in meetings and Slack. Those decisions live in transcripts nobody re-reads. Bridge turns the conversation into a maintained record — actions, decisions, risks and meetings — and refuses to let anything count until a human has checked it.

Two rules define the whole product:

1. **Nothing enters a register without the verbatim sentence that created it, and a link back to it.**
2. **Nothing counts until a human PM verifies it.** Claude proposes; a person decides.

Everything below exists to serve those two rules.

---

## The flow, end to end

```
  Slack channel                GitHub Actions                  Vercel
  ─────────────                ──────────────                  ──────
  someone posts a         ┌─►  slack_pull.py                   index.html
  transcript or talks     │      reads the channel + threads   (static, no
        │                 │      saves Claude's JSON batches    build step)
        ▼                 │            │                            ▲
  @Claude reads it        │            ▼                            │
  and replies with a      │      extract.py                         │
  fenced JSON batch  ─────┘        batch → register entries,        │
  (claude-tag-config.txt)          all marked "pending"             │
                                          │                         │
                                          ▼                         │
                                    apply.py                        │
                                      writes the PM's decisions ────┘
                                      back into the registers
                                          ▲
                                          │
  PM opens the app, verifies, fixes a missing owner,
  clicks Export → drops the file in data/inbox/decisions/
```

Every arrow is automated except the two a human should own: saying something in Slack, and deciding whether Claude got it right.

---

## The four pieces

### 1. Claude Tag — the input layer

`claude-tag-config.txt` is the system prompt for **Claude in Slack**, pasted into the channel's Claude configuration. It does one job: turn what people said into a **fenced JSON block** of candidates. It is written to refuse rather than guess.

- No owner was named → `"owner": null` and `"unclear": ["owner"]`. Never a guess.
- No date was stated → `"due": null`. "Friday the twenty-first" is the 21st, not the next Friday.
- Cannot quote it verbatim → does not propose it at all.

The batch shape (abridged — the full contract is in the config):

```json
{ "batch": "slack-2026-08-13-2053", "items": [
  { "candidateId": "TAG-20260813-09", "register": "action",
    "title": "Provide updated network segmentation testing status",
    "owner": "Jennifer Lee", "due": "2026-08-21", "meetingId": "TAG-20260813-07",
    "provenance": { "author": "Anjali Kalavar", "permalink": "https://…/p1786654225628899",
                    "quote": "Jennifer, please provide an updated network segmentation testing status …" },
    "verification": { "status": "pending" }, "unclear": [] } ] }
```

`register` is one of `action`, `decision`, `risk`, `meeting`. An item carrying a `meetingId` is bound to the meeting from the same batch — that binding is what puts commitments on the calendar next to the meeting that produced them.

### 2. GitHub Actions — the back end

`.github/workflows/bridge-ingest.yml` is the whole server. No laptop, no always-on host.

| Step | Script | What it does |
|---|---|---|
| Pull from Slack | `scripts/slack_pull.py` | Reads the channel *and every thread*, harvests JSON batches, saves them to `data/inbox/candidates/` |
| Extract | `scripts/extract.py` | Turns batches into register entries, all `pending`, and links items to their meeting |
| Apply decisions | `scripts/apply.py` | Writes the PM's verifications and edits back into the registers |
| Verify | inline | Refuses to publish if `snapshot.js` won't parse, a register is invalid JSON, or `index.html` regained a `fetch()` |
| Commit + publish | inline | Commits the registers, deploys to Vercel from the runner |

Triggers: every 5 minutes on weekdays, a manual **Run workflow** button, and any push touching `data/inbox/**`.

**Standard library only.** No `pip install`, no SDK, no Anthropic API key required — the credential-free path is the default, because extraction judgement already happened in Slack. `ANTHROPIC_API_KEY` is optional and upgrades extraction; nothing depends on it.

Secrets, all optional except the first:

- `SLACK_BOT_TOKEN` — reads the channel (`channels:history`, `groups:history`, `files:read`, `users:read`)
- `GH_PUSH_TOKEN` — a PAT, because the org locks `GITHUB_TOKEN` to read-only. Without it the run still completes and uploads the registers as an artifact
- `VERCEL_TOKEN` — deploys from the runner, so the Vercel project needs no GitHub connection

Two failure modes the workflow is built around: it never fails the run on a Slack error (files already in the inbox must still ingest), and it skips push events whose commit message starts with `ingest:` so the bot cannot trigger itself in a loop.

### 3. The app — `index.html`

One file. No build step, no dependencies, **no runtime network requests**. It opens by double-clicking from disk, and the hosted copy is the same file.

Data arrives through classic `<script src>` tags assigning `window.BRIDGE_DATA` — because `fetch()` and ES modules are both blocked on `file://`, and a demo that only works behind a server is a demo with a hidden dependency.

Three surfaces, in the order a PM needs them:

- **Needs attention now** — the six things being asked of the team, computed from overdue / unowned / unverified / stale, not typed by hand.
- **Calendar** — meetings with the commitments made in them attached. Underneath, *"Discussed, not on the calendar"*: meetings with no date and actions with no due date. A date-keyed grid structurally cannot show these, and their invisibility is the failure Bridge exists to catch.
- **Action Items** — one register. Rows Claude wrote are flagged `✦ Claude` with the sentence they came from underneath, and are editable **in the column that is missing**: an owner dropdown in OWNER, a date picker in DUE. The ✓ stays disabled until every field Claude refused to guess is filled. There is no second "review" list, because a second list is a second truth.

Clicking a source chip opens the transcript in-app, scrolled to the highlighted line. A link is only rendered when it goes somewhere — an `href="#"` is a citation-shaped hole, so the app says "no link stored" instead.

### 4. Write-back — the loop closing

The page cannot write to disk, so verification decisions leave as a file. **Export changes** downloads `decisions-<timestamp>.json`; drop it in `data/inbox/decisions/` and commit. That path triggers the workflow, `apply.py` patches the registers and regenerates `snapshot.js`, and the decision is now in the data rather than in one browser's local storage.

`apply.py` accepts only `owner`, `due`, `sev`, `status`, `title` from that file — it arrives from a browser download and is not trusted beyond those. It is idempotent (`meta.appliedDecisions`), and a change pointing at an unknown id is reported, never silently dropped.

---

## Repo layout

```
index.html                     the app — the entire front end
claude-tag-config.txt          the Claude in Slack prompt (paste into the channel config)
.github/workflows/             the back end: schedule, pull, extract, apply, verify, deploy
scripts/
  slack_pull.py                channel + thread reader → data/inbox/
  extract.py                   candidates → registers
  apply.py                     the app's decisions → registers
  AUTOMATION.md                how the schedule and near-instant path work
data/
  snapshot.js                  what the app reads (file://-safe classic script)
  transcripts.js               line-indexed sources, so a citation can land on the sentence
  actions|decisions|risks|meetings.json     the registers
  inbox/candidates/            raw Claude Tag batches, as posted
  inbox/decisions/             drop exported decisions here
TEST-PLAN.md                   what a reviewer should try, and what should happen
```

---

## Running it

**Live:** <https://hackathon-build-theta.vercel.app> — hard-reload if you have opened it before, the CDN edge caches `/`.

**Locally — nothing to install.** No Node, no Python, no package manager. The registers are committed, so a fresh clone is a working app.

```bash
git clone https://github.com/Aberdeen-Advisors/hack-team-07     # private repo — needs org access
cd hack-team-07
start index.html      # Windows · macOS: open index.html · or just double-click it
```

It must work with the wifi off. If it doesn't, that's a bug.

**To watch the pipeline rather than the result:** post a transcript in the project channel and tag Claude. Claude replies in-thread with a JSON batch. Then either wait for the 5-minute schedule or press **Run workflow** on Bridge ingest. New items appear in the app flagged `✦ Claude`, unverified, each carrying the sentence it came from.

**To close the loop:** fix a missing owner in the app, verify a row, click **Export**, drop the downloaded `decisions-*.json` into `data/inbox/decisions/`, commit. That push retriggers the workflow, `apply.py` writes the decision into the registers, and the deploy publishes it.

Python is only ever run by the GitHub runner. You never need it on your machine.

---

## Where it's local today

Worth being straight about this, because the gap is smaller than it looks and the shape is deliberate.

**The repo is the database.** Registers are JSON files, and Git is the transaction log — every change to the record is a commit with an author and a diff. That is a real audit trail for free, and for one engagement with a handful of PMs it is genuinely the right call: no schema migrations, no hosting bill, no service to keep alive, and the whole state is greppable.

It is also the ceiling. Concurrent verification by two PMs would race on the same file; the registers are rewritten wholesale rather than patched per-row; and history is a `git log` rather than something queryable.

**The swap is confined to one function.** The app reads `window.BRIDGE_DATA` from a classic `<script src>` and nothing else — no data access is scattered through the UI. Pointing it at Postgres, Airtable or a Supabase endpoint means replacing how `snapshot.js` is produced, not rewriting the app. On the write side, `apply.py` is already the single choke point for changes going back in; it would become an API call instead of a file rewrite. The provenance contract, the verification gate and the register shape all survive that change untouched, because none of them assume a file.

**The one genuinely manual hop** is the decisions file: the browser downloads it, you drop it in a folder. That exists because the page has no server and refuses to pretend otherwise — an app that shows "Saved!" while nothing left the tab is the exact dishonesty this project is arguing against. With any backend, that hop is a `POST` and disappears.

**Not yet plug-and-play, and close.** Standing this up on a second engagement today means: create the channel, paste `claude-tag-config.txt` into its Claude configuration, set three repo secrets, change one channel ID. Perhaps twenty minutes, all of it configuration rather than code. What's missing for a product is multi-tenancy (one repo currently means one engagement), auth on the hosted view (it is public and read-only by design for the demo), and outbound Slack nudges — deliberately left out because it needs a `chat:write` scope, and a half-built thing that messages your client's team is worse than no thing.

---

## The local gate

Every change is held to this, with the wifi off. A green hosted build proves nothing this does not.

- [ ] Opens from `file://` by double-clicking — no server
- [ ] Zero console errors, zero outbound network requests after a hard reload
- [ ] Renders in Poppins (embedded base64 `woff2`, never a CDN — typography cannot depend on a conference network)
- [ ] Every register row shows a source, or says plainly that it has none
- [ ] Nothing in the UI reports success for something that did not happen

```bash
grep -c 'fetch('  index.html      # expect 0
grep -c 'type="module"' index.html # expect 0
node --check data/snapshot.js      # must parse
```

---

---

## The one thing it refuses to do

Bridge does not silently improve on the source. If nobody named an owner, Claude returns `null`, the app shows an empty amber box, and verification stays blocked until a person fills it in.

Guessing would have been easy and would have demoed better — every row full, every date populated. It is also exactly how project trackers quietly become fiction: a plausible owner nobody agreed to, a due date nobody said. A record you have to double-check is worth less than no record at all, so the gaps are left visible and in your way until someone settles them.
