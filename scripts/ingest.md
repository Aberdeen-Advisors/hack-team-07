# ingest.md — Slack channel → registers

The prompt Claude Code follows to turn a channel into register entries. **This is the sync.**
No server, no Azure, no Claude Tag required: Claude Code reads Slack over the connector and writes the files.

Run it by opening Claude Code in this repo and saying: *"Run scripts/ingest.md against #hack-team-7-app-dev."*

## Channels

| Channel | ID |
|---|---|
| `#hack-team-7-app-dev` (private, test) | `C0BPZH0JXD4` |
| `#hack-team-07` (public, team) | `C0BNB1E5FRP` |

Default to the dev channel. Never ingest a client-adjacent channel into this repo — it is public.

## Steps

1. **Read.** `slack_read_channel` with the channel id, `response_format: detailed`, newest first. For any message with replies, `slack_read_thread` on its `ts`. Transcript files posted as attachments: `slack_read_file`.
2. **Select.** Only messages that contain a commitment, a decision, a risk, a stakeholder fact, or a deliverable. Skip build chatter, joins, and anything addressed to the tooling rather than the programme.
3. **Extract, one candidate per commitment.** For each, capture:
   - `title` — one line, imperative
   - `detail` — what was actually said, plain
   - `owner` — only if a person was named or unambiguously implied, else `null`
   - `due` — ISO date only if stated or derivable, else `null`
   - `ws` — workstream if inferable from the meeting, else `null`
   - `provenance` — `{sourceSystem:'slack', channel, author, messageTs, permalink, quote, confidence}`
   - `verification` — `{status:'pending', decidedBy:null, decidedAt:null, note:'Extracted from Slack. No person has checked it.'}`
4. **The quote must be verbatim.** Copy the sentence exactly as written. If you cannot quote it, do not create the entry.
5. **The permalink must be real.** Build it as `https://aberdeenadv.slack.com/archives/<CHANNEL_ID>/p<ts without the dot>` — e.g. `ts` `1786673636.123456` → `p1786673636123456`. Verify the scheme is `https:`; the app renders anything else as "no link".
6. **Assign ids** in sequence per register from the existing files: `a32`, `a33`, `d9`, `r10`. Never reuse an id. Ids become DOM ids, so no spaces or dots.
7. **Write.** Append to `data/actions.json`, `decisions.json`, `risks.json`, `deliverables.json`, `stakeholders.json`. Update `data/meta.json` `generatedAt`.
8. **Regenerate the snapshot** the app reads: `data/snapshot.js` (`window.BRIDGE_DATA`) and, if transcripts were posted as files, `data/transcripts.js` with line-numbered bodies plus the `.md` originals in `data/inbox/transcripts/`.
9. **Report** before committing: how many commitments were found, how many were already in the registers, how many have no owner, how many have no date.

## Rules

- **Nothing enters a register verified.** Every extracted item is `pending` and waits for a PM in the app.
- **Never guess an owner or a date.** `null` plus the unclear flag is the correct output. The app blocks verification until a human supplies them, which is the point.
- **Do not invent a quote.** No sentence, no entry.
- **Fail loudly.** A message you cannot parse goes to `data/inbox/unparsed-<ts>.json` with its permalink. Silence is the only unacceptable outcome.
- **Confidence.** `high` only when the sentence says it plainly. Anything inferred is `medium` or `low`.
- **Contradictions.** If a new decision conflicts with one already in `decisions.json`, write both and flag it in the report. Never silently supersede.

## Acceptance

- At least five new pending items, each with a verbatim quote and a permalink that opens the real Slack message.
- `git diff` touches only `data/` files.
- The app shows them in **Needs a human**, each with a working citation.
- Clicking a citation opens Slack at that message.

## Then

`npx vercel --prod` to publish, and `git push` so the repo matches.
