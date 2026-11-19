exec(open('p27.py').read().split('def sim(')[0])
import statistics as st, math
# ngày
hd={}
for i in range(n): hd.setdefault(T[i]//86400000,[]).append(i)
kd=sorted(hd); cd=[C[hd[k][-1]] for k in kd]; ed=ema(cd,20); idd={k:i for i,k in enumerate(kd)}
hi4={};lo4={}
for k in k4: idx=h4[k]; hi4[k]=max(H[j] for j in idx); lo4[k]=min(L[j] for j in idx)
tr4=[];prev=None
for k in k4:
    tr4.append(hi4[k]-lo4[k] if prev is None else max(hi4[k]-lo4[k],abs(hi4[k]-prev),abs(lo4[k]-prev))); prev=c4[i4[k]]
a4=[];a=tr4[0]
for x in tr4: a=(a*13+x)/14; a4.append(a)
def trade(i,side,RH,RL,a1):
    W=RH-RL; e=C[i]
    if side==1: sl=RL-0.3*a1; tp1=(RH+RL)/2; tp2=RH-0.1*W
    else: sl=RH+0.3*a1; tp1=(RH+RL)/2; tp2=RL+0.1*W
    R=abs(e-sl); fee=0.001*e/R
    if abs(tp1-e)<R*0.5: return None
    half=False; res=0
    for j in range(i+1,min(n,i+193)):
        hit_sl = L[j]<=sl if side==1 else H[j]>=sl
        if hit_sl: return (res + (0 if half else -1)*(1 if not half else 0.5)) - fee if not half else res - fee  # sau TP1 SL = giá vào -> 0 cho nửa còn lại
        if not half and (H[j]>=tp1 if side==1 else L[j]<=tp1):
            half=True; res+=0.5*abs(tp1-e)/R; sl=e
        if half and (H[j]>=tp2 if side==1 else L[j]<=tp2):
            return res+0.5*abs(tp2-e)/R-fee
    x=C[min(n-1,i+192)]; rem=(0.5 if half else 1)*side*(x-e)/R
    return res+rem-fee
out={}
last=-99
for kk in range(30,len(k4)-12):
    k=k4[kk]; s=h4[k][0]; i=h4[k][-1]
    if s<200 or i+200>=n: continue
    RH=max(H[s-192:s]); RL=min(L[s-192:s]); A=a4[kk-1]; W=RH-RL
    if W>2.5*A or W<0.8*A: continue
    kh=T[i]//3600000; 
    if kh not in i1: continue
    a1=atr[i1[kh]]
    dk=T[i]//86400000-1
    if dk not in idd: continue
    down = cd[idd[dk]]<ed[idd[dk]]
    if RL<C[i]<RL+0.15*W: side=1
    elif RH-0.15*W<C[i]<RH: side=-1
    else: continue
    r=trade(i,side,RH,RL,a1)
    if r is None: continue
    out.setdefault((down,side),[]).append(r)
for (down,side),xs in sorted(out.items()):
    m=st.mean(xs); se=st.pstdev(xs)/math.sqrt(len(xs))
    print(f"Xu hướng ngày {'GIẢM' if down else 'TĂNG'} · {'LONG đáy biên' if side==1 else 'SHORT đỉnh biên'}: n {len(xs)} TB {m:+.3f}R ±{se:.3f} thắng {sum(x>0 for x in xs)/len(xs):.0%}")
