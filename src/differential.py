#!/usr/bin/env python3
"""
Differential analysis of K4 crib positions.
Computes C[i] - P[i] mod 26 (and variants) at the 20 known positions,
then looks for structure: periodicity, polynomial, Fibonacci, etc.
Also performs Kasiski analysis and IC-by-period on the full ciphertext.
"""
import os, sys, math
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
K4_FILE = os.path.join(HERE, "..", "k4.txt")

KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ── Load ciphertext and cribs ──────────────────────────────────────────
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
            cribs[pos - 1 + i] = ch  # 0-indexed

print(f"Ciphertext: {CT}")
print(f"Length: {N}")
print(f"Known crib positions: {len(cribs)}")
print()

# ── 1. Raw differences under each alphabet and variant ─────────────────
print("=" * 72)
print("SECTION 1: Raw key-stream values at crib positions")
print("=" * 72)

sorted_pos = sorted(cribs.keys())

for alpha_name, ALPHA in [("Standard A-Z", AZ), ("KRYPTOS-keyed", KA)]:
    for var_name, diff_fn in [
        ("Vigenère  (C-P)", lambda c, p: (c - p) % 26),
        ("Beaufort  (P-C)", lambda c, p: (p - c) % 26),
        ("VarBeauf  (C+P)", lambda c, p: (c + p) % 26),
    ]:
        label = f"{alpha_name} / {var_name}"
        vals = []
        for pos in sorted_pos:
            ci = ALPHA.index(CT[pos])
            pi = ALPHA.index(cribs[pos])
            vals.append(diff_fn(ci, pi))

        print(f"\n  {label}")
        print(f"    Positions: {sorted_pos}")
        print(f"    Values:    {vals}")
        print(f"    As letters (AZ): {''.join(AZ[v] for v in vals)}")
        print(f"    As letters (KA): {''.join(KA[v] for v in vals)}")

        # Check periodicity: for each period p, check consistency at pos mod p
        best_period = None
        best_red = -1
        for p in range(1, 46):
            slots = {}
            ok = True
            redundant = 0
            for pos, val in zip(sorted_pos, vals):
                r = pos % p
                if r in slots:
                    if slots[r] != val:
                        ok = False
                        break
                    redundant += 1
                else:
                    slots[r] = val
            if ok and redundant > best_red:
                best_period = p
                best_red = redundant

        if best_red > 0:
            print(f"    Best periodic fit: period={best_period}, redundant checks={best_red}")
        else:
            print(f"    No periodic consistency found (all periods produce conflicts)")

# ── 2. Look for polynomial key patterns ────────────────────────────────
print()
print("=" * 72)
print("SECTION 2: Polynomial key-stream patterns (key[i] = a*i + b, a*i²+b*i+c, etc.)")
print("=" * 72)

for alpha_name, ALPHA in [("A-Z", AZ), ("KA", KA)]:
    for var_name, diff_fn in [
        ("Vig", lambda c, p: (c - p) % 26),
        ("Beau", lambda c, p: (p - c) % 26),
    ]:
        vals = []
        for pos in sorted_pos:
            ci = ALPHA.index(CT[pos])
            pi = ALPHA.index(cribs[pos])
            vals.append(diff_fn(ci, pi))

        # Linear: key[pos] = (a*pos + b) mod 26
        linear_hits = []
        for a in range(26):
            for b in range(26):
                if all((a * pos + b) % 26 == val for pos, val in zip(sorted_pos, vals)):
                    linear_hits.append((a, b))
        if linear_hits:
            print(f"\n  *** LINEAR HIT ({alpha_name}/{var_name}): key[i] = (a*i + b) mod 26 ***")
            for a, b in linear_hits:
                print(f"      a={a}, b={b}")

        # Quadratic: key[pos] = (a*pos^2 + b*pos + c) mod 26
        quad_hits = []
        for a in range(26):
            for b in range(26):
                for c in range(26):
                    if all((a * pos * pos + b * pos + c) % 26 == val
                           for pos, val in zip(sorted_pos, vals)):
                        quad_hits.append((a, b, c))
        if quad_hits:
            print(f"\n  *** QUADRATIC HIT ({alpha_name}/{var_name}): key[i] = (a*i²+b*i+c) mod 26 ***")
            for a, b, c in quad_hits[:10]:
                print(f"      a={a}, b={b}, c={c}")
            if len(quad_hits) > 10:
                print(f"      ... and {len(quad_hits) - 10} more")

# ── 3. Fibonacci / Gromark recurrence check ────────────────────────────
print()
print("=" * 72)
print("SECTION 3: Gromark / Fibonacci recurrence check")
print("=" * 72)
print("  Testing: key[i] = (key[i-1] + key[i-2]) mod 10  (Gromark-style)")
print("  Seeds: all pairs (d0, d1) with d0,d1 in 0..9")

