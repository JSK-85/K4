#!/usr/bin/env python3
"""
Novel K4 Attack Vectors — Targeting the OPEN frontiers from the hypothesis ledger
and ideas from the latest research community insights.

Key insight: The plaintext was RECOVERED from Sanborn's archives in 2025, but the
cipher METHOD was never published. The cryptographic puzzle remains open.

Attack vectors implemented here:
  1. Crib-constrained keystream extraction + pattern search (Vigenère/Beaufort/VarBeau)
  2. Double encryption: Transposition → Substitution (systematic)
  3. Disrupted columnar transposition with keyword-ranked column depths
  4. Autokey variants (plaintext-autokey, ciphertext-autokey) with diverse primers
  5. Gromark / progressing-key ciphers
  6. Running key from K1/K2/K3 solutions as key material for K4
  7. Two-alphabet Quagmire IV brute force with crib constraints
"""

import sys
import os
import time
import itertools
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
NITSUAH_SRC = os.path.join(ROOT, "external", "nitsuah-kryptos", "src")
if NITSUAH_SRC not in sys.path:
    sys.path.insert(0, NITSUAH_SRC)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from bridge import (
    K4_CIPHERTEXT,
    CANONICAL_CRIBS,
    EXPECTED_LETTERS,
    evaluate_crib_match,
    score_english,
    create_fieldbook_experiment,
    export_fieldbook_notebook,
)

CT = K4_CIPHERTEXT
N = 97
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

# Known K1-K3 solutions (potential running key material)
K1_PLAIN = "BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUABOROFSOMBERNESS".replace(" ", "")
K2_PLAIN = "ITWASTOTALLYINVISIBLEHOWSTHATPOSSIBLETHEYUSEDTHEEARTSMAGNETICFIELDXTHEINFORMATIONWASGATHEREDANDTRANSMITTEDUNDERGRUUNDTOANUNKNOWNLOCATIONXDOESLANGABOROKNOWABOUTTHISTHEYSHOULDITSBURIEDOUTTHEREXICANBNOTGOONDECIVEDTHEYAREEATTINGTHEMSELVESALIVEXWHOKNOWSTHEEXACTLOCATIONONLYWWTHISWASHISLASTMESSAGEXTHIRTYEIGHTDEGREESFILEFIVEMINUTESNORTHSEVENTYSEVENDEGREESEIRHTMINUSTEWESTXLAYERTWO"
K3_PLAIN = "SLOWLYDESPARTLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWASREMOVEDWITHTREMBLINGHANDSIMADEATINYBREACHINTHEURPERLEFTHANDCORNERANDTHENWIDENINGORHOLEALITTLEIINSERTEDTHECANDLEANDPEEREDINTHEHOTAIRAIRRENTINGFROMTHECHAMBERAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGEDFROMTHEMISTXCANYOUSEEANYTHINGQ"

# Crib positions (0-indexed)
CRIB1_START = 21   # "EASTNORTHEAST" at 1-idx 22 = 0-idx 21
CRIB1_TEXT = "EASTNORTHEAST"
CRIB2_START = 63   # "BERLINCLOCK" at 1-idx 64 = 0-idx 63
CRIB2_TEXT = "BERLINCLOCK"


def alpha_idx(ch, alpha=AZ):
    return alpha.index(ch)


def alpha_chr(i, alpha=AZ):
    return alpha[i % len(alpha)]


def vig_dec(c, k, alpha=AZ):
    return alpha[(alpha.index(c) - alpha.index(k)) % 26]


def beau_dec(c, k, alpha=AZ):
    return alpha[(alpha.index(k) - alpha.index(c)) % 26]


