Meeting ID: LAT-PMO-02
Title: Project Lattice - Weekly Programme Checkpoint
Date: Wednesday, 12 August 2026
Time: 14:00 - 15:00 (BST)
Platform: Calderwood Teams bridge

Attendees:
  Anjali Kalavar - Aberdeen - Engagement Lead, Project Lattice
  Will Brown - Aberdeen - Consultant, Compliance & Controls workstream
  Davis Dean - Aberdeen - Consultant, Delivery & Build workstream
  Marissa Feld - Calderwood Utilities - Programme Manager, Project Lattice (client-side PMO)
  Devon Alvarez - Calderwood Utilities - PMO Analyst
  Gerald Mbeki - Calderwood Utilities - Chief Information Officer, Executive Sponsor (joined 14:48)

Recording transcribed automatically.

---

[14:00:08] Marissa Feld: Right, it's two o'clock, let's go. Devon's driving the tracker, Anjali you're doing the workstream round, and I want to be finished by five to because Gerald's coming on at the back end.
[14:00:22] Anjali Kalavar: Understood. How long have we got him for?
[14:00:26] Marissa Feld: Ten minutes, nominally. He'll ask about the steering pack, he always does, so be ready.
[14:00:34] Devon Alvarez: I've got the tracker up. Do you want me to share or just talk it?
[14:00:39] Marissa Feld: Share it. People read better than they listen.
[14:00:44] Devon Alvarez: [screen share] Okay. So milestones. Fourteen milestones in the current baseline, we're at week twenty-two of thirty-eight. Six complete, three in progress, five not started. Of the three in progress, two are tracking to date and one has slipped.
[14:01:04] Marissa Feld: Which one slipped.
[14:01:07] Devon Alvarez: M9, vendor contract variation countersigned. Baseline date was the seventh of August, it's now forecast the twenty-first.
[14:01:17] Marissa Feld: Two weeks.
[14:01:19] Devon Alvarez: Two weeks as of this morning's forecast, yes.
[14:01:24] Anjali Kalavar: Is that a real forecast or is that a hopeful one?
[14:01:29] Devon Alvarez: It's what procurement told me on Monday.
[14:01:33] Marissa Feld: So it's a hopeful one.
[14:01:36] Devon Alvarez: [laughs] I'm just the messenger.
[14:01:40] Anjali Kalavar: Let's come back to that under risks. Devon, keep going on the milestones.
[14:01:47] Devon Alvarez: M10 is user acceptance testing entry, that's the twenty-fourth of August, tracking green. M11 is integration design freeze, twenty-first of August, tracking green. Then nothing until M12 which is the dress rehearsal on the twelfth of October.
[14:02:06] Davis Dean: I'd query green on integration design freeze.
[14:02:10] Devon Alvarez: Go on.
[14:02:12] Davis Dean: It's green in the sense that the documents will be signed off on the twenty-first. It's not green in the sense that we've got a data question that came out of Monday's security session which might change the sizing underneath it.
[14:02:27] Marissa Feld: Which data question.
[14:02:29] Davis Dean: How much billing history migrates. There's a view that it's the full seven years rather than the eighteen months we'd been sizing against. I'm taking it into Friday's technical deep dive.
[14:02:43] Marissa Feld: Does that change the design or does it change the volumes?
[14:02:48] Davis Dean: Volumes, mostly. Possibly the reconciliation approach. It doesn't change the interface contracts, which is what actually freezes on the twenty-first.
[14:02:59] Marissa Feld: Then it's green for M11 and it's a separate line item. Devon, note it as a watch item against Friday's session, don't reopen the milestone.
[14:03:10] Devon Alvarez: Noted.
[14:03:13] Anjali Kalavar: Fine by me. Let me do the workstream round then. Delivery and build - Davis.
[14:03:20] Davis Dean: So. Build is in reasonable shape. We closed eleven of the fourteen sprint items last week, the three that carried over are all in the customer-communications module and they're carrying over because the content team hasn't given us final letter templates.
[14:03:38] Marissa Feld: That's Sandrine's team? I'll chase it, I'm seeing her tomorrow. Make it an action so it doesn't evaporate - Marissa to get final letter templates from the content team by Wednesday the nineteenth.
[14:04:07] Devon Alvarez: Nineteenth, you own it. Logged.
[14:04:11] Davis Dean: Other than that - environments are stable. One outage in the integration environment on Friday, which turned out to be a certificate expiry. The most boring possible root cause.
[14:04:26] Will Brown: The boring root causes are the good ones.
[14:04:30] Davis Dean: They are, but they're humiliating.
[14:04:34] Anjali Kalavar: Compliance and controls - Will.
[14:04:38] Will Brown: Thirty-four of forty-four control statements now mapped, up from thirty-one on Monday. The audit evidence question is being handled - Tom Okafor's doing a retrospective access review with a date of the twenty-eighth. Which brings me to a request.
[14:04:57] Marissa Feld: Go on.
[14:05:00] Will Brown: Tom asked whether Devon could help with the spreadsheet mechanics of the access review. Roughly six hundred entitlement rows across three environments. It's a couple of days of work, not a couple of weeks.
[14:05:15] Marissa Feld: Devon, what's your load?
[14:05:18] Devon Alvarez: Tight but survivable. If it's two days I can absorb it. If it turns into a project I'll shout.
[14:05:26] Marissa Feld: Then yes, help him. Two days, and if it exceeds that come back to me.
[14:05:33] Devon Alvarez: I'll log it as support to Tom's action rather than a separate one.
[14:05:39] Will Brown: Thank you. That's genuinely helpful.
[14:05:43] Anjali Kalavar: Right. UAT, because that's the thing I actually want to spend time on today. Marissa, where are we on testers?
[14:05:53] Marissa Feld: [pause] Okay, so. This is the difficult bit of my week.
[14:06:00] Anjali Kalavar: I had a feeling.
[14:06:03] Marissa Feld: We need twelve business testers for the UAT cycle starting the twenty-fourth. Six from customer service, four from billing operations, two from field. As of yesterday I had eleven names confirmed, which I was quite pleased about.
[14:06:20] Anjali Kalavar: And as of today?
[14:06:23] Marissa Feld: As of today I have four. There's been a burst main in the Thornbury district - it went Sunday night, it's affected about nine thousand properties, and the incident response has pulled everyone with a customer-facing role into the outage bridge. Including seven of my eleven.
[14:06:44] Davis Dean: For how long?
[14:06:46] Marissa Feld: Nobody will tell me. The operational answer is "until it's resolved" and the honest answer is that these things have a tail. The repair might be done in a week but the complaints and the compensation claims run for a month.
[14:07:03] Anjali Kalavar: And those are exactly the people who'd be testing the billing adjustments.
[14:07:09] Marissa Feld: Exactly the same people. It's the same skill set. That's why they got pulled.
[14:07:16] Will Brown: Can UAT start with four?
[14:07:19] Davis Dean: You can start. You can't finish. Four testers on a nine-week cycle with three hundred and forty scripted test cases - the arithmetic doesn't work. You'd be looking at fourteen, fifteen weeks.
[14:07:35] Marissa Feld: Which pushes us past the dress rehearsal.
[14:07:39] Davis Dean: Which pushes us past the dress rehearsal, and the dress rehearsal is the thing that protects go-live.
[14:07:47] Marissa Feld: Right. So I'm calling this a red. Tester availability for UAT is red. I'm not going to dress it up for Gerald either, he'll see through it.
[14:07:58] Anjali Kalavar: Agreed on red. What are the options?
[14:08:03] Marissa Feld: Three, I think. One, we wait it out and accept the slip. Two, we source testers from outside the affected districts - there's a service centre in Bellhaven that hasn't been touched by this. Three, we reduce the test scope.
[14:08:22] Davis Dean: Option three is how you end up on the front page of a trade magazine.
[14:08:28] Marissa Feld: I know. I'm listing it for completeness, not for adoption.
[14:08:34] Anjali Kalavar: What's wrong with option two?
[14:08:37] Marissa Feld: Only that the Bellhaven staff don't know the billing system as well - newer site, they've mostly used the current platform for lookups rather than adjustments. So they'd need a fortnight of training I hadn't planned for.
[14:08:58] Davis Dean: A fortnight of training is cheaper than a five-week test overrun.
[14:09:04] Marissa Feld: It is, and that's where I'm landing. I just want the cost visible rather than absorbed silently.
[14:09:12] Anjali Kalavar: Then let's put a date on it. Who's approaching Bellhaven?
[14:09:18] Marissa Feld: Me. I'll speak to the site lead - it's Yusuf Adeyemi, I've worked with him before. I'll have an answer on numbers by Monday the seventeenth.
[14:09:29] Devon Alvarez: Marissa, Bellhaven tester sourcing, seventeenth of August. Logged.
[14:09:35] Anjali Kalavar: And Davis, can you rebuild the UAT schedule on a "four now, eight from early September" assumption so we can see the shape?
[14:09:45] Davis Dean: Yes. I'll have a revised UAT plan by Friday the twenty-first.
[14:09:52] Devon Alvarez: Twenty-first, Davis. Logged.
[14:09:56] Marissa Feld: One more thing on this. I don't want the four we have burned on regression scripts. If we've only got four people, they test the things only a business user can judge - the billing adjustments, the dunning letters, the payment plan calculations. Automated regression can wait for the reinforcements.
[14:10:18] Davis Dean: That's sensible sequencing. I'll build it that way.
[14:10:23] Anjali Kalavar: Right. Vendor contract.
[14:10:31] Devon Alvarez: It's the variation covering the additional environment and the extended support hours. With the vendor's legal team since the twenty-ninth of July. Our side signed on the fourth of August. We're waiting on their countersignature, and the account manager says it's "in their legal queue" - he's said that twice, a week apart.
[14:10:59] Will Brown: The legal queue is the corporate equivalent of the sock drawer.
[14:11:05] Marissa Feld: What's the actual impact if it doesn't land?
[14:11:10] Davis Dean: The additional environment is the one we want for the dress rehearsal. If the variation isn't executed we can't provision it, and we'd have to run the dress rehearsal in the same environment as UAT, which means suspending UAT for a week.
[14:11:27] Marissa Feld: When's the drop-dead date?
[14:11:30] Davis Dean: Provisioning takes about three weeks from the vendor side, so working back from the twelfth of October - mid-September. Say the eighteenth.
[14:11:41] Marissa Feld: So we've got five weeks of float. That's amber, not red.
[14:11:47] Anjali Kalavar: I'd agree amber. It's amber with a hard trigger - if it's not signed by the eighteenth of September it becomes a red immediately and it becomes a Gerald problem.
[14:11:59] Marissa Feld: Devon, log it as amber, escalation trigger the eighteenth of September, escalation route to Gerald via me.
[14:12:08] Devon Alvarez: Logged. Do you want an owner for chasing the countersignature?
[14:12:14] Marissa Feld: Procurement owns it. Put Rhona's name against it - Rhona Cattrall, she's the category manager. I'll tell her.
[14:12:23] Devon Alvarez: Rhona Cattrall, chase countersignature, review at next checkpoint.
[14:12:29] Anjali Kalavar: Davis, while we're on the vendor - didn't you have something on rate limits?
[14:12:35] Davis Dean: Yes, and it's turning into a proper problem. Their API is rate-limited at two hundred calls a minute per tenant. During the migration dry runs we're generating something like nine hundred a minute at peak, and during the actual cutover it'll be higher. We got throttled twice in the trial run.
[14:12:57] Marissa Feld: Can't you just batch it differently?
[14:13:01] Davis Dean: We've batched it as far as it'll batch. Some of these calls are inherently per-record. What we actually need is for them to lift the limit for the cutover window, which they do for other customers - it's in their operations guide as a supported request. It just needs somebody to ask them, formally, with lead time.
[14:13:23] Will Brown: How much lead time?
[14:13:26] Davis Dean: Their guide says thirty days' notice for a temporary limit uplift.
[14:13:32] Marissa Feld: So somebody needs to chase the vendor about the API rate limits, and soon, because thirty days from now is basically September.
[14:13:42] Davis Dean: Correct.
[14:13:44] Marissa Feld: Right. And obviously we need to know what the limit would actually be lifted to, because if it goes to four hundred that doesn't help us.
[14:13:54] Davis Dean: Agreed.
[14:13:56] Marissa Feld: Okay. Devon, what's next on the tracker - budget?
[14:14:02] Devon Alvarez: Budget, yes. We're at sixty-one percent of the phase-two envelope with sixty-four percent of the schedule elapsed, so marginally underspent, which is unusual enough that I've double-checked it twice.
[14:14:17] Marissa Feld: Where's the underspend?
[14:14:20] Devon Alvarez: Mostly the security line, because nothing's been committed against it.
[14:14:26] Will Brown: Ah.
[14:14:28] Anjali Kalavar: That's my cue. Priya raised on Monday that the penetration test isn't booked. No purchase order, no scope, no window. Lead times from the framework suppliers are eight to ten weeks and go-live is the ninth of November.
[14:14:44] Marissa Feld: I thought that was in hand.
[14:14:47] Anjali Kalavar: Priya's understanding is that the budget line sits with the programme rather than with her, and every time she's asked she's been told it's in flight.
[14:14:57] Marissa Feld: [pause] Devon, is there a requisition against the security line?
[14:15:03] Devon Alvarez: There's a draft requisition from the twenty-second of June. It's never been submitted for approval.
[14:15:11] Marissa Feld: Whose draft?
[14:15:13] Devon Alvarez: It's in my predecessor's name.
[14:15:17] Marissa Feld: Wonderful. Right, that's on me to fix. Priya's got the action to secure the purchase order by the twenty-first but she can't do it if the requisition's sitting in a dead person's queue - sorry, that's a terrible phrase, he moved to a different division.
[14:15:35] Devon Alvarez: I'll re-raise it under my name today.
[14:15:39] Marissa Feld: Do that, and I'll approve it the moment it appears. Devon, requisition re-raised today, the twelfth.
[14:15:47] Devon Alvarez: Logged.
[14:15:49] Anjali Kalavar: Priya was explicit that she wants the pen test held as red until there's a confirmed test window with a date, not just a purchase order.
[14:15:59] Marissa Feld: That's fair and I'll support that framing. Devon, pen-test readiness stays red on the register.
[14:16:07] Devon Alvarez: It's already red. I put it there Monday afternoon after Will messaged me.
[14:16:13] Will Brown: I did, yes. I try to be efficient about bad news.
[14:16:18] Anjali Kalavar: Right. Self-service portal scope - this is the one we said we'd close today.
[14:16:25] Marissa Feld: Yes. Background for the record - the original scope had the customer self-service portal at go-live with six functions: view bill, pay bill, submit meter read, change contact details, set up direct debit, and manage payment plans.
[14:16:46] Davis Dean: And payment plans is the one causing pain. It touches the arrears engine, which is the most heavily customised part of the legacy platform and the part where our understanding is thinnest. Building self-service on top of logic we've reverse-engineered rather than documented means customers could see the wrong arrears balance. That's a complaint and possibly a regulatory issue.
[14:17:26] Will Brown: It's also the function with the lowest projected usage. The digital team's own numbers had it at about three percent of portal sessions.
[14:17:37] Marissa Feld: Three percent of sessions, forty percent of the risk.
[14:17:42] Anjali Kalavar: What's the alternative for customers who need it?
[14:17:47] Marissa Feld: Same as today - they phone. Not a great answer, but it's the current answer, so it isn't a regression.
[14:17:56] Davis Dean: And deferring it buys about three sprints, which we could put into the payment and meter-read journeys - ninety percent of usage.
[14:18:07] Marissa Feld: Right. Then I'm making the call. Payment plan management is descoped from the go-live release of the self-service portal and moves to the phase-three release in Q1 next year. The other five functions stay in scope for the ninth of November.
[14:18:24] Anjali Kalavar: That's clear. Devon, capture it as a scope decision with today's date.
[14:18:30] Devon Alvarez: Captured. Do you want a change note raised?
[14:18:35] Marissa Feld: Yes, it's a baseline change, it needs the paperwork. You raise it, I'll sign it, and it goes to the steering committee as a notification rather than an approval - I'm not asking permission, I'm telling them.
[14:18:49] Devon Alvarez: Change note by Friday the fourteenth?
[14:18:53] Marissa Feld: Friday's fine.
[14:18:56] Anjali Kalavar: One thing to flag - the digital team put out a customer comms plan in June that mentions payment plan self-service by name. Somebody will need to walk that back.
[14:19:08] Marissa Feld: God. Yes. Devon, add that to the change note as an impact - external comms need revising.
[14:19:16] Devon Alvarez: Adding it.
[14:19:19] Anjali Kalavar: Second risk for the log while we're here. Davis, the arrears engine documentation gap - is that a risk in its own right?
[14:19:29] Davis Dean: It is, and I'd have said amber before this decision. Descoping the self-service piece takes the sharp edge off it, but we still have to migrate arrears data, and we still don't have documentation. I'd keep it amber.
[14:19:45] Marissa Feld: Amber, owner Davis, review fortnightly.
[14:19:50] Devon Alvarez: Logged.
[14:19:53] Marissa Feld: Right, we've got about twenty-five minutes before Gerald. Devon, anything else on the tracker that needs airtime?
[14:20:02] Devon Alvarez: Three small things. Training material sign-off, the data centre migration dependency, and someone's asked whether we're doing a benefits realisation baseline.
[14:20:14] Marissa Feld: Take those in order.
[14:20:17] Devon Alvarez: Training material - the vendor's standard pack has been reviewed and about a third of it doesn't match our configuration. Rewriting it is four weeks of somebody's time and there's no somebody.
[14:20:32] Marissa Feld: Then log it as an issue rather than a risk, because it's already happened, and I'll find a resource. Not today, but I'll find one.
[14:20:44] Devon Alvarez: Second thing - the data centre migration. Infrastructure are moving the primary data centre in October.
[14:21:06] Davis Dean: They're what?
[14:21:08] Devon Alvarez: Moving. Not physically, it's a logical migration between availability zones. But there's a freeze period.
[14:21:17] Davis Dean: When's the freeze?
[14:21:19] Devon Alvarez: Fifth to the nineteenth of October.
[14:21:23] Davis Dean: That's the dress rehearsal.
[14:21:26] Devon Alvarez: That's the dress rehearsal.
[14:21:29] Anjali Kalavar: How did we not know about this?
[14:21:32] Devon Alvarez: It's in their programme plan. It's not in ours. I found it yesterday while looking for something else.
[14:21:40] Marissa Feld: Right. That's a genuine find, Devon, well spotted. I need to talk to the infrastructure programme manager before I know whether this is a real conflict or a paperwork one. Some of those freezes have carve-outs.
[14:21:56] Anjali Kalavar: Do you want it on the register now or after you've spoken to them?
[14:22:02] Marissa Feld: On the register now, unassessed, and I'll bring a severity next week. I'd rather have it visible and vague than invisible and precise.
[14:22:12] Devon Alvarez: Logged as unassessed. Marissa to confirm the freeze impact by next checkpoint, the nineteenth.
[14:22:20] Marissa Feld: Yes. And the benefits baseline?
[14:22:24] Devon Alvarez: Someone in finance has asked whether there's a benefits realisation baseline. There's a benefits section in the 2024 business case, but it's not a baseline you could measure against. It says things like "improved customer experience".
[14:22:44] Will Brown: Measured in what unit?
[14:22:47] Devon Alvarez: Vibes, I think.
[14:22:50] Marissa Feld: [laughs] Park it. It's a real question but it's not a this-week question. Backlog, and we pick it up after UAT entry.
[14:23:02] Anjali Kalavar: Marissa, can I use the gap before Gerald usefully? I'd like to walk the critical path, because I don't think the UAT slip and the environment dependency have been modelled together.
[14:23:19] Marissa Feld: Yes, do it. Devon, put the schedule up.
[14:23:24] Devon Alvarez: [screen share] This is the current critical path view.
[14:23:29] Anjali Kalavar: So the path runs through UAT entry, UAT exit, dress rehearsal, cutover readiness gate, go-live. Five nodes, no float between the last three.
[14:23:42] Davis Dean: There's never been float between the last three. That was true at baseline.
[14:23:48] Anjali Kalavar: I know, and I flagged it at baseline and was told it was acceptable. I'm reflagging it because we now have three independent threats to the same zero-float section - the tester shortage, the environment, and the pen test, since the readiness gate can't pass without it.
[14:24:11] Marissa Feld: Three threats to a zero-float path. That's not a great sentence.
[14:24:17] Anjali Kalavar: It isn't. Which is why I'd like Gerald to hear it from you rather than from me. It lands differently from the client side.
[14:24:27] Marissa Feld: Agreed. Davis, can you get me a one-page critical path view I can put in front of him? Not the full schedule, one page.
[14:24:38] Davis Dean: By when?
[14:24:40] Marissa Feld: Tomorrow, so I can look at it before the steering pack goes out.
[14:24:46] Davis Dean: Thursday the thirteenth. I'll have it with you by lunchtime.
[14:24:51] Devon Alvarez: Logged, Davis, thirteenth.
[14:24:55] Marissa Feld: Anything else before he joins?
[14:24:59] Will Brown: Nothing from me.
[14:25:05] Marissa Feld: Then let's have five minutes of silence, which will be the most productive part of my day.
[14:48:11] Gerald Mbeki: [joins] Afternoon. Sorry, I'm early, or am I late? I've lost track of what day it is.
[14:48:19] Marissa Feld: You're right on time, Gerald. We've been going since two.
[14:48:25] Gerald Mbeki: Good. Give me the version you'd give me in a lift.
[14:48:31] Marissa Feld: Build is fine. Two milestones green, one slipped by two weeks and it's recoverable. The thing you need to know is that the Thornbury burst main has taken seven of my eleven UAT testers into the outage bridge, and I'm carrying that as a red.
[14:48:50] Gerald Mbeki: Ah. Yes. I've had that outage in my ear since Monday morning.
[14:48:57] Marissa Feld: Then you'll know I'm not going to get them back quickly.
[14:49:02] Gerald Mbeki: You are not. Realistically not before the first week of September, and I'd be careful about promising even that. What's the mitigation?
[14:49:12] Marissa Feld: Sourcing testers from Bellhaven, which hasn't been affected. They'll need a fortnight of training. I'm speaking to the site lead on Monday.
[14:49:22] Gerald Mbeki: Do it. If you need me to make a phone call to unblock the site, tell me. Sometimes a call from this chair is faster than a business case.
[14:49:33] Marissa Feld: I'll take you up on that if Monday goes badly.
[14:49:38] Gerald Mbeki: What else is red?
[14:49:41] Anjali Kalavar: The penetration test. It's not booked, and the framework suppliers are quoting eight to ten weeks. Priya's raised it, we've traced the blocker to an unsubmitted requisition, and Devon's re-raising it today.
[14:49:56] Gerald Mbeki: An unsubmitted requisition. From when?
[14:50:00] Devon Alvarez: June.
[14:50:02] Gerald Mbeki: [sighs] Right. That's not a programme failure, that's a handover failure, and I'll take that one. Marissa, send me the requisition reference when it's raised and I'll make sure it doesn't sit anywhere.
[14:50:16] Marissa Feld: Will do.
[14:50:19] Gerald Mbeki: And Anjali - is that pen test a gate for go-live or a nice-to-have?
[14:50:25] Anjali Kalavar: It's a gate. The cutover readiness criteria include a completed penetration test with no unremediated high findings. That's in the approved criteria from March.
[14:50:38] Gerald Mbeki: Then it's not a red, it's a potential stop. I want it treated that way.
[14:50:44] Anjali Kalavar: Understood.
[14:50:47] Gerald Mbeki: Now. The steering committee pack. It's the twenty-fifth, isn't it?
[14:50:53] Marissa Feld: The twenty-fifth, yes.
[14:50:56] Gerald Mbeki: I want it different this time. The last two packs have been forty slides of green boxes and then a conversation in the room where I discover everything that's actually happening. That's not the committee's fault and it's not yours, but I'd like the pack to say the difficult things in writing.
[14:51:17] Marissa Feld: That's - honestly, that's a relief to hear.
[14:51:22] Gerald Mbeki: Front page: three things I need a decision on, three things I need to know about. Then the detail behind it for anyone who wants it. Can you do that?
[14:51:33] Marissa Feld: Yes. I'd want Anjali's input on the framing.
[14:51:38] Anjali Kalavar: Happy to. We've got a house format for exactly that.
[14:51:43] Gerald Mbeki: Good. When does it need to be with me?
[14:51:47] Marissa Feld: Board convention is five working days, so the eighteenth.
[14:51:53] Gerald Mbeki: Make it the seventeenth, I want to read it on a Monday not a Tuesday.
[14:51:59] Marissa Feld: Then Marissa to deliver the steering committee pack to Gerald by Monday the seventeenth of August, with Anjali contributing the risk framing.
[14:52:10] Devon Alvarez: Logged, seventeenth.
[14:52:13] Gerald Mbeki: And in that pack I want the critical path picture. The one where you show me there's no float. I know there's no float, I want the committee to know it too.
[14:52:24] Marissa Feld: Davis is producing a one-pager tomorrow. It'll go in.
[14:52:29] Gerald Mbeki: Perfect. Anything you need from me today other than the requisition?
[14:52:35] Marissa Feld: Not today. Possibly a phone call on Monday.
[14:52:40] Gerald Mbeki: You've got it. Anjali, one question - are you comfortable? Genuinely. Not the client-facing answer, the real one.
[14:52:50] Anjali Kalavar: The real answer is that I'm comfortable with the build and uncomfortable with the schedule. The build team are good and the platform's behaving. What worries me is that we have a zero-float section at the end and three separate things that could eat into it, and we're relying on none of them getting worse at the same time.
[14:53:12] Gerald Mbeki: That's a fair answer. Thank you for not managing me.
[14:53:18] Anjali Kalavar: I'd be bad at it.
[14:53:21] Gerald Mbeki: Everyone's bad at it, that's the thing nobody tells you. Right. I'll leave you to it. Marissa - seventeenth, and the pack says the difficult things.
[14:53:33] Marissa Feld: Seventeenth. Understood.
[14:53:36] Gerald Mbeki: Thanks all. [leaves]
[14:53:41] Marissa Feld: Well. That went better than I'd planned for.
[14:53:46] Will Brown: He asked for bad news in writing. I don't think I've heard a sponsor do that before.
[14:53:53] Marissa Feld: He's been on the other side of a failed programme. It changes you.
[14:54:00] Anjali Kalavar: Right, we're at four minutes to. Devon, can you circulate the actions today rather than tomorrow?
[14:54:08] Devon Alvarez: I'll have them out by five.
[14:54:11] Marissa Feld: Thanks all. Same time next week, and Davis - one page, tomorrow, lunchtime.
[14:54:19] Davis Dean: One page. Understood.
[14:54:22] Anjali Kalavar: Thanks everyone.
[14:54:25] Will Brown: Thanks all.
