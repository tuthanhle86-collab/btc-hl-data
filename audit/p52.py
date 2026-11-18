exec(open('p27.py').read().split('def sim(')[0])
# Hệ C: chiều theo 1H/4H (hòa -> 1H); lệnh giới hạn giá ± 0.5 ATR; hủy nếu chạm TP (1R tạm = 1 ATR) trước khi khớp; chờ 24h; giữ 24h; phí 0.1%
def run(i):
    kh=T[i]//3600000-1; k4h=T[i]//14400000-1
    if kh not in i1 or k4h not in i4: return None
    j1=i1[kh]; j4=i4[k4h]; a=atr[j1]
    up1=c1[j1]>e1[j1]; up4=c4[j4]>e4[j4]
    d=1 if up1 else -1  # long=1 (hòa theo 1H; đồng thuận cũng = 1H)
    p=C[i]; lim=p-d*0.5*a
    f=None
    for j in range(i+1,min(n,i+97)):
        if (H[j]>=lim+d*a if d==1 else L[j]<=lim+d*a) and f is None and ((d==1 and L[j]>lim) or (d==-1 and H[j]<lim)): return None  # TP chạm trước
        if L[j]<=lim<=H[j]: f=j;break
    if f is None: return None
    # SL: max(1 ATR, swing 15m gần nhất ± 0.1 ATR)
    ext=None
    for j in range(f-2,f-16,-1):
        if d==1 and L[j]<=min(L[j-2:j+3]) and L[j]<lim: ext=L[j];break
        if d==-1 and H[j]>=max(H[j-2:j+3]) and H[j]>lim: ext=H[j];break
    R=a if ext is None else max(a,abs(lim-(ext-d*0.1*a)))
    sl=lim-d*R; tp=lim+d*R; fee=0.001*lim/R
    for j in range(f,min(n,f+96)):
        if (L[j]<=sl if d==1 else H[j]>=sl): r=-1-fee;break
        if (H[j]>=tp if d==1 else L[j]<=tp): r=1-fee;break
    else:
        r=d*(C[min(n-1,f+96)]-lim)/R-fee
    rel=(lim-e1[j1])/a  # vị trí giá vào so với EMA20 1H (đơn vị ATR)
    return d,rel,r
res=[]; last=-99
for i in range(400,n-200):
    if i-last<16: continue
    x=run(i)
    if x: res.append(x); last=i
import statistics as st,math
def rep(name,xs):
    if not xs: print(name,0);return
    m=st.mean(xs); se=st.pstdev(xs)/math.sqrt(len(xs)); print(f"{name}: n {len(xs)} TB {m:+.3f}R ±{se:.3f}")
rep('Tất cả',[r for d,rel,r in res])
for d,nm in ((-1,'SHORT'),(1,'LONG')):
    rep(nm+' vào TRÊN EMA20 1H',[r for dd,rel,r in res if dd==d and rel>0])
    rep(nm+' vào DƯỚI EMA20 1H',[r for dd,rel,r in res if dd==d and rel<=0])
    rep(nm+' sát EMA (|lệch|<0.2 ATR)',[r for dd,rel,r in res if dd==d and abs(rel)<0.2])
