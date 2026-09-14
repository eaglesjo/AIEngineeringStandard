# AI Engineering Standard — हिन्दी

<p align="center"><strong>AI विकास, मॉडल प्रशिक्षण और एजेंट इंजीनियरिंग के मानक</strong></p>

> यह पृष्ठ codingStandard के हिंदी दस्तावेज़ों का प्रवेश बिंदु है। हिंदी 20 रनटाइम लोकेल में से एक है और संसाधन की पूर्णता, अर्थगत समानता तथा रनटाइम और दस्तावेज़ों के बीच संगति की वही जाँच लागू होती है।

`codingStandard` AI-सहायित विकास, मॉडल प्रशिक्षण, प्रयोग, LLM/Vision वर्कफ़्लो, सामान्य ML/DL परियोजनाओं और AI कोडिंग एजेंटों के लिए पुन: उपयोग योग्य इंजीनियरिंग मानक है।

## त्वरित शुरुआत

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

उपलब्ध डोमेन `common`, `ml`, `llm`, `vision`, `colab` और `all` हैं। dry-run मोड से बदलावों का पहले से अवलोकन किया जा सकता है, जबकि conflict policies मौजूदा फ़ाइलों को संभालने का तरीका निर्धारित करती हैं।

## Google Colab

सार्वजनिक रिपॉज़िटरी में Google Colab नोटबुक उपलब्ध हैं, जिनसे पूरे मानक, clean runtime, LLM QLoRA और RAG वर्कफ़्लो का सत्यापन किया जा सकता है।

## बहुभाषी गुणवत्ता

दस्तावेज़ और रनटाइम संसाधन अलग-अलग प्रबंधित किए जाते हैं, लेकिन सभी 20 रनटाइम लोकेल पर समान गुणवत्ता मानदंड लागू होते हैं: संसाधन पूर्णता, नीति की अर्थगत समानता और रनटाइम तथा दस्तावेज़ों के बीच संगति।

विस्तृत इंस्टॉलेशन और सत्यापन प्रक्रिया के लिए [English README](../../README.md) और [INSTALL.md](../../INSTALL.md) देखें।
