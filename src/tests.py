KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
C=open("k4.txt").readline().strip(); N=len(C)
cribs={}
for i,ch in enumerate("EASTNORTHEAST"): cribs[21+i]=ch
for i,ch in enumerate("BERLINCLOCK"): cribs[63+i]=ch

def alph(v): return KA if v in (3,4,5) else AZ
names=["AZ Vigenere","AZ Beaufort","AZ VarBeaufort","KA Vigenere","KA Beaufort","KA VarBeaufort"]
def enc(v,p,k,A):
    pi,ki=A.index(p),A.index(k)
    return A[[ (pi+ki)%26, (ki-pi)%26, (pi-ki)%26 ][v%3]]
def keyfrom(v,c,p):
    A=alph(v); ci,pi=A.index(c),A.index(p)
    return [(ci-pi)%26,(ci+pi)%26,(pi-ci)%26][v%3]

print("== TEST A: no transposition, periodic key, periods 2..45 (crib-consistent?) ==")
found=False
for v in range(6):
    for p in range(2,46):
        slot={}; ok=True; red=0
        for q,ch in cribs.items():
            k=keyfrom(v,C[q],ch)
            if q%p in slot:
                if slot[q%p]!=k: ok=False;break
                red+=1
            else: slot[q%p]=k
        if ok and red>=4:
            found=True; print("  consistent:",names[v],"period",p,"redundant checks",red)
print("  none" if not found else "")

print("== TEST B1: ciphertext-feedback autokey, primer length L=1..96 ==")
best=(0,)
for v in range(6):
    A=alph(v)
    for L in range(1,N):
        ok=tot=0
        for q,ch in cribs.items():
            if q>=L:
                k=C[q-L]; tot+=1
                if enc(v,ch,k,A)==C[q]: ok+=1
        if tot>=8 and ok>best[0]: best=(ok,tot,names[v],L)
print("  best crib agreement (matches, tested, variant, L):",best, "(random expectation ~ tested/26)")

print("== TEST B2: plaintext-feedback autokey, primer length L=1..96 ==")
res=[]
for v in range(6):
    A=alph(v)
    for L in range(1,N):
        pairs=[(q,q-L) for q in cribs if q-L in cribs]
        if len(pairs)<3: continue
        ok=sum(enc(v,cribs[q],cribs[q-L],A)==C[q] for q,_ in pairs)
        res.append((ok/len(pairs),ok,len(pairs),names[v],L))
res.sort(reverse=True)
print("  top 3 (fraction, matches, constraints, variant, L):"); [print("   ",r) for r in res[:3]]
print("  full consistency found:", any(r[0]==1.0 for r in res))

print("== Index of coincidence ==")
from collections import Counter
cnt=Counter(C); ic=sum(v*(v-1) for v in cnt.values())/(N*(N-1))
print(f"  IC = {ic:.4f}  (English ~0.066, random ~0.038, periodic Vigenere w/ short key ~0.045-0.055)")
