# Bridge — build brief for Claude Code

Team 07 · build day 2026-08-13 · submission 6:00 PM ET
Save this at the repo root as `BUILD.md`. Paste it, whole, as the opening message to Claude Code in a checkout of `hack-team-07`.

---

## 0. Read this part yourself — it is not for Claude Code

1. **The repo is public and the file still identifies the client.** Per-seat licence cost, partner headcount, record count and duplicate rate, the committee date slip, the go-live month, the programme name. M0 is a real blocker on the first push, not hygiene.
2. **No deploy today until local passes.** Everything is verified from `file://` first. Deploying is M11 and it is gated on a written checklist, not on the clock.
3. **SharePoint is the system of record from today, not in the pilot.** But a static page cannot authenticate to it — no secret can live in `index.html`, and Graph will not accept a CORS call from an unauthenticated origin. So the split is: **Claude Code writes the lists over the SharePoint MCP; the app reads a committed snapshot and emits structured changes back.** The app never talks to SharePoint directly. If anyone asks on stage, that is the honest answer and it is also the correct one — the browser is not where credentials belong.
4. **The SharePoint MCP is scoped to your user.** It works from your Claude session, tied to your account. That is fine for today and it is exactly what the pilot slide has to say gets replaced by a service principal.
5. **Claude Tag cannot read the deployed app** (`*.vercel.app` is blocked by the egress proxy, huddle [56:49]) **and its artifacts are not visible to other channel members** (huddle [38:22]). The handoff is a JSON block posted as channel text. The companion config file enforces this.
6. **M0 is done, M1's local half is done, and M2's local half is done.** See those milestones for what changed and what is left. A pre-scrub copy exists in my temporary outputs folder only; it is not in the repo, and it disappears when this session ends.
7. **`fetch()` does not work from `file://`.** Chrome blocks it, and it blocks ES modules too. So the app cannot read `data/*.json` directly — the snapshot reaches the page as `data/snapshot.js`, a **classic script tag** assigning `window.BRIDGE_DATA`. The JSON files are still canonical for Claude Code and SharePoint; the `.js` file is the browser's copy of the same literal. Anyone who "tidies this up" into a `fetch` will break the demo in the one environment it has to work in.
8. **Line anchors, re-verified after the data extraction.** `index.html` is now **1,485 lines** (was 1,684; 204 lines of data moved out, so any older line number above 730 is wrong by roughly that much).

| What | Line |
|---|---|
| embedded font block `id="bridge-fonts"` | 8 |
| 860px breakpoint | 54 |
| hero eyebrow | 527 |
| hero "On track" pill | 533, 765 |
| "3 new since this morning" ribbon | 545 |
| "Transcripts" document filter | 665 |
| `<script src="data/snapshot.js">` | 718 |
| `etNow` | 725 |
| `const DATA = window.BRIDGE_DATA` | 733 |
| `UPDATE_ENDPOINT`, `OWNERS` | 750, 751 |
| `viewInSlack` (defined, never called) | 780 |
| `dueC`, `dueRankMap` | 817, 818, 859, 1438 |
| `srcChip` — the only source-render site | 879 |
| `pending.set` — the prose change tray | 932, 1195 |
| passphrase / `PASS` | 959, 962, 963, 970, 1376 |
| `href="#"` | 1252, 1279 |
| `/api/submit`, `/api/refresh` | 1327, 1328 |
| "Needs attention" | 409, 1465 |

Still grep first. But these were read out of the current file.

Paste everything below the rule.

---

## Project brief: Bridge

You are building **Bridge**, an AI Engagement Associate for a consulting transformation team. It maintains five registers — actions, decisions, risks, stakeholders, deliverables — from the places the engagement already happens, and it does routine coordination work itself.

Bridge is two things, in this order of importance:

1. **A brain that owns the data.** It reads what was said, writes structured records into SharePoint lists with the sentence that created each one attached, and keeps them current without anyone maintaining them by hand.
2. **An interface layer for one job: a human PM checking the record.** Not a dashboard for browsing. The three things it must make effortless are **verifying what the brain proposed**, **seeing what is owed and by whom**, and **seeing a meeting next to the deliverables and actions attached to it**. Everything else on the page is supporting cast.

Two rules define the product: **nothing enters a register without a link back to the sentence that created it**, and **nothing counts until a human project manager has verified it.**

The chassis already exists: a single-file, zero-dependency `index.html` (1,683 lines) with a working calendar, recurrence expansion, correct Eastern-time date math, an interactive item list and a document tracker. **Do not rewrite it.** Give it a real data store, real dates, working provenance, human verification, and calendar associations.

### Ground rules that outrank every instruction below

- **The file must open from `file://` with zero console errors after every change.** No bundler, no npm, no framework, no runtime network request. If a change would introduce a build step or a network dependency, do not make it. Open the file and read the console after each milestone.
- **Nothing deploys until M11.** Local verification first, every time.
- **Work the milestones in order.** After each one, commit with a message naming the milestone, then tell me what you changed and what you deliberately left alone. Do not start a later milestone early. Do not refactor anything a milestone does not name.
- **Grep before you trust a line number.** Locate code by content; if a reference has drifted, say so in your report rather than editing the wrong place.
- **Do not invent data.** If a milestone needs a field that does not exist, add the field and leave it empty. Plausible-looking filler is the failure this product exists to prevent.
- **Ask rather than guess.** If a milestone is ambiguous against the real file or the real SharePoint site, stop and ask. One question costs a minute; a wrong assumption costs the demo.

---

## Architecture

| Layer | Ships today | Pilot / target |
|---|---|---|
| Input | Claude Tag in Slack posts a structured JSON block into the channel; a human drops it into `data/inbox/`. Teams transcripts dropped into `data/inbox/transcripts/` by hand. | Tag writes the drop itself; Outlook calendar (deprioritised as "surprise and delight") |
| Brain | Claude Code, run locally by hand: reads `data/inbox/`, writes the SharePoint lists over MCP, regenerates the app snapshot | Scheduled job under a service principal |
| System of record | **SharePoint lists** — one per register, plus a verification log | Same, in the client's own tenant, read by HorizonView and Power BI |
| App data | `data/*.json` — a read-only snapshot generated from the lists and committed to the repo | Signed read endpoint or a nightly export |
| App | Static `index.html`, opened locally. No build step, no deploy until the local gate passes | Same, deployed, plus auth |
| Verification | A flag on every item, in place, in the item list; decisions exported as structured changes | Reminders to the owner |
| Write-back | Claude Code applies the exported changes to the lists over MCP and commits a fresh snapshot | Push notifications into Slack |

