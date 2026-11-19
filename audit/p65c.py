exec(open('p65.py').read().split('out={}')[0])
# Hồi về EMA20 4H theo xu hướng ngày: ngày giảm -> lệnh bán chờ tại EMA20 4H khi giá đang dưới; ngày tăng -> mua chờ tại EMA20 4H khi giá trên.
res={}
for slm in (0.5,1.0):
  for tpm in (1.0,2.0):
    out=[]
    last=-10**9
    for kk in range(30,len(k4)-12):
        k=k4[kk]; i=h4[k][-1]
        if i+300>=n or i-last<16: continue
        dk=T[i]//86400000-1
        if dk not in idd: continue
        down=cd[idd[dk]]<ed[idd[dk]]; side=-1 if down else 1
        em=e4[kk]; A=a4[kk]
        if side==-1 and not (C[i]<em-0.3*A): continue
        if side==1 and not (C[i]>em+0.3*A): continue
        f=None
        for j in range(i+1,min(n,i+97)):
            if L[j]<=em<=H[j]: f=j;break
        if f is None: continue
        last=i
        e=em; R=slm*A; sl=e-side*R; tp=e+side*tpm*R; r=None
        for j in range(f,min(n,f+193)):
            if (L[j]<=sl if side==1 else H[j]>=sl): r=-1;break
            if (H[j]>=tp if side==1 else L[j]<=tp): r=tpm;break
        if r is None: r=side*(C[min(n-1,f+192)]-e)/R
        out.append(r-0.001*e/R)
    h=len(out)//2
    print(f"SL {slm} ATR4H, TP {tpm}R: n {len(out)} TB {st.mean(out):+.3f}R ±{st.pstdev(out)/math.sqrt(len(out)):.3f} nửa đầu {st.mean(out[:h]):+.3f} nửa sau {st.mean(out[h:]):+.3f}")
