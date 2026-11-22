exec(open('p65.py').read().split('out={}')[0])
import datetime as dt
# P79: ngày giảm, sell-stop tại đáy 24h - 0.1 ATR1H, chờ 24h
res={}
last=-10**9
for kk in range(30,len(k4)-14):
    k=k4[kk]; i=h4[k][-1]
    if i+300>=n or i<100 or i-last<16: continue
    dk=T[i]//86400000-1
    if dk not in idd or not cd[idd[dk]]<ed[idd[dk]]: continue
    kh=T[i]//3600000
    if kh not in i1: continue
    a1=atr[i1[kh]]; A=a4[kk]
    stp=min(L[i-95:i+1])-0.1*a1
    f=None
    for j in range(i+1,min(n,i+97)):
        if L[j]<=stp-10: f=j;break
    if f is None: continue
    last=i; e=stp-10
    for slm in (0.5,1.0):
        for tpm in (1.0,2.0):
            R=slm*A; sl=e+R; tp=e-tpm*R; r=None
            for j in range(f,min(n,f+193)):
                if H[j]>=sl: r=-1;break
                if L[j]<=tp: r=tpm;break
            if r is None: r=(e-C[min(n-1,f+192)])/R
            res.setdefault((slm,tpm),[]).append(r-0.001*e/R)
for k,v in sorted(res.items()):
    h=len(v)//2; print('P79 sell-stop SL',k[0],'ATR4H TP',k[1],'R: n',len(v),'TB',round(st.mean(v),3),'±',round(st.pstdev(v)/math.sqrt(len(v)),3),'nửa',round(st.mean(v[:h]),3),round(st.mean(v[h:]),3))
# P80: cuối tuần vs ngày thường: biên độ 15m TB, tỷ lệ chạm +2 ATR1H trong 24h
wk={'cuối tuần':[[],0,0],'ngày thường':[[],0,0]}
for i in range(200,n-100,4):
    d=dt.datetime.utcfromtimestamp(T[i]/1000+7*3600).weekday()
    g='cuối tuần' if d>=5 else 'ngày thường'
    wk[g][0].append(H[i]-L[i])
    kh=T[i]//3600000
    if kh in i1 and i%16==0:
        a1=atr[i1[kh]]; tgt=C[i]+2*a1
        wk[g][2]+=1
        if any(H[j]>=tgt for j in range(i+1,i+97)): wk[g][1]+=1
for g,(rg,hit,tot) in wk.items(): print('P80',g,'biên độ 15m TB',round(st.mean(rg),1),'chạm +2 ATR1H trong 24h',f"{hit/tot:.0%}",'n',tot)
