# AIEngineeringStandard 2.2 Installable Distribution

## Decision

Version 2.2 changes the consumer distribution model from repository cloning to package installation.

The GitHub repository remains the single source of truth for development, validation, and release. The consumer receives a versioned Python distribution.

## Runtime layers

```
Git repository
    |
    +-- source validation
    |
    +-- release tag
            |
            +-- wheel
            +-- sdist
            |
            +-- PyPI
                    |
                    +-- pip / pipx
                            |
                            +-- ai-engineering-standard CLI
                                    |
                                    +-- consumer project
```

## Package contract

- Distribution name: `ai-engineering-standard`
- Import package: `ai_engineering_standard`
- CLI command: `ai-engineering-standard`
- Supported Python: 3.10+
- Artifact class: pure Python wheel plus sdist
- Resource loading: `importlib.resources`
- Installation state: `.codingstandard/installation.json`
- Manifest schema: 2

## CLI lifecycle

```
install -> status -> update -> validate -> uninstall
```

The CLI is the consumer-facing interface. Source-tree shell and PowerShell wrappers remain compatibility tooling for repository development and release validation.

## Distribution integrity

Every release must build and inspect both a wheel and source distribution before publishing. The wheel must contain the CLI package and every resource mapping required by the installation domains.

Publishing should use PyPI Trusted Publishing through GitHub Actions OIDC rather than long-lived package credentials.

## Non-goals

2.2 does not make the GitHub repository a runtime dependency. A consumer installation must continue to work after the source repository is absent from the consumer machine.