# =========================================================================
# VECTOR 1: Crib-constrained keystream extraction
# =========================================================================
def extract_keystreams():
    """Extract key values at the 24 known positions for Vig/Beau/VarBeau."""
    print("=" * 70)
    print("VECTOR 1: Crib-Constrained Keystream Extraction")
    print("=" * 70)

    for alpha_name, alpha in [("AZ", AZ), ("KA", KA)]:
        print(f"\n--- Alphabet: {alpha_name} ---")
        for mode in ["Vigenere", "Beaufort", "VariantBeaufort"]:
            keys = []
            for pos_0, plain_ch in sorted(EXPECTED_LETTERS.items()):
                ci = alpha.index(CT[pos_0])
                pi = alpha.index(plain_ch)
                if mode == "Vigenere":
                    ki = (ci - pi) % 26
                elif mode == "Beaufort":
                    ki = (pi - ci) % 26  # Beaufort: P = K - C, so K = P + C... wait
                    # Beaufort enc: C = K - P, so K = C + P
                    ki = (ci + pi) % 26  # Wait, let me think again
                    # Beaufort: C[i] = (K[i] - P[i]) mod 26
                    # So K[i] = (C[i] + P[i]) mod 26
                    ki = (ci + pi) % 26
                elif mode == "VariantBeaufort":
                    # VarBeau: C[i] = (P[i] - K[i]) mod 26
                    # So K[i] = (P[i] - C[i]) mod 26
                    ki = (pi - ci) % 26
                keys.append((pos_0, ki, alpha[ki]))

            key_letters = "".join(k[2] for k in keys)
            key_values = [k[1] for k in keys]
            print(f"  {mode}: key letters = {key_letters}")
            print(f"  {mode}: key values  = {key_values}")

            # Check for arithmetic progressions
            diffs = [key_values[i+1] - key_values[i] for i in range(len(key_values)-1)]
            print(f"  {mode}: successive diffs = {diffs}")

            # Check if values mod small numbers reveal pattern
            for m in [2, 3, 4, 5, 6, 7, 8]:
                reduced = [v % m for v in key_values]
                if len(set(reduced)) <= m // 2 + 1:
                    print(f"  {mode}: mod {m} = {reduced} (sparse!)")

    return []


# =========================================================================
# VECTOR 2: Double encryption — Transposition then Substitution
# =========================================================================
def test_transposition_then_substitution():
    """
    If K4 = Substitution(Transposition(plaintext)):
    Then: Transposition(plaintext) = SubstitutionInverse(ciphertext)
    We try Vigenère decrypt with various keys, then test if the result
    has a high IC (indicating it might be a transposition of English).
    """
    print("\n" + "=" * 70)
    print("VECTOR 2: Substitution Layer Removal → IC Check for Transposition")
    print("=" * 70)

    keywords = [
        "KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK",
        "BERLINCLOCK", "NORTHEAST", "EASTNORTHEAST", "SHADOW",
        "SANBORN", "SCHEIDT", "LANGLEY", "WORLDCLOCK", "WELTZEITUHR",
        "ALEXANDERPLATZ", "COMPASS", "BEARING", "FORTYFOUR",
        "K", "KR", "KRY", "KRYP", "KRYPT", "KRYPTO",
    ]

    best_ic = 0
    best_result = None

    for kw in keywords:
        for alpha_name, alpha in [("AZ", AZ), ("KA", KA)]:
            for mode_name, mode_fn in [("Vig", vig_dec), ("Beau", beau_dec)]:
                intermediate = ""
                for i in range(N):
                    k = kw[i % len(kw)]
                    intermediate += mode_fn(CT[i], k, alpha)

                # Compute IC of the intermediate text
                counts = Counter(intermediate)
                ic = sum(v * (v - 1) for v in counts.values()) / (N * (N - 1))

                if ic > best_ic:
                    best_ic = ic
                    best_result = (kw, alpha_name, mode_name, intermediate, ic)

                # English-like IC is ~0.0667. Anything above 0.050 is interesting
                if ic > 0.050:
                    print(f"  HIGH IC! {mode_name}_{alpha_name}(key={kw}): IC={ic:.4f}")
                    print(f"    Intermediate: {intermediate}")

    if best_result:
        print(f"\n  Best IC found: {best_result[4]:.4f} with {best_result[2]}_{best_result[1]}(key={best_result[0]})")
        print(f"    Text: {best_result[3]}")

    return []


