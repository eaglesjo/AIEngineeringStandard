Release development target: 1.17.2.

Status: release preparation after repository architecture transition. `codingStandard-dev` is now the canonical development, validation, and release source of truth; validated releases are promoted to `eaglesjo/AIEngineeringStandard`. `codingStandard-private` is Luna-only and is not a release source.

Validation focus:
- canonical repository architecture and policy profile validation
- repository dependency and layer-boundary validation
- multilingual runtime resource completeness and semantic policy parity across 20 runtime locales
- runtime/documentation consistency validation
- environment contract and resource detection validation
- installer dry-run/merge/overwrite/skip and lifecycle validation
- installation manifest, update, obsolete-file reconciliation, and protected uninstall behavior
- LLM and Vision CPU memory smoke tests
- Colab runtime and notebook validation
- deterministic RAG regression and quality-gate coverage
- final release-gate validation before creating `v1.17.2`

Release invariants:
- preserve the existing `v1.17.1` tag and historical commits
- do not restore AI Engineering Standard source or release workflows to `codingStandard-private`
- promote only from validated `codingStandard-dev` source to `eaglesjo/AIEngineeringStandard`
