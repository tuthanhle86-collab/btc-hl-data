"""Bộ ghi dữ liệu BTC Hyperliquid chạy trên GitHub Actions (mỗi lượt ~5h45m).
- Ghi mọi giao dịch BTC qua websocket, gộp theo ví mỗi 15 phút -> data/flow/YYYYMMDD.jsonl.gz
- Mỗi 15 phút: làm mới ~600 ví lớn nhất, chụp bản đồ thanh lý (khoảng 250 USD, ±10% giá) -> data/liqsnap/YYYYMMDD.jsonl
- Mỗi 2 giờ: quét lại toàn bộ danh sách ví (top 5,000 bảng xếp hạng + ví đã thấy giao dịch BTC) -> data/positions.json.gz
- Mỗi 15 phút ghi data/status.json và commit (amend, force push) lên nhánh data để kho không phình.
"""
import json, gzip, os, time, threading, subprocess, urllib.request, datetime as dt
from collections import defaultdict
import websocket

RUN_SECONDS = float(os.environ.get("RUN_SECONDS", 5.75 * 3600))
D = "data"; os.makedirs(D + "/flow", exist_ok=True); os.makedirs(D + "/liqsnap", exist_ok=True)
API = "https://api.hyperliquid.xyz/info"
lock = threading.Lock()
T0 = time.time()