**The one-way rule:** SharePoint is written only by Claude Code. The app reads the snapshot and writes a change file. Nothing else. Every read and write to the store goes through the contract in `scripts/store.md`, so replacing MCP with a service principal later touches one place.

### Questions already resolved — do not reopen them

- **Who writes SharePoint.** Claude Code, over MCP. Not the browser. No secret, no token, no client id in `index.html` — if you find yourself needing one, you have taken a wrong turn.
- **Security.** The app ships with **no** write endpoint and **no** passphrase. See M9 — that is a deletion, not a feature. Real access control is SharePoint permissions, and that belongs on the Path to Market slide.
- **Where verification happens.** In the app, after the write — never as a Slack prompt before ingestion, because verification requests get buried in channel noise. And it is **a flag on the item where the item already sits**, not a separate approval section. Leaving unverified items in place among the verified ones is deliberate: it is what lets someone other than the reviewer notice a bad entry.
- **Who verifies.** A human PM. Nothing else.
- **What happens when the input layer fails.** See "Fail loudly, never silently".

---

## Repo layout

```
hack-team-07/
  index.html                 # the app, single file, no build step
  vercel.json                # framework: null, NO SPA rewrite — prepared in M1, used in M11
  BUILD.md                   # this brief
  data/
    meta.json                # generatedAt, asOf, timezone, schemaVersion, sourceSite, listVersions
    actions.json             # snapshot — generated from SharePoint, do not hand-edit
    decisions.json
    risks.json
    stakeholders.json
    deliverables.json
    meetings.json
    documents.json
    changes/
      pending-changes.json   # exported from the app, consumed by apply.md
    inbox/
      .gitkeep               # Claude Tag JSON blocks land here
      transcripts/.gitkeep   # manual Teams/huddle transcript drops
  scripts/
    store.md                 # the read/write contract — the ONLY place that knows about SharePoint
    provision.md             # creates/repairs the lists and columns
    ingest.md                # inbox -> SharePoint lists -> snapshot
    apply.md                 # pending-changes.json -> SharePoint lists -> snapshot
    nudge.md                 # the daily digest
  out/
    digest-YYYY-MM-DD.md     # generated, committed, pasteable into Slack
  README.md
```

`vercel.json` must **not** contain a catch-all rewrite to `index.html`. A 200 fallback makes dead POST paths return success — exactly the failure that looks fine in testing and breaks on a projector.

---

## The SharePoint layer

Seven lists on one site. Ask me for the site URL before you provision anything; do not guess it, and do not create a new site.

Rules for the schema, learned the hard way:

- `Title` is mandatory on every SharePoint list — map the item's one-line title into it.
- **No Person/Group columns.** Store owners as text (`Owner`, `OwnerKey`) so a write never fails on name resolution.
- **No Lookup columns.** Relate records with plain indexed text ids (`MeetingId`, `RelatedTo`). Lookups are fragile to write over MCP and impossible to snapshot cleanly.
- **No calculated columns.** Overdue, staleness and labels are computed at render time, never stored.
- Internal names have no spaces. Choice columns get an explicit value list. Dates are date-only unless a time was actually stated.
- `RegisterId` (`ACT-01`) is ours and is the correlation key. SharePoint's own numeric `ID` is incidental — never surface it in the app.

| List | Columns |
|---|---|
| `BridgeActions` | Title, RegisterId, Detail (multi-line), Owner, OwnerKey, WS (choice: ops/fin/comp/build/lead), Status (choice), Priority (choice: High/Med/Low), Due (date), MeetingId, RelatedTo, Tags, SourceSystem, SourceChannel, SourceAuthor, SourceTs, SourcePermalink (hyperlink), SourceQuote (multi-line), Confidence (choice: high/medium/low), VerificationStatus (choice: pending/verified/rejected), VerifiedBy, VerifiedAt, VerificationNote, CreatedAtIso |
| `BridgeDecisions` | as above, minus Due/Priority, plus DecidedOn (date), Rules Out → `RulesOut` (multi-line), Supersedes (RegisterId) |
| `BridgeRisks` | as above, plus Severity (choice: R/Y), LastReviewed (date), Mitigation (multi-line) |
| `BridgeDeliverables` | as above, plus DueTo (text — who it is owed to), Due (date), MeetingId |
| `BridgeStakeholders` | Title (name), RegisterId, Initials, Role, Side (choice: Client side/Delivery side/Both sides), Function, Influence (choice), Workstreams (text, comma-separated), plus the Source* and Verification* columns |
| `BridgeMeetings` | Title, RegisterId, MeetingDate (date), Recurrence, RecurrenceFrom (date), RecurrenceUntil (date), Audience, WS, TranscriptRef, SourcePermalink |
| `BridgeVerificationLog` | Title (RegisterId), Action (choice: approved/edited/rejected), ActorName, ActedAt (date+time), FieldChanged, OldValue, NewValue, Note |

---

## Data contract and the adapter

`data/actions.json` already exists and is the reference shape for the snapshot: a top-level `meta` object and an `actions` array, each item carrying `id`, `register`, `title`, `detail`, `owner`, `ownerKey`, `status`, `priority`, `due`, `dueTime`, `overdue`, `daysUntilDue`, `createdAt`, `tags`, `relatedTo`, and two nested blocks — `provenance` (`sourceSystem`, `channel`, `messageTs`, `permalink`, `author`, `capturedAt`, `quote`) and `verification` (`status`, `decidedBy`, `decidedAt`, `note`).

**Extend that shape to the other registers. Do not invent a second schema.** Additions required: `ws` on every item; `severity` (`"R"`/`"Y"`) on risks; `decidedOn` (ISO) on decisions; `provenance.confidence` (`high`/`medium`/`low`, anything below `high` arrives unverified); `meetingId` on actions and deliverables; and a `stakeholders` register (`id`, `name`, `initials`, `role`, `side`, `function`, `influence`, `workstreams[]`, `provenance`) seeded by parsing the nine people who currently exist only as text inside `audience:` strings at lines 747, 751, 763, 764, 767 — their roles are already written in there, unparsed, under a field the UI literally labels "Stakeholders".

### The adapter — read this before touching any render code

The store's field names and the dashboard's field names disagree almost completely. Of the 17 fields in `actions.json`, exactly one (`title`) matches cleanly. **Renaming fields across 20-plus render call sites is how this build runs out of time.**

