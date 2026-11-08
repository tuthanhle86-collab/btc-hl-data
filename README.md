# btc-hl-data
Dữ liệu BTC Hyperliquid ghi liên tục cho Project "Chuyên gia phân tích thị trường opus 5.5".

- Nhánh `main`: mã (`collector.py`, `.github/workflows/collector.yml`).
- Nhánh `data`: dữ liệu (ghi đè mỗi 15 phút, giữ 8 ngày):
  - `data/status.json` — tóm tắt lần ghi gần nhất.
  - `data/liqsnap/YYYYMMDD.jsonl` — bản đồ thanh lý 15 phút/lần (khoảng 250 USD, ±10% giá; [long, short] USD).
  - `data/flow/YYYYMMDD.jsonl.gz` — mua/bán của từng ví mỗi 15 phút, kèm vị thế lúc ghi.
  - `data/positions.json.gz` — toàn bộ vị thế BTC đã quét.
- Mỗi lượt chạy ~5h45m rồi tự khởi động lượt sau; lịch 6 giờ/lần là dự phòng.
- Tắt: tab **Actions** → **btc-hl-collector** → **⋯** → **Disable workflow**.
