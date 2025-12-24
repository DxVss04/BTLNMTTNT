🎮 AI Caro (Gomoku) – Python Project
📌 Giới thiệu

Dự án AI Caro (Gomoku) được xây dựng bằng Python, sử dụng Tkinter để tạo giao diện đồ họa và các thuật toán AI khác nhau để điều khiển máy chơi Caro.

Người chơi có thể:

Chơi Người vs Người (PVP)

Chơi Người vs Máy (PVE)

Chọn độ khó của AI: Dễ, Trung bình, Khó

Dự án tập trung vào việc phân tách rõ giao diện – logic – thuật toán AI, đúng chuẩn tổ chức phần mềm.

🧠 Các mức độ AI
Độ khó	Thuật toán
Easy	Chặn thắng + đánh ngẫu nhiên
Medium	Đánh giá điểm tấn công & phòng thủ
Hard	Minimax + Alpha-Beta Pruning
⚙️ Yêu cầu môi trường

Python 3.8+

Thư viện chuẩn:

tkinter

random

copy

❗ Không cần cài thêm thư viện ngoài (pip)

▶️ Cách chạy chương trình
Bước 1: Clone project
git clone https://github.com/<your-username>/PRJ_CARO.git
cd PRJ_CARO

Bước 2: Chạy chương trình
python main.py


➡ Giao diện Caro sẽ xuất hiện và có thể chơi ngay.

🧩 Mô tả các file chính
logic.py

Quản lý bàn cờ Caro

Kiểm tra thắng/thua

Lấy danh sách nước đi hợp lệ cho AI

Tách hoàn toàn khỏi giao diện

ui.py

Tạo giao diện Tkinter

Xử lý click chuột

Kết nối với AI và logic

Không chứa thuật toán AI

ai_easy.py

AI đơn giản

Ưu tiên chặn đối thủ thắng

Nếu không có nguy cơ → đánh ngẫu nhiên

ai_medium.py

AI đánh giá điểm

Kết hợp:

Tấn công

Phòng thủ

Ưu tiên trung tâm

ai_hard.py

AI mạnh nhất

Dùng:

Minimax

Alpha-Beta Pruning

Giới hạn độ sâu + lọc nước đi để tối ưu hiệu năng
