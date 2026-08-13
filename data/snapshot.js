/* Bridge data snapshot — generated. Do not hand-edit.
   Loaded by index.html via a classic <script src>, because fetch() and ES modules
   are blocked on file:// . Regenerated from the register files by scripts/store.md.

   due is an ISO date. The five relative labels this file used to carry ('Today',
   'Tomorrow', 'Mon', 'Wed', 'Later') were resolved once against the moment the tracker
   was last updated by hand — Monday 2026-08-10, 4:35 PM ET, i.e. DATA.updated — because
   that is when a person typed them. Today -> 08-10, Tomorrow -> 08-11, Wed -> 08-12,
   Mon -> 08-17, Later -> 08-24. Human labels are computed at render, never stored.

   reviewed is null on every risk: the source carried no review date. 'Never reviewed'
   is the honest answer and it is what the app shows. Populating it is ingest's job. */
window.BRIDGE_META = {"generatedAt": "2026-08-13T12:39:06", "asOf": "Monday Aug 10, 4:35 PM ET", "timezone": "America/New_York", "schemaVersion": 1, "source": "inline DATA literal, extracted on build day", "sourceSite": null, "listVersions": {}};
window.BRIDGE_DATA =  {
  updated: "Monday Aug 10, 4:35 PM ET",
  workstreams: [
    {id:'ops',  name:'Operations', owner:'Sam Prentice', health:'Y', milestone:'Workflow design sessions running twice weekly. Group 2 (post-launch workflow) still needs a standing slot. Ops readiness checklist is drafted and awaiting sign-off from the site leads.', open:16, docIds:['opsmap','opsdeck','opstrans']},
    {id:'fin',  name:'Finance & Billing', owner:'Morgan Keller · Alex Rivera', health:'Y', milestone:'Finance & Billing kickoff held 8/5. Charge-capture mapping is 45% complete; the reconciliation approach is approved but the exception-handling path is still open.', open:11, docIds:['findeck','plan']},
    {id:'comp', name:'Compliance & Onboarding', owner:'Jordan Chen', health:'G', milestone:'Biweekly cadence running. Standard onboarding started for all 34 partner staff. Review committee target moved from Oct 26 to Nov 9, which is now the long pole on the timeline.', open:9, docIds:['compdeck','complist']},
    {id:'build',name:'System Build & Configuration', owner:'Sam Prentice', health:'Y', milestone:'Integration testing sessions complete for round 1. Cutover planning starts week of 8/17. Change-advisory ownership and the support/ticketing section are still unassigned.', open:24, docIds:['builddeck','testtracker','buildtrans']},
    {id:'lead', name:'Program Leadership', owner:'Alex Rivera · Jordan Chen', health:'G', milestone:'Phase 1 go-live anchor confirmed as end of November 2026. Steering deck v4 posted ahead of the Monday 3:00 PM ET committee meeting; a v2 was requested to call out risks needing escalation.', open:14, docIds:['steer','plan','opsstatus']}
  ],

  /* MEETINGS — dated one-offs only. First instances of a recurring cadence live in `recurring`, not here. */
  meetings: {
    test0811a:{name:'Integration Testing (session 1)', date:'2026-08-11', time:'9:00 ET', ws:'build',
      audience:'Testing team', owner:'Sam Prentice',
      purpose:'Testing-process review ahead of change control.',
      deliverables:[{name:'Testing-process review',required:true,docId:'testtracker'}]},
    test0811b:{name:'Integration Testing (session 2)', date:'2026-08-11', time:'9:30 ET', ws:'build',
      audience:'Testing team', owner:'Sam Prentice',
      purpose:'Best case, cutover planning (change control plus comms). Worst case, another testing round.',
      deliverables:[{name:'Cutover plan (best case)',required:false,docId:null},{name:'Testing-process review',required:false,docId:null}]},
    wqreview0812:{name:'Work Queue Review', date:'2026-08-12', time:'1:00 ET', ws:'build',
      audience:'Riley Novak · Taylor Brooks · Casey Lin · Sam Prentice', owner:'Sam Prentice',
      purpose:'Review the exception and error work queues, decide what changes are needed in the duplicate queues, and agree error-resolution steps plus training.',
      deliverables:[{name:'Interface testing tracker shared with the queue owners',required:true,docId:'testtracker'},{name:'Error-resolution steps and training plan',required:true,docId:null}]},
    dfd0818:{name:'Customer Experience + Change Mgmt, Training & Comms (combined kickoff)', date:'2026-08-18', time:'3:30 ET', ws:'ops',
      audience:'Avery Diaz · Priya Raman · Chris Oyelaran · Dana Whitfield · Casey Lin', owner:'TBD',
      purpose:'Combined kickoff, held after the Operational Kickoff so the scope is already agreed.',
      deliverables:[]},
    itmgr0810:{name:'Weekly Delivery Managers Sync', date:'2026-08-10', time:'12:30 ET', ws:'build',
      audience:'Delivery managers, both sides', owner:'Alex Rivera',
      purpose:'Weekly status. Decision pending on whether to keep the meeting or move to an emailed recap.',
      deliverables:[]}
  },
  standupDays:['2026-08-03','2026-08-04','2026-08-05','2026-08-06','2026-08-07','2026-08-10','2026-08-11','2026-08-12','2026-08-13','2026-08-14','2026-08-17','2026-08-18','2026-08-19','2026-08-20','2026-08-21'],

  /* RECURRING cadences — expanded onto every matching day by eventsOn(). dow: 1=Mon…5=Fri. */
  recurring:[
    {id:'opsweekly', name:'Operations Integration — Project Weekly', dow:2, time:'9:00 ET', cadence:'weekly', from:'2026-07-21', ws:'ops', owner:'Morgan Keller · Sam Prentice', audience:'Riley Novak · Taylor Brooks · Casey Lin · Avery Diaz · Priya Raman', purpose:'Weekly operational integration status across the site teams.', deliverables:[{name:'Weekly ops status roll-up',required:false,docId:null}]},
    {id:'build1', name:'Workflow Design and Build — Group 1', dow:3, time:'10:00 ET', cadence:'weekly', from:'2026-07-29', ws:'build', owner:'Morgan Keller (relay) · Alex Rivera (build execution)', audience:'Scheduling — Riley Novak · Front office — Taylor Brooks · Portal — Dana Whitfield · Interfaces — Casey Lin · Reporting — Jamie Ford · Training — Chris Oyelaran', purpose:'This is the execution track. Identify build needs and work through the build. Target is twice weekly; the second slot is still not locked.', deliverables:[{name:'Build-needs list',required:true,docId:null}]},
    {id:'itmgr', name:'Delivery Leadership Project Status', dow:1, time:'12:30 ET', cadence:'biweekly', anchor:'2026-08-03', ws:'build', owner:'Alex Rivera · Partner delivery leads', audience:'Delivery leadership, both sides', purpose:'Biweekly leadership status and workstream ownership review.', deliverables:[{name:'Delivery leadership deck',required:true,docId:'builddeck'}]},
    {id:'fincyc', name:'Finance & Billing / Compliance Review', dow:3, time:'11:30 ET', cadence:'biweekly', anchor:'2026-08-05', ws:'fin', owner:'Morgan Keller (sched) · Alex Rivera (deck)', audience:'Finance leads · Billing operations · Compliance', purpose:'Biweekly revenue and billing coordination.', deliverables:[{name:'Finance & Billing deck',required:true,docId:'findeck'},{name:'Decisions log seeded',required:false,docId:null}]},
    {id:'build2', name:'Workflow Design and Build — Group 2 (post-launch)', dow:4, time:'11:00 ET', cadence:'weekly', from:'2026-08-06', ws:'build', owner:'Morgan Keller (relay)', audience:'Billing — Jamie Ford · Scheduling — Riley Novak · Records — Casey Lin · Interfaces — Taylor Brooks · Training — Chris Oyelaran', purpose:'Post-launch workflow build session.', deliverables:[]},
    {id:'steer', name:'Weekly Steering Committee', dow:1, time:'3:00 ET', cadence:'weekly', from:'2026-07-20', ws:'lead', owner:'Alex Rivera (facilitation) · Jordan Chen (deck)', audience:'Executive sponsors, both sides · Program leads · Workstream owners', purpose:'Weekly executive steering status. Workstream calls carry the deeper drill-down.', deliverables:[{name:'Steering deck',required:true,docId:'steer'}]},
    {id:'compws', name:'Compliance & Onboarding Working Session', dow:2, time:'3:30 ET', cadence:'biweekly', anchor:'2026-08-04', ws:'comp', owner:'Jordan Chen · Dana Whitfield', audience:'Compliance · Onboarding · Partner readiness team', purpose:'Biweekly onboarding and approvals coordination.', deliverables:[{name:'Onboarding document list',required:true,docId:'complist'}]},
    {id:'leadstrat', name:'Leadership Strategy Sync (internal)', dow:5, from:'2026-07-24', until:'2026-08-08', time:'3:30 ET', cadence:'weekly', ws:'lead', owner:'Alex Rivera', audience:'Program leads only, no vendor present', purpose:'Internal leadership sync. On hold pending a scheduling follow-up.', deliverables:[]}
  ],

  /* NEEDS SCHEDULING — discussed in the channel but no date/time locked yet. */
  unscheduled:[
    {id:'u1', title:'System Build & Config (full workstream leads), biweekly', ws:'build', reason:'Cadence changed from weekly on 7/20. New slot not yet locked.'},
    {id:'u2', title:'Weekly delivery status roll-up (sub-team)', ws:'build', reason:'Newly added standing meeting, on top of the biweekly System Build cadence. @mkeller scheduling.'},
    {id:'u3', title:'Operations recurring cadence', ws:'ops', reason:'Kickoff happened 8/3. Day and time for the weekly still not locked; waiting on availability from three site leads.'},
    {id:'u4', title:'Finance and Compliance joint working session', ws:'fin', reason:'Covers both workstreams operationally. Not yet scheduled.'},
    {id:'u5', title:'Operational Kickoff (full cross-functional)', ws:'lead', reason:'Large cross-functional kickoff targeted for week of 8/17, 1 hour. Exact day and time not set.'},
    {id:'u6', title:'Executive internal sync, twice weekly', ws:'lead', reason:'New request. Two internal syncs per week to drive tracking. @arivera scheduling.'},
    {id:'u7', title:'Workflow Design & Build — second weekly slot', ws:'build', reason:'First slot is Wed 10:00 ET. Target is twice weekly per the 7/23 decision. Second slot not locked.'},
    {id:'u8', title:'Cutover and go-live review', ws:'build', reason:'To be scheduled after the 8/11 testing sessions. Cutover to be treated as a named deliverable.'}
  ],

  /* ITEMS — unified: Action / Decision / Blocker / Risk / Issue. */
  items: [
    /* — Alex Rivera (@arivera) — */
    {id:'a1', kind:'Action', urg:'High', title:'Send the approved Finance & Billing deck to attendees ahead of the call', owner:'AR', due:'2026-08-10', status:'open', meetingId:'fincyc', deliv:{mid:'fincyc'}, note:'Deck reviewed and approved. Requested to go out before the call, by end of day if possible.', src:{kind:'slack', url:'#'}, verification:{status:'pending',decidedBy:null,decidedAt:null,note:'Captured from a source; no person has checked it.'}},
    {id:'a2', provenance:{"sourceSystem": "transcript", "docId": "steertrans", "line": 15, "author": "Alex Rivera", "messageTs": "2026-08-07 09:17 ET", "permalink": null, "quote": "I will chase the partner team on the outstanding contract signatures.", "confidence": "high"}, meetingId:'steer', kind:'Action', urg:'High', title:'Chase the partner team on outstanding contract signatures', owner:'AR', due:'2026-08-10', status:'open', note:'No-show at the 8/3 steering call. Overdue from 8/4, in progress.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a3', kind:'Action', urg:'High', title:'Finalize the Compliance V1 deck — add standards slides plus a decisions-needed slide', owner:'AR', due:'2026-08-10', status:'open', meetingId:'compws', deliv:{mid:'compws'}, note:'Overdue from 8/4, in progress.', src:{kind:'transcript', docId:'comptrans'}, verification:{status:'pending',decidedBy:null,decidedAt:null,note:'Captured from a source; no person has checked it.'}},
    {id:'a4', provenance:{"sourceSystem": "transcript", "docId": "buildtrans", "line": 13, "author": "Alex Rivera", "messageTs": "2026-08-06 14:20 ET", "permalink": null, "quote": "On the build timeline — I will present the system build timeline at the leadership deliverable review on the seventeenth.", "confidence": "high"}, kind:'Action', urg:'High', title:'Present the system build timeline at the 8/17 leadership deliverable review', owner:'AR', due:'2026-08-24', status:'open', note:'Sequence: individual meetings, deep dive, timeframes and dependencies, partner overlay, align, present.', src:{kind:'transcript', docId:'buildtrans'}, verification:{status:'pending',decidedBy:null,decidedAt:null,note:'Captured from a source; no person has checked it.'}},
    {id:'a5', provenance:{"sourceSystem": "transcript", "docId": "steertrans", "line": 12, "author": "Alex Rivera", "messageTs": "2026-08-07 09:12 ET", "permalink": null, "quote": "I will send the consolidated project plan to the partner team for validation and a discrepancy review.", "confidence": "high"}, meetingId:'steer', kind:'Action', urg:'Med', title:'Send the consolidated project plan to the partner team for validation and discrepancy review', owner:'AR', due:'2026-08-24', status:'open', note:'From the 8/4 morning standup.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a6', kind:'Action', urg:'Med', title:'Confirm who owns taking the integration to the Change Advisory Board', owner:'AR', due:'2026-08-24', status:'open', meetingId:'itmgr', deliv:{mid:'itmgr'}, note:'Raised as a deliverable gap on the delivery leadership call.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a7', kind:'Action', urg:'Med', title:'Add a support and ticketing section to the leadership status — who receives tickets after go-live', owner:'AR', due:'2026-08-24', status:'open', meetingId:'itmgr', deliv:{mid:'itmgr'}, note:'Leadership status deliverable, still unowned.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a8', kind:'Action', urg:'Med', title:'Merge the consolidated project plan with the partner implementation team plan', owner:'AR', due:'2026-08-24', status:'open', note:'Loop the partner implementation team into the relevant workstream meetings going forward.', src:{kind:'transcript', docId:'steertrans'}, verification:{status:'pending',decidedBy:null,decidedAt:null,note:'Captured from a source; no person has checked it.'}},
    {id:'a9', provenance:{"sourceSystem": "transcript", "docId": "steertrans", "line": 17, "author": "Alex Rivera", "messageTs": "2026-08-07 09:22 ET", "permalink": null, "quote": "I will confirm the steering committee roster on the delivery side and come back on whether we need a technical executive sponsor.", "confidence": "high"}, meetingId:'steer', kind:'Action', urg:'Low', title:'Confirm the steering committee roster on the delivery side', owner:'AR', due:'2026-08-24', status:'open', note:'Is a technical executive sponsor needed beyond the current list?', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a10', kind:'Action', urg:'High', title:'Build the steering deck timeline slide, date-anchored to an end-of-November phase 1 go-live', owner:'AR', due:'2026-08-24', status:'done', meetingId:'steer', deliv:{mid:'steer'}, note:'Completed 2026-08-07. Go-live anchor confirmed as end of November 2026, superseding the prior early-November back-plan. v4 posted as a lean four-slide pack.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},

    /* — Jordan Chen (@jchen) — */
    {id:'a11', kind:'Action', urg:'High', title:'Book a session with the onboarding team to start standard enrollment immediately', owner:'JC', due:'2026-08-10', status:'open', meetingId:'compws', deliv:{mid:'compws'}, note:'The delegated path is off. With only 34 partner staff, standard individual onboarding starts now, so there is no agreement to wait on.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a12', kind:'Action', urg:'High', title:'Send the partner team the exact onboarding document list and get a review meeting booked', owner:'JC', due:'2026-08-11', status:'open', note:'From the 8/7 steering transcript.', src:{kind:'transcript', docId:'steertrans'}, verification:{status:'pending',decidedBy:null,decidedAt:null,note:'Captured from a source; no person has checked it.'}},
    {id:'a13', provenance:{"sourceSystem": "transcript", "docId": "comptrans", "line": 10, "author": "Jordan Chen", "messageTs": "2026-08-04 16:09 ET", "permalink": null, "quote": "I will confirm the delegated-approval agreement legal review status and return the signed agreement. Due end of week.", "confidence": "high"}, meetingId:'compws', kind:'Action', urg:'Med', title:'Confirm delegated-approval agreement legal review status and return the signed agreement', owner:'JC', due:'2026-08-24', status:'open', note:'Due end of week.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a14', kind:'Action', urg:'Med', title:'Roll the week of action-item updates into the steering Next Steps slide', owner:'JC', due:'2026-08-17', status:'open', meetingId:'steer', deliv:{mid:'steer'}, note:'Folded into the per-workstream next-steps slide.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a15', kind:'Action', urg:'Low', title:'Schedule a training-environment walkthrough of the flagged workflows for the clinical reviewers', owner:'JC', due:'2026-08-24', status:'open', note:'Screen-out versus refer-out logic needs a live demo.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a16', kind:'Action', urg:'Med', title:'Second-pass review of the consolidated project plan draft', owner:'JC', due:'2026-08-24', status:'done', note:'Completed 2026-08-06 with feedback from all three workstream leads folded in.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},

    /* — Sam Prentice (@sprentice) — */
    {id:'a17', kind:'Action', urg:'High', title:'Resubmit the failed test message using a known-good provider record and notify the workflow tester', owner:'SP', due:'2026-08-10', status:'open', note:'Workaround while partner identity records are unresolved.', src:{kind:'transcript', docId:'buildtrans'}, verification:{status:'pending',decidedBy:null,decidedAt:null,note:'Captured from a source; no person has checked it.'}},
    {id:'a18', provenance:{"sourceSystem": "transcript", "docId": "buildtrans", "line": 11, "author": "Sam Prentice", "messageTs": "2026-08-06 14:12 ET", "permalink": null, "quote": "Configurable. I will confirm the partner records exist in the target system with the correct identifiers, and the records team will create them if they are missing.", "confidence": "high"}, kind:'Action', urg:'High', title:'Confirm partner records exist in the target system with correct identifiers', owner:'SP', due:'2026-08-10', status:'open', note:'Records team to create them if missing. Production intent, which removes the test workaround.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a19', kind:'Action', urg:'Med', title:'Walk through the partner workflow to test message triggers', owner:'SP', due:'2026-08-24', status:'open', note:'Blocked on the partner delivering the open-item steps.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a20', kind:'Action', urg:'Med', title:'Share the combined interface script tracker with the partner team', owner:'SP', due:'2026-08-10', status:'open', meetingId:'wqreview0812', deliv:{mid:'wqreview0812'}, note:'Due 8/12 ahead of the work queue review.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a21', kind:'Action', urg:'Med', title:'Locate and document the record-matching weight configuration; confirm the weighting is adequate', owner:'SP', due:'2026-08-24', status:'open', note:'From the 8/6 interface review.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a22', kind:'Action', urg:'Med', title:'Determine viable test-run count per script given the partner email and phone reuse limit', owner:'SP', due:'2026-08-10', status:'open', note:'Overdue from 8/5.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a23', kind:'Action', urg:'Med', title:'Confirm that partner-sourced documents render as expected in the customer portal', owner:'SP', due:'2026-08-24', status:'open', note:'From the 8/6 interface review.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a24', kind:'Action', urg:'Low', title:'Clarify the release-of-information process for partner-sourced documents', owner:'SP', due:'2026-08-24', status:'open', note:'Confirm scope with the vendor. May need a separate statement of work.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},

    /* — Morgan Keller (@mkeller) — */
    {id:'a25', kind:'Action', urg:'High', title:'Lock the second weekly slot for Workflow Design & Build', owner:'MK', due:'2026-08-11', status:'open', note:'Target is twice weekly per the 7/23 decision. Waiting on availability from two leads.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a26', kind:'Action', urg:'Med', title:'Schedule the cutover and go-live review after the 8/11 testing sessions', owner:'MK', due:'2026-08-12', status:'open', note:'Cutover to be treated as a named deliverable, not an event.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a27', kind:'Action', urg:'Med', title:'Stand up a 15-minute weekly all-group status call', owner:'MK', due:'2026-08-24', status:'open', note:'Deferring one to two weeks until there is enough to report. Target roughly 8/24.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a28', kind:'Action', urg:'Med', title:'Update meeting dates on steering deck slide 3', owner:'MK', due:'2026-08-24', status:'done', meetingId:'steer', deliv:{mid:'steer'}, note:'Completed 2026-08-07. Slide 3 stays as an overview; dates moved to the timeline slide.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a29', kind:'Action', urg:'Low', title:'Confirm whether the 8/12 session is the last testing round before change control', owner:'MK', due:'2026-08-24', status:'open', note:'From the 8/5 standup.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},

    /* — Unassigned — */
    {id:'a30', kind:'Action', urg:'Med', title:'Fill the open operations program manager seat', owner:'Unassigned', due:'2026-08-24', status:'open', note:'Two new partner-side PM seats are open: operations PM and technical PM.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'a31', kind:'Action', urg:'Med', title:'Send over the onboarding documentation already on hand for the 34 partner staff', owner:'Unassigned', due:'2026-08-24', status:'open', note:'Speeds the partner packet build. Due end of week.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},

    /* — RISKS, BLOCKERS, ISSUES — */
    {id:'r1', kind:'Blocker', urg:'High', title:'Partner team to provide open-item details — unblocks the workflow test', owner:'SP', sev:'R', reviewed:null, status:'open', due:'2026-08-10', note:'Consent, procedures, exception handling, and update triggers all still outstanding. Being chased.', src:{kind:'transcript', docId:'buildtrans'}, verification:{status:'pending',decidedBy:null,decidedAt:null,note:'Captured from a source; no person has checked it.'}},
    {id:'r2', provenance:{"sourceSystem": "transcript", "docId": "buildtrans", "line": 7, "author": "Sam Prentice", "messageTs": "2026-08-06 14:03 ET", "permalink": null, "quote": "Roughly a third of the 14,500 records in the initial load read as potential duplicates.", "confidence": "high"}, kind:'Risk', urg:'High', title:'Record load duplicate matching — roughly a third of 14,500 records read as duplicates', owner:'SP', sev:'R', reviewed:null, status:'open', note:'Proposed workaround is a provisional-record workflow: hold the load, work the duplicates, then finalize. Internal decision still pending.', src:{kind:'transcript', docId:'buildtrans'}, verification:{status:'pending',decidedBy:null,decidedAt:null,note:'Captured from a source; no person has checked it.'}},
    {id:'r3', provenance:{"sourceSystem": "transcript", "docId": "comptrans", "line": 11, "author": "Jordan Chen", "messageTs": "2026-08-04 16:15 ET", "permalink": null, "quote": "One risk worth recording — the review committee meets monthly, and the realistic slot is the ninth of November rather than the twenty-sixth of October.", "confidence": "high"}, meetingId:'compws', kind:'Risk', urg:'High', title:'Onboarding timeline is the main risk to the end-of-November go-live', owner:'JC', sev:'R', reviewed:null, status:'open', note:'The review committee meets monthly. Nov 9 is more realistic than Oct 26, which pushes past the planned go-live date.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'r4', kind:'Risk', urg:'Med', title:'Partner workflow spec unclear — which configuration triggers a status message', owner:'SP', sev:'Y', reviewed:null, status:'open', note:'Behavior on a return interaction within 24 hours versus after is still open. Blocks workflow testing.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'r5', kind:'Risk', urg:'Med', title:'Test-record coverage limit — the partner system requires a unique email and phone per record', owner:'SP', sev:'Y', reviewed:null, status:'open', note:'The tester may be out of test emails and phone numbers, capping coverage.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'r6', kind:'Risk', urg:'Med', title:'Analytics licensing caps at 4 seats — over-dependent on a single partner-side SME', owner:'MK', sev:'Y', reviewed:null, status:'open', note:'Additional seats run $6,200 per year each. Plan is to add no-license raw-data access for an internal team member as redundancy.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'r7', kind:'Risk', urg:'Med', title:'Stale project tracker still circulating', owner:'AR', sev:'Y', reviewed:null, status:'open', note:'Do not use as-is. The consolidated project plan is canonical. Watching.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'r8', kind:'Risk', urg:'Low', title:'Deck versioning slip — an old version was shared on 8/3', owner:'JC', sev:'Y', reviewed:null, status:'open', note:'Always share the active version going forward. Watching.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'i1', kind:'Issue', urg:'Med', title:'Document format needs sign-off — section order differs from the house standard', owner:'SP', sev:'Y', reviewed:null, status:'open', note:'Asks on record: remove the dead link, fix the confusing prior-interaction reference, and reorder the summary block to the top.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},

    /* — DECISIONS — */
    {id:'d1', provenance:{"sourceSystem": "transcript", "docId": "steertrans", "line": 8, "author": "Morgan Keller", "messageTs": "2026-08-07 09:04 ET", "permalink": null, "quote": "Phase 1 go-live is anchored to the end of November 2026. That is confirmed on both sides, and it supersedes the early-November back-plan.", "confidence": "high"}, meetingId:'steer', kind:'Decision', urg:'High', title:'Phase 1 go-live anchored to end of November 2026', owner:'Team', date:'Aug 7', note:'Confirmed on both sides. Supersedes the earlier early-November back-plan. All timeline slides now key off this date.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'d2', provenance:{"sourceSystem": "transcript", "docId": "comptrans", "line": 9, "author": "Morgan Keller", "messageTs": "2026-08-04 16:06 ET", "permalink": null, "quote": "Then the delegated path is not worth the wait. Standard individual onboarding starts now.", "confidence": "high"}, meetingId:'compws', kind:'Decision', urg:'High', title:'Delegated approval path is off — standard individual onboarding starts now', owner:'Team', date:'Aug 4', note:'With only 34 partner staff, the delegated agreement is not worth the wait. Individual onboarding begins immediately.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'d3', kind:'Decision', urg:'Med', title:'Two-week sprint cadence for phase 1', owner:'Team', date:'Aug 5', note:'Chosen over three weeks so there are two full review points before go-live.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'d4', kind:'Decision', urg:'Med', title:'Steering deck rebuilt as a lean four-slide pack', owner:'Team', date:'Aug 3', note:'Title, Focus, Workstream Overview, Two-Sprint Timeline. The old week-by-week slide and the appendix were dropped rather than extended.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'d5', kind:'Decision', urg:'Med', title:'Workflow design sessions split into pre-launch and post-launch groups', owner:'Team', date:'Jul 30', note:'Group 1 covers pre-launch design, Group 2 covers post-launch. Both run weekly.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'d6', kind:'Decision', urg:'Low', title:'The consolidated project plan is the canonical source for milestones', owner:'Team', date:'Jul 28', note:'The older tracker is archived. Any milestone question resolves against the consolidated plan.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'d7', provenance:{"sourceSystem": "transcript", "docId": "steertrans", "line": 11, "author": "Morgan Keller", "messageTs": "2026-08-07 09:08 ET", "permalink": null, "quote": "Agreed. We rename it to Platform Consolidation. All decks get updated.", "confidence": "high"}, meetingId:'steer', kind:'Decision', urg:'Low', title:'Program renamed from "Revenue Systems" to "Platform Consolidation"', owner:'Team', date:'Aug 7', note:'Clarified at steering. The old name understated the scope. All decks updated.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}},
    {id:'d8', kind:'Decision', urg:'Low', title:'Cutover treated as a named deliverable with an owner', owner:'Team', date:'Aug 6', note:'Previously tracked as an event with no owner, which is how it kept slipping.', verification:{status:'verified',decidedBy:'seeded',decidedAt:null,note:'Typed into the tracker by a person before Bridge existed.'}}
  ],

  documents: [
    {id:'plan', title:'Consolidated Project Plan.xlsx', type:'spreadsheet', kind:'link', source:'SharePoint', ws:'lead', updated:'Re-shared in thread 8/6', new:false,
      url:'#',
      ctx:'The consolidated project plan and risk list. Canonical source for milestones. Dated items currently stop at 9/18; testing, soft launch, training, and go-live rows are still to be filled in.'},
    {id:'steer', title:'Weekly Steering Committee.pptx', type:'deck', kind:'link', source:'SharePoint', ws:'lead', updated:'v4 posted 8/7 10:14 AM; structure finalized the same morning ahead of the 3:00 PM meeting', new:true,
      url:'#',
      ctx:'Executive steering deck. Rebuilt into a lean four-slide pack (Title, Focus, Workstream Overview, Two-Sprint Timeline). Phase 1 end date updated to end of November.'},
    {id:'builddeck', title:'Delivery_Leadership_Status_v4.pptx', type:'deck', kind:'link', source:'SharePoint', ws:'build', updated:'Draft posted 8/7 10:21 AM', new:true,
      url:'#',
      ctx:'Deck for the 12:30 ET delivery leadership call. Next steps per workstream plus the System Build drill-down. Flagged as needing cleanup before it goes out.'},
    {id:'findeck', title:'Finance_Billing_Compliance_Kickoff_v2.pptx', type:'deck', kind:'link', source:'SharePoint', ws:'fin', updated:'Posted 8/7, reviewed and approved 10:26 AM, sent for input', new:true,
      url:'#',
      ctx:'Kickoff deck for the biweekly Finance & Billing review. Mirrors the Compliance deck structure so the two read consistently.'},
    {id:'compdeck', title:'Compliance_Onboarding_V1.pptx', type:'deck', kind:'link', source:'SharePoint', ws:'comp', updated:'V1 posted 8/4; standards slides still to be added', new:false,
      url:'#',
      ctx:'Working-session deck for the biweekly Compliance & Onboarding call. Still needs the standards slides and a decisions-needed slide.'},
    {id:'complist', title:'Onboarding Document Checklist.xlsx', type:'spreadsheet', kind:'link', source:'SharePoint', ws:'comp', updated:'Updated 8/6 with the full 34-person roster', new:false,
      url:'#',
      ctx:'Per-person document checklist for the 34 partner staff. Drives the onboarding status column on the steering deck.'},
    {id:'testtracker', title:'Integration Test Script Tracker.xlsx', type:'spreadsheet', kind:'needs-sp', source:'Uploaded to the channel', ws:'build', updated:'Posted in channel 8/6, not yet moved to SharePoint', new:true,
      ctx:'Combined interface and workflow test scripts with pass/fail status. Loose upload, needs to move to SharePoint so both sides can open the current version.'},
    {id:'opsmap', title:'Operational Workflow Map (draft).pdf', type:'pdf', kind:'needs-sp', source:'Uploaded to the channel', ws:'ops', updated:'Draft shared 8/4', new:false,
      ctx:'Hand-drawn workflow map from the 8/4 design session, scanned and posted. Needs to be redrawn properly and moved to SharePoint.'},
    {id:'opsdeck', title:'Operations_Readiness_Checklist.docx', type:'doc', kind:'link', source:'SharePoint', ws:'ops', updated:'Drafted 8/5, awaiting site lead sign-off', new:false,
      url:'#',
      ctx:'Site-by-site readiness checklist. Four of six site leads have signed off.'},
    {id:'opsstatus', title:'Workstream Status Roll-up.xlsx', type:'spreadsheet', kind:'link', source:'SharePoint', ws:'lead', updated:'Auto-refreshed 8/10 12:07 AM', new:false,
      url:'#',
      ctx:'Generated roll-up that feeds the workstream cards on this page. Rebuilt on every refresh pass.'},
    {id:'steertrans', title:'Steering Committee transcript — Aug 7', type:'doc', kind:'slack', source:'Posted in channel', ws:'lead', updated:'Posted 8/7 4:12 PM', new:true,
      slackUrl:'#',
      ctx:'Full transcript. Source for the go-live anchor confirmation, the program rename, and four of the open actions.'},
    {id:'buildtrans', title:'Interface Review transcript — Aug 6', type:'doc', kind:'slack', source:'Posted in channel', ws:'build', updated:'Posted 8/6 2:40 PM', new:true,
      slackUrl:'#',
      ctx:'Source for the duplicate-matching risk, the record-matching weight question, and the portal rendering check.'},
    {id:'comptrans', title:'Compliance Working Session transcript — Aug 4', type:'doc', kind:'slack', source:'Posted in channel', ws:'comp', updated:'Posted 8/4 4:35 PM', new:false,
      slackUrl:'#',
      ctx:'Source for the delegated-versus-standard onboarding decision and the committee timing risk.'},
    {id:'opstrans', title:'Operations Design Session transcript — Aug 4', type:'doc', kind:'slack', source:'Posted in channel', ws:'ops', updated:'Posted 8/4 11:20 AM', new:false,
      slackUrl:'#',
      ctx:'Source for the workflow map and the pre-launch versus post-launch group split.'}
  ],

  threads: [
    {id:'t1', time:'Mon 8/10 · 4:23–4:29 PM', participants:['AR','CL'], ws:null,
      topic:'Completion sweep — 4 items moved to Completed',
      summary:'Four finished action items were moved to Completed in one pass: the steering timeline slide, the slide 3 date update, the project plan second-pass review, and the workstream overview slide. Each was confirmed against its source message before being moved, and the workstream open counts were recalculated.',
      links:[{slack:'#'},{docId:'plan'}],
      into:[{kind:'action', label:'4 items completed (a10, a16, a28, and the workstream overview slide)', route:'items'}]},
    {id:'t2', time:'Fri 8/7 · 3:00–4:10 PM', participants:['AR','JC','MK'], ws:'lead',
      topic:'Steering committee — go-live anchor confirmed, program renamed',
      summary:'The end-of-November phase 1 go-live was confirmed on both sides, superseding the earlier early-November back-plan. The program was renamed from Revenue Systems to Platform Consolidation because the old name understated the scope. Two new partner-side PM seats were announced. The onboarding committee timing was flagged as the main risk to holding the date.',
      links:[{slack:'#'},{docId:'steertrans'}],
      into:[{kind:'decision', label:'Go-live anchored to end of November 2026', route:'items'},{kind:'decision', label:'Program renamed to Platform Consolidation', route:'items'},{kind:'action', label:'3 new actions captured', route:'items'}]},
    {id:'t3', time:'Thu 8/6 · 2:00–2:55 PM', participants:['SP','MK'], ws:'build',
      topic:'Interface review — duplicate matching and record identity',
      summary:'The reconciled testing sheet was walked against the partner follow-up, then the conversation pivoted into record matching. Three scenarios were agreed: match, potential duplicate, and no match creating a new record, with creation never allowed to block document filing. Open before 8/18: which work queue catches a non-match, who owns cleanup, and whether the document feed uses the same identity logic as the demographic feed.',
      links:[{slack:'#'},{docId:'buildtrans'}],
      into:[{kind:'risk', label:'Duplicate matching risk raised to High', route:'items'},{kind:'action', label:'2 new actions captured', route:'items'}]},
    {id:'t4', time:'Wed 8/5 · 11:30 AM–12:15 PM', participants:['MK','AR'], ws:'fin',
      topic:'Finance & Billing kickoff',
      summary:'Charge-capture mapping is roughly 45 percent complete. The reconciliation approach was approved, but exception handling is still open and nobody owns it yet. The deck was approved for distribution and asked to go out before the next call.',
      links:[{slack:'#'},{docId:'findeck'}],
      into:[{kind:'action', label:'Send the approved deck ahead of the call', route:'items'}]},
    {id:'t5', time:'Tue 8/4 · 3:30–4:20 PM', participants:['JC','SP'], ws:'comp',
      topic:'Compliance working session — delegated path is off',
      summary:'With only 34 partner staff in scope, waiting on a delegated approval agreement was judged not worth the delay. Standard individual onboarding starts immediately. The review committee meets monthly, and November 9 is more realistic than October 26, which is now the long pole on the timeline.',
      links:[{slack:'#'},{docId:'comptrans'}],
      into:[{kind:'decision', label:'Delegated approval path off, standard onboarding starts now', route:'items'},{kind:'risk', label:'Onboarding timeline risk raised to High', route:'items'}]},
    {id:'t6', time:'Tue 8/4 · 10:00–11:15 AM', participants:['SP','MK','AR'], ws:'ops',
      topic:'Operations design session — pre-launch and post-launch split',
      summary:'The single design track was split into two groups, one for pre-launch workflow and one for post-launch. Both run weekly. A hand-drawn workflow map came out of the session and was posted to the channel; it still needs to be redrawn and moved to SharePoint.',
      links:[{slack:'#'},{docId:'opstrans'}],
      into:[{kind:'decision', label:'Design sessions split into two weekly groups', route:'items'},{kind:'action', label:'Move the workflow map to SharePoint', route:'documents'}]}
  ],

  digest: [
    {title:'Go-live date is anchored, but onboarding is the long pole', open:['Does the review committee timing leave enough runway, or does phase 1 scope need to shrink?'],
      summary:'The end-of-November phase 1 go-live is now confirmed on both sides and every timeline slide keys off it. The complication is that the onboarding review committee meets monthly and the realistic slot is November 9, which lands inside the go-live window rather than before it. Standard individual onboarding has started immediately to buy back time, but this is the single thread most likely to move the date.'},
    {title:'Duplicate record matching is the largest technical risk', open:['Which work queue catches a non-match, and who owns cleanup?','Does the document feed use the same identity logic as the demographic feed?'],
      summary:'Roughly half of the 14,500 records in the initial load read as potential duplicates. The proposed workaround is a provisional-record workflow: hold the load, work the duplicates, then finalize. The internal decision on that is still pending. Agreement was reached that record creation must never block document filing, which removes the worst failure mode even if the volume question stays open.'},
    {title:'Several deliverables have no owner', open:['Who takes the integration to the Change Advisory Board?','Who receives support tickets after go-live?'],
      summary:'Three items surfaced on the delivery leadership call with no owner attached: change advisory board ownership, the support and ticketing path after go-live, and the cutover itself. Cutover has since been reclassified as a named deliverable rather than an event, which is the reason it kept slipping. The other two are still open and are being tracked as leadership deliverables.'}
  ],

  team: [
    {ini:'AR', nm:'Alex Rivera', rl:'Program lead / builder', side:'Both sides', color:'#0f2a43', sidec:'#dcfce7', sidefg:'#15803d'},
    {ini:'JC', nm:'Jordan Chen', rl:'Compliance / status reporting', side:'Both sides', color:'#7c3aed', sidec:'#dcfce7', sidefg:'#15803d'},
    {ini:'SP', nm:'Sam Prentice', rl:'Testing · integrations · build', side:'Delivery side', color:'#0369a1', sidec:'#e0f2fe', sidefg:'#0369a1'},
    {ini:'MK', nm:'Morgan Keller', rl:'Operations / scheduling', side:'Client side', color:'#be185d', sidec:'#fce7f3', sidefg:'#be185d'}
  ]
};
