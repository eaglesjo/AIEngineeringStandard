# AI Engineering Standard — Türkçe

<p align="center"><strong>Yapay zekâ geliştirme, eğitim ve ajan mühendisliği standartları</strong></p>

> Bu sayfa codingStandard belgelerinin Türkçe giriş noktasıdır. Türkçe, 20 çalışma zamanı yerelinden biridir ve kaynak bütünlüğü, anlamsal eşdeğerlik ve çalışma zamanı/belge tutarlılığı açısından aynı doğrulamalardan geçer.

`codingStandard`; yapay zekâ destekli geliştirme, model eğitimi, deneyler, LLM/Vision iş akışları, genel ML/DL projeleri ve yapay zekâ kodlama ajanları için yeniden kullanılabilir bir mühendislik standardıdır.

## Hızlı başlangıç

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Kullanılabilir alanlar `common`, `ml`, `llm`, `vision`, `colab` ve `all` seçenekleridir. Değişiklikleri önceden görmek için dry-run modunu, mevcut dosyaların nasıl ele alınacağını belirlemek için çakışma politikalarını kullanabilirsiniz.

## Google Colab

Herkese açık depo; standardın tamamını, temiz bir çalışma ortamını, LLM QLoRA ve RAG iş akışlarını doğrulamak için Google Colab not defterleri sağlar.

## Çok dilli kalite

Belgeler ve çalışma zamanı kaynakları ayrı yönetilir; ancak 20 çalışma zamanı yerelinin tamamına aynı kalite ölçütleri uygulanır: kaynak bütünlüğü, politika anlamsal eşdeğerliği ve çalışma zamanı ile belgeler arasındaki tutarlılık.

Ayrıntılı kurulum ve doğrulama adımları için [English README](../../README.md) ve [INSTALL.md](../../INSTALL.md) dosyalarına bakın.
