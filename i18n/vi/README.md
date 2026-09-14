# AI Engineering Standard — Tiếng Việt

<p align="center"><strong>Tiêu chuẩn kỹ thuật cho phát triển, huấn luyện và tác nhân AI</strong></p>

> Đây là trang mở đầu cho tài liệu codingStandard bằng tiếng Việt. Tiếng Việt là một trong 20 locale runtime và được áp dụng cùng các kiểm tra về tính đầy đủ của tài nguyên, tính tương đương về ngữ nghĩa và tính nhất quán giữa runtime với tài liệu.

`codingStandard` là một tiêu chuẩn kỹ thuật có thể tái sử dụng cho phát triển có hỗ trợ AI, huấn luyện mô hình, thử nghiệm, quy trình LLM/Vision, các dự án ML/DL nói chung và tác nhân lập trình AI.

## Bắt đầu nhanh

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Các domain khả dụng gồm `common`, `ml`, `llm`, `vision`, `colab` và `all`. Có thể dùng chế độ dry-run để xem trước thay đổi và các chính sách xung đột để xác định cách xử lý các tệp đã tồn tại.

## Google Colab

Kho lưu trữ công khai cung cấp các notebook Google Colab để kiểm tra toàn bộ tiêu chuẩn, clean runtime, cũng như các quy trình LLM QLoRA và RAG.

## Chất lượng đa ngôn ngữ

Tài liệu và tài nguyên runtime được quản lý riêng, nhưng cả 20 locale runtime đều áp dụng cùng một bộ tiêu chí chất lượng: tính đầy đủ của tài nguyên, tính tương đương về ngữ nghĩa của chính sách và tính nhất quán giữa runtime với tài liệu.

Để xem hướng dẫn cài đặt và xác thực chi tiết, hãy tham khảo [README tiếng Anh](../../README.md) và [INSTALL.md](../../INSTALL.md).
