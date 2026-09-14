# AI Engineering Standard — Türkçe

> **Yapay zekâ geliştirme, eğitim ve ajan mühendisliği standartları**
>
> **Sürüm:** v2.0.0 — Genel yayın adayı

**Diller:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · Türkçe · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard; yapay zekâ destekli geliştirme, model eğitimi, deneyler, LLM/Vision iş akışları, genel ML/DL süreçleri ve AI kodlama ajanları için yeniden kullanılabilir bir mühendislik standardıdır.

## 2.0.0 öne çıkanlar

- Makine tarafından okunabilir mimari ve politika sözleşmeleri ile açık Agent/Skill yönlendirmesi.
- Gerçekte algılanan ortam ve kaynaklara dayalı çalışma politikaları.
- Platformlar arası kurulum, güncelleme ve güvenli kaldırma yaşam döngüsü.
- 20 runtime locale için kaynak bütünlüğü, anlamsal eşdeğerlik ve dokümantasyon tutarlılığı doğrulaması.
- AI kod kalitesi doğrulaması, AI/LLM değerlendirmesi, kanıtların kökeni ve izlenebilirliği ile yeniden üretilebilirlik sözleşmeleri.
- ML, LLM, Vision ve Google Colab için çalıştırma ve doğrulama standartları.

## Hızlı başlangıç

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Kullanılabilir alanlar: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Doğrulama

```bash
python ./AIEngineeringStandard/scripts/validation/validate.py
python ./AIEngineeringStandard/scripts/installers/test_installers.py
```

Kurulum ayrıntıları için [`INSTALL.md`](../../INSTALL.md), yayın süreci için [`RELEASE.md`](../../docs/releases/RELEASE.md) dosyasına bakın.