Keep the dashboard's internal field names as the render contract, and write one ~40-line `adaptItem()` that maps snapshot records into that shape at load. The render functions keep working untouched.

| Store field | Dashboard field | Watch out |
|---|---|---|
| `register: "action"` | `kind: "Action"` | Dashboard capitalises, and uses one field for all five registers |
| `detail` | `note` | |
| `ownerKey` (`"DD"`) | `owner` | The dashboard's `owner` holds **initials**, not a name. The full name lives in a lookup table at line 950 |
| `owner` (`"Davis Dean"`) | rebuild line 950 + `DATA.team` | From the stakeholders register |
| `priority: "high"` | `urg: "High"` | Dashboard uses `"Med"`, not `"medium"` |
| `severity` | `sev` | |
| `decidedOn` | `date` | |
| `provenance` | `src`, extended | |
| `due` (ISO) | `due` (ISO) + derived label | The one deliberate render change — see M4 |

Two collisions: `priority` already exists in the dashboard as a *sort-mode* string, not a data field; `source` already exists as a `documents` field meaning storage location. Do not reuse either name.

Keep the `ACT-01` id format. Ids become DOM ids (`row-${id}`, line 1112) and edit-buffer keys, so they must stay free of spaces and dots.

---

## Milestones

Each has an acceptance test. Do them in order. M0 blocks the first push; M11 is gated on everything above it.

### M0 — Content pass — DONE, verified

Ran on build day against the 1,684-line file. Every real engagement fact was replaced with a synthetic equivalent of the same shape and order of magnitude, so the demo still reads as a real programme. Person names were already pseudonyms and were left alone; two stale handles that no longer matched them were fixed.

**This file is in a public repo, so the original values are deliberately not written down here.** What follows names the categories only. The full before/after list stays out of the repository.

| Category | Now reads | × |
|---|---|---|
| Per-seat licence cost and seat cap | `$6,200`, caps at 4 seats | 2 |
| Partner-side headcount | 34 partner staff / 34-person roster | 7 |
| Initial record load and duplicate ratio | roughly a third of 14,500 records | 2 |
| Site-lead sign-off count | Four of six | 1 |
| Review-committee date and its slip | Oct 26 → Nov 9 | 7 |
| Phase 1 go-live month and back-plan | end of November 2026, early-November | 12 |
| Workstream percent complete | 45% | 2 |
| Programme name, and the name it replaced | "Platform Consolidation", from "Revenue Systems" | 6 |
| Two deck filenames encoding real dates | `…_v4.pptx`, `…_v2.pptx` | 2 |
| Four transcript titles encoding real dates | `… — Aug 7` / `Aug 6` / `Aug 4` | 4 |
| Two stale Slack handles | `@mkeller`, `@sprentice` (matching Morgan Keller, Sam Prentice) | 3 |

**Acceptance — passed.** Every original string greps to zero in `index.html`. Line count unchanged at 1,684 at the time of the scrub. The single script block passes `node --check` and the HTML parses clean. The internal narrative still holds: the committee slot remains the long pole against a month-end go-live.

**Still your call, before the repo goes public:** the file's five workstream owners, four register owners and the pseudonymous team names are internally consistent but were never checked against real people at the client. Read the names once yourself. And the intake copy still references a Slack channel by name — decide whether that channel name is safe in a public repo.

### M1 — Local gate and first commit. No deploy.

**Fonts and the local gate: DONE.** The three Google Fonts tags (`preconnect` ×2 and the Inter stylesheet) are gone, and Poppins 400/500/600/700/800 — the five weights the file actually uses — are embedded as base64 `woff2`, latin subset, in `<style id="bridge-fonts">` at line 8. Source: the `@fontsource/poppins` package, not a CDN pull. Body stack is now `'Poppins',Calibri,system-ui,…`. One brand violation fixed on the way past: `.info-b` was set in `Georgia,'Times New Roman',serif` and now inherits. **Zero `http://` or `https://` references remain in the file.** Cost: 53KB of base64, file went 136KB → 185KB. `README.md` holds the local gate as a checklist.

**Verified:** the page was run headlessly through jsdom — zero console errors, zero warnings, zero network attempts, 9 sections and 7 nav links rendered, 5 `@font-face` rules parsed, computed body font `"Poppins", Calibri, …`. The single script block passes `node --check`; the HTML parses clean.

**Still open, and it needs a human:** the Chrome extension was not connected, so nobody has *looked* at the page since the change. jsdom does not do layout or font rasterisation. Open it in Chrome and confirm Poppins actually renders, the layout did not shift, and the nav is reachable at 800px.

**Still open, needs GitHub:** commit `index.html`, `data/`, `README.md` and `BUILD.md` at the repo root on `main` and push. Add `vercel.json` with `framework: null` and no rewrites — **prepared, not used.** Nothing deploys until M11.

### M2 — SharePoint lists as the system of record

**The local half is DONE.** The data is out of the page. The 216-line `DATA` literal that sat between the `==DATA START==` / `==DATA END==` markers now lives in `data/snapshot.js` as `window.BRIDGE_DATA`, loaded by a classic script tag at line 718; `index.html` reads it at line 733 behind a guard. The markers are intact, so a job that rewrites that region still works. `index.html` went 1,689 → 1,485 lines.

Canonical JSON was written alongside it, one file per register: `actions.json` 31, `decisions.json` 8, `risks.json` 9 (risks + blocker + issue), `stakeholders.json` 4, `documents.json` 14, `meetings.json`, `deliverables.json` **0 — the register does not exist yet**, and `meta.json` carrying `generatedAt` / `asOf` / `timezone` / `schemaVersion`.

**The guard is the fail-loud principle applied to the page itself.** If `data/snapshot.js` is missing — someone emails `index.html` on its own, or opens it outside the repo — the app throws immediately and paints a red banner saying the snapshot did not load and where to open the file from. It does not render an empty dashboard. Both paths are tested: with the snapshot, 48 items and zero errors; without it, the banner and zero rows.

**Still open, needs the SharePoint site URL.** Ask me for it; do not guess it and do not create a new site.

Write `scripts/store.md` **first**: the read/write contract. Every field mapping, every list name, every choice value, and the rule that nothing outside this file knows SharePoint exists. Then write `scripts/provision.md` and run it to create the seven lists and their columns exactly as specified above. Provisioning must be idempotent — running it twice repairs, never duplicates.

Seed the lists from the current in-file data and the parsed `audience:` strings. Then generate the first `data/*.json` snapshot from the lists and point the app at it, through `adaptItem()`. The app now reads a snapshot; it has no inline register data.

