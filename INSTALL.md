# Installation Guide

`install-domains.ps1` and `install-domains.sh` are the supported installers for the public `AIEngineeringStandard` distribution.

## 1. Clone

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
```

Run the installer from the repository root of the project you want to configure.

## 2. Choose Language and Domain

Documentation and runtime resources are catalogued for 20 locales. Runtime resources use English fallback where a locale-specific resource is not available at a domain-specific level.

```text
Documentation / runtime locales
  en      = English
  ko      = Korean
  fr      = French
  es      = Spanish
  zh-CN   = Simplified Chinese
  ja      = Japanese
  ru      = Russian
  tr      = Turkish
  de      = German
  it      = Italian
  pt      = Portuguese
  ar      = Arabic
  hi      = Hindi
  id      = Indonesian
  vi      = Vietnamese
  th      = Thai
  nl      = Dutch
  pl      = Polish
  sv      = Swedish
  uk      = Ukrainian

Install domains
  common = common rules only
  ml     = common + general ML/DL lifecycle
  llm    = common + LLM
  vision = common + Vision
  colab  = common + Colab runtime policy
  all    = common + ML + LLM + Vision + Colab
```

### Windows / PowerShell

Interactive mode:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Explicit mode:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target . -Language ko -Domain ml
```

### Linux / macOS

Interactive mode:

```bash
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Explicit mode:

```bash
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh . ko ml overwrite false
```

Arguments are:

```text
TARGET LANGUAGE DOMAIN CONFLICT_POLICY DRY_RUN
```

## 3. Preview Before Installing

PowerShell:

```powershell
... -Language en -Domain all -DryRun
```

Bash:

```bash
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh . en all ask true
```

Dry-run never writes installation files.

## 4. Existing Files

When a target file already exists:

```text
Ask       choose per file
Merge     preserve existing content and update the AIEngineeringStandard-managed block
Overwrite replace the complete target file
Skip      keep the existing target file
```

Use `Merge` for project-owned instruction files when preserving local rules is important. Use `Overwrite` for files fully owned by the standard.

## 5. What Common Installs

The Common layer installs the AI-agent entrypoints and shared rules used by supported tools:

```text
AGENTS.md
CLAUDE.md
GEMINI.md
.github/*
.cursor/*
.windsurf/*
.clinerules/*
.continue/*
.junie/*
.amazonq/*
CONVENTIONS.md
.aider.conf.yml
core/common/*
```

## 6. What ML Adds

ML installs the cross-domain machine-learning lifecycle contract:

```text
.github/instructions/ml.instructions.md
domains/ml/AGENT.md
domains/ml/SKILL.md
domains/ml/ENVIRONMENT.md
domains/ml/README.md
domains/ml/skills/*
```

Skills cover data validation, experiments, evaluation, generic training, distributed training, HPO, inference, and MLOps.

## 7. What LLM Adds

LLM installs:

```text
domains/llm/AGENT.md
domains/llm/SKILL.md
domains/llm/ENVIRONMENT.md
domains/llm/environment.py
domains/llm/memory_smoke_test.py
domains/llm/skills/*
```

LLM includes fine-tuning, PEFT, and quantization Skills in addition to its existing task Skills.

## 8. What Vision Adds

Vision installs:

```text
domains/vision/AGENT.md
domains/vision/SKILL.md
domains/vision/ENVIRONMENT.md
domains/vision/memory_smoke_test.py
domains/vision/skills/*
```

Vision Skills cover classification, detection, segmentation, OCR, pose estimation, image generation, and VLM.

## 9. What Colab Adds

Colab installs:

```text
platform/colab/AGENT.md
platform/colab/SKILL.md
```

The policy treats hosted notebook sessions as ephemeral and requires runtime detection, resource profiling, reproducible dependency bootstrap, durable checkpoints/artifacts, and resume validation for long-running work.

## 10. Validation After Installation

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

For LLM:

```bash
python domains/llm/memory_smoke_test.py --cpu --steps 2
```

For Vision:

```bash
python domains/vision/memory_smoke_test.py --device auto --image-size 224 --batch-size 1 --steps 2
```

For Colab, run the validation notebook under `tests/colab/` from a fresh runtime and verify checkpoint persistence/resume behavior.

## Language-specific documentation

See the language catalog in [`i18n/languages.json`](i18n/languages.json) and the localization guide in [`i18n/README.md`](i18n/README.md).

## Public distribution

Validated releases are promoted through `codingStandard-dev` to `AIEngineeringStandard`.
