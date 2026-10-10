# Releases

This directory is the human-readable history and planning area for releases.

## Rules

- `VERSION` at the repository root is the authoritative version for the next release.
- Git tags such as `v2.2.1` are the immutable release identifiers and must match `VERSION`.
- Release-specific notes belong here, using one Markdown file per release when notes are needed (for example `2.2.1.md`).
- Temporary release staging files do not belong in the repository.
- `FINAL_VERSION.txt`, `VERSION.next`, `VERSION.tmp`, and version-specific staging files are obsolete and must not be recreated.

## Release boundary

`eaglesjo/AIEngineeringStandard` is the single source of truth for development, validation, and release. Do not export or promote source from a separate private, development, staging, or distribution repository.

Before publishing, use an exact, clean checkout of `main` and run `python3 scripts/release/check_release.py`. If preflight passes, run `python3 scripts/release/publish_release.py` to create and push the annotated version tag and create the GitHub Release. Pushing a `v*.*.*` tag triggers `.github/workflows/publish-package.yml`, which verifies the tag against `VERSION`, builds and checks the distributions, publishes them to PyPI, and creates or updates the GitHub Release with build artifacts.

After publishing, verify the tag target, GitHub Actions workflow result, GitHub Release assets, and the published package version. Report any stage that has not completed as blocked or incomplete; do not infer successful publication from tag creation alone.
