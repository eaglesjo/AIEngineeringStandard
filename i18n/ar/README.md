# AI Engineering Standard — العربية

> **معايير هندسة تطوير الذكاء الاصطناعي وتدريب النماذج والوكلاء**
>
> **الإصدار:** v2.0.0 — مرشح إصدار عام

**اللغات:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · العربية · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard هو معيار هندسي قابل لإعادة الاستخدام لتطوير البرمجيات بمساعدة الذكاء الاصطناعي، وتدريب النماذج، والتجارب، وسير عمل LLM/Vision، وسير عمل ML/DL العامة، ووكلاء البرمجة بالذكاء الاصطناعي.

## أبرز ما جاء في 2.0.0

- عقود معمارية وسياسات قابلة للقراءة آليًا مع توجيه واضح للوكلاء والمهارات.
- سلوك تشغيل يعتمد على البيئة المكتشفة والموارد المتاحة فعليًا.
- دورة حياة متعددة المنصات للتثبيت والتحديث والإزالة الآمنة.
- التحقق من اكتمال الموارد والتكافؤ الدلالي واتساق الوثائق عبر 20 لغة تشغيل.
- التحقق من جودة كود الذكاء الاصطناعي، وتقييم AI/LLM، وتتبع مصدر الأدلة، وعقود قابلية إعادة الإنتاج.
- معايير تنفيذ والتحقق لـ ML وLLM وVision وGoogle Colab.

## البدء السريع

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

النطاقات المتاحة: `common` و`ml` و`llm` و`vision` و`colab` و`all`.

## التحقق

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

للتثبيت راجع [`INSTALL.md`](../../INSTALL.md)، ولعملية الإصدار راجع [`RELEASE.md`](../../docs/releases/RELEASE.md).