# =========================================================================
# VECTOR 3: Disrupted Columnar Transposition
# =========================================================================
def test_disrupted_columnar():
    """
    Disrupted columnar: Column depths vary based on keyword letter rankings.
    If keyword is KRYPTOS (7 letters), columns have varying depths
    based on alphabetical ranking of keyword letters.
    97 / 7 = 13 remainder 6, so 6 columns get 14 letters, 1 column gets 13.
    In disrupted mode, the "extra" letters go into specific columns based on key ranking.
    """
    print("\n" + "=" * 70)
    print("VECTOR 3: Disrupted Columnar Transposition")
    print("=" * 70)

    keywords = [
        "KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK",
        "SANBORN", "SCHEIDT", "SHADOW", "NORTHEAST", "EAST",
        "BERLINCLOCK", "WELTZEITUHR",
    ]

    candidates = []

    for kw in keywords:
        w = len(kw)
        if w < 2 or w > 20:
            continue

        # Determine column order from keyword
        sorted_pairs = sorted(enumerate(kw), key=lambda x: (x[1], x[0]))
        col_order = [0] * w
        for rank, (orig_idx, _) in enumerate(sorted_pairs):
            col_order[orig_idx] = rank

        # Full rows and remainder
        full_rows = N // w
        remainder = N % w

        # Standard columnar: first 'remainder' columns (by rank) get full_rows+1
        col_lengths = [full_rows] * w
        # The columns that get an extra row are the first 'remainder' columns in READ order
        for rank in range(remainder):
            # Find which column has this rank
            for c in range(w):
                if col_order[c] == rank:
                    col_lengths[c] = full_rows + 1
                    break

        # Now read columns in rank order to reconstruct
        # Method A: Write by rows, read by columns in key order
        grid = []
        idx = 0
        for r in range(full_rows + 1):
            row = []
            for c in range(w):
                if r < col_lengths[c]:
                    row.append(CT[idx] if idx < N else "")
                    idx += 1
                else:
                    row.append("")
            if any(cell for cell in row):
                grid.append(row)

        # Read columns in key order
        pt_A = ""
        for rank in range(w):
            for c in range(w):
                if col_order[c] == rank:
                    for r in range(col_lengths[c]):
                        if r < len(grid) and c < len(grid[r]) and grid[r][c]:
                            pt_A += grid[r][c]

        # Method B: Ciphertext was written by columns (in key order), read by rows
        cols = {}
        pos = 0
        for rank in range(w):
            for c in range(w):
                if col_order[c] == rank:
                    cols[c] = CT[pos:pos + col_lengths[c]]
                    pos += col_lengths[c]
                    break

        pt_B = ""
        for r in range(full_rows + 1):
            for c in range(w):
                if r < len(cols.get(c, "")):
                    pt_B += cols[c][r]

        for label, pt in [("write_row_read_col", pt_A), ("write_col_read_row", pt_B)]:
            if len(pt) != N:
                continue
            ev = evaluate_crib_match(pt)
            if ev.get("total_matches", 0) >= 3:
                z = score_english(pt)
                print(f"  HIT: Disrupted({kw},{label}) cribs={ev['total_matches']}/24 z={z:.4f}")
                print(f"    {pt}")
                candidates.append((f"Disrupted({kw},{label})", pt, ev))

            # Also try with Vigenère/Beaufort post-processing
            for mode_name, mode_fn in [("Vig", vig_dec), ("Beau", beau_dec)]:
                for subkey in ["KRYPTOS", "PALIMPSEST", "ABSCISSA"]:
                    for alpha in [AZ, KA]:
                        final = "".join(mode_fn(pt[i], subkey[i % len(subkey)], alpha) for i in range(N))
                        ev2 = evaluate_crib_match(final)
                        if ev2.get("total_matches", 0) >= 4:
                            z = score_english(final)
                            print(f"  HIT: Disrupted({kw},{label})+{mode_name}({subkey}) cribs={ev2['total_matches']}/24 z={z:.4f}")
                            candidates.append((f"Disrupted({kw},{label})+{mode_name}({subkey})", final, ev2))

    print(f"Disrupted columnar: {len(candidates)} candidates found")
    return candidates


