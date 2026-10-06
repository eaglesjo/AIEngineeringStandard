# Language Resources

`AI Engineering Standard` keeps English as the canonical source language and Korean as the only localized language.

## Documentation languages

| Locale | Language |
|---|---|
| `en` | English |
| `ko` | 한국어 |

Each documentation locale has its own README entrypoint and is tracked in [`languages.json`](languages.json).

## Runtime resource languages

English is the canonical runtime source and Korean is the only localized runtime resource. Korean explicitly falls back to `en` for resources that are not localized at a domain-specific level.

The runtime contract requires the common policy layer (`AGENT.md`, `SKILL.md`, `ENVIRONMENT.md`) and locale README entrypoint to exist.

## Runtime localization quality

CI validates every locale declared under `runtime_resources` in [`languages.json`](languages.json).

The localization quality contract requires three gates:

1. **Resource completeness** — required runtime resources exist.
2. **Semantic policy parity** — required engineering-policy intents are expressed consistently in Korean.
3. **Runtime/documentation consistency** — runtime and documentation entries remain aligned.

Every supported localized runtime locale must reach quality grade **A** before release promotion.

## Colab documentation

The canonical English Colab guide remains [`../tests/colab/README.md`](../tests/colab/README.md). Korean localization is maintained under `i18n/ko/`.

## Localization rules

1. English remains the canonical source of truth.
2. Korean is the only supported localized language.
3. Korean may be listed as a runtime resource language only when its required common resources pass CI validation.
4. Missing domain-specific Korean translations must fall back to English rather than copying or inventing untranslated text.
5. Documentation and runtime support must remain explicitly represented in `languages.json`.
6. Any future locale change must be explicitly approved, added to `i18n/languages.json`, and validated in CI.
