# AIEngineeringStandard 2.0 Master Plan

> Status: Proposed architecture and implementation plan
>
> Target major version: **2.0.0**
>
> Current baseline: **1.17.2**

## 1. Vision

AIEngineeringStandard 2.0 evolves the project from a collection of AI-development rules and platform adapters into a **portable, agent-native AI engineering standard**.

The standard should allow an engineering policy to be defined once and consumed consistently by multiple AI agents, IDEs, CLIs, notebook environments, cloud agents, and agent runtimes.

### Positioning

> **AIEngineeringStandard 2.0 — Portable, Agent-Native AI Engineering Standard**

The core objective is not to optimize for one vendor. The core objective is to define portable engineering contracts and provide thin adapters where a runtime requires them.

## 2. Why 2.0

Version 1.x already provides a strong foundation:

- canonical common rules;
- domain-specific ML/LLM/Vision guidance;
- Colab runtime policy;
- Skills and agent instructions;
- architecture and policy profiles;
- installation lifecycle management;
- multilingual resource validation;
- validation and installer test suites.

The 2.0 release expands that foundation to the rapidly converging agent ecosystem. In particular, portable Agent Skills and Agent Plugins make it possible to package reusable agent behavior independently from any single client.

2.0 is therefore a **major architectural release**, not a version-number-only update.

## 3. 2.0 Architecture

The target architecture is:

```text
AIEngineeringStandard 2.0
│
├── core/
│   ├── common/          # universal engineering rules
│   ├── agent/           # agent behavior and execution contracts
│   ├── skill/           # portable Skill contracts and metadata
│   ├── plugin/          # portable Agent Plugin contracts
│   ├── mcp/             # MCP integration and security contracts
│   └── validation/      # machine-checkable validation contracts
│
├── skills/              # canonical portable Skills
├── plugins/             # distributable portable Plugins
├── agents/              # thin client/runtime adapters
├── profiles/            # project, architecture, policy and agent profiles
├── compatibility/       # capability catalog and compatibility matrix
├── docs/
│   ├── agents/
│   ├── skills/
│   ├── plugins/
│   ├── mcp/
│   └── compatibility/
├── scripts/             # installers, validators and tooling
└── tests/               # conformance and compatibility tests
```

This is a target architecture. Existing 1.x paths must be preserved until each migration has an explicit compatibility and deprecation strategy.

## 4. Core Standards

### 4.1 Portable AI Engineering Standard

The existing common, ML, LLM, Vision and Colab contracts remain the foundation.

2.0 adds explicit contracts for:

- agent execution;
- task delegation;
- sub-agents;
- Skills;
- Plugins;
- MCP tools/resources/prompts;
- permissions;
- provenance;
- reproducibility;
- validation evidence.

### 4.2 Agent Skills Standard

Agent Skills become a first-class portable distribution layer.

Requirements:

1. Prefer the open `SKILL.md` format.
2. Use `.agents/skills/` as the canonical project-level portable location where supported.
3. Keep reusable Skill content vendor-neutral.
4. Avoid duplicating identical Skills for individual clients.
5. Use thin adapters only when a client requires a different entry point or metadata.
6. Skills containing executable code must declare security and execution expectations.
7. Skill versions and provenance must be inspectable.

### 4.3 Agent Plugin Standard

Agent Plugins become the preferred portable packaging model for bundles of reusable agent components.

The 2.0 baseline targets the published Agent Plugins **1.0.0** specification.

A portable plugin should be able to contain:

- `plugin.json` metadata;
- `skills/` reusable Skills;
- optional `mcp.json` MCP configuration;
- vendor-specific extensions only under explicit extension namespaces.

The project should track future Plugin specification changes without making an unstable draft a hard dependency.

### 4.4 MCP Standard

MCP is treated as an integration boundary, not as an implicit trust boundary.

2.0 will define:

- server registration requirements;
- tool/resource/prompt handling rules;
- permission expectations;
- secret handling;
- provenance and source verification;
- version pinning where possible;
- failure and timeout behavior;
- audit/evidence requirements.

### 4.5 Multi-Agent and Sub-Agent Standard

2.0 will define common expectations for delegated work:

- explicit task ownership;
- bounded scope;
- context requirements;
- tool/Skill permissions;
- result contract;
- failure propagation;
- evidence/reporting;
- termination conditions.

