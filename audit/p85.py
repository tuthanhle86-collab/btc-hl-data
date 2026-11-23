exec(open('p65.py').read().split('out={}')[0])
def run(mode):
    out=[]; last=-10**9
    for kk in range(30,len(k4)-12):
        k=k4[kk]; i=h4[k][-1]
        if i+300>=n or i-last<16 or i<100: continue
        dk=T[i]//86400000-1
        if dk not in idd or not cd[idd[dk]]<ed[idd[dk]]: continue
        A=a4[kk]; em=e4[kk]
        if not C[i]<em-0.3*A: continue
        if mode=='ema':
            e=em; f=None
            for j in range(i+1,min(n,i+97)):
                if H[j]>=em+10: f=j;break
            if f is None: continue
        else:
            e=C[i]-10; f=i+1
        last=i; R=0.5*A; sl=e+R; tp=e-R; r=None
        for j in range(f,min(n,f+193)):
            if H[j]>=sl: r=-1;break
            if L[j]<=tp: r=1;break
        if r is None: r=(e-C[min(n-1,f+192)])/R
        out.append(r-0.001*e/R)
    h=len(out)//2
    return len(out),round(st.mean(out),3),round(st.pstdev(out)/math.sqrt(len(out)),3),round(st.mean(out[:h]),3),round(st.mean(out[h:]),3)
print('Chờ tại EMA20 4H',run('ema')); print('Bán ngay',run('mkt'))
