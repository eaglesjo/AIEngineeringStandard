# AI Engineering Standard — ไทย

<p align="center"><strong>มาตรฐานวิศวกรรมสำหรับการพัฒนา การฝึกโมเดล และเอเจนต์ AI</strong></p>

> หน้านี้เป็นจุดเริ่มต้นของเอกสาร codingStandard ภาษาไทย ภาษาไทยเป็นหนึ่งใน 20 โลคัลสำหรับรันไทม์ และผ่านการตรวจสอบมาตรฐานเดียวกันในด้านความครบถ้วนของทรัพยากร ความสอดคล้องเชิงความหมาย และความสอดคล้องระหว่างรันไทม์กับเอกสาร

`codingStandard` คือมาตรฐานวิศวกรรมที่นำกลับมาใช้ซ้ำได้สำหรับการพัฒนาที่มี AI ช่วย การฝึกโมเดล การทดลอง เวิร์กโฟลว์ LLM/Vision โครงการ ML/DL ทั่วไป และเอเจนต์สำหรับเขียนโค้ดด้วย AI

## เริ่มต้นอย่างรวดเร็ว

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

โดเมนที่ใช้งานได้ ได้แก่ `common`, `ml`, `llm`, `vision`, `colab` และ `all` สามารถใช้โหมด dry-run เพื่อดูการเปลี่ยนแปลงล่วงหน้า และใช้นโยบายการจัดการความขัดแย้งเพื่อกำหนดวิธีจัดการไฟล์ที่มีอยู่แล้ว

## Google Colab

ที่เก็บข้อมูลสาธารณะมีโน้ตบุ๊ก Google Colab สำหรับตรวจสอบมาตรฐานทั้งหมด clean runtime รวมถึงเวิร์กโฟลว์ LLM QLoRA และ RAG

## คุณภาพหลายภาษา

เอกสารและทรัพยากร runtime ได้รับการจัดการแยกกัน แต่ทั้ง 20 runtime locale ใช้เกณฑ์คุณภาพเดียวกัน ได้แก่ ความครบถ้วนของทรัพยากร ความสอดคล้องเชิงความหมายของนโยบาย และความสอดคล้องระหว่าง runtime กับเอกสาร

สำหรับขั้นตอนการติดตั้งและการตรวจสอบโดยละเอียด โปรดดู [README ภาษาอังกฤษ](../../README.md) และ [INSTALL.md](../../INSTALL.md)