Sub-agents must not be assumed to inherit parent capabilities automatically. Capability inheritance must be explicit.

## 5. Agent Compatibility Tiers

### P0 — First-class compatibility

These environments receive direct validation and documented integration paths:

1. OpenAI Codex
2. Claude Code
3. GitHub Copilot
4. Gemini / Antigravity
5. **Google Colab Gemini Agent**
6. Cursor
7. OpenCode
8. Roo Code

### P1 — Active compatibility

9. Cline
10. Continue
11. Windsurf
12. Amazon Q Developer

### P2 — Compatibility/adapters

The initial P2 set includes Aider, Amp, Goose, Devin, JetBrains Junie, Augment, Cortex Code, Crush, CodeBuddy, Command Code, IBM Bob and other environments selected from the active agent ecosystem.

P2 means compatibility is measured and documented, but does not require the same depth of platform-specific integration as P0.

## 6. Google Colab Gemini Agent

Google Colab Gemini is a first-class 2.0 target.

The standard will provide a dedicated Colab/Gemini integration contract covering:

- notebook-level custom instructions;
- project policy discovery;
- portable Skills where supported;
- runtime/resource validation;
- reproducible execution;
- checkpoint and recovery policy;
- safe tool usage;
- notebook sharing considerations;
- validation of the effective instruction set.

Colab must not be treated as merely another IDE adapter because its execution environment is ephemeral and notebook-scoped.

## 7. Compatibility Matrix

2.0 introduces a formal compatibility matrix rather than informal claims of support.

The matrix will track at minimum:

| Capability | P0/P1/P2 agents |
|---|---|
| Instruction discovery | Required measurement |
| Skill discovery | Required measurement |
| Skill loading | Required measurement |
| Plugin loading | Required measurement where supported |
| MCP integration | Required measurement where supported |
| Tool permissions | Required measurement |
| Sub-agent delegation | Capability-specific |
| Project profiles | Required |
| Validation execution | Required |
| Failure/recovery behavior | Required |
| Evidence/reporting | Required |

Support status must be evidence-based:

```text
PASS       validated
PARTIAL    capability works with documented limitations
ADAPTER    requires a platform adapter
UNTESTED   integration exists but has not yet passed conformance tests
UNSUPPORTED not provided by the target runtime
```

## 8. Conformance Test Model

Compatibility testing follows a common sequence:

```text
Discovery
   ↓
Instruction Loading
   ↓
Skill Discovery
   ↓
Skill Loading
   ↓
Plugin/MCP Capability Check
   ↓
Permission Check
   ↓
Task Execution
   ↓
Validation
   ↓
Failure Recovery
   ↓
Evidence / Result Reporting
```

Tests must validate behavior, not merely the presence of files.

Where a runtime cannot be automated in CI, the repository will provide a deterministic manual conformance procedure and record the test date, runtime version, capabilities and result.

## 9. Security and Trust Model

Agent-native standards introduce executable and externally sourced components. 2.0 therefore treats Skills, Plugins and MCP servers as potentially untrusted inputs.

The standard will define:

- provenance requirements;
- source/repository verification;
- version pinning;
- integrity checks where practical;
- permission boundaries;
- executable-content detection;
- secret isolation;
- prompt-injection awareness;
- MCP server trust classification;
- install/preview validation;
- CI security checks;
- explicit human approval for high-risk capabilities.

Portable content and executable components must be clearly distinguished.

## 10. Profiles and Policy Inheritance

Existing project, architecture and policy profiles remain authoritative.

2.0 adds agent-aware profiles such as:

```text
project
architecture
policy
agent
skill
plugin
runtime
```

Profiles should be machine-readable where practical and validated before implementation changes.

Policy inheritance must be explicit:

```text
Project Policy
      ↓
Domain Policy
      ↓
Agent Policy
      ↓
Skill Policy
      ↓
Task/Runtime Constraints
```

A lower layer may specialize a policy only within the boundaries declared by the higher layer.

## 11. Migration from 1.x

2.0 must be adoptable without forcing an immediate destructive migration.

### Phase A — Compatibility bridge

- Preserve current 1.x installation domains.
- Preserve existing platform adapters.
- Introduce portable Skills alongside existing adapters.
- Add compatibility metadata.

### Phase B — Portable-first distribution