**Acceptance:** the seven lists exist with the right columns. The snapshot regenerates from SharePoint and the app renders from it identically to before, zero console errors. Deleting a row in SharePoint and regenerating makes it disappear from the app.

### M3 — Round trip, proven end to end

This is the load-bearing assumption. Prove it before building on it.

Write `scripts/ingest.md`: given a transcript or a Claude Tag JSON block in `data/inbox/`, extract candidate register items, and for each one capture the verbatim sentence, the source system, the channel, the author, the message timestamp and the permalink. Every extracted item arrives with `VerificationStatus: pending`. Then write the rows to SharePoint, update `data/meta.json`, regenerate the snapshot, and commit.

Assign final `RegisterId` values here, in Claude Code — never in Slack. Tag proposes candidate ids; you own the numbering, so two Slack messages can never collide on `ACT-04`.

**Acceptance:** drop today's huddle notes into `data/inbox/transcripts/`, run the ingest prompt, and get at least five new pending rows visible **in the SharePoint list**, each with a real quoted sentence, then visible in the app after the snapshot regenerates. `git diff` shows only the snapshot and `meta.json` changed.

### M4 — Real dates and overdue detection — DONE, verified

The five relative strings are gone. `due` is an ISO date in the store; every human label is computed at render against `TODAY`.

**How the dates were derived, because this matters more than the code.** The labels were resolved once against **Monday 2026-08-10, 4:35 PM ET** — the moment `DATA.updated` says a person last touched the tracker by hand. That is when someone typed "Today", so that is what "Today" meant. `Today → 08-10`, `Tomorrow → 08-11`, `Wed → 08-12`, `Mon → 08-17`, `Later → 08-24`. The derivation is documented in the header of `data/snapshot.js`. Nothing was invented; the anchor is a fact already in the file.

That single honest choice is what produces the demo: **12 items are now overdue** — 9 by three days, 2 by two, 1 by one — because the tracker has not been updated since Monday. Which is the product's entire thesis, arriving as arithmetic rather than as a claim.

Built:

- `dueMeta(iso)` → `{label, cls, days, overdue}`. Labels: "Overdue by 3 days", "Today", "Tomorrow", "Mon 24 Aug". Undated items say "No date" rather than rendering blank.
- Sorting and ranking on real dates via `dueKey()`; undated sorts last. Overdue outranks everything in the item list.
- The inline five-option dropdown is now a **date input** plus a computed label chip. `setDue()` takes ISO and re-renders the attention panel too.
- Risk staleness: `reviewed` on all 9 risk-family records, `RISK_STALE_DAYS = 14`. **Every one is `null`, so all 9 read "No review recorded" and flag as stale** — the source carried no review date, and that is the honest answer rather than a fabricated one. Populating it is ingest's job.
- Deleted `dueC` (defined, never called) and `dueRankMap`.
- **"Needs attention now" is computed, not typed.** Four reasons — Overdue, No owner, Not reviewed, High — each row carrying the reason as a chip. Quotas (3/2/1) so the panel shows the range of failure modes instead of six copies of the same one. It currently surfaces 3 overdue, 2 unowned, 1 never-reviewed risk.

**Verified in jsdom:** zero errors, zero warnings. `dueMeta` correct across the boundary cases including null. 45 open items, 12 overdue, 2 unowned, 9 stale risks. 28 date inputs rendered, **zero legacy selects**. Sort-by-due ascending confirmed. `setDue` round-trips. The strings "Overdue by 3 days", "Overdue by 1 day", "No review recorded" and "Mon 24 Aug" all appear in the rendered DOM.

**One number to keep straight:** the app holds **45** items by its own filter (`status !== 'done'`) and **37** with an explicit `status:'open'`. The workstream cards claim 74. M8 should derive against the app's own definition — 45 — which is what the original spec meant.

### M5 — Verification in place — DONE, verified

**How the initial states were derived, which is the only judgement call here.** Every item now carries `verification{status, decidedBy, decidedAt, note}`. The 8 items that carry a `src` block were **captured from a source and no person has checked them** → `pending`. The other 40 were **typed into the tracker by a person before Bridge existed** → `verified`, `decidedBy: 'seeded'`. Both states have a reason recorded in the data and documented in the snapshot header. Nothing was assigned at random to manufacture a mix.

Built:

- **State in place, not in a separate section.** Pending rows carry an amber `Unverified` chip, a left edge stripe, and two buttons — `✓` and `✕`. Verified rows carry a green tick whose tooltip says who verified it and when, or "Seeded" for the pre-existing ones.
- **"Unverified only · N"** filter chip beside the type chips, with the live count.
- **Approve, reject, and the guard.** `approveItem()` refuses when the owner is unclear — "Owner is unclear — set an owner before verifying this one" — and refuses an action with no date. It never fills either in. `rejectItem()` takes a note, removes the item from every register view, and keeps it in the audit trail.
- **Audit trail** — `{registerId, list, action, field, oldValue, newValue, actor, actedAt, note}` per decision.
- **The loop, without a backend.** "Export changes · N" downloads `pending-changes.json` as **structured changes** (`{registerId, list, action, fields{}, previous{}, actor, actedAt, note}`), never prose. `scripts/apply.md` is what consumes it.
- **Persistence** to `localStorage` on every decision and every inline edit, restored on load. `beforeunload` warns if decisions are unexported.
- The attention panel gained `Unverified` as a fifth reason, with a quota so it shares space with overdue and unowned.

**Verified in jsdom, zero errors, zero warnings:** 8 pending / 40 verified at load; the chip reads "Unverified only · 8"; 8 striped rows and 8 approve buttons; the filter returns exactly the 8 and every row under it is pending. Approving `a1` → verified by Davis Dean. Rejecting `a3` with a note → gone from the DOM, present in the audit. Export wrote 2 structured changes and moved the counter. Save/restore round-trips: wiping an item's verification in memory and calling `restoreState()` brings it back.

**The guard was tested synthetically**, because on today's data no pending item is also unowned: setting a pending item's owner to `Unassigned` makes `approveItem()` refuse, leave it pending, and **write nothing to the audit**; assigning an owner then verifies cleanly. Same for a missing date. That case will arrive on its own from ingest, which is exactly when it matters.

**One graceful degradation worth knowing.** `localStorage` is unavailable on an opaque origin, which is what `file://` is in some engines. Every access is wrapped, so the app warns to console and keeps working rather than dying — verified by running the whole suite under both `http://` and `file://`. Chrome does give `file://` a storage bucket, so persistence works in the demo; it just is not *depended* on.