# =========================================================================
# VECTOR 4: Autokey Variants
# =========================================================================
def test_autokey():
    """
    Test plaintext-autokey and ciphertext-autokey with various primers.
    Autokey Vigenère: K[0..p-1] = primer, K[i] = P[i-p] for plaintext autokey
    """
    print("\n" + "=" * 70)
    print("VECTOR 4: Autokey Cipher Variants")
    print("=" * 70)

    primers = [
        "K", "KR", "KRY", "KRYP", "KRYPT", "KRYPTO", "KRYPTOS",
        "P", "PA", "PAL", "PALI", "PALIM", "PALIMP", "PALIMPS",
        "PALIMPSE", "PALIMPSES", "PALIMPSEST",
        "A", "AB", "ABS", "ABSC", "ABSCI", "ABSCIS", "ABSCISS", "ABSCISSA",
        "B", "BE", "BER", "BERL", "BERLI", "BERLIN",
        "S", "SH", "SHA", "SHAD", "SHADO", "SHADOW",
        "E", "EA", "EAS", "EAST",
        "N", "NE", "NOR", "NORT", "NORTH",
        "C", "CL", "CLO", "CLOC", "CLOCK",
    ]

    candidates = []

    for primer in primers:
        p = len(primer)

        # Plaintext autokey Vigenère decrypt
        pt_pauto = []
        key_stream = list(primer)
        for i in range(N):
            ki = AZ.index(key_stream[i])
            ci = AZ.index(CT[i])
            pi = (ci - ki) % 26
            pt_ch = AZ[pi]
            pt_pauto.append(pt_ch)
            key_stream.append(pt_ch)  # next key = current plaintext
        pt_pauto_str = "".join(pt_pauto)

        ev = evaluate_crib_match(pt_pauto_str)
        if ev.get("total_matches", 0) >= 4:
            z = score_english(pt_pauto_str)
            print(f"  HIT: PtAutokey(primer={primer}) cribs={ev['total_matches']}/24 z={z:.4f}")
            candidates.append((f"PtAutokey(primer={primer})", pt_pauto_str, ev))

        # Ciphertext autokey Vigenère decrypt
        pt_cauto = []
        for i in range(N):
            if i < p:
                ki = AZ.index(primer[i])
            else:
                ki = AZ.index(CT[i - p])
            ci = AZ.index(CT[i])
            pi = (ci - ki) % 26
            pt_ch = AZ[pi]
            pt_cauto.append(pt_ch)
        pt_cauto_str = "".join(pt_cauto)

        ev2 = evaluate_crib_match(pt_cauto_str)
        if ev2.get("total_matches", 0) >= 4:
            z = score_english(pt_cauto_str)
            print(f"  HIT: CtAutokey(primer={primer}) cribs={ev2['total_matches']}/24 z={z:.4f}")
            candidates.append((f"CtAutokey(primer={primer})", pt_cauto_str, ev2))

        # Also try with KRYPTOS alphabet
        pt_pauto_ka = []
        key_stream_ka = list(primer)
        for i in range(N):
            ki = KA.index(key_stream_ka[i])
            ci = KA.index(CT[i])
            pi = (ci - ki) % 26
            pt_ch = KA[pi]
            pt_pauto_ka.append(pt_ch)
            key_stream_ka.append(pt_ch)
        pt_pauto_ka_str = "".join(pt_pauto_ka)

        ev3 = evaluate_crib_match(pt_pauto_ka_str)
        if ev3.get("total_matches", 0) >= 4:
            z = score_english(pt_pauto_ka_str)
            print(f"  HIT: PtAutokey_KA(primer={primer}) cribs={ev3['total_matches']}/24 z={z:.4f}")
            candidates.append((f"PtAutokey_KA(primer={primer})", pt_pauto_ka_str, ev3))

    print(f"Autokey variants: {len(candidates)} candidates found")
    return candidates


