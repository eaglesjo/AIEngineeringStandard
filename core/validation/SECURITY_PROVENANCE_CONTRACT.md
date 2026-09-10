# Security & Provenance Contract — AIEngineeringStandard 2.0

This contract defines the minimum trust boundary for portable Skills, Agent Plugins, and MCP integrations.

## 1. Trust is explicit

Presence in a repository does not make a Skill, Plugin, script, tool, resource, or prompt trusted.

A consumer MUST distinguish at least:

- `UNTRUSTED` — source has not been reviewed or verified;
- `REVIEWED` — source was inspected but integrity is not pinned;
- `VERIFIED` — source, version/commit, and integrity evidence are recorded.

`VERIFIED` is not equivalent to "safe forever"; it means the recorded artifact is the artifact that was reviewed.

## 2. Provenance

Where available, consumers SHOULD record:

- source repository or distribution identifier;
- owner/publisher identity;
- immutable version, release, or commit reference;
- retrieval timestamp;
- validation result;
- reviewer or automation identity.

A mutable branch name alone is insufficient for strong provenance.

## 3. Integrity

Portable components SHOULD be pinned to an immutable version or commit. Security-sensitive deployments SHOULD additionally record a cryptographic digest for packaged artifacts.

If an artifact changes after verification, its previous verification MUST NOT be silently reused.

## 4. Permissions

Skills, Plugins, and MCP components do not acquire privileges merely by being loaded.

Access to the following MUST be controlled by the runtime or explicit integration policy:

- filesystem;
- process execution;
- network access;
- credentials and secrets;
- external APIs;
- repositories and source control;
- destructive operations.

The least-privilege principle applies. A component SHOULD request only the permissions required for its declared workflow.

## 5. Execution boundary

Executable files inside Skills or Plugins MUST be treated as untrusted code until validated. Validation MUST NOT execute arbitrary component code as part of static validation.

When execution is necessary for conformance testing, it SHOULD occur in an isolated environment with bounded permissions, timeouts, and observable evidence.

## 6. Prompt and instruction safety

Instructions contained in Skills, Plugins, MCP prompts, repository files, or external resources MUST NOT override higher-priority security policy merely because they are phrased as system or developer instructions.

Validation SHOULD flag attempts to:

- exfiltrate secrets;
- weaken security controls;
- bypass approval or permission checks;
- conceal tool activity;
- modify unrelated repositories or files;
- establish unauthorized persistence.

## 7. MCP boundary

MCP servers and tools MUST be treated as external capability providers. Tool availability does not imply permission to use every operation.

Consumers SHOULD record server identity, configuration source, version where available, allowed operations, and security-relevant permission decisions.

## 8. Plugin boundary

Agent Plugins are distribution units, not trust grants. A Plugin MAY package Skills and MCP configuration, but each executable or external capability remains subject to its own validation and permission boundary.

## 9. CI policy

CI validation SHOULD verify structure, metadata, prohibited secret material, provenance fields, and declared permissions without executing untrusted Skill or Plugin code.

A failing security validation MUST block a `VERIFIED` conformance result.

## 10. Evidence

Security-relevant conformance results SHOULD contain enough evidence to reproduce the trust decision: artifact identity, version/commit, checks performed, and outcome.