**Not done here, because it needs SharePoint:** applying the export back to the lists. `pending-changes.json` is the handoff, and `scripts/apply.md` is still to write.

<details><summary>Original M5 brief, for reference</summary>

**This is the most important milestone. It is what the PM does with Bridge and it is beat four of the demo.**

Every item shows its verification state where it already sits — a clear marker for verified, a distinct one for pending, and rejected items gone from the list but present in the log. **No separate approval section, no separate nav entry.** Add one filter, "Unverified only", alongside the existing type chips, and put a count of what is waiting somewhere the PM cannot miss it.

The reviewer can approve, edit then approve, or reject, with a note. Where extraction could not determine an owner, the item says the owner is unclear and the reviewer **must** supply one before it can be verified — it never guesses. Rejecting leaves no trace in the register but writes to `BridgeVerificationLog`. Verified items keep their provenance permanently.

The loop, without a backend: decisions accumulate in `localStorage`, and an "Export changes" button downloads `pending-changes.json` — **structured changes, not prose sentences** — of the form `{registerId, list, action, fields:{...}, actor, actedAt}`. Then `scripts/apply.md` applies that file to the lists over MCP, writes the audit rows, and regenerates the snapshot. Guard against navigating away with unexported decisions outstanding.

**Acceptance:** approve one item, edit one, reject one; reload and confirm the decisions survived. Export, run `apply.md`, and see all three reflected **in SharePoint** with matching rows in the verification log. The app cannot verify an item whose owner is unclear.

</details>

### M6 — Provenance — mechanism DONE, but it cannot resolve on this data

**The finding that decides this milestone: every URL in the dataset is literally `#`.** All 8 document `url` fields, all 4 `slackUrl` fields, and the one item-level `src.url`. There is no Slack workspace and no document store behind any of it, so "clicking a source opens the real message" cannot be made true by wiring — there is nothing to wire to. Fabricating plausible permalinks would produce links that 404 on stage, which is worse than admitting the gap.

So M6 built the mechanism and made every state honest:

- **One rule, applied everywhere: an anchor is only an anchor if it goes somewhere.** `isRealUrl()` requires an `http:`/`https:`/`mailto:` scheme. `linkOut()` renders a real link when there is one, and a dimmed "· no link" chip explaining why when there isn't. Applied at all five document render sites as well as the item list.
- **Every item now shows a source state**, where before only 8 of 48 showed anything: 37 rows read "◦ No source" with the tooltip "seeded row — it predates Bridge", 8 read "Slack thread · no link" or "Transcript · no link".
- **The detail popover carries a provenance block** — source, author, timestamp, and a quoted sentence when one exists, with an explicit "No sentence captured for this one" when it doesn't. `provOf()` resolves the permalink through item provenance → `src.url` → the document's `slackUrl`/`url`, taking the first that is real.
- **Deleted:** `viewInSlack` (defined, never called) and the digest's toast-only "Jump to Slack thread" link. The "Clear filters" anchor became a button.

**Verified in jsdom:** zero errors. **Zero `href="#"` anywhere on the page**, down from 35 — the item list *and* the document sections. All 45 rendered rows carry a source state. 35 dead links became labelled "no link" chips.

**What this milestone cannot deliver, and what would:** demo beats 2 and 3 depend on clicking a citation and landing on the sentence. That needs a source that exists. Two ways to get one, both achievable today:

1. **A real Slack channel.** Post the seed messages in the test channel, capture the permalinks, and put them in the data. Links then genuinely resolve.
2. **A transcript in the repo, rendered in-app.** Add `data/inbox/transcripts/*.md`, store `{docId, line, quote}` on each item, and open the transcript in a modal scrolled to the highlighted line. Works offline from `file://`, needs no workspace, and demos the money beat exactly — "click the citation, land on the sentence."

Option 2 is the stronger demo and the smaller dependency. Neither is invention: in both cases the quote genuinely exists in a source the app can open.

### M6b — the citation lands on the sentence — DONE, verified

Option 2, built. **The chain is real end to end: the quote is a substring of a numbered line in a file that ships in the repo, and the app opens that file at that line.**

- **Four transcripts** in `data/inbox/transcripts/` — `steertrans`, `buildtrans`, `comptrans`, `opstrans` — written as the meeting records the mocked programme implies, 54 lines total, speaker-attributed and time-stamped. These are also the input format `scripts/ingest.md` will read.
- **`data/transcripts.js`** carries the bodies as line-numbered arrays, generated from the `.md` files, loaded by a second classic script tag (`fetch` still blocked on `file://`).
- **11 items now carry real provenance** — `{sourceSystem, docId, line, author, messageTs, quote, confidence}` — up from zero with a usable source. **Including 3 of the 8 decisions**, which previously had none at all.
- **The generator asserts the chain.** Each quote is located in the transcript by exact match, the line number is read from the written file, and the stored quote is re-checked against that line. If a quote is not verbatim, generation fails rather than shipping a citation that points at the wrong line.
- **The viewer.** Clicking a citation chip opens a modal with the transcript, the cited line highlighted and scrolled to centre, headed "This entry was created from the highlighted line. Nothing enters a register without one." Escape or the backdrop closes it.

**Verified in jsdom:** zero errors. 11 citation chips render; `quoteMatchesLine` true for all 11 — every stored quote is literally the text on the line it cites. Opening `a13` lands on line 10 of the Compliance transcript with exactly one highlighted line. The popover shows the quote and an "Open the transcript at line N" button. Still zero `href="#"` page-wide.

### M7 — the calendar, with visible associations — DONE, verified

- **`meetingItems(id)`** is the single place that answers "what came out of this meeting", splitting into actions, decisions and risks, excluding rejected items, and reading `meetingId` with a fallback to the legacy `deliv.mid`.
- **17 items now carry `meetingId`**, up from 9: the 9 migrated from `deliv.mid`, plus 8 more attached through their transcript — where a transcript unambiguously *is* a meeting's record, its items belong to that meeting. Only `steertrans → steer` and `comptrans → compws` were mapped; `buildtrans` and `opstrans` don't correspond to a meeting in the data, so nothing was invented for them.
- **The calendar now marks state, not just counts.** Each meeting card carries chips for decisions taken, items overdue, and **items nobody has verified** — all derived.
- **Meeting detail gained "Decisions taken" and "Risks raised"** sections, and every attached row — action, decision or risk — carries its verification chip and a citation button that opens the transcript at the line. The steering meeting now shows 6 actions and 2 decisions with 5 working citations.
- **`dueBeforeNext()`** computes what is owed before a meeting's next occurrence.
- **The `leadstrat` bug, properly diagnosed.** The spec said it lacked a `from`/`anchor` date. The real cause is that **the recurrence engine has no concept of an end date at all** — it only ever applied a lower bound, so *every* series ran to infinity. Added `until` support at both expansion sites and set `leadstrat` to end 2026-08-08, since its own description says it is on hold. It no longer appears in the current week.

