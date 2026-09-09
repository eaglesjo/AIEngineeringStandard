# Agent Profiles

Agent profiles describe runtime-specific capabilities without redefining the portable engineering standard.

An agent profile may declare:

- runtime identity and version;
- discovery locations;
- Skill/Plugin/MCP support;
- permission boundaries;
- sub-agent capabilities;
- validation/conformance status.

Profiles specialize the common standard. They must not silently weaken higher-level project or domain policy.

The initial profile set is introduced during 2.0-M1; concrete P0 profiles are added only with evidence in later milestones.
