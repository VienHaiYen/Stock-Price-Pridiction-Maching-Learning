# [Đồ án nhóm cuối kì ứng dụng Machine Learning]

## Nhóm sinh viên:

- Nhóm: 3
- Thành viên: 
    - 20120383 - Nguyễn Đức Tiến
    - 20120447 - Trịnh Quốc Cường
    - 20120633 - Viên Hải Yến
    - 20120634 - Lê Minh Trí
- Link github: https://github.com/VienHaiYen/Stock-Price-Pridiction-Maching-Learning
- Video demo: https://www.youtube.com/watch?v=ImtZThBnUyg&feature=youtu.be

## Yêu cầu:

Xây dựng trang DashBoard phân tích trading theo các tiêu chí sau
1) Người dùng chọn một trong các phương pháp dự đoán :
a. XGBoost, RNN, LSTM (bắt buộc) hoặc các phương pháp khác.
2) Người dùng chọn một hay nhiều đặc trưng để dự đoán :
a. Close, ROC (bắt buộc)
3) Hiển thị giá dự đoán của timeframe kế tiếp (visualize)
4) Lấy dữ liệu Real-time từ websocket của Binance, chứng khoán,...
a. Lấy dữ liệu lớn hơn 1000 nến(candle) từ lịch sử
b. Lấy dữ liệu real-time append vô dữ liệu hiện tại
c. Dự đoán giá nến(candle) kế tiếp

## Cách cài đặt

**Tải packages**
`pip install -r requirements.txt`

- **Chạy dashboard**
`python app.py`

- **Build lại models**
`python build_model.py`

**Truy cập htpp://localhost:8050 trên browser**