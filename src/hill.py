import itertools
from sympy import Matrix
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
C=open("k4.txt").readline().strip(); N=len(C)
cribs={}
for i,ch in enumerate("EASTNORTHEAST"): cribs[21+i]=ch
for i,ch in enumerate("BERLINCLOCK"): cribs[63+i]=ch
def run(n):
    total=0
    for A,aname in ((AZ,"AZ"),(KA,"KA")):
        for off in range(n):
            blocks=[b for b in range(off,N-n+1,n) if all(b+i in cribs for i in range(n))]
            if len(blocks)<n+1: continue
            Ps=[[A.index(cribs[b+i]) for i in range(n)] for b in blocks]
            Cs=[[A.index(C[b+i]) for i in range(n)] for b in blocks]
            for combo in itertools.combinations(range(len(blocks)),n):
                P=Matrix([Ps[i] for i in combo]); Cm=Matrix([Cs[i] for i in combo])
                if P.det()%2==0 or P.det()%13==0: continue
                M=(P.inv_mod(26)*Cm).applyfunc(lambda x:x%26)
                ok=[ (Matrix([Ps[i]])*M).applyfunc(lambda x:x%26).tolist()[0]==Cs[i] for i in range(len(blocks)) if i not in combo]
                total+=1
                if all(ok): print(f"  HILL {n}x{n} CONSISTENT alphabet={aname} offset={off} M={M.tolist()}")
    return total
for n in (2,3):
    t=run(n); print(f"Hill {n}x{n}: solved/verified {t} candidate systems, consistent: see HIT lines above (none if blank)")
