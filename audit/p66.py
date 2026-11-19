src=open('p52.py').read().split("res=[]")[0]
exec(src)
hd={}
for i in range(n): hd.setdefault(T[i]//86400000,[]).append(i)
kd=sorted(hd); cdl=[C[hd[k][-1]] for k in kd]; ed=ema(cdl,20); idd={k:i for i,k in enumerate(kd)}
import statistics as st,math
res={}; last=-99
for i in range(400,n-200):
    if i-last<16: continue
    x=run(i)
    if not x: continue
    last=i; d,rel,r=x
    dk=T[i]//86400000-1
    if dk not in idd: continue
    j=idd[dk]; dev=(cdl[j]-ed[j])/ed[j]
    reg='giảm mạnh (giá < EMA20 ngày −5%)' if dev<-0.05 else ('tăng mạnh (> +5%)' if dev>0.05 else 'quanh EMA20 ngày (±5%)')
    res.setdefault(reg,[]).append(r)
    res.setdefault(reg+(' · SHORT' if d==-1 else ' · LONG'),[]).append(r)
for k in sorted(res):
    v=res[k]; print(f"{k}: n {len(v)} TB {st.mean(v):+.3f}R ±{st.pstdev(v)/math.sqrt(len(v)):.3f}")
