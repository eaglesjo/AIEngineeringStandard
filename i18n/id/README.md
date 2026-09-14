# AI Engineering Standard — Bahasa Indonesia

> **Standar rekayasa untuk pengembangan, pelatihan, dan agen AI**
>
> **Versi:** v2.0.0 — Kandidat rilis publik

**Bahasa:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · Bahasa Indonesia · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard adalah standar rekayasa yang dapat digunakan kembali untuk pengembangan berbantuan AI, pelatihan model, eksperimen, alur kerja LLM/Vision, ML/DL umum, dan agen coding AI.

## Sorotan 2.0.0

- Kontrak arsitektur dan kebijakan yang dapat dibaca mesin, dengan routing Agent/Skill yang eksplisit.
- Perilaku runtime berdasarkan lingkungan yang terdeteksi dan sumber daya yang benar-benar tersedia.
- Siklus hidup instalasi, pembaruan, dan penghapusan aman lintas platform.
- Validasi kelengkapan sumber daya, paritas semantik, dan konsistensi dokumentasi untuk 20 runtime locale.
- Verifikasi kualitas kode AI, evaluasi AI/LLM, provenance bukti, dan kontrak reproduktibilitas.
- Standar eksekusi dan validasi untuk ML, LLM, Vision, dan Google Colab.

## Mulai cepat

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Domain yang tersedia: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Validasi

```bash
python ./AIEngineeringStandard/scripts/validation/validate.py
python ./AIEngineeringStandard/scripts/installers/test_installers.py
```

Lihat [`INSTALL.md`](../../INSTALL.md) untuk instalasi dan [`RELEASE.md`](../../docs/releases/RELEASE.md) untuk proses rilis.
