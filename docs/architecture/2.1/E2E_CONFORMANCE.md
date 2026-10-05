# v2.1 End-to-End Conformance

The canonical fixtures exercise the v2.1 lifecycle through distinct Work Units, evidence, handoffs, evaluation, acceptance, retry lineage, parallel join boundaries, and human approval.

## Primary multi-agent scenario

The Planner, Implementer, and Verifier fixture demonstrates:

- distinct Work Unit identities;
- child Work Units retaining parent_id;
- bounded permissions;
- evidence-backed handoffs;
- evidence-backed evaluation;
- explicit evaluation actors;
- acceptance only after PASS;
- explicit receiving-agent ownership.

The implementation Work Unit remains HANDOFF_PENDING after transfer; the Verifier owns the verification boundary. The root Work Unit is accepted only after verification evidence exists.

## Retry and recovery scenario

The retry fixture demonstrates this sequence:

FAILED ATTEMPT → BLOCKED → retry(reason, failure_evidence_refs) → NEW WORK UNIT / ATTEMPT

The retry retains parent_id, an explicit retry_reason, and failure_evidence_refs. A retry must not overwrite or discard the failed attempt. The reference runtime rejects retries that omit a reason, reference missing evidence, or reference evidence belonging to another Work Unit.

## Parallel work scenario

The parallel fixture demonstrates independent sibling Work Units with explicit parent_id lineage and an explicit join evidence boundary before root acceptance.

## Human approval scenario

The human approval fixture demonstrates that human intervention is represented by:

- an explicit Evaluation actor with type human;
- human-approval evidence;
- matching human actor identity in the approval evidence source;
- PASS → ACCEPTED acceptance.

The reference runtime rejects human acceptance without matching approval evidence and rejects ACCEPTED evaluations whose result is not PASS.
