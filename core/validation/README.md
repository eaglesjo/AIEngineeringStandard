# 2.0 Validation Foundation

The 2.0 validation layer extends the existing 1.x validation suite rather than replacing it.

## M1 contracts

- `conformance-result.schema.json` defines the machine-readable result contract for agent compatibility tests.
- `compatibility/agents.json` defines the initial capability catalog contract.

## Validation rule

A platform is not considered supported merely because an adapter file exists. Support status must be backed by a conformance result or explicitly marked `UNTESTED`.

Existing structure, domain, profile, language, installer and Colab validation remain part of the 2.0 release gate.
