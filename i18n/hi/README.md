# AI Engineering Standard — हिन्दी

> **AI विकास, मॉडल प्रशिक्षण और एजेंट इंजीनियरिंग के मानक**
>
> **संस्करण:** v2.0.0 — सार्वजनिक रिलीज़ उम्मीदवार

**भाषाएँ:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · हिन्दी · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard AI-सहायित विकास, मॉडल प्रशिक्षण, प्रयोग, LLM/Vision वर्कफ़्लो, सामान्य ML/DL वर्कफ़्लो और AI कोडिंग एजेंटों के लिए पुन: उपयोग योग्य इंजीनियरिंग मानक है।

## 2.0.0 की प्रमुख बातें

- मशीन-पठनीय आर्किटेक्चर और नीति अनुबंध तथा स्पष्ट Agent/Skill रूटिंग।
- वास्तविक रूप से पहचाने गए वातावरण और उपलब्ध संसाधनों के आधार पर रनटाइम व्यवहार।
- विभिन्न प्लेटफ़ॉर्म पर इंस्टॉलेशन, अपडेट और सुरक्षित अनइंस्टॉल का जीवनचक्र।
- 20 runtime locale के लिए संसाधन पूर्णता, semantic parity और दस्तावेज़ संगति की जाँच।
- AI कोड गुणवत्ता सत्यापन, AI/LLM मूल्यांकन, evidence provenance और reproducibility अनुबंध।
- ML, LLM, Vision और Google Colab के लिए निष्पादन तथा सत्यापन मानक।

## त्वरित शुरुआत

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

उपलब्ध डोमेन: `common`, `ml`, `llm`, `vision`, `colab`, `all`।

## सत्यापन

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

इंस्टॉलेशन के लिए [`INSTALL.md`](../../INSTALL.md) और रिलीज़ प्रक्रिया के लिए [`RELEASE.md`](../../docs/releases/RELEASE.md) देखें।
