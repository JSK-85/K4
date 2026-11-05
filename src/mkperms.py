import sys
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
seen=set(); out=open("perms.txt","w"); n=0
words=[w.strip().upper() for w in open("words.txt")]
extra=["KRYPTOS","PALIMPSEST","ABSCISSA","BERLIN","CLOCK","NORTHEAST","SANBORN","SHADOW","LUCID","MEMORY","VIRTUALLY","INVISIBLE","DIGETAL","INTERPRETATION","UNDERGRUUND","LANGLEY","SLOWLY","DESPARATLY","IQLUSION","ENIGMA","COMPASS","LODESTONE","WEBSTER","EGYPT","CARTER","TOMB","LAYER","TWO","POSITION","DESPARATELY","COORDINATES","MAGNETIC","FIELD","LOCATION","BURIED","UNKNOWN","WHATSTHEPOINT","DELIVER","MESSAGE","DIGITAL","REPRESENTS","SHADING","ABSENCE","LIGHT","SUBTLE","TRANSMITTED","EARTHS","UNDERGROUND"]
for w in extra+words:
    w=w.strip()
    if not w.isalpha() or not (4<=len(w)<=25): continue
    for name,alpha in (("az","ABCDEFGHIJKLMNOPQRSTUVWXYZ"),("ka",KA)):
        order=sorted(range(len(w)),key=lambda i:(alpha.index(w[i]),i))
        t=(len(w),tuple(order))
        if t in seen: continue
        seen.add(t); out.write(f"{len(w)} "+" ".join(map(str,order))+"\n"); n+=1
print("distinct keyword permutations:",n)
