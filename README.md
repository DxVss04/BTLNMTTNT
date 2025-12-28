# 🎮 Dự Án: Cờ Caro AI (Gomoku) - Python & Tkinter

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 📌 Giới Thiệu

Chào mừng bạn đến với dự án **Cờ Caro AI (Gomoku)**! Đây là một trò chơi trí tuệ kinh điển với bàn cờ 15x15 ô, được xây dựng hoàn toàn bằng ngôn ngữ lập trình **Python** và thư viện giao diện chuẩn **Tkinter**.

Dự án này được thiết kế để:
* Phục vụ người mới bắt đầu học Python và AI cơ bản.
* Minh họa cách áp dụng thuật toán **Minimax** và **Alpha-Beta Pruning** trong game.
* Cung cấp mã nguồn mở, sạch sẽ và dễ dàng mở rộng.



## ✨ Tính Năng Chính

### 👥 Chế Độ Chơi Đa Dạng
* **Người vs Người (PVP):** Hai người chơi thay phiên nhau đánh trên cùng một máy tính.
* **Người vs Máy (PVE):** Bạn (quân X, đi trước) thử sức với AI (quân O).
* **Máy vs Máy (EVE):** Quan sát hai AI tự đấu với nhau (rất thú vị để học chiến thuật).

### 🧠 Trí Tuệ Nhân Tạo (AI) - 3 Cấp Độ
Hệ thống AI được chia làm 3 mức độ khó để phù hợp với mọi trình độ:

1.  **Dễ (Easy):**
    * Logic đơn giản.
    * Ưu tiên thắng ngay nếu có cơ hội, hoặc chặn đối thủ.
    * Nếu không có nguy cơ, đánh ngẫu nhiên gần các quân đã có.
2.  **Trung bình (Medium):**
    * Sử dụng hàm đánh giá (Heuristic).
    * Tính điểm dựa trên thế cờ (số quân liên tiếp, đầu mở).
    * Cân bằng giữa tấn công và phòng thủ.
3.  **Khó (Hard):**
    * Sử dụng thuật toán **Minimax** kết hợp **Cắt tỉa Alpha-Beta** (Depth = 3).
    * Tối ưu hóa ứng viên (Candidate selection): Chỉ xét các ô có liên quan để tăng tốc độ.
    * Thời gian suy nghĩ: ~1-2 giây/nước đi trên CPU thường.



### 🖥️ Giao Diện & Tiện Ích
* **Giao diện Tkinter:** Bàn cờ lưới trực quan, vẽ X/O rõ nét.
* **Thông báo trạng thái:** Tự động kiểm tra Thắng/Thua/Hòa sau mỗi nước đi.
* **Mượt mà:** Xử lý đa luồng hoặc delay hợp lý giúp game không bị giật (Not Responding) khi AI suy nghĩ.

## ⚙️ Yêu Cầu Hệ Thống

Dự án được thiết kế để chạy "ngay và luôn", không cần cài đặt phức tạp.

* **Hệ điều hành:** Windows, MacOS, Linux.
* **Python:** Phiên bản 3.6 trở lên (Khuyến nghị 3.8+).
* **Thư viện:** Chỉ sử dụng thư viện chuẩn (Standard Libraries):
    * `tkinter` (Giao diện)
    * `random` (Xử lý ngẫu nhiên)
    * `copy` (Sao chép trạng thái bàn cờ)

## 🗂️ Cấu Trúc Thư Mục

```text
caro-ai/
├── main.py          # File chính (Entry point): Kết nối UI và Logic
├── ui.py            # Giao diện: Vẽ bàn cờ, xử lý sự kiện chuột, nút bấm
├── logic.py         # Logic game: Check thắng thua, quản lý lượt đi
├── ai_easy.py       # Thuật toán AI cấp độ Dễ
├── ai_medium.py     # Thuật toán AI cấp độ Trung bình
├── ai_hard.py       # Thuật toán AI cấp độ Khó (Minimax core)
└── README.md        # Tài liệu hướng dẫn
