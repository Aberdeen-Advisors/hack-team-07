# Bridge — test plan and known gaps

Two people, about 15 minutes. One drives, one reads this aloud and records pass/fail.
Live: https://hackathon-build-theta.vercel.app · Local: `index.html` opened from the repo folder.

---

## A. The gate — 2 minutes, do this first

Run it **locally with the wifi off**, because that is the environment that must never fail.

| # | Do | Expect | P/F |
|---|---|---|---|
| A1 | Turn wifi off. Double-click `index.html`. | Page renders fully. Type is **Poppins**, not a serif fallback. | |
| A2 | Open DevTools → Console. | **Zero errors.** Warnings about `localStorage` on `file://` are acceptable. | |
| A3 | DevTools → Network, hard-reload (`Ctrl+Shift+R`). | **Zero outbound requests.** Everything is `file://`. | |
| A4 | Move `index.html` alone to your Desktop and open it. | **Red banner:** "Data snapshot did not load…". It must not render an empty dashboard. Delete that copy afterwards. | |
| A5 | Wifi on. Open the Vercel URL, check the console. | Same: no errors, no red banner. | |

**If A1–A3 fail locally, do not demo the hosted version.** Fix locally first.

## B. Does it tell the truth — 4 minutes

The pitch is "nothing false on screen". These are the claims a judge could check by clicking.

| # | Do | Expect | P/F |
|---|---|---|---|
| B1 | Read the hero pill next to the coloured dots. | "3 of 5 need watching" — **not** "On track". It must agree with the dots. | |
| B2 | Read the ribbon under the hero. | "11 waiting on you to verify · 12 overdue" — numbers, not prose. | |
| B3 | Read the header timestamp. | "Snapshot generated 2026-08-13 · today". No frozen date beside a live clock. | |
| B4 | Workstreams → read a card and the note under the grid. | "N open items attributed", and a note saying 30 items are not attached to a workstream. Cards must **not** claim 74. | |
| B5 | Hover any grey "◦ none" chip in the item list. | Tooltip explains it is a seeded row with no captured source. No fake link. | |
| B6 | Click any source chip that says "· no link". | **Nothing happens** — it is a `<span>`, not a link. It must never open a blank tab. | |
| B7 | Ctrl+F the page for "Rebuilt by Claude" or "posts to the project channel". | **No matches.** | |

## C. The money beat — provenance — 3 minutes

| # | Do | Expect | P/F |
|---|---|---|---|
| C1 | Go to **Needs a human**. | 11 large cards. Every one shows a quoted sentence and a "Read it in … · line N" button. | |
| C2 | Click "Read it in Steering Committee · line 15". | Transcript opens, **line 15 highlighted and centred**, header says "cited at line 15". | |
| C3 | Read the highlighted line against the card's quote. | **Word for word identical.** This is the whole claim — check it properly. | |
| C4 | Press `Escape`. | Modal closes. | |
| C5 | Action Items → click any "▤ Aug 7 · L15" chip. | Same transcript, same line. The citation works from both surfaces. | |

## D. Verification — the answer to "what if it's wrong" — 4 minutes

| # | Do | Expect | P/F |
|---|---|---|---|
| D1 | **Needs a human** → note the count. Click **Verify** on the top card. | Card disappears. Count drops by one. Toast confirms. | |
| D2 | Action Items → find that item. | Green ✓ instead of the amber "Unverified" chip. Left stripe gone. | |
| D3 | Click the "Unverified only · N" chip. | Only unverified items listed. Count matches the review queue. | |
| D4 | Back to **Needs a human** → **Reject** a card, type a reason. | Card gone. Item **disappears from the register entirely** — search for its title in Action Items. | |
| D5 | Reload the page (`F5`). | Your verify and reject both **survived**. | |
| D6 | Click **Export decisions**. | `pending-changes.json` downloads. Open it: structured objects with `registerId`, `action`, `actor`, `actedAt`, `note` — **no English sentences**. | |
| D7 | Make one more decision, then try to close the tab. | Browser warns about leaving with unexported decisions. | |
| D8 | Calendar → open the Steering Committee meeting. | "Decisions taken" and action rows show ✓ / Unverified chips matching what you just did. | |

