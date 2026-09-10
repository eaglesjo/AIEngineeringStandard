# AIEngineeringStandard 2.0 Adapter Contract

An agent adapter is a thin vendor-specific boundary between an agent runtime and the vendor-neutral 2.0 conformance harness.

## Required adapter surface

Every runtime adapter MUST provide equivalent behavior for:

1. **discovery** — determine whether the runtime executable is available;
2. **version** — return a stable runtime identity/version or `UNTESTED`;
3. **invocation** — construct a bounded invocation without silently widening permissions;
4. **event parsing** — map only documented/observed runtime events to normalized observations;
5. **capability mapping** — report MCP, Plugin, Skill, instruction, permission, and task evidence only when directly observable;
6. **evidence handoff** — invoke the common runtime harness and preserve scenario/revision/runtime provenance.

## Evidence rules

- Unknown runtime event shapes MUST NOT be promoted into semantic evidence.
- Prompt text, expected-output markers, and harness assertions MUST NOT manufacture runtime capability evidence.
- File access to a Skill is not equivalent to a first-class Skill-load event unless the adapter has an explicit, attributable runtime signal.
- Protected-file integrity is a safety backstop, not proof of runtime permission enforcement.
- `PASS` requires the same mandatory-check and evidence requirements defined by the conformance policy.
- An unavailable runtime MUST result in `UNTESTED` rather than an inferred failure or pass.

## Invocation safety

Adapters MUST choose a documented restrictive baseline and MUST NOT accept arbitrary caller flags that can widen filesystem, network, secret, or destructive-operation permissions without an explicit conformance scenario and policy review.

## Normalized observation IDs

Adapters MAY add vendor-specific observation IDs, but the following normalized concepts SHOULD be used when applicable:

- instruction discovery
- Skill discovery
- Skill loading
- Plugin capability
- MCP capability
- permission denial
- task execution
- validation
- failure recovery
- evidence reporting

The absence of an observable event is `NOT_OBSERVED`; it is never silently inferred from a nearby event.
