exec(open('p27.py').read().split('def sim(')[0])
# 4H nến theo chỉ số 15m: mỗi 16 nến; atr4 tính từ c4
import statistics as st
hi4={};lo4={}
for k in k4:
    idx=h4[k]; hi4[k]=max(H[j] for j in idx); lo4[k]=min(L[j] for j in idx)
tr4=[];prev=None
for k in k4:
    tr4.append(hi4[k]-lo4[k] if prev is None else max(hi4[k]-lo4[k],abs(hi4[k]-prev),abs(lo4[k]-prev))); prev=c4[i4[k]]
a4=[];a=tr4[0]
for x in tr4: a=(a*13+x)/14; a4.append(a)
ev=[];base=[]
last=-10**9
for kk in range(20,len(k4)-8):
    k=k4[kk]; s=h4[k][0]; e=h4[k][-1]
    if s<200 or e+200>=n: continue
    RH=max(H[s-192:s]); RL=min(L[s-192:s]); A=a4[kk-1]; W=RH-RL
    if W>2.5*A or W<0.8*A: continue
    for side in (1,-1):
        brk = C[e]<RL if side==1 else C[e]>RH   # side=1: phá xuống giả -> kỳ vọng lên
        if not brk or e-last<32: continue
        rc=None
        for j in range(e+1,min(n,e+33)):
            if (C[j]>RL if side==1 else C[j]<RH): rc=j;break
        if rc is None: continue
        last=e
        mid=(RH+RL)/2; far=RH if side==1 else RL
        tm=tf=False
        for j in range(rc+1,min(n,rc+97)):
            if (H[j]>=mid if side==1 else L[j]<=mid): tm=True
            if (H[j]>=far if side==1 else L[j]<=far): tf=True
        ev.append((side,tm,tf))
    # nền: nến 15m nằm trong 25% dưới/trên của biên
    j=e
    if RL<C[j]<RL+0.25*W:
        tm=any(H[x]>=(RH+RL)/2 for x in range(j+1,min(n,j+97))); tf=any(H[x]>=RH for x in range(j+1,min(n,j+97))); base.append((1,tm,tf))
    if RH-0.25*W<C[j]<RH:
        tm=any(L[x]<=(RH+RL)/2 for x in range(j+1,min(n,j+97))); tf=any(L[x]<=RL for x in range(j+1,min(n,j+97))); base.append((-1,tm,tf))
def rep(nm,xs):
    if not xs: print(nm,0);return
    print(f"{nm}: n {len(xs)} chạm giữa {sum(t for _,t,_ in xs)/len(xs):.0%} chạm mép đối diện {sum(f for _,_,f in xs)/len(xs):.0%}")
rep('Phá vỡ giả (cả hai)',ev); rep(' phá xuống giả',[x for x in ev if x[0]==1]); rep(' phá lên giả',[x for x in ev if x[0]==-1])
rep('Nền (giá ở 25% sát mép)',base)