for alpha_name, ALPHA in [("A-Z", AZ), ("KA", KA)]:
    for var_name, diff_fn in [
        ("Vig", lambda c, p: (c - p) % 26),
        ("Beau", lambda c, p: (p - c) % 26),
    ]:
        vals = {}
        for pos in sorted_pos:
            ci = ALPHA.index(CT[pos])
            pi = ALPHA.index(cribs[pos])
            vals[pos] = diff_fn(ci, pi)

        # Try numeric seeds of length 2-8 generating a Fibonacci-chain mod 10
        for seed_len in range(2, 9):
            for seed_val in range(10 ** seed_len):
                seed = [(seed_val // (10 ** i)) % 10 for i in range(seed_len)]
                # Generate key stream up to max position
                ks = list(seed)
                while len(ks) <= max(sorted_pos):
                    ks.append((ks[-1] + ks[-2]) % 10)
                # Check: key at position = key_stream digit (mod 26)
                if all(ks[pos] == vals[pos] for pos in sorted_pos):
                    print(f"\n  *** GROMARK HIT ({alpha_name}/{var_name}) seed={seed}")
            if seed_len >= 4:
                break  # 10^4 = 10k, getting expensive, skip longer seeds

print("  (done)")

# ── 4. Kasiski analysis ────────────────────────────────────────────────
print()
print("=" * 72)
print("SECTION 4: Kasiski examination (repeated n-grams in ciphertext)")
print("=" * 72)

for n in range(2, 6):
    repeats = {}
    for i in range(N - n + 1):
        gram = CT[i:i + n]
        if gram in repeats:
            repeats[gram].append(i)
        else:
            repeats[gram] = [i]
    found = {g: pos for g, pos in repeats.items() if len(pos) > 1}
    if found:
        print(f"\n  Repeated {n}-grams:")
        for gram, positions in sorted(found.items()):
            spacings = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
            factors = set()
            for sp in spacings:
                for f in range(2, sp + 1):
                    if sp % f == 0:
                        factors.add(f)
            print(f"    {gram}: positions {positions}, spacings {spacings}, "
                  f"common factors {sorted(factors)[:15]}")

# ── 5. IC by period ────────────────────────────────────────────────────
print()
print("=" * 72)
print("SECTION 5: Index of Coincidence by assumed period")
print("=" * 72)
print("  (Higher IC → closer to English mono-alphabetic → better period guess)")
print(f"  English ≈ 0.066, random ≈ 0.038\n")

for p in range(1, 31):
    ics = []
    for offset in range(p):
        subset = [CT[i] for i in range(offset, N, p)]
        if len(subset) < 2:
            continue
        cnt = Counter(subset)
        ic = sum(v * (v - 1) for v in cnt.values()) / (len(subset) * (len(subset) - 1))
        ics.append(ic)
    avg_ic = sum(ics) / len(ics) if ics else 0
    bar = "█" * int(avg_ic * 400)
    print(f"  period {p:2d}: avg IC = {avg_ic:.4f}  {bar}")

# ── 6. Crib-position difference structure ──────────────────────────────
print()
print("=" * 72)
print("SECTION 6: Adjacent-crib difference analysis")
print("=" * 72)
print("  Looking at differences between consecutive crib key values")
print("  (constant = linear key, linear = quadratic key, etc.)\n")

for alpha_name, ALPHA in [("A-Z", AZ), ("KA", KA)]:
    for var_name, diff_fn in [
        ("Vig", lambda c, p: (c - p) % 26),
    ]:
        vals = []
        for pos in sorted_pos:
            ci = ALPHA.index(CT[pos])
            pi = ALPHA.index(cribs[pos])
            vals.append(diff_fn(ci, pi))

        print(f"  {alpha_name}/{var_name}:")
        print(f"    pos:     {sorted_pos}")
        print(f"    key val: {vals}")
        diffs1 = [(vals[i + 1] - vals[i]) % 26 for i in range(len(vals) - 1)]
        pos_diffs = [sorted_pos[i + 1] - sorted_pos[i] for i in range(len(sorted_pos) - 1)]
        print(f"    Δ(val):  {diffs1}")
        print(f"    Δ(pos):  {pos_diffs}")
        # Normalized: diff per position step
        normed = [(d / dp) if dp != 0 else None for d, dp in zip(diffs1, pos_diffs)]
        print(f"    Δ(val)/Δ(pos): {[f'{x:.3f}' if x is not None else 'N/A' for x in normed]}")
        print()

print("\n=== Analysis complete ===")
