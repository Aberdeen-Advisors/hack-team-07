# Bridge

An AI Engagement Associate for a consulting transformation team. It maintains five registers — actions, decisions, risks, stakeholders, deliverables — from the places the engagement already happens, and does routine coordination work itself.

Two rules define the product:

1. **Nothing enters a register without a link back to the sentence that created it.**
2. **Nothing counts until a human project manager has verified it.**

`index.html` is the whole app: one file, no build step, no dependencies, no runtime network requests. Open it from disk.

The build plan and its milestones live in [`BUILD.md`](./BUILD.md).

---

## The local gate

Every milestone ends here, and **the deploy in M11 is gated on this checklist passing on the current file**. A green hosted build proves nothing that this does not.

Run it with the wifi physically off.

- [ ] `index.html` opens by double-clicking it — `file://`, no server
- [ ] **Zero console errors**, and zero warnings you cannot explain
- [ ] **Zero outbound network requests** in the Network panel after a hard reload
- [ ] The page renders in **Poppins**, not a fallback — headings and body
- [ ] The section navigation is reachable at 800px wide
- [ ] A reload does not lose demo state
- [ ] No number on screen contradicts the data behind it
- [ ] Every register item shows either a source or an explicit "no source" marker
- [ ] Nothing in the UI can report success for an action that did not happen

### Checking the last three quickly

```
grep -c 'https\?://' index.html          # expect 0 outside comments
grep -c 'fetch(' index.html              # expect 0 after M9
grep -o '#[0-9a-fA-F]\{3,8\}' index.html | wc -l   # expect 0 outside tokens after M10
```

---

## Fonts

Poppins is embedded as base64 `woff2` (latin subset, weights 400/500/600/700/800) in the `<style id="bridge-fonts">` block, with a `Calibri` fallback. The Google Fonts links are gone deliberately.

**Do not re-add a font CDN.** The typography cannot change because a conference network dropped. If a weight is missing, add it to that block from a local file rather than linking out.

Never Arial, never Times New Roman.

---

## Layout

```
index.html      the app
BUILD.md        the build plan, milestone by milestone
data/           registers — snapshot for the app, written by Claude Code
scripts/        the prompts Claude Code runs: store, provision, ingest, apply, nudge
out/            generated digests, pasteable into Slack
```

## What this is not, today

No backend, no database, no auth, no write endpoint. No live Teams, Outlook or calendar integration. No real-time transcription. One programme at a time.

Those are on the Path to Market slide, not in this file.
