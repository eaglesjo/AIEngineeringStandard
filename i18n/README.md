# Language Resources

`AI Engineering Standard` separates **documentation localization** from **runtime policy localization** so a language is never advertised as fully translated before its Agent / Skill / Environment resources are actually translated and validated.

## Documentation languages

The documentation catalog covers the canonical English source and one localized locale:

| Locale | Language |
|---|---|
| `en` | English |
| `ko` | 한국어 |
Each documentation locale has its own README entrypoint and is tracked in [`languages.json`](languages.json).

## Runtime resource languages

The canonical English source and Korean are declared as runtime-resource languages. Korean explicitly falls back to `en` for resources that are not localized at a domain-specific level.

The runtime contract requires the common policy layer (`AGENT.md`, `SKILL.md`, `ENVIRONMENT.md`) and locale README entrypoint to exist. Runtime promotion is subject to the current 2.0 localization quality contract.

## Runtime i18n quality

CI validates every locale declared under `runtime_resources` in [`languages.json`](languages.json).

The 2.0 quality contract requires three gates:

1. **Resource completeness** — required runtime resources exist.
2. **Semantic policy parity** — required engineering-policy intents are expressed consistently in the locale.
3. **Runtime/documentation consistency** — runtime and documentation entries remain aligned.

Every supported runtime locale must reach quality grade **A** before release promotion.

## Colab documentation

The public Colab validation flow is documented in locale-specific guides. The canonical English guide remains [`../tests/colab/README.md`](../tests/colab/README.md).

## Localization rules

1. English remains the canonical source of truth; Korean is the only localized locale.
2. Korean may be listed as the localized documentation language once its README entrypoint exists.
3. Korean may be listed as a runtime resource language only when its required common resources pass CI validation.
4. Missing domain-specific translations must fall back to English rather than copying or inventing untranslated text.
5. Documentation and runtime support must remain explicitly represented in `languages.json`.
6. Any future locale change must be explicitly approved, added to `i18n/languages.json`, and validated in CI.
7. 