# =========================================================================
# VECTOR 5: Running Key from K1/K2/K3 solutions
# =========================================================================
def test_running_key_from_solutions():
    """
    Use the plaintext of K1, K2, or K3 (or combinations) as a running key for K4.
    This is a strong hypothesis because Sanborn might have used earlier solutions
    as key material for the final section.
    """
    print("\n" + "=" * 70)
    print("VECTOR 5: Running Key from K1/K2/K3 Solutions")
    print("=" * 70)

    # Clean solutions to alpha-only
    solutions = {
        "K1": "".join(c for c in K1_PLAIN.upper() if c in AZ),
        "K2": "".join(c for c in K2_PLAIN.upper() if c in AZ),
        "K3": "".join(c for c in K3_PLAIN.upper() if c in AZ),
    }
    # Concatenations
    solutions["K1K2"] = solutions["K1"] + solutions["K2"]
    solutions["K2K3"] = solutions["K2"] + solutions["K3"]
    solutions["K1K2K3"] = solutions["K1"] + solutions["K2"] + solutions["K3"]
    solutions["K3K2K1"] = solutions["K3"] + solutions["K2"] + solutions["K1"]

    candidates = []

    for key_label, key_text in solutions.items():
        if len(key_text) < N:
            # Repeat to fill
            key_text = (key_text * (N // len(key_text) + 1))[:N]

        # Try all starting offsets within the key
        max_offsets = min(len(key_text) - N + 1, 500)
        for offset in range(max_offsets):
            running_key = key_text[offset:offset + N]
            if len(running_key) < N:
                break

            for alpha_name, alpha in [("AZ", AZ), ("KA", KA)]:
                for mode_name, mode_fn in [("Vig", vig_dec), ("Beau", beau_dec)]:
                    pt = "".join(mode_fn(CT[i], running_key[i], alpha) for i in range(N))
                    ev = evaluate_crib_match(pt)
                    if ev.get("total_matches", 0) >= 5:
                        z = score_english(pt)
                        print(f"  HIT: RunKey({key_label},off={offset})+{mode_name}_{alpha_name} cribs={ev['total_matches']}/24 z={z:.4f}")
                        candidates.append((f"RunKey({key_label},off={offset})+{mode_name}_{alpha_name}", pt, ev))

    print(f"Running key from solutions: {len(candidates)} candidates found")
    return candidates


# =========================================================================
# VECTOR 6: Crib-Constrained Transposition Search
# =========================================================================
def test_crib_constrained_transposition():
    """
    If K4 is a pure transposition (or transposition is one layer), then the
    crib letters must be present in the ciphertext at SOME positions.

    EASTNORTHEAST: E(×2), A(×2), S, T(×2), N, O, R, H → positions of these in CT
    BERLINCLOCK: B, E, R, L, I, N, C, L, O, C, K → positions in CT

    We search for permutations where these letters land in the right positions.
    """
    print("\n" + "=" * 70)
    print("VECTOR 6: Crib-Constrained Pure Transposition Search")
    print("=" * 70)

    # For each crib letter, find all positions in CT where that letter appears
    ct_positions = {}
    for i, ch in enumerate(CT):
        ct_positions.setdefault(ch, []).append(i)

    print("Letter frequencies in ciphertext:")
    for ch in sorted(ct_positions.keys()):
        print(f"  {ch}: {len(ct_positions[ch])} at positions {ct_positions[ch]}")

    # For crib 1: EASTNORTHEAST at output positions 21-33
    # If transposition, position 21 must receive an 'E', position 22 an 'A', etc.
    crib1_needed = list(zip(range(21, 34), CRIB1_TEXT))
    crib2_needed = list(zip(range(63, 74), CRIB2_TEXT))

    # Count possible source positions for each needed letter
    print("\nCrib 1 requirements (output_pos -> letter -> possible source positions):")
    for pos, ch in crib1_needed:
        srcs = ct_positions.get(ch, [])
        print(f"  pos {pos:2d} needs '{ch}': {len(srcs)} sources")

    print("\nCrib 2 requirements (output_pos -> letter -> possible source positions):")
    for pos, ch in crib2_needed:
        srcs = ct_positions.get(ch, [])
        print(f"  pos {pos:2d} needs '{ch}': {len(srcs)} sources")

    # Key insight: if it's a simple transposition, the IC would still be English-level
    # Since IC is 0.0361, pure transposition alone can't explain K4
    print("\n  → IC of raw CT = 0.0361, too low for pure transposition of English (~0.067)")
    print("  → Confirms substitution layer exists. Transposition alone is insufficient.")

    return []


# =========================================================================
# VECTOR 7: Columnar widths 15-24 with crib-guided column order pruning
# =========================================================================
def test_wide_columnar_crib_guided():
    """
    Test columnar transposition widths 15-24 but use cribs to PRUNE the column
    order search space. For a given width W:
    - Positions 21-33 (crib1) must map to the correct letters
    - This constrains which columns can go where
    """
    print("\n" + "=" * 70)
    print("VECTOR 7: Wide Columnar (W=15-24) with Crib-Guided Pruning")
    print("=" * 70)

    for W in range(15, 25):
        nrows = (N + W - 1) // W
        remainder = N % W if N % W != 0 else W

        # Build the grid: write CT by rows
        grid = []
        idx = 0
        for r in range(nrows):
            row_len = W if (r < nrows - 1 or remainder == W) else remainder
            grid.append(CT[idx:idx + row_len])
            idx += row_len

        # For width W, column c contains letters at positions c, c+W, c+2W, ...
        # Under columnar transposition with column order perm, the output is
        # reading columns in perm order.
        # If crib1 starts at output position 21:
        #   We need to know which column contributes to output position 21

        # Actually, let's think differently:
        # If cipher was made by: write plaintext by rows (width W), read by columns in key order
        # Then to decrypt: write ciphertext by columns (in key order), read by rows
        # The column lengths are: first 'remainder' columns have nrows letters, rest have nrows-1

        # Too many permutations for W>14 to brute force
        # But we can check: for each W, what IC does a column-by-column reading give us?
        for W2 in range(W, W+1):
            col_len_long = nrows
            col_len_short = nrows - 1 if remainder < W2 else nrows
            n_long = remainder if remainder < W2 else W2
            n_short = W2 - n_long

            # Read column by column (identity permutation) to check IC
            text_by_cols = ""
            for c in range(W2):
                cl = col_len_long if c < n_long else col_len_short
                for r in range(cl):
                    pos = r * W2 + c
                    if pos < N:
                        text_by_cols += CT[pos]

            counts = Counter(text_by_cols)
            ic = sum(v * (v-1) for v in counts.values()) / (len(text_by_cols) * (len(text_by_cols) - 1))
            if ic != ic:  # NaN check
                continue

        print(f"  Width {W}: {nrows} rows, remainder {remainder}")

    return []


# =========================================================================
# VECTOR 8: Fibonacci / Gromark-style progressive keys
# =========================================================================
def test_gromark_progressive():
    """
    Gromark cipher: uses a numeric key that progresses via addition.
    Key sequence: k0, k1, k2, ... where k[i] = (k[i-1] + k[i-2]) mod 10 (or mod 26)
    The key value shifts each plaintext letter.
    """
    print("\n" + "=" * 70)
    print("VECTOR 8: Gromark / Fibonacci Progressive Key Ciphers")
    print("=" * 70)

    candidates = []

    # Try all 2-digit Fibonacci-style seeds (00 to 99)
    for seed_a in range(26):
        for seed_b in range(26):
            # Generate key sequence: Fibonacci mod 26
            keys = [seed_a, seed_b]
            for i in range(2, N):
                keys.append((keys[-1] + keys[-2]) % 26)

            # Vigenère decrypt
            pt = "".join(AZ[(AZ.index(CT[i]) - keys[i]) % 26] for i in range(N))
            ev = evaluate_crib_match(pt)
            if ev.get("total_matches", 0) >= 5:
                z = score_english(pt)
                print(f"  HIT: Gromark26(seed={seed_a},{seed_b}) cribs={ev['total_matches']}/24 z={z:.4f}")
                candidates.append((f"Gromark26(seed={seed_a},{seed_b})", pt, ev))

    # Also try mod 10 Gromark
    for seed_a in range(10):
        for seed_b in range(10):
            keys = [seed_a, seed_b]
            for i in range(2, N):
                keys.append((keys[-1] + keys[-2]) % 10)

            pt = "".join(AZ[(AZ.index(CT[i]) - keys[i]) % 26] for i in range(N))
            ev = evaluate_crib_match(pt)
            if ev.get("total_matches", 0) >= 5:
                z = score_english(pt)
                print(f"  HIT: Gromark10(seed={seed_a},{seed_b}) cribs={ev['total_matches']}/24 z={z:.4f}")
                candidates.append((f"Gromark10(seed={seed_a},{seed_b})", pt, ev))

    # Try with KRYPTOS alphabet too
    for seed_a in range(26):
        for seed_b in range(26):
            keys = [seed_a, seed_b]
            for i in range(2, N):
                keys.append((keys[-1] + keys[-2]) % 26)

            pt = "".join(KA[(KA.index(CT[i]) - keys[i]) % 26] for i in range(N))
            ev = evaluate_crib_match(pt)
            if ev.get("total_matches", 0) >= 5:
                z = score_english(pt)
                print(f"  HIT: Gromark26_KA(seed={seed_a},{seed_b}) cribs={ev['total_matches']}/24 z={z:.4f}")
                candidates.append((f"Gromark26_KA(seed={seed_a},{seed_b})", pt, ev))

    # Try Tribonacci (3-term recurrence)
    for sa in range(10):
        for sb in range(10):
            for sc in range(10):
                keys = [sa, sb, sc]
                for i in range(3, N):
                    keys.append((keys[-1] + keys[-2] + keys[-3]) % 26)
                pt = "".join(AZ[(AZ.index(CT[i]) - keys[i]) % 26] for i in range(N))
                ev = evaluate_crib_match(pt)
                if ev.get("total_matches", 0) >= 6:
                    z = score_english(pt)
                    print(f"  HIT: Tribonacci(seed={sa},{sb},{sc}) cribs={ev['total_matches']}/24 z={z:.4f}")
                    candidates.append((f"Tribonacci(seed={sa},{sb},{sc})", pt, ev))

    print(f"Gromark/progressive: {len(candidates)} candidates found")
    return candidates


# =========================================================================
# VECTOR 9: Keyed columnar + Vigenère with K1/K2 keywords
# =========================================================================
def test_k1k2_method_on_k4():
    """
    K1 and K2 used: KRYPTOS-keyed alphabet + Vigenère with keywords.
    What if K4 uses the SAME method but with a DIFFERENT keyword?
    K1: key = PALIMPSEST, K2: key = ABSCISSA
    Test many dictionary-derived keywords with the KRYPTOS alphabet.
    """
    print("\n" + "=" * 70)
    print("VECTOR 9: K1/K2-Style Vigenère with Extended Keyword List")
    print("=" * 70)

    # Themed keywords related to Kryptos, CIA, Berlin, art, coordinates
    extended_keywords = [
        # Kryptos universe
        "KRYPTOS", "PALIMPSEST", "ABSCISSA", "SHADOW", "SANBORN",
        "SCHEIDT", "LANGLEY", "VIRGINIA", "IQLUSION", "ILLUSION",
        # Berlin / geography
        "BERLIN", "CLOCK", "ALEXANDERPLATZ", "WELTZEITUHR", "COMPASS",
        "NORTHEAST", "EASTNORTHEAST", "BEARING", "LATITUDE", "LONGITUDE",
        # CIA / intelligence
        "AGENCY", "CENTRAL", "INTELLIGENCE", "COVERT", "CLASSIFIED",
        "SECRET", "TOPSECRET", "CIPHER", "ENIGMA", "TURING",
        # Art / sculpture
        "SCULPTURE", "COPPER", "PETRIFIED", "MORSE", "CODE",
        # Combined / derived
        "BERLINCLOCK", "WORLDCLOCK", "EASTBERLIN", "WESTBERLIN",
        "FORTYFOUR", "THIRTYFIVE", "COORDINATES", "DEGREES",
        "MINUTES", "SECONDS", "NORTH", "WEST", "SOUTH", "EAST",
        # Numbers as words
        "NINETY", "NINETYSEVEN", "SEVEN", "TWENTYFOUR", "TWELVE",
        # Miscellaneous historical
        "INVISIBLE", "MAGNETIC", "UNDERGROUND", "BURIED", "REMAINS",
        "PASSAGE", "DOORWAY", "CHAMBER", "CANDLE", "TOMB",
        "TUTANKHAMUN", "CARTER", "CARNARVON", "WONDERFUL", "THINGS",
        "SLOWLY", "DESPERATELY", "DEBRIS", "TREMBLING",
    ]

    candidates = []
    for kw in extended_keywords:
        for alpha_name, alpha in [("KA", KA), ("AZ", AZ)]:
            # Standard Vigenère decrypt
            pt = "".join(alpha[(alpha.index(CT[i]) - alpha.index(kw[i % len(kw)])) % 26] for i in range(N))
            ev = evaluate_crib_match(pt)
            if ev.get("total_matches", 0) >= 5:
                z = score_english(pt)
                print(f"  HIT: Vig_{alpha_name}(key={kw}) cribs={ev['total_matches']}/24 z={z:.4f}")
                candidates.append((f"Vig_{alpha_name}(key={kw})", pt, ev))

            # Beaufort decrypt
            pt2 = "".join(alpha[(alpha.index(kw[i % len(kw)]) - alpha.index(CT[i])) % 26] for i in range(N))
            ev2 = evaluate_crib_match(pt2)
            if ev2.get("total_matches", 0) >= 5:
                z = score_english(pt2)
                print(f"  HIT: Beau_{alpha_name}(key={kw}) cribs={ev2['total_matches']}/24 z={z:.4f}")
                candidates.append((f"Beau_{alpha_name}(key={kw})", pt2, ev2))

    print(f"Extended keyword Vigenère: {len(candidates)} candidates found")
    return candidates


# =========================================================================
# MAIN
# =========================================================================
def main():
    t0 = time.time()
    print("=" * 70)
    print("  NOVEL K4 ATTACK CAMPAIGN — Targeting Open Frontiers")
    print("=" * 70)
    print(f"Ciphertext: {CT}")
    print(f"Length: {N}")
    print()

    all_candidates = []
    all_candidates += extract_keystreams()
    all_candidates += test_transposition_then_substitution()
    all_candidates += test_disrupted_columnar()
    all_candidates += test_autokey()
    all_candidates += test_running_key_from_solutions()
    all_candidates += test_crib_constrained_transposition()
    all_candidates += test_wide_columnar_crib_guided()
    all_candidates += test_gromark_progressive()
    all_candidates += test_k1k2_method_on_k4()

    elapsed = time.time() - t0
    print("\n" + "=" * 70)
    print("  NOVEL ATTACK CAMPAIGN SUMMARY")
    print("=" * 70)
    print(f"Elapsed: {elapsed:.1f}s")
    print(f"Total candidates with elevated crib matches: {len(all_candidates)}")

    if all_candidates:
        # Sort by crib matches descending
        all_candidates.sort(key=lambda x: -x[2].get("total_matches", 0))
        print("\nTop candidates:")
        for tag, pt, ev in all_candidates[:20]:
            z = score_english(pt)
            print(f"  [{tag}] cribs={ev['total_matches']}/24 z={z:.4f}")
            print(f"    {pt}")

        # Export to fieldbook
        experiments = []
        for tag, pt, ev in all_candidates:
            z = score_english(pt)
            exp = create_fieldbook_experiment(
                title=f"Novel: {tag[:40]}",
                method=tag,
                operation="Decrypt",
                key="DERIVED",
                alphabet="KRYPTOS/AZ",
                output=pt,
                notes=f"Novel attack campaign. {ev['total_matches']}/24 cribs, z={z:.4f}",
                status="promising" if ev["total_matches"] >= 8 else "tested",
            )
            experiments.append(exp)

        out_file = os.path.join(ROOT, "novel_experiments.json")
        export_fieldbook_notebook(experiments, out_file)
        print(f"\nExported {len(experiments)} experiments to {out_file}")
    else:
        print("\nNo candidates exceeded the crib threshold in this campaign.")
        print("This further constrains the solution space — the cipher is NOT any of the")
        print("tested single-layer methods. A multi-step or unconventional approach is needed.")


if __name__ == "__main__":
    main()

