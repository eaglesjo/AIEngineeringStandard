# v2.1 End-to-End Conformance

The canonical fixture exercises Planner, Implementer, and Verifier agents through distinct Work Units, evidence, handoffs, evaluation, and acceptance. Child Work Units retain parent_id. The implementation Work Unit remains HANDOFF_PENDING after transfer; the Verifier owns the verification boundary. The root Work Unit is accepted only after verification evidence exists.

Required invariants: distinct Work Unit identities; bounded permissions; evidence-backed handoffs; evidence-backed evaluation; acceptance only after PASS; explicit receiving-agent ownership.

Parallel scheduling, retries, and human approval remain separate conformance scenarios so each invariant has an isolated failure signal.