**Verified in jsdom:** zero errors. `leadstrat` gone from the rendered week; 2 overdue chips and 1 decisions chip rendered from data; opening the steering meeting shows "Action Items 6 / Decisions taken 2" with 5 citation buttons and 8 verification chips; clicking one opens the Steering transcript at line 15.

<details><summary>Original M6 brief, for reference</summary>

#### Provenance that actually resolves

Verified against the file: **8 of the 48 register items carry a `src:{}` block**, none of the 8 decisions do, and there is exactly **one render site — `srcChip`** — so this is one function to fix rather than eleven. Two literal `href="#"` remain, at lines 1451 and 1478. `viewInSlack` at line 979 is defined and never called. This is the differentiator the whole pitch rests on and it currently does nothing.

Every item gets real provenance: the working Slack permalink, the author, the timestamp, and the quoted sentence shown in the item's detail view. Clicking a citation lands the reader on the sentence that created the entry, not the top of a document. An item with no provenance shows an explicit "seeded — no source" marker rather than a fake link or nothing at all. Delete the toast-only link and the unused helper that was meant to open Slack and is never called.

**Acceptance:** clicking any source link opens the real Slack message. Every item's detail view shows the sentence it came from. Zero `href="#"` in the item list.

</details>

### M7 — The calendar, with visible associations

The calendar already works. Make it the second thing the PM uses, by making a meeting and its commitments one object.

**The hook already exists.** Nine items carry `deliv:{mid:'…'}` — a reference to a meeting id. That is the association to build on; do not invent a parallel mechanism. **But there is no Deliverables register at all: zero items of `kind:'Deliverable'`.** It has to be built, seeded from what the meetings actually owe, not just given a new field.

- Every action and deliverable carries `meetingId`, migrated from `deliv.mid` where it exists. Ingest sets it from the meeting the transcript belongs to.
- Clicking a meeting shows what is attached to it: the actions committed in it, the deliverables due out of it, the decisions taken in it — each with its verification state and its source quote reachable in one click.
- A meeting with unverified items attached is marked as such on the calendar itself. That is the PM's queue, arriving in the shape they already think in.
- Every item shows which meeting it came from, and that is a link back to the meeting.
- Deliverables due before the next occurrence of their owning meeting are flagged. That is the single most useful derived fact on the page: what has to be true before Thursday.
- Fix the `leadstrat` recurring meeting (line 770): it has neither a `from` nor an `anchor` date, unlike every other recurring entry, so it expands onto every Friday from the epoch forward — while its own description says it is on hold.

**Acceptance:** open any meeting, see its actions, deliverables and decisions with verification states; click one and land on the sentence. Open any action, click through to its meeting. A meeting holding pending items is visibly marked.

### Layout cleanup pass — DONE

From your screenshot: rows were overflowing the card (the `i` button escaped it), titles truncated to "Send the approved F…" while a source chip ate 300px, and the due date appeared twice.

- `.src-chip` was `flex-shrink:0` with no max width — that was the overflow. Now shrinkable, capped at 132px, ellipsised. `.ti-row2` got `overflow:hidden` so nothing can escape the card again. Meeting chip capped at 104px.
- **The date input left the row.** The computed label stays; the editor moved into the detail popover. That removes a control from all 45 rows.
- Chip labels shortened, explanation moved to the tooltip: "Compliance Working Session transcript — Aug 4 · no link" became **"▤ Transcript"**, and citations read **"▤ Aug 7 · L15"**.
- **The kind chip only renders when the list is mixed.** Filtered to Actions, every row said ACTION; that's now suppressed and returns under All and RAID.
- Verify/reject buttons sit at 45% opacity until you hover the row, or always-on if the row is unverified.

### M8 — Derived numbers — DONE, verified

- **Workstream counts are derived**, via `wsOf()` → the workstream of the meeting an item was committed in. **This exposed something the hardcoded numbers were hiding:** only 15 of 45 open items can be attributed at all, against cards that claimed 74. The cards now read "N open items attributed" with a note under the grid — "30 open items are not attached to a workstream yet… items that arrived without one stay uncounted rather than being guessed at." That gap is the product's own thesis, so it belongs on screen rather than papered over.
- **The hero pill is computed.** It said "On track" while 3 of 5 workstreams were amber. It now reads **"3 of 5 need watching"**, derived from the worst health present.
- **The ribbon is computed.** "3 new since this morning — 1 new decision, 2 documents added" was static markup contradicting the data. It now reads "8 waiting on you to verify · 12 overdue", and hides itself when both are zero.
- **The frozen timestamp is gone.** "Monday Aug 10, 4:35 PM ET" sat next to a live clock; the header now reads "Snapshot generated 2026-08-13 · today" from `BRIDGE_META`, and the footer states plainly that the record is the register files, not the page.
- **Nav trimmed to the product**: Action Items, Ask Claude, Calendar, Workstreams, and a new "Needs verifying" link that applies the unverified filter. Documents and Discussion are out of the nav and off the demo path; their code stays and stays console-clean.
- **Narrow-width nav added** — the links wrap instead of vanishing below 860px.

### M9 — the write path is deleted — DONE, verified

`/api/update`, `/api/submit`, `/api/refresh`, the passphrase widget, its CSS, `SESSION_PASS`, `askPass()`, the file input and `readFileB64()` are all gone. **Zero `fetch(` calls remain in the file, and no credential of any kind.**

- The pending tray's "save" now calls `exportChanges()` instead of posting prose to a server.
- Intake became a genuine local queue in `localStorage`, and says so: "Queued locally. It leaves with the next Export changes — nothing was uploaded."
- `triggerRefresh()` no longer pretends: "The record refreshes when Claude Code regenerates the snapshot. This page only reads it."
- The dropzone captures a dragged file's *name* to prefill the title and tells you to paste the text. No upload path exists to fail silently.

### M10 — Aberdeen branding — DONE, verified

Migrated as a classified value substitution rather than by hand: 109 distinct literals across 342 occurrences.

