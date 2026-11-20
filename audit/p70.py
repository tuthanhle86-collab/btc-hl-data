exec(open('p27.py').read().split('def sim(')[0])
import statistics as st, math
def direction(i):
    kh=T[i]//3600000-1; k4h=T[i]//14400000-1
    if kh not in i1 or k4h not in i4: return None
    j1=i1[kh]; return (1 if c1[j1]>e1[j1] else -1), atr[j1]
def swing_R(i,d,e,a):
    ext=None
    for j in range(i-2,i-16,-1):
        if d==1 and L[j]<=min(L[j-2:j+3]) and L[j]<e: ext=L[j];break
        if d==-1 and H[j]>=max(H[j-2:j+3]) and H[j]>e: ext=H[j];break
    return a if ext is None else max(a,abs(e-(ext-d*0.1*a)))
def outcome(f,d,e,R):
    sl=e-d*R; tp=e+d*R; fee=0.001*e/R
    for j in range(f,min(n,f+96)):
        if (L[j]<=sl if d==1 else H[j]>=sl): return -1-fee
        if (H[j]>=tp if d==1 else L[j]<=tp): return 1-fee
    return d*(C[min(n-1,f+96)]-e)/R-fee
lim_res=[];auto_res=[];cancel=0;unfill=0;days=0
for i in range(500,n-200):
    t=T[i]
    if (t//900000)%96!=4: continue   # 01:00 UTC = 08:00 VN (nến 15m bắt đầu 01:00)
    x=direction(i)
    if not x: continue
    days+=1
    d,a=x; p=C[i]; lim=p-d*0.5*a; tp_pre=lim+d*a
    end=i+52  # tới 14:00 UTC = 21:00 VN
    filled=None
    for j in range(i+1,end):
        if (L[j]<=lim-10 if d==1 else H[j]>=lim+10): filled=j;break
        if (H[j]>=tp_pre if d==1 else L[j]<=tp_pre): cancel+=1; break
    if filled:
        R=swing_R(filled,d,lim,a); lim_res.append(outcome(filled,d,lim,R)); continue
    if not filled: unfill+=1
    k=end
    y=direction(k)
    if not y: continue
    d2,a2=y; e=C[k-1]+d2*10; R=swing_R(k,d2,e,a2); auto_res.append(outcome(k,d2,e,R))
def rep(nm,xs): print(f"{nm}: n {len(xs)} TB {st.mean(xs):+.3f}R ±{st.pstdev(xs)/math.sqrt(len(xs)):.3f}")
print('ngày',days,'hủy vì chạm TP trước',cancel, f"({cancel/days:.0%})")
rep('Khớp giới hạn',lim_res); rep('Tự vào 21:00',auto_res)
