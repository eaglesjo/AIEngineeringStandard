# AI Engineering Standard — العربية

<p align="center"><strong>معايير هندسة تطوير الذكاء الاصطناعي وتدريب النماذج ووكلاء البرمجة</strong></p>

> هذه الصفحة هي نقطة الدخول العربية إلى وثائق codingStandard. تُعد العربية واحدة من 20 لغة تشغيل، وتخضع للضوابط نفسها للتحقق من اكتمال الموارد والتكافؤ الدلالي والاتساق بين بيئة التشغيل والتوثيق.

`codingStandard` هو معيار هندسي قابل لإعادة الاستخدام للتطوير بمساعدة الذكاء الاصطناعي، وتدريب النماذج، والتجارب، وسير عمل LLM/Vision، ومشروعات ML/DL العامة، ووكلاء البرمجة بالذكاء الاصطناعي.

## البدء السريع

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

المجالات المتاحة هي `common` و`ml` و`llm` و`vision` و`colab` و`all`. يتيح وضع dry-run معاينة التغييرات قبل تطبيقها، بينما تحدد سياسات التعارض كيفية التعامل مع الملفات الموجودة مسبقًا.

## Google Colab

يوفر المستودع العام دفاتر Google Colab للتحقق من المعيار بالكامل، وبيئة تشغيل نظيفة، ومسارات عمل LLM QLoRA وRAG.

## جودة الترجمة متعددة اللغات

تُدار الوثائق وموارد التشغيل بشكل منفصل، لكن اللغات التشغيلية العشرين تخضع لمعايير الجودة نفسها: اكتمال الموارد، والتكافؤ الدلالي للسياسات، والاتساق بين بيئة التشغيل والتوثيق.

للاطلاع على إجراءات التثبيت والتحقق بالتفصيل، راجع [README بالإنجليزية](../../README.md) و[INSTALL.md](../../INSTALL.md).
