#!/usr/bin/env python3
"""
Quagmire I/II/III/IV cipher search.
Tests keyword-mixed alphabets (from dictionary) × periodic keys against the known cribs.

Quagmire I:   mixed plaintext alphabet, standard cipher alphabet, periodic key
Quagmire II:  standard plaintext alphabet, mixed cipher alphabet, periodic key
Quagmire III: same mixed alphabet for both plaintext and cipher (= "Keyed Vigenère")
Quagmire IV:  different mixed alphabets for plaintext and cipher

We already test standard + KRYPTOS-keyed alphabets. This script tests ALL
dictionary-derived keyword alphabets.
"""
import os, sys, time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
K4_FILE = os.path.join(HERE, "..", "k4.txt")
WORDS_FILE = os.path.join(HERE, "words.txt")

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

# ── Load ───────────────────────────────────────────────────────────────
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

sorted_pos = sorted(cribs.keys())
ncrib = len(sorted_pos)


def make_keyed_alphabet(keyword, base=AZ):
    """Build a keyword-mixed alphabet: KEYWORD + remaining letters in order."""
    seen = set()
    alpha = []
    for ch in keyword.upper():
        if ch in seen or ch not in base:
            continue
        seen.add(ch)
        alpha.append(ch)
    for ch in base:
        if ch not in seen:
            alpha.append(ch)
    return "".join(alpha)


def check_quagmire(ct_alpha, pt_alpha, label):
    """
    For each variant (Vig/Beau/VarBeau), compute key-stream values at crib
    positions using given cipher/plaintext alphabets. Check periodic consistency.
    """
    hits = []
    for var_id, var_name, key_fn in [
        (0, "Vig", lambda ci, pi: (ci - pi) % 26),
        (1, "Beau", lambda ci, pi: (pi - ci) % 26),
        (2, "VarBeau", lambda ci, pi: (ci + pi) % 26),
    ]:
        vals = []
        valid = True
        for pos in sorted_pos:
            c = CT[pos]
            p = cribs[pos]
            if c not in ct_alpha or p not in pt_alpha:
                valid = False
                break
            ci = ct_alpha.index(c)
            pi = pt_alpha.index(p)
            vals.append(key_fn(ci, pi))
        if not valid:
            continue

        # Check periodic consistency for periods 2..45
        for period in range(2, 46):
            slots = {}
            ok = True
            redundant = 0
            for pos_idx, pos in enumerate(sorted_pos):
                r = pos % period
                v = vals[pos_idx]
                if r in slots:
                    if slots[r] != v:
                        ok = False
                        break
                    redundant += 1
                else:
                    slots[r] = v
            if ok and redundant >= 7:  # Stricter threshold for significance
                key_str = ""
                for i in range(period):
                    if i in slots:
                        key_str += ct_alpha[slots[i]]  # Key letter in cipher alphabet
                    else:
                        key_str += "?"
                hits.append(f"HIT {label} variant={var_name} period={period} "
                            f"redundant={redundant} key={key_str}")
    return hits


def load_keywords():
    """Load dictionary words + Kryptos-specific words."""
    extra = [
        "KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK", "NORTHEAST",
        "SANBORN", "SHADOW", "LUCID", "MEMORY", "VIRTUALLY", "INVISIBLE",
        "DIGETAL", "INTERPRETATION", "UNDERGRUUND", "LANGLEY", "SLOWLY",
        "DESPARATLY", "IQLUSION", "ENIGMA", "COMPASS", "LODESTONE", "WEBSTER",
        "EGYPT", "CARTER", "TOMB", "LAYER", "POSITION", "COORDINATES",
        "MAGNETIC", "LOCATION", "BURIED", "UNKNOWN", "DELIVER", "MESSAGE",
        "DIGITAL", "SHADING", "ABSENCE", "LIGHT", "SUBTLE", "TRANSMITTED",
        "UNDERGROUND",
    ]
    words = list(extra)
    if os.path.exists(WORDS_FILE):
        with open(WORDS_FILE) as f:
            words += [w.strip().upper() for w in f if 3 <= len(w.strip()) <= 20]
    else:
        print(f"  Warning: {WORDS_FILE} not found. Using only built-in keywords.")
        print(f"  Run the main script first to download the wordlist, or:")
        print(f"  curl -o {WORDS_FILE} {WORDS_FILE}")
    return words


