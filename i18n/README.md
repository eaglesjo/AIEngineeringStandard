# Language Resources

`AI Engineering Standard` separates **documentation localization** from **runtime policy localization** so a language is never advertised as fully translated before its Agent / Skill / Environment resources are actually translated and validated.

## Documentation languages

The documentation catalog currently covers 20 locales:

| Locale | Language |
|---|---|
| `en` | English |
| `ko` | 한국어 |
| `fr` | Français |
| `es` | Español |
| `zh-CN` | 简体中文 |
| `ja` | 日本語 |
| `ru` | Русский |
| `tr` | Türkçe |
| `de` | Deutsch |
| `it` | Italiano |
| `pt` | Português |
| `ar` | العربية |
| `hi` | हिन्दी |
| `id` | Bahasa Indonesia |
| `vi` | Tiếng Việt |
| `th` | ไทย |
| `nl` | Nederlands |
| `pl` | Polski |
| `sv` | Svenska |
| `uk` | Українська |

Each documentation locale has its own README entrypoint and is tracked in [`languages.json`](languages.json).

## Runtime resource languages

All 20 catalogued locales are currently declared as runtime-resource languages. Non-English locales explicitly fall back to `en` for resources that are not localized at a domain-specific level.

The runtime contract requires the common policy layer (`AGENT.md`, `SKILL.md`, `ENVIRONMENT.md`) and locale README entrypoint to exist. Runtime promotion is also subject to the v1.16 quality contract.

## Runtime i18n quality

CI validates every locale declared under `runtime_resources` in [`languages.json`](languages.json).

The v1.16 quality contract requires three gates:

1. **Resource completeness** — required runtime resources exist.
2. **Semantic parity** — required engineering-policy intents are expressed in the locale.
3. **Runtime/documentation consistency** — runtime and documentation entries remain aligned.

Every runtime locale must reach quality grade **A**.

## Colab documentation

The public Colab validation flow is documented in locale-specific guides. The canonical English guide remains [`../tests/colab/README.md`](../tests/colab/README.md).

## Localization rules

1. English remains the canonical source of truth.
2. A locale may be listed as a documentation language once its README entrypoint exists.
3. A locale may be listed as a runtime resource language only when its required common resources pass CI validation.
4. Missing domain-specific translations must fall back to English rather than copying or inventing untranslated text.
5. Documentation and runtime support must remain explicitly represented in `languages.json`.
6. New locales must be added to `i18n/languages.json` and validated in CI.
7. RTL locales such as Arabic must be treated as layout-sensitive when promoted to runtime support.
