exec(open('p65.py').read().split('out={}')[0])
fill={'1-2':[0,0],'2-3':[0,0],'>3':[0,0]}
one=[];two=[]
last=-10**9
for kk in range(30,len(k4)-12):
    k=k4[kk]; i=h4[k][-1]
    if i+300>=n or i<100: continue
    dk=T[i]//86400000-1
    if dk not in idd: continue
    if not cd[idd[dk]]<ed[idd[dk]]: continue
    A=a4[kk]; kh=T[i]//3600000
    if kh not in i1: continue
    a1=atr[i1[kh]]; lim=e4[kk]
    dist=(lim-C[i])/a1
    if dist<1: continue
    g='1-2' if dist<2 else ('2-3' if dist<3 else '>3')
    f=None
    for j in range(i+1,min(n,i+97)):
        if H[j]>=lim+10: f=j;break
    fill[g][1]+=1
    if f is None: continue
    fill[g][0]+=1
    if i-last<16: continue
    last=i
    R=0.5*A; fee=0.001*lim/R
    # một lần TP 1R
    sl=lim+R; tp=lim-R; r=None
    for j in range(f,min(n,f+193)):
        if H[j]>=sl: r=-1;break
        if L[j]<=tp: r=1;break
    if r is None: r=(lim-C[min(n-1,f+192)])/R
    one.append(r-fee)
    # hai nấc: 50% ở 1R, dời SL về giá vào, 50% ở 2.5R
    sl=lim+R; half=False; res=0; r2=None
    for j in range(f,min(n,f+193)):
        if H[j]>=sl: r2=res+(0 if half else -1); break
        if not half and L[j]<=lim-R: half=True; res+=0.5; sl=lim
        if half and L[j]<=lim-2.5*R: r2=res+1.25; break
    if r2 is None: r2=res+(0.5 if half else 1)*(lim-C[min(n-1,f+192)])/R
    two.append(r2-fee)
for g,(a,b) in fill.items(): print('khoảng cách',g,'ATR 1H: khớp trong 24h',f"{a}/{b} = {a/max(b,1):.0%}")
h=len(one)//2
print('TP 1R một lần: n',len(one),'TB',round(st.mean(one),3),'±',round(st.pstdev(one)/math.sqrt(len(one)),3),'nửa',round(st.mean(one[:h]),3),round(st.mean(one[h:]),3))
print('Hai nấc 1R/2.5R: n',len(two),'TB',round(st.mean(two),3),'±',round(st.pstdev(two)/math.sqrt(len(two)),3),'nửa',round(st.mean(two[:h]),3),round(st.mean(two[h:]),3))
