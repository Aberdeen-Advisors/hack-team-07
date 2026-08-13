Meeting ID: LAT-SEC-01
Title: Project Lattice - Security & Compliance Working Session
Date: Monday, 10 August 2026
Time: 09:30 - 10:20 (BST)
Platform: Calderwood Teams bridge

Attendees:
  Anjali Kalavar - Aberdeen - Engagement Lead, Project Lattice
  Will Brown - Aberdeen - Consultant, Compliance & Controls workstream
  Davis Dean - Aberdeen - Consultant, Delivery & Build workstream
  Priya Raghunathan - Calderwood Utilities - Chief Information Security Officer
  Tom Okafor - Calderwood Utilities - Identity & Access Lead (reports to P. Raghunathan)

Recording transcribed automatically.

---

[09:30:12] Anjali Kalavar: Morning all. I can see Priya and Will. Davis, are you there?
[09:30:19] Davis Dean: I'm here, just wrestling with the headset. Can you hear me now?
[09:30:23] Anjali Kalavar: Loud and clear.
[09:30:31] Priya Raghunathan: Before we start - is Tom on? He's the one who actually knows the answer here.
[09:30:37] Anjali Kalavar: Not yet. He accepted, so I'd assume he's coming.
[09:30:44] Priya Raghunathan: Fine. Let's do the parts he doesn't need to be in the room for and I'll flag when we need him.
[09:30:52] Anjali Kalavar: Works for me. So, agenda - four things. Single sign-on integration, the pen test, encryption keys, and access-review evidence for the audit. Will's going to walk the status.
[09:31:06] Will Brown: Thanks. So where we are on compliance and controls as of this morning. We've got thirty-one of the forty-four control statements mapped from your ISMS onto the Lattice design. Of those thirty-one, nineteen are green, nine are amber pending design detail, and three are - I'll be honest - three are open.
[09:31:28] Priya Raghunathan: Which three.
[09:31:31] Will Brown: Key management, which we're coming to. Privileged session recording on the new platform, because the vendor's answer changed between the RFP and the build. And retention of billing history, which is more of a data question than a security one but it lands on your side of the fence.
[09:31:52] Priya Raghunathan: Noted. Keep going.
[09:31:56] Will Brown: On the audit evidence pack, the external auditors have asked for access-review artefacts covering the full build period, not just from go-live. That's a change from what we understood in June.
[09:32:11] Priya Raghunathan: That's not a change, that's them finally reading their own methodology.
[09:32:16] Will Brown: [laughs] Possibly. Either way it means we need quarterly review evidence for the Lattice non-production environments going back to April, and we don't have it.
[09:32:29] Davis Dean: We have the entitlement exports. We don't have anyone's signature saying they looked at them.
[09:32:36] Will Brown: Right. The data exists. The attestation doesn't.
[09:32:41] Priya Raghunathan: Then we manufacture the attestation properly - someone reviews the historic exports now, signs, and we note in the pack that the review was performed retrospectively. I'd rather have an honest late review than a backdated one.
[09:32:57] Anjali Kalavar: Agreed, and auditors generally prefer that too.
[09:33:04] Tom Okafor: [joins] Sorry - sorry, I'm here. Previous call ran long. What have I missed?
[09:33:10] Priya Raghunathan: Access-review evidence. We're doing a retrospective review of non-prod entitlements back to April and signing it honestly.
[09:33:19] Tom Okafor: That's - okay. That's about six hundred entitlement rows across three environments. It's doable but it's not a morning's work.
[09:33:29] Anjali Kalavar: How long realistically?
[09:33:33] Tom Okafor: Give me two weeks. If I can pull Devon in for the spreadsheet mechanics, less.
[09:33:41] Will Brown: Devon's PMO side, so that's Marissa's call, but I can raise it Wednesday.
[09:33:48] Anjali Kalavar: Let's put it down as Tom completing the retrospective access review by Friday the twenty-eighth of August. Tom, you own it. If Devon helps, great, but it's your date.
[09:34:01] Tom Okafor: Twenty-eighth. Fine. I'll take that.
[09:34:07] Priya Raghunathan: Good. Single sign-on.
[09:34:11] Tom Okafor: Yeah, so. This is the one I wanted to be in the room for. The new platform speaks SAML and OIDC, that's all fine, we've stood up the test federation and Davis's team have logged in.
[09:34:26] Davis Dean: We have. Three of us, last Thursday. It worked first time, which frightened me.
[09:34:33] Tom Okafor: The problem isn't the new platform. The problem is the old one. The legacy billing system does not support modern auth. At all. No SAML, no OIDC, no OAuth, nothing. It does LDAP bind against a directory we're retiring, and it does a local password file for about forty accounts that predate me.
[09:34:56] Priya Raghunathan: Forty.
[09:34:58] Tom Okafor: Forty-one, actually, and one of them is called "billadmin2" and nobody living knows what it does.
[09:35:07] Will Brown: I love this project.
[09:35:11] Anjali Kalavar: So the question is what happens to those during the parallel-run period, because we've got roughly four months where both systems are live.
[09:35:22] Tom Okafor: Correct. And my view is we can't put the legacy system behind the new identity provider. It's technically not possible without a reverse proxy in front of it that terminates the session and replays the LDAP bind, which is - I mean, it's a thing you can build, but it's a thing you can build badly.
[09:35:43] Davis Dean: We've done it elsewhere. It works. It's about six weeks of effort and it becomes a piece of infrastructure nobody wants to own afterwards.
[09:35:53] Priya Raghunathan: I'm not funding a proxy for a system we're switching off in March.
[09:36:00] Tom Okafor: Then the alternative is compensating controls. We freeze the legacy account population - no new accounts from a fixed date - we enforce break-glass procedure on the shared ones, and we put session logging on the jump host so at least we know who was on it.
[09:36:19] Will Brown: From a controls perspective I can defend that. It's not elegant but it's defensible and it's time-boxed.
[09:36:28] Priya Raghunathan: Then that's the decision. We are not integrating the legacy billing platform with single sign-on. We freeze the legacy account population, wrap it in compensating controls, and it dies with the platform in March.
[09:36:43] Anjali Kalavar: Recorded. Tom, what's the fixed freeze date?
[09:36:48] Tom Okafor: First of September. That gives the business three weeks to ask for anything they've forgotten.
[09:36:55] Anjali Kalavar: Tom to publish the legacy account freeze notice by the first of September. Will, can you write up the compensating control set?
[09:37:04] Will Brown: Yes. I'll have a draft control note by Thursday the twentieth.
[09:37:10] Anjali Kalavar: Thursday the twentieth, Will owns it. Good. Pen test.
[09:37:17] Will Brown: Right, so. This is the bit where I stop being cheerful.
[09:37:22] Priya Raghunathan: Go on.
[09:37:25] Will Brown: The go-live penetration test is not booked. Not "provisionally pencilled", not "with the supplier awaiting dates" - not booked. There is no purchase order, there is no scope document, and the two firms on your framework are both quoting eight to ten weeks' lead time for an engagement of this size.
[09:37:47] Priya Raghunathan: Go-live is the ninth of November.
[09:37:51] Will Brown: Go-live is the ninth of November. Eight weeks from today is the fifth of October, which sounds fine until you account for scoping, the test window itself, remediation, and a retest. On the current trajectory we would be walking into a go-live gate with an untested platform.
[09:38:10] Priya Raghunathan: That's a red for me. That is unambiguously a red.
[09:38:15] Will Brown: I've got it as a red on the register as of this morning, yes.
[09:38:20] Anjali Kalavar: Priya, is the blocker money or is it process?
[09:38:26] Priya Raghunathan: It's neither, it's that the security budget line for Lattice sits under the programme, not under me, and every time I've asked I've been told it's in flight. Which is the corporate way of saying nobody's signed it.
[09:38:41] Anjali Kalavar: Then I'll take that to Marissa on Wednesday and escalate to Gerald if it doesn't move.
[09:38:48] Priya Raghunathan: Do. And be blunabout it. Be blunt about it, sorry.
[09:38:54] Davis Dean: I liked "blunabout".
[09:38:57] Priya Raghunathan: It's Monday.
[09:39:02] Tom Okafor: Can I ask a practical thing - is the test scoped to the new platform only, or does it include the integration layer?
[09:39:11] Will Brown: It has to include the integration layer. That's where the interesting failures live. Which also means it can't be scoped until the integration design is frozen.
[09:39:22] Davis Dean: Integration design freezes on the twenty-first.
[09:39:27] Will Brown: Then the earliest honest scoping date is the twenty-fourth, and I'd want the supplier engaged in parallel rather than sequentially. Book the window on a draft scope, refine after.
[09:39:41] Anjali Kalavar: Priya, are you comfortable committing a window against a draft scope?
[09:39:47] Priya Raghunathan: I'm more comfortable with that than with not testing. Yes.
[09:39:53] Anjali Kalavar: Then action - Priya to secure the pen-test purchase order and provisional test window by Friday the twenty-first of August.
[09:40:03] Priya Raghunathan: Twenty-first. I'll own it. If it hasn't moved by Wednesday I'll say so on the checkpoint call.
[09:40:12] Will Brown: And I'll draft the scope document so it's ready to hand over. I'll have that by the twenty-fourth.
[09:40:20] Anjali Kalavar: Will, twenty-fourth of August, pen-test scope document. Right. Encryption keys.
[09:40:28] Priya Raghunathan: This is the one that's been going round in circles for a month.
[09:40:34] Davis Dean: Let me share, it's easier with the diagram. [screen share]
[09:40:40] Davis Dean: Okay, so - can everyone see the architecture view? Priya?
[09:40:45] Priya Raghunathan: I see three boxes and a lot of arrows.
[09:40:49] Davis Dean: That's the one. So the vendor's default posture is vendor-managed keys. Their KMS, their rotation schedule, their HSM estate. It's certified, it's fine, it's what ninety percent of their customers run.
[09:41:05] Priya Raghunathan: And our policy says customer-managed keys for anything holding personal data at scale.
[09:41:12] Davis Dean: Right. And Lattice holds meter reads and payment details for - what is it, four hundred and twenty thousand accounts?
[09:41:21] Tom Okafor: Four hundred and thirty-eight thousand as of the last count.
[09:41:26] Davis Dean: So the policy applies. Unambiguously. The question is whether the vendor supports client-managed keys on the tier we've bought, and the answer we've had is - Anjali, how would you characterise the answer we've had?
[09:41:41] Anjali Kalavar: Evasive.
[09:41:43] Davis Dean: Evasive. Their solution architect said "that's typically an enterprise-tier capability" and then changed the subject.
[09:41:52] Priya Raghunathan: Typically.
[09:41:55] Will Brown: The word "typically" is doing an enormous amount of load-bearing work in that sentence.
[09:42:02] Priya Raghunathan: What's the exposure if the answer is no? Genuinely, walk me through it, because I need to know whether I'm dying on this hill.
[09:42:12] Will Brown: If the answer is no, we have a policy exception that needs your signature and, above a certain threshold, the risk committee's. It's not a regulatory breach - the ICO isn't going to knock - but it's a documented deviation from your own control framework at the exact moment external auditors are looking at you.
[09:42:33] Priya Raghunathan: Which is the worst possible moment.
[09:42:37] Will Brown: It's not ideal.
[09:42:40] Tom Okafor: There's a middle path. Some of these platforms support what they call "bring your own key" where you supply the key material but they still hold it. It's not true customer-managed - you can't revoke unilaterally - but it satisfies a chunk of the control intent.
[09:42:58] Priya Raghunathan: It satisfies the letter and not the spirit.
[09:43:03] Tom Okafor: Yes. But it's better than nothing and it might be available on our tier.
[09:43:09] Anjali Kalavar: So the open question is: does the vendor support client-managed keys on our contracted tier, and if not, what's the BYOK option and its exact revocation semantics. That's what we need answered.
[09:43:23] Priya Raghunathan: And I want it in writing from them, not from a solution architect on a call. I've been burned by that before.
[09:43:32] Davis Dean: I'll raise it as a formal written question through the vendor's technical account manager. I can do that today and I'd expect a response inside a week.
[09:43:43] Anjali Kalavar: Davis to submit the formal written question on client-managed key support by Wednesday the twelfth, response chased for the nineteenth.
[09:43:53] Davis Dean: Twelfth for the question, nineteenth for the answer. Got it.
[09:43:59] Priya Raghunathan: And if the answer is no, I want the exception paperwork drafted in parallel. I don't want to discover in October that we need a risk committee slot and the next one's in December.
[09:44:12] Will Brown: Sensible. I'll draft the exception on a contingent basis - it either gets filed or binned.
[09:44:20] Anjali Kalavar: Second risk for the register, then. Encryption key model unresolved. Priya, severity?
[09:44:28] Priya Raghunathan: Amber. It's amber because there's a viable fallback that doesn't stop go-live, it just costs me a conversation I'd rather not have. Come back to me if the vendor says no outright, then it's a different colour.
[09:44:44] Anjali Kalavar: Amber, with a review trigger on the vendor response. Noted.
[09:44:51] Tom Okafor: Can I flag something adjacent? On the federation side, we've got about nine hundred customer-service agents who'll need role mappings in the new platform. I don't have the role definitions yet. That's not on this agenda but it's going to bite.
[09:45:08] Davis Dean: The role model's being finalised in the build workstream. I'd say two weeks.
[09:45:15] Tom Okafor: Two weeks is fine if it's actually two weeks.
[09:45:19] Davis Dean: I'll put a date on it. Role definitions to Tom by Friday the twenty-eighth.
[09:45:26] Tom Okafor: Thank you.
[09:45:29] Anjali Kalavar: Right, the last thing on my list is data retention, which Will flagged as one of his three open items.
[09:45:38] Will Brown: Yes. So this is about how much legacy billing history comes across into Lattice. The build team have been sizing on an assumption and I don't think anyone's actually decided.
[09:45:51] Davis Dean: We've been sizing on eighteen months because that's what the vendor's reference architecture assumes.
[09:45:59] Priya Raghunathan: No.
[09:46:02] Davis Dean: Okay.
[09:46:04] Priya Raghunathan: No, sorry, that's - I don't mean to be abrupt. Our retention obligation on billing records is seven years. Water and energy both, and the energy side has an additional requirement around dispute records that effectively extends to seven as well. If a customer disputes a bill from 2021, we have to be able to produce it.
[09:46:27] Will Brown: You can produce it from an archive, though. It doesn't have to be in the live platform.
[09:46:34] Priya Raghunathan: In theory. In practice every time we've relied on an archive for a dispute it has taken us six weeks and someone has complained to the ombudsman. I've been through two of those. I'm not doing a third because we saved some storage.
[09:46:51] Anjali Kalavar: So your position is -
[09:46:54] Priya Raghunathan: My position is a decision, not a position. The full seven years of legacy billing history migrates into the new platform, for retention reasons.
[09:47:05] Anjali Kalavar: Understood. That's clear.
[09:47:09] Davis Dean: That's a significant sizing change. Seven years versus eighteen months is - roughly - it's not four and a half times the data because the early years are thinner, but it's a factor of three, easily.
[09:47:24] Priya Raghunathan: Then it's a factor of three. Storage is the cheapest thing in this programme.
[09:47:31] Davis Dean: It's not the storage, it's the migration runtime and the reconciliation effort. But understood, I'll take it to the technical session.
[09:47:41] Anjali Kalavar: There's a data migration deep dive on Friday - Davis, you're in that with Hank and Renata. Carry it in.
[09:47:49] Davis Dean: Will do.
[09:47:52] Will Brown: On the data protection side, this makes the DPIA more important rather than less. Seven years of personal data moving between platforms is exactly the sort of processing change that needs a written assessment, and we don't have one.
[09:48:08] Priya Raghunathan: We don't have one at all?
[09:48:11] Will Brown: There's a screening questionnaire from February that concluded a full assessment was required. Nobody wrote the assessment.
[09:48:20] Priya Raghunathan: Marvellous.
[09:48:23] Will Brown: I'll do it. I've got the template and I've got most of the inputs from the control mapping. I'll circulate a draft data protection impact assessment by Wednesday.
[09:48:34] Anjali Kalavar: This Wednesday, the twelfth?
[09:48:37] Will Brown: This Wednesday. It won't be finished-finished, it'll be a draft with gaps flagged, but it'll be circulatable.
[09:48:45] Priya Raghunathan: Send it to me and Tom. Don't send it to the wider distribution until I've read it.
[09:48:52] Will Brown: Understood. You and Tom only.
[09:48:56] Anjali Kalavar: Good. Anything else on security before we wrap? We've got twenty minutes back.
[09:49:04] Tom Okafor: One thing, quickly. The privileged session recording item Will mentioned at the top - what's actually changed there?
[09:49:13] Will Brown: The vendor's RFP response said native session recording for privileged roles. In the build they've clarified that it records API-level actions but not the administrative UI. Which is - I mean, the administrative UI is where you'd do the damage.
[09:49:31] Tom Okafor: So it records the boring things and not the interesting things.
[09:49:36] Will Brown: Concisely put.
[09:49:39] Priya Raghunathan: Is there a third-party option?
[09:49:43] Davis Dean: There's the privileged access management tooling you already run. It could front the admin UI. It's ugly but it's already licensed.
[09:49:53] Priya Raghunathan: Then look at that rather than buying something. Tom, can you assess whether our existing PAM tooling can front the Lattice admin console?
[09:50:03] Tom Okafor: Yes. I'll need a test tenant.
[09:50:07] Davis Dean: You've got one. I'll send you the details after this.
[09:50:12] Tom Okafor: Then I can give you an answer by the twenty-first.
[09:50:17] Anjali Kalavar: Tom, PAM feasibility assessment for the Lattice admin console, twenty-first of August. Noted.
[09:50:25] Priya Raghunathan: I need to drop in five, I've got a board pre-read.
[09:50:31] Anjali Kalavar: We're basically done. To close the loop - Tom's got the retrospective access review by the twenty-eighth and the freeze notice by the first, Will's got the compensating control note by the twentieth, the pen-test scope by the twenty-fourth and the DPIA draft on Wednesday, Priya's got the pen-test purchase order by the twenty-first, and Davis has got the key management question in by Wednesday and role definitions to Tom by the twenty-eighth. Plus the seven-year retention decision goes into Friday's technical session.
[09:51:02] Will Brown: That's my list too.
[09:51:05] Priya Raghunathan: One correction. The pen test is a red until there's a booked window with a date on it. Not until the purchase order lands - until there's a date. I don't want it quietly downgraded next week because paperwork moved.
[09:51:21] Anjali Kalavar: Understood. Red until there's a confirmed test window.
[09:51:27] Priya Raghunathan: Then I'm happy. Or rather, I'm not happy, but I'm informed.
[09:51:33] Davis Dean: The two are rarely the same thing.
[09:51:37] Priya Raghunathan: Thanks all. Tom, stay on for two minutes?
[09:51:42] Tom Okafor: Yep.
[09:51:44] Anjali Kalavar: Thanks everyone. Same time in a fortnight unless the pen test forces something sooner.
[09:51:51] Will Brown: Thanks all.
[09:51:53] Davis Dean: Bye.