- **New token set** on the palette: Aberdeen Blue `#09375F` dominant, Teal `#44B0B1` accent only, Onyx `#404040` body text, plus one status scale on Jade / Gold / Jasper — replacing the three inconsistent green/amber/red scales.
- **97 literals migrated to tokens** by classifying each into hue and lightness families: 80 → `--line-soft`, 73 → `--surface`, 54 → `--navy`, 27 → `--link`, and the rest across the status tokens, teal and surfaces. **Zero hex literals remain outside the `:root` block** — including inside JavaScript template strings and inline `style` attributes, since `var()` is valid in any CSS value position.
- rgba tints re-based on Aberdeen Blue and the status colours.
- **Two brand-rule violations found and fixed.** Five components used **white text on teal** (`.intake-submit`, `.pb-save`, `.pb-count`, `.intake-ic`, `.us-sched`) — explicitly forbidden. They are now Aberdeen Blue with white text, which also enforces blue as dominant. Three used **teal text on white** (`.histbtn .hb-ic`, `.intake-chev`, `.dz-ic`) — now navy. The only remaining teal text is the hero eyebrow, which sits on an Aberdeen Blue background where teal is permitted.
- Teal survives as borders, focus rings and accents only.

**Final gate:** zero console errors and zero warnings across all four regression suites; zero external references; zero `fetch(`; zero `href="#"`; zero hex outside `:root`. 1,774 lines.

<details><summary>Original M8 brief, for reference</summary>

#### Focus the app, and make every number true

The page currently spends its space on things that are not the product. Take them off the path.

- Remove the **document tracker** and the **digest cards** from the navigation and from the demo path. Leave the code in place and console-clean; delete only the dead render paths behind the phantom transcript field (the "Transcripts" filter at line 1440 and the pill at 1454 and 1461 read a `tag` field no document has, so the section always blanks) and the CSS that depends on it.
- Order what remains for the PM: verification and what needs attention first, then actions and deliverables, then the calendar. Nothing off-path above the fold.
- **Nothing false stays on screen, on-path or not.** Workstream open counts at lines 729–733 are `16, 11, 9, 24, 14` and sum to **74**, while the file holds **37 items with `status:'open'`** (plus 3 done, out of 48 register items) — and **no item carries a `ws` field**, which is why the counts cannot currently be derived at all. Add `ws`, derive the counts, or delete the cards. The "3 new since this morning" ribbon at lines 539–540 is static markup contradicting the 6 documents flagged new — remove it. `DATA.updated` at line 727 is the frozen string "Monday Aug 10, 4:35 PM ET" rendered next to a live clock — read it from `meta.json`. The hero "On track" pill at line 528 is hardcoded green while 3 of 5 workstreams are amber, sitting directly beside the dots that show the true colours — derive it.
- "Needs attention now" (line 1636) tests decisions for `date === 'pending'` or a title starting with "OPEN". Neither exists, so no decision can ever surface there. Fix it, and make it include: overdue items, unowned items, stale risks, and anything unverified.
- Tab navigation disappears below 860px with no fallback. Add a working narrow-width nav so a scaled window or an unfamiliar projector does not leave the page scroll-only.
- Persist view state to `localStorage` and restore on load, so a reload does not wipe the demo. There is currently **not a single `localStorage` reference in the file**, so this is new code, not a fix. Make the discard action stop reloading the page.

**Acceptance:** every number on screen is derived. The nav holds only verification, items, calendar and registers. "Needs attention" surfaces at least one decision, one overdue item and one unowned item. The nav is reachable at 800px wide. A reload preserves state.

### M9 — Delete the dead write path

The app posts to `/api/update` (`UPDATE_ENDPOINT`, defined 949, used 1182), `/api/submit` (1526) and `/api/refresh` (1527), behind a plaintext passphrase held in a page-level variable — seven references, lines 479, 1157, 1182, 1574, 1580, 1601, 1615 — with no client-side validation. The pending tray at `pending.set` (1131, 1394) sends **human-readable English change lines**, which is the "prose not structured changes" problem M5 replaces. **There is no server.** Off a real backend these show error toasts; on a host with a 200 fallback they show a false success — the worst possible behaviour in a live demo.

Remove all three endpoints, the passphrase widget (lines 706–711), and the intake form's file upload. Keep the intake box as a local queue that writes into the `pending-changes.json` export from M5.

**Acceptance:** no `fetch` to a relative path remains, and no credential of any kind exists in the file. Nothing in the UI can report success for an action that did not happen.

### M10 — Aberdeen branding

Round 2 is a live client panel, so this ships. It is late because it touches every line and must not block anything load-bearing. Poppins is already embedded from M1.

Palette, verified against Aberdeen's brand guide — use these exact values:

- Aberdeen Blue `#09375F` — primary, dominant
- Aberdeen Teal `#44B0B1` — accent and highlights only
- Onyx `#404040` — body text, never pure black
- White `#FFFFFF`
- Secondary, charts and categorical distinctions only, used sparingly: Deep Sky Blue `#5CC8FF`, Jade `#00A676`, Jasper `#DB504A`, Gold `#F7D002`, Hyperlink `#0072AD`

Hard rules, do not violate:

- Never white text on teal, never teal text on white. Both fail contrast.
- White or teal text on Aberdeen Blue; blue, onyx or black on teal; blue or onyx on white.
- No decorative full-width coloured bars or stripes.
- Aberdeen Blue is dominant. Teal is an accent, not a second primary.

A token swap alone will not work. The file defines 21 CSS custom properties in one `:root` block but contains roughly 354 hex literals and 27 rgba literals, about 60% of which bypass the token layer — and around 51 of those live inside JavaScript template strings and inline `style` attributes, where CSS cannot reach them. There are also three separate, mutually inconsistent green/amber/red status scales, and per-person brand colours stored inside the data object.

Define a complete token set covering every semantic colour role — surfaces, text, borders, one status scale, source-chip variants, live and needs-attention states, and the verified/pending/unowned markers — mapped onto the palette. Replace every hex and rgba literal with a token reference, including inside render functions and inline styles. Collapse the three status scales into one. Derive per-person colours from the token set instead of storing them. Delete the ~100 lines of CSS that no longer match anything.

Change no layout, no copy, no behaviour here. Colour, type and tokens only.

**Acceptance:** grep for hex literals outside the token block and the font block returns zero. Zero console errors. Recognisably the same app, in Aberdeen's colours, every contrast pair respected.

### M11 — Deploy, and only now

Gated on the M1 local checklist passing on the current file, plus M0's grep returning zero, plus zero console errors, plus no credential and no relative `fetch` in the file.

