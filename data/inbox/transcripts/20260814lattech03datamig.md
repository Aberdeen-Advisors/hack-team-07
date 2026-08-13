Meeting ID: LAT-TECH-03
Title: Project Lattice - Data Migration Technical Deep Dive
Date: Friday, 14 August 2026
Time: 11:00 - 12:05 (BST)
Platform: Calderwood Teams bridge

Attendees:
  Anjali Kalavar - Aberdeen - Engagement Lead, Project Lattice
  Davis Dean - Aberdeen - Consultant, Delivery & Build workstream
  Hank Liu - Calderwood Utilities - Platform Engineering SME
  Renata Voss - Calderwood Utilities - Billing Data Steward / Data Owner
  (Will Brown - Aberdeen - apologies)

Recording transcribed automatically.

---

[11:00:14] Anjali Kalavar: Morning. Hank, Renata - thanks for making a Friday morning work.
[11:00:25] Hank Liu: Friday's the only day I get to think.
[11:00:31] Anjali Kalavar: Quick note - Will Brown's not on this one, he's out today, so anything that needs a compliance view we'll park and I'll take it to him Monday.
[11:00:56] Renata Voss: Fine. Most of what I've got is data, not compliance.
[11:01:04] Anjali Kalavar: Good. Davis is going to walk the trial migration results, then I want to get to the duplicate key problem, then cutover windows, then reconciliation. Davis, over to you.
[11:01:31] Davis Dean: Thanks. Let me share the run report. [screen share] Can everyone see the summary tab?
[11:01:45] Hank Liu: Yes.
[11:01:49] Renata Voss: I can see it. It's a lot of red.
[11:01:57] Davis Dean: It is more red than I'd like, though some of it is red for boring reasons. So - trial migration run two, executed Tuesday night into Wednesday morning. Full extract from the legacy billing platform, transform, load into the Lattice staging tenant.
[11:02:25] Davis Dean: Runtime was eleven hours forty minutes. Our target for cutover is under eight, so that's the first problem.
[11:02:42] Hank Liu: Eleven forty is better than run one though.
[11:02:49] Davis Dean: Run one was nineteen hours, so yes. We've nearly halved it. The remaining time is heavily concentrated in one place - the meter read history transform is about sixty percent of the total runtime on its own.
[11:03:13] Renata Voss: How many rows are we talking?
[11:03:20] Davis Dean: Meter reads at eighteen months' depth, it's about two hundred and ten million rows.
[11:03:37] Renata Voss: And at seven years?
[11:03:42] Davis Dean: Somewhere north of nine hundred million. It's not linear because read frequency went up when the smart meter rollout started in 2022.
[11:04:00] Hank Liu: So the recent years are much fatter than the old ones.
[11:04:11] Davis Dean: Considerably. A 2019 account might have six reads a year. A 2025 smart-metered account has one every half hour, aggregated to daily for billing, but we hold the half-hourly.
[11:04:44] Renata Voss: We hold the half-hourly for two years and then it aggregates. That's the policy, at least - it's enforced by a job that runs monthly and fails about a third of the time.
[11:05:14] Davis Dean: So it's aspirational.
[11:05:33] Renata Voss: It's aspirational with good intentions.
[11:05:48] Anjali Kalavar: Then let's check rather than assume. Renata, can somebody profile how much unaggregated half-hourly data is actually sitting in there?
[11:06:11] Renata Voss: I can do that myself, it's a query. I'll have a number by Tuesday the eighteenth.
[11:06:23] Anjali Kalavar: Renata, half-hourly data volume profile, eighteenth of August. Noted.
[11:06:33] Davis Dean: Right, moving down the report. Record counts. We extracted four hundred and thirty-eight thousand two hundred and six accounts. We loaded four hundred and thirty-one thousand nine hundred and eighty-eight.
[11:07:01] Renata Voss: So six thousand two hundred and eighteen didn't land.
[11:07:13] Davis Dean: Six thousand two hundred and eighteen rejected. And that number is the reason I wanted this session.
[11:07:27] Hank Liu: Rejected on what?
[11:07:33] Davis Dean: Ninety-one percent of them on a single validation rule. Duplicate account key on the meter read join.
[11:07:51] Renata Voss: Ah.
[11:07:56] Davis Dean: You've said "ah" in a way that suggests you know what I'm about to describe.
[11:08:10] Renata Voss: I might. Go on, describe it, and I'll tell you if it's the thing I'm thinking of.
[11:08:21] Davis Dean: So. In the legacy platform, meter reads are keyed on what the schema calls ACCT_REF. We'd assumed ACCT_REF was unique per account, because it's named like a primary key and it's indexed like a primary key.
[11:08:45] Hank Liu: It's not a primary key.
[11:08:50] Davis Dean: It is not a primary key. It's a composite in disguise. There are ACCT_REF values that appear against two, three, in one case eleven different accounts.
[11:09:16] Renata Voss: Eleven?
[11:09:21] Davis Dean: Eleven. It's a block of flats in Aberdeenshire.
[11:09:30] Renata Voss: Right, then it is the thing I'm thinking of. This goes back to the 2016 merger. When we absorbed the Kincraig water assets we brought over their account references as-is, and their reference scheme wasn't account-level, it was supply-point-level. So a building with a shared supply point got one reference and multiple billing accounts hanging off it.
[11:10:23] Hank Liu: And nobody remediated it.
[11:10:29] Renata Voss: There was a remediation project. It ran for eighteen months, fixed about forty percent of the population, and then got cancelled when the person running it left.
[11:10:51] Davis Dean: So the sixty percent is still there.
[11:11:00] Renata Voss: Some of it. There's been organic cleanup since - every time someone touches one of these accounts manually they tend to fix it. So it's decayed rather than been solved.
[11:11:29] Anjali Kalavar: Do we know how many accounts are affected in total, as opposed to how many failed this particular run?
[11:11:44] Davis Dean: That's the question I can't answer yet. Six thousand two hundred failed validation, but validation only catches the ones where the duplication causes an actual join collision. There could be a larger population where the duplication exists but happens not to break anything in this particular transform.
[11:12:30] Hank Liu: And those are worse, because they'd migrate silently and be wrong on the other side.
[11:12:44] Davis Dean: Exactly. Those are the ones that keep me awake.
[11:12:55] Renata Voss: Okay. That's a red. I want to be clear about that - as the data owner, that's a red for me. Not because it's unfixable, but because we don't know the size of it, and we're eleven weeks from go-live.
[11:13:29] Anjali Kalavar: Agreed, red. And I'd say it's a red on two counts - the volume is unknown, and the remediation path is unknown.
[11:13:46] Hank Liu: Can I ask something on the remediation path? Is this something we fix in the source or something we fix in the transform?
[11:14:10] Davis Dean: That's exactly the decision we need to make today.
[11:14:18] Hank Liu: Then let me argue one side. If we fix it in the transform - if we synthesise a new unique key on the way through - then the legacy platform stays wrong for the four months of parallel run, and any manual work anybody does on the legacy side during that period creates new divergence.
[11:14:57] Renata Voss: That's true. And the operations team do a lot of manual work.
[11:15:10] Hank Liu: Whereas if we fix it in the source, we're doing surgery on a live billing platform that's about to be decommissioned, which is - not enjoyable.
[11:15:28] Davis Dean: Not enjoyable and not fast. You'd be looking at a change control per batch.
[11:15:41] Renata Voss: There's a third option and it's the one I'd push for. We fix it in the transform, and we freeze manual account-reference changes on the legacy platform during the parallel run.
[11:16:01] Davis Dean: Can you freeze that? Operationally?
[11:16:10] Renata Voss: I can. It's my data domain. I'd need to give the operations leads notice and I'd need an exception route for genuine emergencies, but the volume of account-reference changes is tiny - it's maybe twenty a month.
[11:16:46] Hank Liu: Twenty a month is manageable as a manual reconciliation.
[11:16:57] Renata Voss: Right. Twenty a month I can handle on a spreadsheet if I have to, and I probably will have to.
[11:17:16] Anjali Kalavar: So the decision is: synthesise unique keys in the transform, freeze source-side reference changes, manual reconciliation for exceptions. Everyone comfortable?
[11:17:39] Davis Dean: Comfortable. It's the least bad option.
[11:17:48] Hank Liu: Comfortable, with one condition - I want the synthesised key to be deterministic. If we rerun the migration, the same legacy record has to produce the same Lattice key. Otherwise the dry runs are worthless as a rehearsal.
[11:18:22] Davis Dean: Agreed, and that's how I'd build it anyway. Hash of the composite - reference plus supply point plus account creation date.
[11:18:43] Hank Liu: Creation date is populated on all of them?
[11:18:51] Davis Dean: [pause] I'll check. If it isn't I'll find a different third element.
[11:19:06] Renata Voss: It'll be populated. It's one of the few fields that's mandatory in the legacy UI.
[11:19:24] Anjali Kalavar: Right, decision taken. Davis, action - build the deterministic key synthesis and rerun the affected subset. When?
[11:19:43] Davis Dean: The build's about three days. I'd want to run it against the full extract, which means the next full trial run. That's scheduled for the twenty-sixth. So I'd say deterministic key synthesis implemented and validated by the twenty-sixth of August.
[11:20:23] Anjali Kalavar: Twenty-sixth, Davis owns it. Renata, the freeze?
[11:20:31] Renata Voss: I'll issue the freeze notice to the operations leads. Give me until the twenty-first - I want to talk to them before they read it in an email.
[11:20:56] Anjali Kalavar: Renata, account-reference change freeze notice, twenty-first of August.
[11:21:10] Renata Voss: Yes.
[11:21:17] Anjali Kalavar: And the sizing question - how many accounts are actually affected. Who takes that?
[11:21:34] Davis Dean: I can profile it from the extract, but Renata's team would need to validate what the profile means. I'd rather do it jointly.
[11:21:52] Renata Voss: Then let's do it jointly and put my name on it, because if it slips it's my problem. Full duplicate-reference population profile by Friday the twenty-first, Davis produces the profile, I validate and sign it.
[11:22:22] Anjali Kalavar: Renata owns it, twenty-first. Good.
[11:22:31] Hank Liu: Sorry, before we move on - what happens to the eleven-flat case? Genuinely, what does that look like in Lattice?
[11:22:44] Davis Dean: Eleven billing accounts, one supply point, and the meter reads apportioned per the existing apportionment table.
[11:23:02] Renata Voss: There isn't an apportionment table.
[11:23:09] Davis Dean: There's a -
[11:23:13] Renata Voss: There's a - sorry, go on.
[11:23:18] Davis Dean: No, you go, you clearly know.
[11:23:26] Renata Voss: There's an apportionment percentage field on the account, but it's free text, and about a fifth of them contain things like "as before" or "see note".
[11:23:45] Hank Liu: [laughs] Of course they do.
[11:23:51] Davis Dean: Right, so that's a discovery item rather than a blocker for today. I'll add it to the data quality log.
[11:24:07] Anjali Kalavar: Do that, and Renata - is that population large enough to worry about?
[11:24:23] Renata Voss: Shared supply points across the whole estate, maybe eleven hundred accounts. A fifth of those with unusable apportionment text is two hundred-odd. That's a manual exercise, not an automated one.
[11:24:46] Anjali Kalavar: Then it's a bounded manual exercise, which is the best kind. Log it, size it properly next session.
[11:25:03] Davis Dean: Logged.
[11:25:09] Anjali Kalavar: Cutover windows. Hank, this is yours I think.
[11:25:21] Hank Liu: It is, and I've got bad news that isn't technically my fault, which is my favourite sort.
[11:25:38] Anjali Kalavar: Go on.
[11:25:44] Hank Liu: The proposed cutover window is the weekend of the seventh and eighth of November, going live Monday the ninth. Freeze the legacy platform Friday evening, run migration overnight Friday into Saturday, reconcile Saturday, business verification Sunday, open Monday morning.
[11:26:19] Davis Dean: That's the plan, yes.
[11:26:25] Hank Liu: The regulatory reporting run for the quarter executes on the first working day after the first Friday of November. Which this year is the ninth. Monday the ninth.
[11:26:48] Renata Voss: Oh no.
[11:26:55] Hank Liu: Oh yes. And it reads from the billing platform. Directly. It's a batch job that's been running since 2011 and it points at the legacy database by hostname.
[11:27:25] Davis Dean: By hostname.
[11:27:29] Hank Liu: By hostname, in a config file, that I'm fairly sure only two people know the location of.
[11:27:41] Anjali Kalavar: What's the report?
[11:27:46] Renata Voss: The quarterly submission on supply interruptions and billing accuracy. It goes to the regulator, it's not optional, and the deadline isn't movable. Submission is end of November - the run happens early because the data then goes through a three-week validation cycle with the compliance team.
[11:28:35] Davis Dean: So the run date has slack even if the deadline doesn't.
[11:28:44] Renata Voss: In principle. In practice compliance have built their whole cycle around it and they will not enjoy being compressed.
[11:28:59] Hank Liu: There's a second option - we point the batch job at the archive copy of the legacy database rather than the live one. We'll have a frozen copy anyway. We're not deleting the legacy platform on the ninth, we're just stopping writes to it.
[11:29:34] Davis Dean: That would work. The report's looking at Q3 data, which is closed. It doesn't need anything that happened in the cutover weekend.
[11:29:55] Hank Liu: That's my thinking. The data it needs is static by then.
[11:30:06] Renata Voss: Then the question is whether it can be repointed without changing the job itself, because if we change the job we're into compliance change control and that's six weeks.
[11:30:44] Hank Liu: We could repoint the hostname rather than the job. DNS-level. The job doesn't know or care.
[11:31:01] Davis Dean: That's - I mean, that's slightly horrifying but it's completely valid.
[11:31:14] Hank Liu: Everything on that platform is slightly horrifying and completely valid.
[11:31:27] Anjali Kalavar: What's the residual risk?
[11:31:35] Hank Liu: That we get it wrong and the regulator gets a report built on the wrong data. That's the risk. Which is why I'd want it rehearsed at the dress rehearsal in October rather than discovered on the day.
[11:31:58] Renata Voss: I'd say that's an amber. It's amber because there's a viable path, we've identified it eleven weeks out, and we've got a rehearsal to prove it in. If we hadn't spotted it until October it would be a different conversation.
[11:32:39] Anjali Kalavar: Amber, agreed. Owner?
[11:32:46] Hank Liu: Mine. I'll own the repoint design. I'll have a written approach by Friday the twenty-eighth of August, and I'll include it in the dress rehearsal test script.
[11:33:15] Anjali Kalavar: Hank, regulatory batch repoint approach, twenty-eighth of August. And who tells the compliance team?
[11:33:35] Renata Voss: Me. They'll want to hear it from a Calderwood name and they'll want to hear it early. I'll brief them the week of the seventeenth.
[11:33:55] Anjali Kalavar: Renata to brief the compliance team on the regulatory run interaction by Friday the twenty-first.
[11:34:11] Renata Voss: Twenty-first, fine.
[11:34:16] Hank Liu: One more thing on cutover. The eight-hour target for migration runtime. If we're at eleven forty now and the meter read transform is sixty percent of it, then the runtime problem and the history-depth question are the same problem.
[11:34:53] Davis Dean: They are. Which is where I wanted to get to next.
[11:35:00] Anjali Kalavar: Let's do it. History depth.
[11:35:06] Davis Dean: So the sizing question. How far back does billing history go into Lattice. We've been building against eighteen months because that's the vendor's reference architecture assumption, and it's what the current transform is tuned for.
[11:35:35] Renata Voss: And what's the argument for more?
[11:35:41] Davis Dean: Retention obligations. Billing records have a seven-year retention requirement.
[11:35:54] Renata Voss: They do, and I'm the person who signs the retention schedule, so let me be precise about it. The obligation is that we can produce the record. It says nothing about where the record lives. There is no requirement anywhere in that schedule that the record lives in the primary billing platform.
[11:36:27] Hank Liu: That matches my reading too. And there's a strong technical argument against putting it in the primary platform - you're paying for hot storage and index maintenance on data that gets touched maybe a few thousand times a year.
[11:36:52] Renata Voss: How often does anyone actually look at billing data older than eighteen months? I can answer that, roughly. The dispute team pull historic bills about nine hundred times a year. Of those, maybe a hundred and fifty are older than two years.
[11:37:21] Davis Dean: A hundred and fifty queries a year.
[11:37:27] Renata Voss: Against four hundred and thirty-eight thousand accounts. It's noise.
[11:37:39] Hank Liu: And for a hundred and fifty queries a year you can absolutely serve from an archive store, as long as the archive is properly indexed and somebody can actually query it without raising a ticket.
[11:38:01] Renata Voss: That last part is the part that's always failed before. The archive existed, technically, and it took six weeks to get anything out of it.
[11:38:27] Hank Liu: Because it was tape. This wouldn't be tape. This would be object storage with a query layer over it. Sub-second for a single account lookup if we index on account reference and billing period.
[11:38:58] Renata Voss: If you can give me that, my objection disappears entirely.
[11:39:07] Hank Liu: I can give you that. It's not even novel - we did the same thing for the meter asset register in 2024 and it works fine.
[11:39:24] Davis Dean: What's the effort?
[11:39:29] Hank Liu: The archive store itself, three weeks. The query layer, another two. Call it five weeks of one engineer, and it can run in parallel with the main build because it's not on the critical path.
[11:39:56] Davis Dean: And it takes about six hundred and ninety million rows out of the cutover-night transform.
[11:40:08] Hank Liu: It takes the runtime problem and turns it into somebody else's Tuesday.
[11:40:23] Davis Dean: [laughs] Which is the ideal outcome for any runtime problem.
[11:40:37] Anjali Kalavar: So where does that leave us?
[11:40:44] Renata Voss: It leaves us somewhere clear, I think. As data owner I'm making the call: only eighteen months of billing history migrates into the new platform, and everything older goes to a separate archive store.
[11:41:14] Hank Liu: Agreed. And I'll build the archive store to serve it.
[11:41:22] Davis Dean: That's a much more comfortable cutover.
[11:41:29] Anjali Kalavar: Right. Let me capture it properly - eighteen months into Lattice, everything beyond eighteen months into a queryable archive store, retention obligation satisfied by the archive rather than the primary platform, Renata as decision owner. Renata, you're comfortable signing that as the data owner?
[11:42:09] Renata Voss: I'm comfortable. It's my schedule and it's my domain. I'd want the retention position written down properly rather than just decided on a call, but the decision itself is mine to make and I've made it.
[11:42:36] Anjali Kalavar: Then let's get it written down. Renata, can you produce a short retention position note?
[11:42:54] Renata Voss: Yes. Two pages, referencing the schedule clauses. By the twenty-sixth.
[11:43:04] Anjali Kalavar: Renata, retention position note, twenty-sixth of August. Hank, the archive store?
[11:43:15] Hank Liu: I'll need to raise it as a work package because it's five weeks of engineering and it isn't in anyone's plan. I'll write the work package request by Wednesday the nineteenth and take it to Marissa.
[11:43:52] Anjali Kalavar: Hank, archive store work package request, nineteenth of August, to Marissa Feld.
[11:44:07] Hank Liu: Yes.
[11:44:11] Davis Dean: And I'll rebaseline the migration runtime estimate on the eighteen-month scope. I'd expect it to come in around four and a half hours, which gives us real contingency in the window. I'll have the revised estimate by the twenty-sixth alongside the next trial run.
[11:44:51] Anjali Kalavar: Noted. Reconciliation - Renata, this is the bit you wanted time on.
[11:45:01] Renata Voss: It is. So my problem is this. On cutover Saturday, somebody has to say "the data in the new platform is the same as the data in the old platform" and mean it. And I don't currently have a method for saying that which I would defend to an auditor.
[11:45:38] Davis Dean: We've got the count reconciliation. Row counts by entity, source versus target.
[11:45:55] Renata Voss: Row counts tell me nothing. Row counts tell me the same number of things arrived. They don't tell me the right things arrived with the right values.
[11:46:23] Hank Liu: You want financial reconciliation. Balances.
[11:46:33] Renata Voss: I want balances, and I want them to a penny, and I want them per account not in aggregate. Because aggregate balance reconciliation is how you end up with two accounts that are wrong by equal and opposite amounts and a total that looks perfect.
[11:47:05] Davis Dean: That's fair. That's a real failure mode and I've seen it.
[11:47:15] Renata Voss: Everybody's seen it. That's why I'm asking.
[11:47:22] Davis Dean: So what I'd propose is three tiers. Tier one, row counts by entity - fast, runs in minutes, catches gross failure. Tier two, control totals by entity and by billing cycle - catches structural problems. Tier three, per-account balance comparison across the full population - catches the thing you're describing.
[11:48:14] Renata Voss: How long does tier three take?
[11:48:21] Davis Dean: On four hundred and thirty-eight thousand accounts, if we do it as a set-based comparison rather than row by row, maybe forty minutes.
[11:48:45] Renata Voss: Forty minutes is nothing. Why isn't that already in the plan?
[11:48:55] Davis Dean: [pause] Honestly? Because the plan was written against the vendor's standard reconciliation pack, and their standard pack is tiers one and two.
[11:49:14] Renata Voss: Then their standard pack is inadequate and we're not using it as-is.
[11:49:29] Anjali Kalavar: Is that a decision you're making?
[11:49:39] Renata Voss: Yes. Cutover reconciliation includes a per-account balance comparison across the full population, to the penny, and I don't sign off cutover without it.
[11:50:07] Anjali Kalavar: Clear. Davis, that's a change to the reconciliation design.
[11:50:21] Davis Dean: It's an addition rather than a change, and it's a couple of days of work. I'll fold it into the reconciliation pack and have it ready for the next trial run on the twenty-sixth.
[11:50:53] Renata Voss: And I want to run it myself. Not watch someone run it. I want the query in my hands.
[11:51:10] Davis Dean: I'll build it as a script you can execute. I'll walk you through it before the twenty-sixth.
[11:51:23] Renata Voss: Thank you. That's the first time in this programme I've felt properly equipped.
[11:51:37] Hank Liu: There's a wrinkle. Per-account balance comparison assumes the account populations match. If we've synthesised keys for the duplicate-reference accounts, the target account population isn't one-to-one with the source.
[11:52:07] Davis Dean: True. So for that subset the comparison has to be at the supply-point level rather than the account level.
[11:52:20] Renata Voss: Which means the six thousand two hundred accounts, or however many it turns out to be, get a different reconciliation treatment.
[11:52:35] Davis Dean: They do. And that treatment needs designing.
[11:52:43] Renata Voss: Then that goes in the profile work we already agreed. When I validate the duplicate population I'll define the reconciliation treatment for it at the same time.
[11:53:05] Anjali Kalavar: Good, that's efficient. Anything else on reconciliation?
[11:53:17] Renata Voss: One thing, and it's more of a courtesy than a dependency. Finance have asked for a reconciliation report - they want to see, in advance of cutover, what the reconciliation will actually prove. Their controller's been burned by a migration at a previous employer and he's nervous.
[11:54:08] Anjali Kalavar: Reasonable ask.
[11:54:14] Renata Voss: Completely reasonable. I'll pull together a reconciliation report for finance and send it over to them.
[11:54:35] Anjali Kalavar: When do they need it?
[11:54:43] Renata Voss: They haven't said. I'll get it to them as soon as I can - I've got the freeze notice and the compliance briefing ahead of it, but it's on my list.
[11:55:12] Davis Dean: If you want the tier-three design to reference, I can send you the specification once it's written.
[11:55:27] Renata Voss: Do, that'd help. Then it's largely a write-up job.
[11:55:36] Anjali Kalavar: Right. What else. Hank, you had something on the staging tenant?
[11:55:47] Hank Liu: Yes, quickly. The staging tenant is sized at forty percent of production. That was fine when we were testing logic. It's not fine now we're doing full-volume trial runs - run two spilled to disk twice and I think some of that eleven forty runtime is us fighting our own environment rather than a real bottleneck.
[11:56:25] Davis Dean: That's a good point and it makes the runtime figure less reliable than I presented it.
[11:56:37] Hank Liu: I'd say your eleven forty is pessimistic by maybe fifteen percent.
[11:56:50] Anjali Kalavar: Can the tenant be resized?
[11:56:59] Hank Liu: Temporarily, yes, for a trial run. It costs money but not much - it's a couple of hundred pounds a day. The problem is it needs a request to the vendor with five working days' notice.
[11:57:32] Davis Dean: Then for the twenty-sixth run we'd need the request in by the nineteenth.
[11:57:45] Hank Liu: Correct. I'll raise it. Temporary staging tenant uplift request submitted by Tuesday the eighteenth, to give a day's margin.
[11:58:06] Anjali Kalavar: Hank, eighteenth. Good.
[11:58:14] Renata Voss: Can I raise something that's been bothering me all week?
[11:58:22] Anjali Kalavar: Please.
[11:58:28] Renata Voss: The trial runs are all validated against the same July extract. So we're getting very good at migrating July's data. We're not getting good at migrating whatever's in there in November.
[11:59:06] Davis Dean: That's a legitimate criticism.
[11:59:14] Renata Voss: It's not a criticism, it's a worry. The dunning population in November is not the dunning population in July - November is when arrears build up going into winter. And the arrears logic is the least well understood part of the platform.
[11:59:57] Hank Liu: Seasonal data profile risk. Is that on anyone's register?
[12:00:10] Davis Dean: Not as far as I know.
[12:00:17] Anjali Kalavar: Then let's put it on. Renata, how would you characterise it?
[12:00:28] Renata Voss: I'd want the answer before I gave it a colour. If a refreshed extract shows the same behaviour, it's nothing. If it shows new failure modes, it's serious.
[12:00:57] Davis Dean: We can refresh the extract - it's a day of elapsed time. Fresh extract for the October dress rehearsal at minimum, ideally one in September too.
[12:01:30] Renata Voss: September, please. October is too late to discover something structural.
[12:01:42] Davis Dean: Then I'll take an action - refreshed full extract taken and trial-run against by Friday the eighteenth of September.
[12:02:00] Anjali Kalavar: Davis, eighteenth of September. And Renata, we'll log the seasonal profile question as an open risk pending that run.
[12:02:24] Renata Voss: Good.
[12:02:30] Anjali Kalavar: We're a couple of minutes over. Anything else that can't wait for the next session?
[12:02:41] Hank Liu: Nothing from me. I'd like an hour with Davis on the key synthesis design before he builds it, though.
[12:02:54] Davis Dean: Monday morning? I'm free until eleven.
[12:03:01] Hank Liu: Monday at nine-thirty. I'll send an invite.
[12:03:12] Renata Voss: I'd like to be on that.
[12:03:19] Hank Liu: I'll add you.
[12:03:23] Anjali Kalavar: Then I'll let you three get on with it. Thank you both, genuinely - this was the most useful hour I've had this week.
[12:03:32] Renata Voss: It helped that somebody finally asked me what I actually needed rather than telling me what the pack contained.
[12:03:41] Anjali Kalavar: I'll take that as feedback and a compliment.
[12:03:50] Renata Voss: It was both.
[12:03:59] Davis Dean: Thanks all. Hank, Monday.
[12:04:08] Hank Liu: Monday. Have a decent weekend, everyone.
[12:04:17] Anjali Kalavar: You too. Thanks all.
