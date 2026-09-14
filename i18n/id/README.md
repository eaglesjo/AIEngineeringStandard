# AI Engineering Standard — Bahasa Indonesia

<p align="center"><strong>Standar rekayasa untuk pengembangan, pelatihan, dan agen AI</strong></p>

> Halaman ini adalah pintu masuk dokumentasi codingStandard dalam bahasa Indonesia. Bahasa Indonesia merupakan salah satu dari 20 lokal runtime dan menjalani pemeriksaan yang sama untuk kelengkapan sumber daya, kesepadanan semantik, serta konsistensi antara runtime dan dokumentasi.

`codingStandard` adalah standar rekayasa yang dapat digunakan kembali untuk pengembangan berbantuan AI, pelatihan model, eksperimen, alur kerja LLM/Vision, proyek ML/DL umum, dan agen pemrograman AI.

## Mulai cepat

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Domain yang tersedia adalah `common`, `ml`, `llm`, `vision`, `colab`, dan `all`. Mode dry-run memungkinkan Anda melihat perubahan terlebih dahulu, sedangkan kebijakan konflik menentukan cara menangani berkas yang sudah ada.

## Google Colab

Repositori publik menyediakan notebook Google Colab untuk memvalidasi standar secara menyeluruh, clean runtime, serta alur kerja LLM QLoRA dan RAG.

## Kualitas multibahasa

Dokumentasi dan sumber daya runtime dikelola secara terpisah, tetapi seluruh 20 lokal runtime mengikuti kriteria kualitas yang sama: kelengkapan sumber daya, kesepadanan semantik kebijakan, serta konsistensi antara runtime dan dokumentasi.

Untuk prosedur instalasi dan validasi selengkapnya, lihat [README bahasa Inggris](../../README.md) dan [INSTALL.md](../../INSTALL.md).
