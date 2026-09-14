# AI Engineering Standard — ภาษาไทย

> **มาตรฐานวิศวกรรมสำหรับการพัฒนา การฝึกโมเดล และเอเจนต์ AI**
>
> **เวอร์ชัน:** v2.0.0 — ผู้สมัครเผยแพร่สู่สาธารณะ

**ภาษา:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · ไทย · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard คือมาตรฐานวิศวกรรมที่นำกลับมาใช้ซ้ำได้สำหรับการพัฒนาที่มี AI ช่วย การฝึกโมเดล การทดลอง เวิร์กโฟลว์ LLM/Vision เวิร์กโฟลว์ ML/DL ทั่วไป และเอเจนต์สำหรับเขียนโค้ดด้วย AI

## ไฮไลต์ของ 2.0.0

- สัญญาด้านสถาปัตยกรรมและนโยบายที่อ่านได้ด้วยเครื่อง พร้อมการกำหนดเส้นทาง Agent/Skill อย่างชัดเจน
- พฤติกรรมขณะรันที่อิงจากสภาพแวดล้อมและทรัพยากรที่ตรวจพบจริง
- วงจรชีวิตการติดตั้ง อัปเดต และถอนการติดตั้งอย่างปลอดภัยบนหลายแพลตฟอร์ม
- การตรวจสอบความครบถ้วนของทรัพยากร semantic parity และความสอดคล้องของเอกสารสำหรับ runtime locale ทั้ง 20 ภาษา
- การตรวจสอบคุณภาพโค้ด AI การประเมิน AI/LLM แหล่งที่มาของหลักฐาน และสัญญาด้าน reproducibility
- มาตรฐานการทำงานและการตรวจสอบสำหรับ ML, LLM, Vision และ Google Colab

## เริ่มต้นอย่างรวดเร็ว

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

โดเมนที่ใช้ได้: `common`, `ml`, `llm`, `vision`, `colab`, `all`

## การตรวจสอบ

```bash
python ./AIEngineeringStandard/scripts/validation/validate.py
python ./AIEngineeringStandard/scripts/installers/test_installers.py
```

ดู [`INSTALL.md`](../../INSTALL.md) สำหรับการติดตั้ง และ [`RELEASE.md`](../../docs/releases/RELEASE.md) สำหรับกระบวนการเผยแพร่
