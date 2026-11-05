#!/usr/bin/env python3
"""
Progressive / non-periodic key search for K4.

Tests key patterns that the existing periodic-key brute force cannot catch:
1. Linear progressive:   key[i] = (a*i + b) mod 26
2. Quadratic progressive: key[i] = (a*i^2 + b*i + c) mod 26
3. Gromark (Fibonacci chain from numeric seed, lengths 2-8)
4. Running key from known Kryptos plaintext (K1-K3 decrypts as key stream)
5. Porta cipher (reciprocal alphabet, period-based)
"""
import os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
K4_FILE = os.path.join(HERE, "..", "k4.txt")

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

with open(K4_FILE) as f:
    lines = f.read().strip().split("\n")
CT = lines[0].strip()
N = len(CT)

cribs = {}
for line in lines[1:]:
    parts = line.strip().split()
    if len(parts) == 2:
        pos, word = int(parts[0]), parts[1]
        for i, ch in enumerate(word):
            cribs[pos - 1 + i] = ch

sorted_pos = sorted(cribs.keys())
ncrib = len(sorted_pos)

# Known Kryptos plaintext sections (K1-K3 decryptions)
# These could serve as running-key material
K1_PLAIN = "BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUABOROFLUMINESCENCE"
K2_PLAIN = "ITWASTOTALLYINVISIBLEHOWSTHATPOSSIBLETHEYUSEDTHEEARTZQMAGNETICZFIELD"\
           "XTOACCUMULATEINFORMATIXONTHEWINDOWOFTHEBUILDINGTOCOLLECTMAPSINFORMATION"\
           "WHICHISACRUCIALSTEPINNEGATIVELYDEPLOYABLEINTELLIGENCEOPERATIONS"
K3_PLAIN = "SLOWLYDESPARATELYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWER"\
           "PARTOFTHEDOORWAYWASREMOVEDWITHTREMBLINGHANDSIMADEATINYBREACHINTHEUPPER"\
           "LEFTHANDCORNERANDTHENWIDENLIGHTTHEHOELSLIGHTLYIAPPLIEDMYEYEANDILOOKEDIN"

KNOWN_TEXTS = {
    "K1": K1_PLAIN.upper(),
    "K2": K2_PLAIN.upper(),
    "K3": K3_PLAIN.upper(),
    "K1K2K3": (K1_PLAIN + K2_PLAIN + K3_PLAIN).upper(),
}

all_hits = []


def key_fn(variant, ci, pi):
    """Compute key value from cipher/plaintext indices under a variant."""
    v = variant % 3
    if v == 0:
        return (ci - pi) % 26
    elif v == 1:
        return (ci + pi) % 26
    else:
        return (pi - ci) % 26


def get_alpha(variant):
    return KA if variant >= 3 else AZ


def test_key_stream(key_stream, label):
    """Test if a key stream is consistent with cribs under any variant."""
    for var_id in range(6):
        ALPHA = get_alpha(var_id)
        var_names = ["AZ/Vig", "AZ/Beau", "AZ/VarBeau", "KA/Vig", "KA/Beau", "KA/VarBeau"]
        all_match = True
        for pos in sorted_pos:
            if pos >= len(key_stream):
                all_match = False
                break
            ci = ALPHA.index(CT[pos])
            pi = ALPHA.index(cribs[pos])
            expected_key = key_fn(var_id, ci, pi)
            if key_stream[pos] != expected_key:
                all_match = False
                break
        if all_match:
            all_hits.append(f"HIT {label} variant={var_names[var_id]}")