def main():
    t0 = time.time()
    words = load_keywords()

    # Deduplicate alphabets (different keywords can produce the same alphabet)
    seen_alphas = set()
    unique_keyword_alphas = []

    for kw in words:
        kw = kw.strip().upper()
        if not kw.isalpha() or len(kw) < 3:
            continue
        alpha = make_keyed_alphabet(kw)
        if alpha not in seen_alphas:
            seen_alphas.add(alpha)
            unique_keyword_alphas.append((kw, alpha))

    print(f"Unique keyword alphabets: {len(unique_keyword_alphas)}")
    print(f"Crib positions: {ncrib}")
    print()

    all_hits = []

    # ── Quagmire I: mixed PT alphabet, standard CT alphabet ────────────
    print("Testing Quagmire I (mixed plaintext alphabet, standard cipher alphabet)...")
    for kw, alpha in unique_keyword_alphas:
        hits = check_quagmire(AZ, alpha, f"QuagI(pt_kw={kw})")
        all_hits += hits
    print(f"  {len(all_hits)} hits so far")

    # ── Quagmire II: standard PT alphabet, mixed CT alphabet ───────────
    n_before = len(all_hits)
    print("Testing Quagmire II (standard plaintext alphabet, mixed cipher alphabet)...")
    for kw, alpha in unique_keyword_alphas:
        hits = check_quagmire(alpha, AZ, f"QuagII(ct_kw={kw})")
        all_hits += hits
    print(f"  {len(all_hits) - n_before} new hits")

    # ── Quagmire III: same mixed alphabet for both ─────────────────────
    n_before = len(all_hits)
    print("Testing Quagmire III (same mixed alphabet for plaintext and cipher)...")
    for kw, alpha in unique_keyword_alphas:
        hits = check_quagmire(alpha, alpha, f"QuagIII(kw={kw})")
        all_hits += hits
    print(f"  {len(all_hits) - n_before} new hits")

    # ── Quagmire IV: two different mixed alphabets ─────────────────────
    # This is O(n^2) in keywords. We limit to Kryptos-specific keywords only.
    n_before = len(all_hits)
    kryptos_words = [
        "KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK", "NORTHEAST",
        "SANBORN", "SHADOW", "LUCID", "MEMORY", "INVISIBLE", "ENIGMA",
        "COMPASS", "LODESTONE", "EGYPT", "WEBSTER", "LANGLEY", "POSITION",
        "COORDINATES", "MAGNETIC", "UNDERGROUND", "BURIED", "LIGHT",
        "ABSENCE", "SUBTLE", "TRANSMITTED", "DIGITAL", "LAYER",
    ]
    q4_alphas = []
    q4_seen = set()
    for kw in kryptos_words:
        a = make_keyed_alphabet(kw)
        if a not in q4_seen:
            q4_seen.add(a)
            q4_alphas.append((kw, a))

    print(f"Testing Quagmire IV (two different keyword alphabets, {len(q4_alphas)} x {len(unique_keyword_alphas)})...")
    for kw1, alpha1 in q4_alphas:
        for kw2, alpha2 in unique_keyword_alphas:
            if alpha1 == alpha2:
                continue
            hits = check_quagmire(alpha1, alpha2, f"QuagIV(ct={kw1},pt={kw2})")
            all_hits += hits
    print(f"  {len(all_hits) - n_before} new hits")

    elapsed = time.time() - t0
    print(f"\nTotal: {len(all_hits)} hit(s) in {elapsed:.1f}s")

    if all_hits:
        hitfile = os.path.join(HERE, "..", "hits_quagmire.txt")
        with open(hitfile, "w") as f:
            f.write("\n".join(all_hits) + "\n")
        print(f"\nHits written to {hitfile}")
        for h in all_hits[:20]:
            print(f"  {h}")
        if len(all_hits) > 20:
            print(f"  ... and {len(all_hits) - 20} more")
    else:
        print("\nNo hits. Quagmire I/II/III/IV ruled out for tested keywords + periods 2-45.")


if __name__ == "__main__":
    main()