## E. Calendar and glanceability — 2 minutes

| # | Do | Expect | P/F |
|---|---|---|---|
| E1 | Look at the calendar without clicking. | Meeting names readable at a glance. Chips show deliverables, decisions, overdue, unverified. | |
| E2 | Click a meeting. | Expands to stakeholders, purpose, deliverables, actions, decisions, risks. Nothing important hidden before the click. | |
| E3 | Look for "Leadership Strategy Sync". | **Absent** from this week — the series ended 8 Aug. | |
| E4 | Narrow the window to ~800px. | Nav links **wrap and stay reachable**. They must not vanish. | |
| E5 | Project it, or zoom to 150%. | Still readable from the back of a room. | |

## F. Nothing can lie about success — 1 minute

| # | Do | Expect | P/F |
|---|---|---|---|
| F1 | Click **Refresh** in the top bar. | Honest message about Claude Code regenerating the snapshot. No fake "requested". | |
| F2 | Add to the Bridge → paste text → **Queue for the next export**. | "Queued locally… nothing was uploaded." | |
| F3 | Click the dropzone. | Says upload is off because there is no server. No file picker that goes nowhere. | |
| F4 | DevTools → Network, click everything above. | **Zero requests.** Nothing posts anywhere. | |

---

# Known gaps — what is not built

## Blocked on the tenant, not on time

1. **No SharePoint round trip.** The connector has no list-write tool and writes need an Azure app registration. `data/*.json` is the record; the CSVs in `data/export/` are ready for a one-time import.
2. **`scripts/` is empty.** `store.md`, `provision.md`, `ingest.md`, `apply.md`, `nudge.md` are all specified in `BUILD.md` and none are written. **`apply.md` is the important one** — without it, `pending-changes.json` has nothing that consumes it, so the verification loop stops at the download.
3. **No ingest has ever run.** Every item in the app was seeded. The pipeline transcript → extraction → pending item has not been executed end to end.

## Data gaps you can see on screen

4. **37 of 48 items have no source.** Only the 11 machine-extracted ones carry a quote. Honest, and visible, but it is most of the register.
5. **30 of 45 open items have no workstream**, so the cards read low. Attribution only exists where an item is attached to a meeting.
6. **The Deliverables register is empty** — zero records. It is one of the five registers in the pitch.
7. **Stakeholders holds 4 records, not 9.** The other five people still exist only as unparsed text inside `audience:` strings.
8. **No Slack permalink resolves.** Every URL in the data is `#`, so citations only work for in-app transcripts.
9. **All 9 risks read "No review recorded"** — no review dates exist in the source.

## Product gaps

10. **The owner guard cannot be demonstrated by clicking.** All 11 pending items have owners, so "owner is unclear — set one before verifying" never fires. It is your best answer to "what if it's confidently wrong". **One seeded item with no owner fixes this** — the highest-value data change available.
11. **A rejection cannot be undone**, and there is no UI to view the audit trail. Both live in `localStorage` only.
12. **An item cannot be un-verified** once verified.
13. **View state is not persisted** — filters, sort and calendar position reset on reload. Verification decisions do persist.
14. **Verification is per-browser.** Anyone opening the link verifies into their own `localStorage`; it is not shared state. Say this out loud if you share the URL.
15. **Documents and Discussion still render** below the fold. Off the nav and off the demo path, but present.

## Process

16. **The Claude Tag config has never been installed** in the testing channel or exercised on a real message.
17. **Vercel is not linked to GitHub.** Every change needs both `git push` and `npx vercel --prod`.
18. **Nobody has watched a full six-minute run** end to end against the clock.

---

## If you only fix three things

1. **Seed one extracted item with no owner** — makes the guard demonstrable (gap 10).
2. **Write `scripts/apply.md`** — closes the verification loop so the export means something (gap 2).
3. **Rehearse the run once, timed** (gap 18).