def main():
    t0 = time.time()

    # ── 1. Linear progressive key ──────────────────────────────────────
    print("Testing linear progressive key: key[i] = (a*i + b) mod 26...")
    n1 = 0
    for a in range(26):
        for b in range(26):
            ks = [(a * i + b) % 26 for i in range(N)]
            test_key_stream(ks, f"Linear(a={a},b={b})")
            n1 += 1
    print(f"  Tested {n1} linear keys, {len(all_hits)} hit(s)")

    # ── 2. Quadratic progressive key ───────────────────────────────────
    n_before = len(all_hits)
    print("Testing quadratic progressive key: key[i] = (a*i²+b*i+c) mod 26...")
    n2 = 0
    for a in range(26):
        for b in range(26):
            for c in range(26):
                ks = [(a * i * i + b * i + c) % 26 for i in range(N)]
                test_key_stream(ks, f"Quadratic(a={a},b={b},c={c})")
                n2 += 1
    print(f"  Tested {n2} quadratic keys, {len(all_hits) - n_before} new hit(s)")

    # ── 3. Gromark (Fibonacci chain) ───────────────────────────────────
    n_before = len(all_hits)
    print("Testing Gromark cipher (Fibonacci chain from numeric seed)...")
    n3 = 0
    for seed_len in range(2, 9):
        for seed_val in range(10 ** seed_len):
            seed = [(seed_val // (10 ** i)) % 10 for i in range(seed_len)]
            ks = list(seed)
            while len(ks) < N:
                ks.append((ks[-1] + ks[-2]) % 10)
            # Gromark uses digit key stream mod 26 to shift
            test_key_stream(ks, f"Gromark(seed={''.join(map(str,seed))})")
            n3 += 1
        print(f"    seed_len={seed_len}: {n3} total seeds so far")
        if seed_len >= 5 and len(all_hits) == n_before:
            # Skip longer seeds if no hits at all
            break
    print(f"  Gromark: {len(all_hits) - n_before} hit(s)")

    # ── 4. Running key from K1/K2/K3 decryptions ──────────────────────
    n_before = len(all_hits)
    print("Testing running key from K1/K2/K3 plaintext...")
    for text_name, text in KNOWN_TEXTS.items():
        # Try the known plaintext as a running key, starting at various offsets
        for start in range(len(text)):
            key_text = text[start:]
            if len(key_text) < max(sorted_pos) + 1:
                continue
            for alpha_name, ALPHA in [("AZ", AZ), ("KA", KA)]:
                ks = [ALPHA.index(ch) if ch in ALPHA else 0 for ch in key_text[:N]]
                if len(ks) < N:
                    ks += [0] * (N - len(ks))
                test_key_stream(ks, f"RunningKey({text_name},off={start},{alpha_name})")
    print(f"  Running key: {len(all_hits) - n_before} hit(s)")

    # ── 5. Porta cipher ────────────────────────────────────────────────
    n_before = len(all_hits)
    print("Testing Porta cipher (reciprocal alphabets, periods 2-45)...")
    # Porta: 13 reciprocal alphabets, key letter selects which one
    PORTA_TABS = []
    for k in range(13):
        tab = list(range(26))
        for i in range(13):
            j = (i + k) % 13 + 13
            tab[i] = j
            tab[j] = i
        PORTA_TABS.append(tab)

    for period in range(2, 46):
        for key_combo in range(13 ** min(period, 6)):
            key = []
            val = key_combo
            for _ in range(min(period, 6)):
                key.append(val % 13)
                val //= 13
            if len(key) < period:
                # For longer periods, only test if short part is consistent
                key = key * ((period // len(key)) + 1)
                key = key[:period]

            all_match = True
            for pos in sorted_pos:
                ct_idx = AZ.index(CT[pos])
                tab = PORTA_TABS[key[pos % period]]
                pt_idx = tab[ct_idx]
                expected = cribs[pos]
                if expected == 'J':
                    expected = 'I'
                if AZ[pt_idx] != expected:
                    all_match = False
                    break

            if all_match:
                all_hits.append(f"HIT Porta period={period} key={''.join(map(str,key[:period]))}")

        if period <= 5:
            print(f"    period {period} done")

    print(f"  Porta: {len(all_hits) - n_before} hit(s)")

    elapsed = time.time() - t0
    print(f"\nTotal: {len(all_hits)} hit(s) in {elapsed:.1f}s")

    if all_hits:
        hitfile = os.path.join(HERE, "..", "hits_progressive.txt")
        with open(hitfile, "w") as f:
            f.write("\n".join(all_hits) + "\n")
        print(f"\nHits written to {hitfile}")
        for h in all_hits[:20]:
            print(f"  {h}")
    else:
        print("\nNo hits. All progressive key patterns ruled out.")


if __name__ == "__main__":
    main()