- Move reusable behavior into canonical Skills.
- Generate or maintain thin platform adapters.
- Introduce Plugin packaging.
- Add conformance tests.

### Phase C — 2.0 default architecture

- Make portable Skills and Plugins the preferred integration path.
- Keep legacy adapters as compatibility surfaces.
- Mark superseded paths explicitly.
- Remove legacy paths only in a later breaking release when migration evidence supports removal.

## 12. Versioning Policy

2.0 follows semantic versioning:

- `2.0.x` — fixes, security updates, documentation corrections and compatibility corrections.
- `2.1.x` — new agents, Skills, Plugins and non-breaking capabilities.
- `2.x` — additive standard evolution that preserves the 2.0 contract.
- `3.0` — breaking changes to the core standard or incompatible contract changes.

External specifications are versioned independently. AIEngineeringStandard must record the specification version it targets.

## 13. Implementation Roadmap

### Milestone 2.0-M1 — Foundation

- Freeze the 1.17.2 baseline.
- Add the 2.0 architecture and terminology.
- Define agent/skill/plugin/MCP profiles.
- Define compatibility metadata schema.
- Define conformance result schema.

### Milestone 2.0-M2 — Portable Skills

- Establish canonical portable Skill layout.
- Migrate reusable existing Skills.
- Add Skill validation.
- Add Skill security/provenance checks.
- Add P0 Skill compatibility tests.

### Milestone 2.0-M3 — Plugins and MCP

- Add Plugin 1.0 packaging.
- Add plugin validation.
- Add MCP integration contract.
- Add MCP security checks.
- Add example portable plugin(s).

### Milestone 2.0-M4 — Agent Compatibility

- Implement P0 adapters and conformance tests.
- Add Colab Gemini integration.
- Add P1 adapters.
- Establish P2 compatibility catalog.

### Milestone 2.0-M5 — Validation and Release Gate

- Automate compatibility metadata validation.
- Add security validation to CI.
- Add installer/package validation.
- Add migration tests from representative 1.x projects.
- Require release evidence for P0 support claims.

### Milestone 2.0-M6 — Public 2.0 Release

- Update documentation and multilingual entry points.
- Publish migration guide.
- Publish compatibility matrix.
- Publish security/trust model.
- Update version to `2.0.0` only after the release gate passes.

## 14. Definition of Done for 2.0.0

2.0.0 is complete only when all of the following are true:

- The portable core is documented and validated.
- Agent Skills are a first-class standard layer.
- Agent Plugins 1.0 is supported as a packaging baseline.
- MCP integration has explicit security and permission rules.
- P0 compatibility is measured rather than claimed.
- Google Colab Gemini Agent has a documented and validated path.
- Agent/sub-agent behavior has explicit contracts.
- Security/provenance validation is part of the release gate.
- 1.x migration is documented and tested.
- Existing architecture/profile validation remains intact.
- Existing multilingual quality contracts remain intact.
- CI validates the new 2.0 contracts.
- Release documentation accurately reflects the implementation.

## 15. Non-Goals

2.0 will not:

- become a vendor-specific agent framework;
- replace MCP with a proprietary tool protocol;
- require every agent to implement every capability;
- duplicate identical Skills for every platform;
- declare support based only on file presence;
- make unstable external drafts mandatory dependencies;
- remove working 1.x integrations without migration evidence.

## 16. Engineering Principles for 2.0

1. **Portable first.**
2. **Vendor neutral.**
3. **Evidence over claims.**
4. **Secure by default.**
5. **Thin adapters, strong core.**
6. **Explicit capability and permission boundaries.**
7. **Reproducible and observable execution.**
8. **Backward-compatible migration where practical.**
9. **Machine-checkable contracts over documentation-only promises.**
10. **Human approval for consequential or high-risk actions.**

## 17. Immediate Next Actions

The next implementation step after this plan is **2.0-M1 Foundation**:

1. audit the complete 1.17.2 repository structure;
2. identify existing Skills, agent adapters, profiles and validators;
3. define the 2.0 schemas without duplicating existing contracts;
4. add the compatibility and security foundations;
5. implement the first portable Skill and conformance test;
6. then proceed to Plugin/MCP packaging.

This document is the architectural baseline for that work. Implementation changes should reference this plan when introducing 2.0-specific files or contracts.
