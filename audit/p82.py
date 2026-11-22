exec(open('p65.py').read().split('out={}')[0])
def run(cond_daily_down, side):
    out=[]; last=-10**9
    for kk in range(30,len(k4)-12):
        k=k4[kk]; i=h4[k][-1]
        if i+300>=n or i-last<16 or i<100: continue
        dk=T[i]//86400000-1
        if dk not in idd: continue
        down=cd[idd[dk]]<ed[idd[dk]]
        if down!=cond_daily_down: continue
        A=a4[kk]; em=e4[kk]
        # 4H đang trên EMA20 4H (nhịp hồi) -> mua chờ tại EMA20 4H
        if side==1 and not C[i]>em+0.3*A: continue
        if side==-1 and not C[i]<em-0.3*A: continue
        f=None
        for j in range(i+1,min(n,i+97)):
            if (L[j]<=em-10 if side==1 else H[j]>=em+10): f=j;break
        if f is None: continue
        last=i; R=0.5*A; sl=em-side*R; tp=em+side*R; r=None
        for j in range(f,min(n,f+193)):
            if (L[j]<=sl if side==1 else H[j]>=sl): r=-1;break
            if (H[j]>=tp if side==1 else L[j]<=tp): r=1;break
        if r is None: r=side*(C[min(n-1,f+192)]-em)/R
        out.append(r-0.001*em/R)
    h=len(out)//2
    return len(out),round(st.mean(out),3),round(st.pstdev(out)/math.sqrt(len(out)),3),round(st.mean(out[:h]),3),round(st.mean(out[h:]),3)
print('Ngày giảm, 4H trên EMA20 → MUA chờ tại EMA20 4H:',run(True,1))
print('Ngày tăng, 4H trên EMA20 → MUA chờ tại EMA20 4H:',run(False,1))
print('Ngày giảm, 4H dưới EMA20 → BÁN chờ tại EMA20 4H:',run(True,-1))
