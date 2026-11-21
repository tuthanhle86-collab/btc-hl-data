exec(open('p65.py').read().split('out={}')[0])
ev=[];trades=[];last=-10**9
for kk in range(30,len(k4)-14):
    pass
A4={}
for kk,k in enumerate(k4):
    for j in h4[k]: A4[j]=a4[kk-1] if kk>0 else a4[0]
i=40
while i<n-300:
    A=A4.get(i)
    if A is None: i+=1;continue
    w=range(i-32,i+1)
    hi=max(H[j] for j in w); lo=L[i]
    if lo<=min(L[j] for j in w) and hi-lo>=3.5*A and i-last>96:
        # xác nhận đáy: 4 nến sau không thấp hơn? dùng đáy tại i khi chưa biết -> mô phỏng thực tế: vào lệnh sau khi có đáy tạm (dùng i là đáy hiện tại)
        D=hi-lo; last=i
        r38=lo+0.382*D; r50=lo+0.5*D
        t38=any(H[j]>=r38 for j in range(i+1,i+97)); t50=any(H[j]>=r50 for j in range(i+1,i+97))
        ev.append((t38,t50))
        e=lo+0.437*D; sl=lo+0.675*D; R=sl-e; tp1=e-R; tp2=lo-0.109*D; fee=0.001*e/R
        f=None
        for j in range(i+1,i+97):
            if H[j]>=e+10: f=j;break
            if L[j]<lo-0.25*D: break
        if f:
            half=False;res=0;s=sl;r=None
            for j in range(f,min(n,f+193)):
                if H[j]>=s: r=res+(0 if half else -1);break
                if not half and L[j]<=tp1: half=True;res+=0.5;s=e
                if half and L[j]<=tp2: r=res+0.5*(e-tp2)/R;break
            if r is None: r=res+(0.5 if half else 1)*(e-C[min(n-1,f+192)])/R
            trades.append(r-fee)
        i+=96
    else: i+=1
import statistics as st
print('Cú rơi ≥3.5 ATR4H trong ≤8h: n',len(ev),'chạm 38.2% trong 24h',f"{sum(a for a,b in ev)/len(ev):.0%}",'chạm 50%',f"{sum(b for a,b in ev)/len(ev):.0%}")
if trades: print('Lệnh kiểu E5: khớp',len(trades),'/',len(ev),'TB',round(st.mean(trades),3),'±',round(st.pstdev(trades)/math.sqrt(len(trades)),3),'thắng',f"{sum(x>0 for x in trades)/len(trades):.0%}")
