# Release Process

## Repository role

`AIEngineeringStandard` is the canonical development, validation, and release repository.

```text
feature/fix/docs branch
        ↓
Pull Request
        ↓
Local validation gate
        ↓
main
        ↓
version bump
        ↓
annotated release tag
        ↓
tag validation
        ↓
GitHub Release
```

There is no `codingStandard-private`, `codingStandard-dev`, staging repository, promotion repository, or public-export repository.

## Release contract

1. Make the required implementation and documentation changes in a feature/fix/release branch.
2. Run focused validation during development.
3. Open a pull request against `main`.
4. Require Local validation gate to pass.
5. Merge only a validated commit into `main`.
6. Update `VERSION` and matching release metadata.
7. Create tag `v<VERSION>` from the exact `main` commit.
8. Run `python3 scripts/release/check_release.py` from the exact `main` commit.
9. Run `python3 scripts/release/publish_release.py` to create the annotated tag and GitHub Release explicitly.

## Evidence rules

- Record the exact source commit and release tag.
- Treat validation as execution evidence only when the corresponding local gate completed successfully; record the environment and exact commit.
- Mark unavailable checks as `UNTESTED`, `UNSUPPORTED`, `SKIPPED`, or `BLOCKED`.
- Never convert missing live-runtime evidence into a pass by assumption.
- Preserve historical tags and commits.

## Release gate

A release is blocked if version metadata is inconsistent, required validation fails, release documentation describes an obsolete repository model, or the release tag does not exactly match `VERSION`.

## Historical releases

`v2.0.0` is preserved as historical provenance from the former promotion-based release model. It is not reproduced or rewritten as part of the independent-release transition.
