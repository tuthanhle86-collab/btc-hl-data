import json,glob,urllib.request,math,statistics as st
snaps=[]
for f in sorted(glob.glob('/home/claude/hldata/data/liqsnap/*.jsonl')):
    for l in open(f): snaps.append(json.loads(l))
snaps.sort(key=lambda r:r['t'])
t0=snaps[0]['t']*1000; t1=snaps[-1]['t']*1000
K=[]; s=t0-30*86400000
while s<t1+86400000:
    d=json.load(urllib.request.urlopen(f"https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=15m&startTime={s}&limit=1000"))
    if not d: break
    K+=d; s=d[-1][0]+900000
T=[k[0] for k in K]; H=[float(k[2]) for k in K]; L=[float(k[3]) for k in K]; C=[float(k[4]) for k in K]
idx={t:i for i,t in enumerate(T)}
# ATR 1H xấp xỉ từ 15m: TR 15m * 2 trung bình 56 nến
def atr1h(i):
    tr=[max(H[j]-L[j],abs(H[j]-C[j-1]),abs(L[j]-C[j-1])) for j in range(i-55,i+1)]
    return st.mean(tr)*2
res={}
for side in (1,-1):
  for mult in (1.0,1.5):
    for r in snaps[::16]:   # mỗi 4 giờ
        tm=r['t']*1000//900000*900000
        if tm not in idx: continue
        i=idx[tm]
        if i+97>=len(C) or i<60: continue
        e=C[i]; A=atr1h(i); R=mult*A; sl=e-side*R; tp=e+side*R
        # cụm cùng phía (long nếu side=1) ≥10M nằm giữa giá vào và SL, hoặc trong 0.3 ATR sau SL? -> 'trước SL' = giữa giá vào và SL
        cl=0
        for b,(lv,sv) in r['liq'].items():
            b=int(b); v=lv if side==1 else sv
            lo,hi=(sl,e) if side==1 else (e,sl)
            if v>=1e7 and lo<=b+125<=hi: cl+=v
        grp='có cụm ≥10M trước SL' if cl>0 else 'không cụm'
        out=None
        for j in range(i+1,i+97):
            if (L[j]<=sl if side==1 else H[j]>=sl): out='SL';break
            if (H[j]>=tp if side==1 else L[j]<=tp): out='TP';break
        res.setdefault((side,mult,grp),[]).append(out)
for k,v in sorted(res.items()):
    n=len(v); sl=sum(x=='SL' for x in v); tp=sum(x=='TP' for x in v)
    print(('LONG' if k[0]==1 else 'SHORT'),f"SL {k[1]} ATR", k[2], 'n',n,'chạm SL',f"{sl/n:.0%}",'chạm TP',f"{tp/n:.0%}")
print('số ảnh',len(snaps),'từ',snaps[0]['t'],'đến',snaps[-1]['t'])
