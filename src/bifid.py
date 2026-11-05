#!/usr/bin/env python3
"""
Bifid and Trifid cipher search for K4.
Tests keyword-ordered Polybius squares × periods 2-45 against the known cribs.

Bifid: 5x5 grid (I/J merged), encode as (row,col), fractionate by period, decode
Trifid: 3x3x3 cube (26 letters + pad), encode as (layer,row,col), fractionate, decode
"""
import os, sys, time
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
K4_FILE = os.path.join(HERE, "..", "k4.txt")
WORDS_FILE = os.path.join(HERE, "words.txt")

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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

# ── Bifid ──────────────────────────────────────────────────────────────

def make_polybius_5x5(keyword):
    """Build a 5x5 Polybius square from a keyword (I/J merged)."""
    seen = set()
    square = []
    for ch in keyword.upper():
        if ch == 'J':
            ch = 'I'
        if ch in seen or ch not in AZ:
            continue
        seen.add(ch)
        square.append(ch)
    for ch in AZ:
        if ch == 'J':
            continue
        if ch not in seen:
            square.append(ch)
    # Build lookup
    pos_of = {}
    for i, ch in enumerate(square):
        pos_of[ch] = (i // 5, i % 5)
    pos_of['J'] = pos_of['I']  # J maps to I
    return square, pos_of


def bifid_decrypt(ciphertext, square, pos_of, period):
    """Decrypt ciphertext using Bifid cipher with given square and period."""
    plaintext = []
    for block_start in range(0, len(ciphertext), period):
        block = ciphertext[block_start:block_start + period]
        blen = len(block)

        # Get row/col coordinates
        rows = []
        cols = []
        for ch in block:
            if ch == 'J':
                ch = 'I'
            if ch not in pos_of:
                return None
            r, c = pos_of[ch]
            rows.append(r)
            cols.append(c)

        # De-fractionate: the original coordinates were interleaved
        # Encryption: take rows+cols, split into pairs → (row,col) → letter
        # Decryption: take (row,col) of each cipher letter → stream = rows+cols
        #   This stream was originally: r0,c0,r1,c1,... → split into first-half=rows, second-half=cols
        #   So to decrypt: stream = rows+cols → re-pair as (stream[0],stream[blen]),...
        stream = rows + cols
        for i in range(blen):
            r2, c2 = stream[i], stream[blen + i]
            idx = r2 * 5 + c2
            if idx >= len(square):
                return None
            plaintext.append(square[idx])

    return plaintext


def check_bifid(square, pos_of, keyword):
    """Test all periods against the cribs."""
    hits = []
    for period in range(2, 46):
        pt = bifid_decrypt(CT, square, pos_of, period)
        if pt is None:
            continue
        # Check against cribs
        matches = 0
        total = 0
        for pos in sorted_pos:
            if pos < len(pt):
                total += 1
                expected = cribs[pos]
                if expected == 'J':
                    expected = 'I'
                actual = pt[pos]
                if actual == expected:
                    matches += 1
        if matches == total and total >= 15:
            hits.append(f"HIT Bifid keyword={keyword} period={period} "
                        f"matches={matches}/{total}")
    return hits


# ── Trifid ─────────────────────────────────────────────────────────────

def make_trifid_cube(keyword, pad_char='+'):
    """Build a 3x3x3 = 27-symbol Trifid cube (26 letters + pad)."""
    seen = set()
    cube = []
    for ch in keyword.upper():
        if ch in seen or ch not in AZ:
            continue
        seen.add(ch)
        cube.append(ch)
    for ch in AZ:
        if ch not in seen:
            cube.append(ch)
    cube.append(pad_char)  # 27th symbol

    pos_of = {}
    for i, ch in enumerate(cube):
        layer = i // 9
        row = (i % 9) // 3
        col = i % 3
        pos_of[ch] = (layer, row, col)
    return cube, pos_of


def trifid_decrypt(ciphertext, cube, pos_of, period):
    """Decrypt using Trifid cipher."""
    plaintext = []
    for block_start in range(0, len(ciphertext), period):
        block = ciphertext[block_start:block_start + period]
        blen = len(block)

        # Get (layer, row, col) for each cipher letter
        layers, rows, cols = [], [], []
        for ch in block:
            if ch not in pos_of:
                return None
            l, r, c = pos_of[ch]
            layers.append(l)
            rows.append(r)
            cols.append(c)

        # De-fractionate: stream = layers + rows + cols
        stream = layers + rows + cols
        # Re-group into triples
        for i in range(blen):
            l2 = stream[i]
            r2 = stream[blen + i]
            c2 = stream[2 * blen + i]
            idx = l2 * 9 + r2 * 3 + c2
            if idx >= len(cube):
                return None
            plaintext.append(cube[idx])

    return plaintext


def check_trifid(cube, pos_of, keyword):
    """Test all periods against the cribs."""
    hits = []
    for period in range(2, 46):
        pt = trifid_decrypt(CT, cube, pos_of, period)
        if pt is None:
            continue
        matches = 0
        total = 0
        for pos in sorted_pos:
            if pos < len(pt):
                total += 1
                expected = cribs[pos]
                actual = pt[pos]
                if actual == expected:
                    matches += 1
        if matches == total and total >= 15:
            hits.append(f"HIT Trifid keyword={keyword} period={period} "
                        f"matches={matches}/{total}")
    return hits


def load_keywords():
    """Load dictionary words + Kryptos-specific words."""
    extra = [
        "", "KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK", "NORTHEAST",
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
        print(f"  Warning: {WORDS_FILE} not found, using built-in keywords only.")
    return words


def main():
    t0 = time.time()
    words = load_keywords()

    # Deduplicate by Polybius square
    seen_squares = set()
    unique_kws = []
    for kw in words:
        kw = kw.strip().upper() if kw else ""
        if kw and not kw.isalpha():
            continue
        square, pos_of = make_polybius_5x5(kw if kw else "A")
        sq_key = "".join(square)
        if sq_key not in seen_squares:
            seen_squares.add(sq_key)
            unique_kws.append(kw if kw else "(standard)")

    print(f"Unique Polybius squares: {len(unique_kws)}")
    print(f"Crib positions: {ncrib}")
    print()

    all_hits = []

    # ── Bifid ──────────────────────────────────────────────────────────
    print("Testing Bifid cipher (5x5 Polybius × periods 2-45)...")
    for i, kw in enumerate(unique_kws):
        actual_kw = kw if kw != "(standard)" else ""
        square, pos_of = make_polybius_5x5(actual_kw if actual_kw else "A")
        hits = check_bifid(square, pos_of, kw)
        all_hits += hits
        if (i + 1) % 10000 == 0:
            print(f"  {i + 1}/{len(unique_kws)} keywords tested...")

    print(f"  Bifid: {len(all_hits)} hit(s)")

    # ── Trifid ─────────────────────────────────────────────────────────
    n_before = len(all_hits)
    print("Testing Trifid cipher (3x3x3 cube × periods 2-45)...")
    seen_cubes = set()
    for i, kw in enumerate(unique_kws):
        actual_kw = kw if kw != "(standard)" else ""
        cube, pos_of = make_trifid_cube(actual_kw if actual_kw else "A")
        cube_key = "".join(cube)
        if cube_key in seen_cubes:
            continue
        seen_cubes.add(cube_key)
        hits = check_trifid(cube, pos_of, kw)
        all_hits += hits
        if (i + 1) % 10000 == 0:
            print(f"  {i + 1}/{len(unique_kws)} keywords tested...")

    print(f"  Trifid: {len(all_hits) - n_before} hit(s)")

    elapsed = time.time() - t0
    print(f"\nTotal: {len(all_hits)} hit(s) in {elapsed:.1f}s")

    if all_hits:
        hitfile = os.path.join(HERE, "..", "hits_bifid.txt")
        with open(hitfile, "w") as f:
            f.write("\n".join(all_hits) + "\n")
        print(f"\nHits written to {hitfile}")
        for h in all_hits[:20]:
            print(f"  {h}")
    else:
        print("\nNo hits. Bifid and Trifid ruled out for tested keyword squares + periods 2-45.")


if __name__ == "__main__":
    main()
