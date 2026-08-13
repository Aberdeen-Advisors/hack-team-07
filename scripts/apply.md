# apply.md — verification decisions → registers

Closes the loop. The app cannot write anything, so a PM's decisions leave as `pending-changes.json`
and this prompt applies them to the register files.

Run it by opening Claude Code in this repo and saying: *"Run scripts/apply.md on ~/Downloads/pending-changes.json."*

## Input

The file the **Export decisions** button downloads:

```json
{ "generatedAt": "...", "actor": "Davis Dean", "schemaVersion": 1,
  "changes": [
    { "registerId": "a13", "list": "Action", "action": "approved",
      "fields": { "verification.status": "verified" },
      "previous": { "verification.status": "pending" },
      "actor": "Davis Dean", "actedAt": "2026-08-13T18:22:04.113Z", "note": null } ] }
```

`action` is `approved`, `edited` or `rejected`. Structured changes only — if you find English sentences in here, something upstream regressed; stop and say so.

## Steps

1. **Read** the export. Reject the file if `schemaVersion` is not 1.
2. **Match** each change to a record by `registerId` across `data/*.json`. A change whose id does not exist is an error, not a create — report it and skip it.
3. **Check the previous value.** If a record's current `verification.status` does not match `previous`, the register moved since the export. **Do not overwrite.** Report the conflict and leave that record alone.
4. **Apply**, per action:
   - `approved` → `verification = {status:'verified', decidedBy: actor, decidedAt: actedAt, note}`
   - `rejected` → `verification = {status:'rejected', decidedBy: actor, decidedAt: actedAt, note}`. Keep the record in the file; the app hides rejected items from every register view. Never delete it — the audit trail is the point.
   - `edited` → apply the named fields, then treat as `approved`. Only ever the fields in `fields`.
5. **Never touch provenance.** A verified item keeps the sentence it came from, permanently.
6. **Append to the audit trail** — `data/audit.json`, creating it if absent: one row per applied change with `registerId, action, field, oldValue, newValue, actor, actedAt, note, appliedAt`.
7. **Update** `data/meta.json` `generatedAt`, then **regenerate `data/snapshot.js`** so the app reflects the new state.
8. **Report**: applied, skipped, conflicted, with ids. Then move the input to `data/inbox/applied/pending-changes-<date>.json` so it cannot be applied twice.

## Rules

- **Idempotent.** Re-applying the same file changes nothing the second time.
- **Never invent a record.** Only existing ids.
- **Never mass-verify.** One change, one decision, one actor, one timestamp.
- **A partial failure fails loudly.** If any write fails, do not regenerate the snapshot from a half-applied state — report which ids landed and which did not.

## Acceptance

- Every `approved` id reads `verified` in its register file, with the actor and timestamp.
- Rejected ids are still present in the file and absent from every register view in the app.
- `data/audit.json` has one row per applied change.
- Reloading the app shows the decisions without anyone re-clicking them.

## Later, not today

When SharePoint writes are available, step 4 also patches the matching list item and step 6 writes a
`BridgeVerificationLog` row. `scripts/store.md` is the only file that should need to change.
