exec(open('p65.py').read().split('out={}')[0])
def runset(mode,slm=0.5,tpm=1.0):
    out=[]; last=-10**9
    for kk in range(30,len(k4)-12):
        k=k4[kk]; i=h4[k][-1]
        if i+300>=n or i-last<16 or i<100: continue
        dk=T[i]//86400000-1
        if dk not in idd: continue
        down=cd[idd[dk]]<ed[idd[dk]]
        if not down: continue
        A=a4[kk]; kh=T[i]//3600000
        if kh not in i1: continue
        a1=atr[i1[kh]]
        if mode=='ema':
            lim=e4[kk]
            if not C[i]<lim-0.3*A: continue
        else:
            lim=max(H[i-95:i+1])+0.05*a1
            if not C[i]<lim-0.3*A: continue
        f=None
        for j in range(i+1,min(n,i+97)):
            if H[j]>=lim+10: f=j;break
        if f is None: continue
        last=i
        R=slm*A; sl=lim+R; tp=lim-tpm*R; r=None
        for j in range(f,min(n,f+193)):
            if H[j]>=sl: r=-1;break
            if L[j]<=tp: r=tpm;break
        if r is None: r=(lim-C[min(n-1,f+192)])/R
        out.append(r-0.001*lim/R)
    h=len(out)//2
    return len(out),st.mean(out),st.pstdev(out)/math.sqrt(len(out)),st.mean(out[:h]),st.mean(out[h:])
for m in ('ema','high'):
    for slm,tpm in ((0.5,1.0),(0.75,1.5)):
        n_,mu,se,a,b=runset(m,slm,tpm); print(m,f"SL {slm} ATR4H TP {tpm}R: n {n_} TB {mu:+.3f} ±{se:.3f} nửa {a:+.3f}/{b:+.3f}")
