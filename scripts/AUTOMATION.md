# Automation — how Bridge stays current without anyone's laptop

The pipeline is three prompt files and one workflow. Nothing runs on a personal machine and
nothing depends on a signed-in session.

```
data/inbox/**  ──┐
                 ├─→  .github/workflows/bridge-ingest.yml  ──→  scripts/ingest.md
Slack channel  ──┘         (cron, or a push, or a button)          │
                                                                   ▼
                                                         data/*.json + snapshot.js
                                                                   │
                                          commit ──→ Vercel deploy hook ──→ live app
                                                                   │
                                          PM verifies in the app ──┘
                                                   │
                                     pending-changes.json ──→ scripts/apply.md
```

## What runs, and when

| Trigger | Effect |
|---|---|
| Every 30 min, 9am–6pm ET, weekdays | Reads unprocessed sources, updates the registers |
| Push touching `data/inbox/**` | Immediate ingest — drop a transcript, it appears |
| **Run workflow** button | On demand, for a demo |

Every extracted item lands `verification.status: pending`. **The job never verifies anything** — that is a human PM in the app, and the decisions come back through `scripts/apply.md`.

## Setup — three secrets, in order of effort

Settings → Secrets and variables → Actions → New repository secret.

### 1. `ANTHROPIC_API_KEY` — required, self-serve

From the Anthropic Console. Without it the workflow exits cleanly and logs a notice, so an
unconfigured repo produces no red X's.

**With just this, phase 1 works:** commit a transcript to `data/inbox/transcripts/`, push, and the
registers update themselves and commit back. No Slack, no admin, no waiting.

### 2. `VERCEL_DEPLOY_HOOK_URL` — optional, one click

Vercel → Project → Settings → Git → Deploy Hooks → create one for `main`. Paste the URL in.
Now an ingest publishes itself. Without it the data is committed but you deploy by hand.

### 3. `SLACK_BOT_TOKEN` — phase 2, needs workspace admin

A Slack app installed to the Aberdeen workspace with a bot token (`xoxb-…`) and these scopes:

- `channels:history` — public channel messages
- `groups:history` — private channels, needed for `#hack-team-7-app-dev`
- `channels:read`, `groups:read` — resolve channel metadata
- `files:read` — read posted transcript files

Then invite the app to the channel: `/invite @Bridge`. **This is the only piece that needs someone
else's approval**, and it is the same class of ask as the Azure app registration for SharePoint.
Until it lands, phase 1 covers the demo: a transcript in the repo is a real source with real
line-level citations.

## Why not a scheduled job on a laptop

It works, and it is a worse story. It dies when the machine sleeps, it runs as one person's
account, and it cannot be handed to a client team. The workflow file is the artifact that makes
"scheduled Claude Code job" a thing you can read rather than a claim on a slide.

## Before you trust the schedule

Run it once with the **Run workflow** button and read the log. Two things to confirm, because they
are the parts most likely to need a tweak on first contact:

1. The `claude -p` invocation — flag names on the CLI move occasionally. If the step fails on
   arguments, check `claude --help` in the log output and adjust that one line.
2. The commit step pushes to `main`. If `main` is protected, either allow the
   `bridge-ingest[bot]` actor or point the workflow at a branch and merge by PR.

The verify step is deliberately strict: it fails the run if any register file stops parsing, if
`snapshot.js` breaks, or if `index.html` regains a `fetch(` call. A broken snapshot must never
reach the deployed app, because that is what gets demoed.