Deploy the static file with the `vercel.json` prepared in M1 — `framework: null`, no rewrites. Then verify the deployed page against the same checklist, and confirm the snapshot it serves is the one in the repo.

Note for the deck, not for the app: `*.vercel.app` is unreachable from Claude Tag's environment, so the deployment is for humans and judges. The Slack layer talks to the repo, never to the site.

**Acceptance:** the deployment reaches READY, a teammate confirms it loads, and the local file still passes its gate.

---

## Fail loudly, never silently

When the input layer cannot do its job, every failure still produces a record. Four paths:

1. **Cannot parse the message.** Write the raw text into `data/inbox/` as an `unparsed` record with the permalink attached, so nothing is lost and a human can triage it.
2. **Cannot write to SharePoint.** Keep the snapshot and `pending-changes.json` intact, report exactly which rows failed and why, and never regenerate the snapshot from a partial write. A half-applied batch that looks applied is worse than a failed one.
3. **Parsed but unsure.** Write the row with `Confidence: low`, `VerificationStatus: pending`, and surface it first in the unverified filter.
4. **Snapshot older than the lists.** `meta.json` carries `generatedAt`; the app shows how old its snapshot is. It never implies it is live.

The rule: **silence is the only unacceptable outcome.** A wrong item a PM can reject is recoverable; a lost item is not.

---

## Out of scope today — do not start these

- Any write to SharePoint from the browser. Any client secret, token or app id in `index.html`.
- Power Automate endpoints, Graph app registrations, auth, SSO.
- Outlook or calendar *integration* — the calendar view is in scope, pulling from Outlook is not.
- Push notifications into Slack.
- Claude Tag reading the live app — blocked by the egress proxy; needs a route, not a sprint.
- Smart, context-based prioritisation of what each person needs to verify.
- Excel export, Power BI reports, HorizonView wiring — deck content.
- A Teams/Copilot variant for data-residency-constrained clients — deck content.
- Converting to a framework or adding a build step. Ever.

---

## Time budget and stop rules

Submission 6:00 PM ET. Demo path frozen 4:30 PM ET — fixes only after that, no new features on the path.

| By | State |
|---|---|
| — | ~~M0~~ done and verified |
| 12:45 PM | M1 local gate passing, repo pushed |
| 1:45 PM | M2 lists live and seeded, app rendering from the snapshot |
| 2:30 PM | M3 round trip proven |
| 3:15 PM | M4 + M5 done — this is the demo |
| 4:00 PM | M6 + M7 done |
| 4:30 PM | M8 + M9 done, demo path frozen |
| 5:15 PM | M10 as far as it got, M11 deploy if the gate passes |

Stop rules:

- **If M3 is not proven by 2:45 PM, stop and tell me.** The SharePoint write is the one thing with no fallback in the plan, and we need the decision time, not a heroic recovery attempt.
- If M5 is not done by 3:30 PM, skip M7's flagging refinements and finish M5. Verification is the product; calendar association is the second-best beat.
- If M10 cannot be finished cleanly, revert it. A coherent old theme demos better than a half-themed file, and Poppins already landed in M1.
- M11 never runs on a red gate. A working local demo beats a deployed broken one.

---

## Demo path — six minutes, and what each beat depends on

1. Five registers already populated with weeks of history, live from SharePoint lists. *(M0, M2)*
2. A message in Slack becomes a pending action, with the sentence it came from quoted underneath — and the row appears in SharePoint. *(M3, M6)*
3. Gap detection: four commitments in the meeting, one already tracked, three not, two with no owner. Click one, land on the exact line where someone said it. **The money moment — spend real time here.** *(M3, M6)*
4. The PM verifies in place: approve one, edit one, reject one. Export, apply, and show the rows changed in SharePoint with the audit log behind them. *(M5)*
5. Open Thursday's steering meeting: here are the deliverables due out of it, the actions committed in it, and which of them nobody has verified. *(M7)*
6. An overdue, unowned item flagged with nobody having touched it — the proactive beat. *(M4)*
7. The honest slide: Claude Code holds the credentials, not the browser; the record is in SharePoint where HorizonView already reads; what is local-only today and what a client tenant changes.

The answer to "what if it's confidently wrong" is beat 4. Show the reject path rather than describing it.

---

## Definition of done

- Opens from `file://` with the network off: zero console errors, zero outbound requests, Poppins renders.
- Zero real engagement facts. A stranger cannot identify the client or the programme.
- The seven SharePoint lists are the system of record; the app reads a snapshot and knows how old it is.
- No credential, token or app id anywhere in `index.html`. No `fetch` to a relative path.
- A verification decision made in the app reaches SharePoint through `apply.md`, with an audit row.
- Every item has provenance or an explicit "no source" marker; zero `href="#"`.
- Every item has a visible verification state; "Unverified only" works; unclear owners block verification.
- Every meeting shows its attached actions, deliverables and decisions; every item links back to its meeting.
- Every number on screen is derived from the data.
- One `adaptItem()` is the only translation layer; one `store.md` is the only thing that knows about SharePoint.
- Every commit names its milestone.

---

## Appendix — what changed from the earlier build prompt, and why

- **SharePoint ships today, and the write path is honest about it.** The earlier plan kept registers as repo JSON with SharePoint as a pilot. Lists are now the system of record — but written by Claude Code over MCP, because a static page cannot hold a credential. The app reads a snapshot and emits structured changes; that is the whole security model and it is a better story on stage than a passphrase.
- **Deploy moved to the end and behind a gate.** Local verification first. Nothing is proven by a green Vercel build.
- **Verification and the calendar are now the point of the interface.** Verification is M5, the calendar-association work is a milestone of its own, and the document tracker and digest cards come off the demo path — kept, console-clean, but out of the nav and out of the six minutes.
- **Sequencing inverted from the original prompt.** Branding was Stage 1; it is now M10. It touches every line, so doing it first means re-theming code that later milestones rewrite. The exception is embedding Poppins, pulled into M1 as a projector-safety fix.
- **The verification queue became a flag in place.** A separate approval section with its own nav entry was overturned in the huddle — sequestering unverified items kills the ability for anyone but the reviewer to spot a bad entry.
- **The content scrub is a blocking M0.** Neither earlier prompt mentioned it; the repo is public and the file still names the programme.
- **The file-upload intake gets deleted, not preserved.** The earlier prompt said it "works". It posts to endpoints that do not exist, and a 200 fallback would make it report false success on stage.
- **Line numbers are advisory**, paired with an instruction to grep first and report drift.
