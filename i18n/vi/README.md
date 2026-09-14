# AI Engineering Standard — Tiếng Việt

> **Tiêu chuẩn kỹ thuật cho phát triển, huấn luyện và tác nhân AI**
>
> **Phiên bản:** v2.0.0 — Ứng viên phát hành công khai

**Ngôn ngữ:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · Tiếng Việt · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard là bộ tiêu chuẩn kỹ thuật có thể tái sử dụng cho phát triển có AI hỗ trợ, huấn luyện mô hình, thử nghiệm, quy trình LLM/Vision, ML/DL nói chung và tác nhân lập trình AI.

## Điểm nổi bật của 2.0.0

- Hợp đồng kiến trúc và chính sách dạng máy đọc được, cùng cơ chế định tuyến Agent/Skill rõ ràng.
- Hành vi runtime dựa trên môi trường được phát hiện và tài nguyên thực tế.
- Vòng đời cài đặt, cập nhật và gỡ cài đặt an toàn trên nhiều nền tảng.
- Kiểm tra tính đầy đủ tài nguyên, tính tương đương ngữ nghĩa và tính nhất quán tài liệu cho 20 runtime locale.
- Xác minh chất lượng mã AI, đánh giá AI/LLM, provenance của bằng chứng và hợp đồng tái lập kết quả.
- Tiêu chuẩn thực thi và kiểm định cho ML, LLM, Vision và Google Colab.

## Bắt đầu nhanh

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Các domain khả dụng: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Kiểm định

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

Xem [`INSTALL.md`](../../INSTALL.md) để biết cách cài đặt và [`RELEASE.md`](../../docs/releases/RELEASE.md) để biết quy trình phát hành.
