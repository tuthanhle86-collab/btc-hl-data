# Kiểm định nhận định và lệnh hệ C, 12/11–17/11/2026 (theo yêu cầu người dùng lúc 09:04 ngày 17/11)

## 1. Chiều nhận định so với giá thật (Binance 15m)
| Lúc | Lệnh | Giá | +4h | +12h | +24h (USD theo chiều) | MFE 24h (ATR) | MAE 24h (ATR) |
|---|---|---|---|---|---|---|---|
| 12/11 10:20 | C1 short giới hạn | 73,844 | +235 | +2,358 | +4,457 | 11.4 | 0.1 |
| 12/11 21:30 | C2 short ngay | 71,862 | −126 | +1,340 | +2,690 | 10.0 | 1.0 |
| 13/11 11:46 | C3 short giới hạn | 68,581 | −136 | −113 | +1,493 | 3.5 | 2.7 |
| 13/11 14:19 | C4 short giới hạn | 68,995 | −281 | −50 | +1,741 | 4.2 | 2.0 |
| 14/11 21:30 | C5 short ngay | 66,268 | +338 | +1,768 | +1,367 | 8.2 | 0.2 |
| 15/11 18:45 | C6 long ngay | 65,514 | −813 | −185 | −915 | 0.4 | 1.7 |
| 15/11 23:35 | C7 short giới hạn | 64,744 | −294 | −126 | +117 | 1.1 | 1.2 |
| 16/11 09:40 | nhắc C7 | 65,150 | +554 | −142 | — | 2.1 | 0.9 |
| 16/11 13:54 | nhắc C7 | 64,710 | +135 | −342 | — | 1.3 | 1.6 |
| 16/11 22:03 | nhắc C7 | ~64,400 | −493 | — | — | 0.4 | 2.0 |
Đúng chiều sau 24 giờ 6/7; sau 12 giờ 3/9. Từ 15/11 (thị trường đi ngang): 0/6 đúng sau 12 giờ.

## 2. Kết quả lệnh thật: 4 đóng (+0.93, +0.91, −1.08, −0.13 = +0.63R), 3 hủy (C1, C3, C4).
- C1, C3, C4 hủy vì chạm TP trước khi khớp, cả ba đúng chiều; MFE 3.5–11.4 ATR bị bỏ lỡ.
- C2, C5 thắng 1R trong khi MFE 8–10 ATR → TP cố định 1R cắt mất phần lớn nhịp.
- C6 (Trung tính, long theo 1H) thua; C7 short trong biên ngang đóng theo giờ.

## 3. Kiểm định 3 năm các cách vào/ra (hệ C, 5,605 tín hiệu, phí 0.1%)
| Vào | Ra | Kỳ vọng mỗi tín hiệu | Hai nửa |
|---|---|---|---|
| Vào ngay | TP 1R | −0.147R | −0.115 / −0.179 |
| Vào ngay | TP 1.5R | −0.146R | −0.111 / −0.181 |
| Vào ngay | chốt nửa 1R + kéo dừng 2 ATR, tối đa 72h | −0.140R | −0.103 / −0.177 |
| Giới hạn +0.5 ATR | TP 1R | −0.070R | −0.037 / −0.104 |
| Giới hạn +0.5 ATR | TP 1.5R | −0.060R | −0.011 / −0.108 |
| Giới hạn +0.5 ATR | chốt nửa 1R + kéo dừng | −0.054R | −0.010 / −0.098 |
Không cách nào dương. Kéo dừng tốt nhất nhưng chỉ hơn TP 1R ~0.016R.

## 4. Kết luận
- Người dùng đúng: phân tích đã thu hẹp thành chạy một luật EMA cơ học; điểm vào (giới hạn + hủy khi chạm TP trước) bỏ lỡ 3 nhịp lớn; TP 1R cắt lời; sau khi xu hướng dừng (15/11) luật vẫn short trong biên → nhận định 12 giờ 0/6.
- Gốc vấn đề: hệ C là luật cơ học bắt buộc 1 lệnh/ngày, kiểm định 3 năm âm ở mọi biến thể. Không thể sửa bằng tinh chỉnh vào/ra.
- Chưa có dữ liệu để so với lệnh cảm tính.
