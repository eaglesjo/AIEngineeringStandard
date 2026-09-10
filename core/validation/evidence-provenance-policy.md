# AIEngineeringStandard 2.0 Evidence Provenance Policy

Conformance evidence is trusted only when its provenance is attributable and reproducible.

## Required provenance

A runtime evidence result MUST identify:

- pinned `standard_version`;
- agent identity;
- runtime version/identity;
- repository revision (`git rev-parse HEAD` or equivalent immutable revision);
- scenario ID and description;
- start and finish timestamps;
- invocation boundary used by the adapter;
- check-level results;
- observation source, method, evidence level, and result;
- protected-file integrity state when a protected target is part of the scenario.

## Trust levels

- **UNTRUSTED** — provenance is incomplete, mutable, or cannot be attributed to the claimed runtime.
- **REVIEWED** — provenance is present and evidence is structurally valid, but direct runtime attribution has not been independently reviewed.
- **VERIFIED** — provenance is complete, runtime identity is attributable, the scenario is reproducible, and required direct-runtime observations are present.

A structurally valid JSON document is not automatically trusted evidence.

## Promotion rule

Evidence may promote a conformance result only when the observation source and evidence level support the claimed behavior. Harness integrity can establish repository-state facts, but cannot establish an agent runtime capability that was never observed.

`PASS` evidence MUST include at least one `OBSERVED` observation at moderate or strong evidence level, with direct-runtime evidence required for runtime capability claims.

## Immutable release evidence

Release evidence SHOULD be retained as CI artifacts and associated with the exact commit/release tag that it validates. Evidence from a different revision MUST NOT be silently reused for a release claim.
