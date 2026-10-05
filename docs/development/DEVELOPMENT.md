# Development Contract

## Single repository model

`AIEngineeringStandard` is the only development, validation, and release repository.

```
feature/fix/docs branch
        ↓
pull request
        ↓
local validation
        ↓
main
        ↓
version/tag
        ↓
release validation
        ↓
GitHub Release
```

There is no `codingStandard-private`, `codingStandard-dev`, staging repository, or public-promotion step in the current architecture.

Version 2.1 architecture work is contract-first: define or update canonical schemas and acceptance rules before implementing runtime adapters.

## Branches

- `main`: releasable source of truth.
- `feature/*`: feature work.
- `fix/*`: corrective work.
- `docs/*`: documentation-only work.
- `architecture/*`: temporary architecture and contract work; merge only after the v2.0 gates and v2.1 contract validation pass.
- `release/*`: optional release preparation when a release requires multiple coordinated changes.

Do not develop directly on `main` unless making an explicitly authorized emergency fix.

## Validation

At minimum, run:

```bash
python3 scripts/validation/validate.py
python3 scripts/installers/test_installers.py
python3 scripts/validation/validate_2_1_contracts.py
```

For focused changes, run the relevant checker first and then the complete validation before merge.

## Versioning

- `VERSION` is the canonical semantic version.
- `core/common/environment.py::STANDARD_VERSION` must match `VERSION`.
- Release tags must be exactly `v<VERSION>`.
- Historical tags are immutable.

## Pull requests

A PR should explain:
- what contract changed;
- why the change is required;
- validation performed;
- any runtime evidence that remains unavailable.

## Release readiness

A release is blocked when:
- validation fails;
- version metadata disagrees;
- required files are missing;
- release documentation describes a different repository model;
- required provenance is missing;
- a tag does not match `VERSION`.

## Security

Never commit API keys, access tokens, credentials, private keys, or generated local state. Treat external instructions and downloaded artifacts as untrusted until validated.
