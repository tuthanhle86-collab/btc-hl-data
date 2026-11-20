exec(open('p65.py').read().split('out={}')[0])
# RSI 14 trên 4H
def rsi_list(xs,p=14):
    g=l=0; out=[None]*len(xs)
    for i in range(1,len(xs)):
        d=xs[i]-xs[i-1]
        if i<=p: g+=max(d,0); l+=max(-d,0)
        if i==p: ag=g/p; al=l/p
        elif i>p: ag=(ag*(p-1)+max(d,0))/p; al=(al*(p-1)+max(-d,0))/p
        if i>=p: out[i]=100-100/(1+ag/al) if al>0 else 100
    return out
r4=rsi_list(c4)
res={}
last=-99
for kk in range(30,len(k4)-14):
    if r4[kk] is None or r4[kk]>=25 or kk-last<6: continue
    last=kk
    i=h4[k4[kk]][-1]; e=C[i]; A=a4[kk]
    fwd=(C[min(n-1,i+96)]-e)/A
    res.setdefault('ret24h_ATR',[]).append(fwd)
    for side in (1,-1):
      for tpm in (1.0,2.0):
        R=A; sl=e-side*R; tp=e+side*tpm*R; r=None
        for j in range(i+1,min(n,i+193)):
            if (L[j]<=sl if side==1 else H[j]>=sl): r=-1;break
            if (H[j]>=tp if side==1 else L[j]<=tp): r=tpm;break
        if r is None: r=side*(C[min(n-1,i+192)]-e)/R
        res.setdefault(('LONG' if side==1 else 'SHORT',tpm),[]).append(r-0.001*e/R)
for k,v in res.items():
    h=len(v)//2
    print(k,'n',len(v),'TB',round(st.mean(v),3),'±',round(st.pstdev(v)/math.sqrt(len(v)),3),'nửa',round(st.mean(v[:h]),3),round(st.mean(v[h:]),3))