def post(body, tries=6):
    for i in range(tries):
        try:
            r = urllib.request.Request(API, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(r, timeout=20) as x: return json.load(x)
        except Exception: time.sleep(2 * (i + 1))
    return None

def utc(ts=None): return dt.datetime.fromtimestamp(ts or time.time(), dt.timezone.utc)
def day(ts=None): return utc(ts).strftime("%Y%m%d")

# ---------- state ----------
positions = {}   # wallet -> dict
known = set()    # wallets seen trading BTC or holding BTC
try:
    with gzip.open(D + "/positions.json.gz", "rt") as f:
        old = json.load(f); positions = {p["vi"]: p for p in old.get("positions", [])}; known = set(old.get("known", []))
except Exception: pass
flow = defaultdict(lambda: [0.0, 0.0, 0])  # wallet -> [buy_usd, sell_usd, n]
ntrades = [0]

# ---------- websocket ----------
def ws_loop():
    while time.time() - T0 < RUN_SECONDS:
        try:
            ws = websocket.create_connection("wss://api.hyperliquid.xyz/ws", timeout=60)
            ws.send(json.dumps({"method": "subscribe", "subscription": {"type": "trades", "coin": "BTC"}}))
            last_ping = time.time()
            while time.time() - T0 < RUN_SECONDS:
                if time.time() - last_ping > 40:
                    ws.send(json.dumps({"method": "ping"})); last_ping = time.time()
                m = json.loads(ws.recv())
                if m.get("channel") != "trades": continue
                with lock:
                    for t in m["data"]:
                        u = float(t["sz"]) * float(t["px"]); b, s = [x.lower() for x in t["users"]]
                        flow[b][0] += u; flow[b][2] += 1; flow[s][1] += u; flow[s][2] += 1
                        known.add(b); known.add(s); ntrades[0] += 1
        except Exception:
            time.sleep(3)

# ---------- scanning ----------
def scan(wallets, rate=8):
    out = {}
    for a in wallets:
        t = time.time()
        d = post({"type": "clearinghouseState", "user": a})
        if d is not None:
            p = None
            for ap in d.get("assetPositions", []):
                q = ap["position"]
                if q["coin"] == "BTC":
                    p = {"vi": a, "szi": float(q["szi"]), "val": float(q["positionValue"]), "entry": float(q["entryPx"]),
                         "liq": float(q["liquidationPx"]) if q.get("liquidationPx") else None,
                         "lev": q["leverage"]["value"], "upnl": float(q["unrealizedPnl"]), "t": int(time.time())}
            out[a] = p
        dl = 1 / rate - (time.time() - t)
        if dl > 0: time.sleep(dl)
    with lock:
        for a, p in out.items():
            if p: positions[a] = p; known.add(a)
            else: positions.pop(a, None)

def leaderboard():
    try:
        with urllib.request.urlopen("https://stats-data.hyperliquid.xyz/Mainnet/leaderboard", timeout=120) as x:
            rows = json.load(x)["leaderboardRows"]
        rows.sort(key=lambda r: -float(r.get("accountValue", 0)))
        return [r["ethAddress"].lower() for r in rows[:5000]]
    except Exception:
        return []

def full_scan():
    lst = list(dict.fromkeys(leaderboard() + sorted(known)))
    scan(lst, rate=8)

def mark_price():
    m, c = post({"type": "metaAndAssetCtxs"})
    i = [x["name"] for x in m["universe"]].index("BTC")
    return float(c[i]["markPx"]), float(c[i]["openInterest"]) * float(c[i]["markPx"])

# ---------- writers ----------
def write_snapshot():
    price, oi = mark_price()
    with lock:
        P = list(positions.values())
        fl = dict(flow); flow.clear(); nt = ntrades[0]; ntrades[0] = 0
    now = time.time(); t15 = int(now // 900 * 900)
    lq = defaultdict(lambda: [0.0, 0.0])
    for p in P:
        if p["liq"] and price * 0.9 < p["liq"] < price * 1.1:
            lq[int(p["liq"] // 250 * 250)][0 if p["szi"] > 0 else 1] += p["val"]
    L = sum(p["val"] for p in P if p["szi"] > 0); S = sum(p["val"] for p in P if p["szi"] < 0)
    snap = {"t": t15, "price": price, "oi": round(oi), "long": round(L), "short": round(S), "n": len(P),
            "liq": {str(b): [round(v[0]), round(v[1])] for b, v in sorted(lq.items())}}
    with open(f"{D}/liqsnap/{day(now)}.jsonl", "a") as f: f.write(json.dumps(snap) + "\n")
    # flow: one line per 15 min, wallet -> [buy, sell, n] (only wallets with >= 1,000 USD)
    rec = {"t": t15, "trades": nt, "w": {a: [round(v[0]), round(v[1]), v[2]] for a, v in fl.items() if v[0] + v[1] >= 1000},
           "pos": {a: (round(positions[a]["szi"], 5) if a in positions else 0) for a in fl if fl[a][0] + fl[a][1] >= 1000}}
    with gzip.open(f"{D}/flow/{day(now)}.jsonl.gz", "at") as f: f.write(json.dumps(rec) + "\n")
    with gzip.open(D + "/positions.json.gz", "wt") as f:
        json.dump({"t": int(now), "positions": P, "known": sorted(known)}, f)
    json.dump({"updated": utc(now).isoformat(), "price": price, "oi_usd": round(oi), "positions": len(P),
               "long_usd": round(L), "short_usd": round(S), "coverage_pct": round((L + S) / oi * 100, 1),
               "known_wallets": len(known), "trades_last_15m": nt}, open(D + "/status.json", "w"), indent=1)
    # keep 8 days
    cutoff = day(now - 8 * 86400)
    for sub in ["flow", "liqsnap"]:
        for fn in os.listdir(f"{D}/{sub}"):
            if fn[:8] < cutoff: os.remove(f"{D}/{sub}/{fn}")

def commit():
    subprocess.run(["git", "add", "-A", D], check=False)
    subprocess.run(["git", "commit", "-q", "--amend", "-m", "data snapshot"], check=False)
    subprocess.run(["git", "push", "-q", "-f", "origin", "HEAD:data"], check=False)

# ---------- main ----------
threading.Thread(target=ws_loop, daemon=True).start()
if not positions: full_scan()
last_full = time.time() if positions else 0
while time.time() - T0 < RUN_SECONDS - 120:
    nxt = (time.time() // 900 + 1) * 900
    if time.time() - last_full > 2 * 3600:
        full_scan(); last_full = time.time()
    else:
        top = sorted(positions.values(), key=lambda p: -p["val"])[:600]
        with lock: recent = [a for a, v in flow.items() if v[0] + v[1] >= 20000]
        scan(list(dict.fromkeys([p["vi"] for p in top] + recent)), rate=8)
    time.sleep(max(0, nxt - time.time()))
    try: write_snapshot(); commit()
    except Exception as e: print("snapshot error", e, flush=True)
write_snapshot(); commit()
