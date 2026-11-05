#!/usr/bin/env python3
"""
Playfair / Four-Square / Two-Square cipher search for K4.
Tests keyword-ordered 5x5 grids against the known cribs.
"""
import os, sys, time

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
            cribs[pos - 1 + i] = ch

sorted_pos = sorted(cribs.keys())
ncrib = len(sorted_pos)


def make_grid(keyword):
    """Build a 5x5 Playfair grid from keyword (I/J merged)."""
    seen = set()
    grid = []
    for ch in keyword.upper():
        if ch == 'J':
            ch = 'I'
        if ch in seen or ch not in AZ:
            continue
        seen.add(ch)
        grid.append(ch)
    for ch in AZ:
        if ch == 'J':
            continue
        if ch not in seen:
            grid.append(ch)
    # Position lookup
    pos_of = {}
    for i, ch in enumerate(grid):
        pos_of[ch] = (i // 5, i % 5)
    pos_of['J'] = pos_of['I']
    return grid, pos_of


def playfair_decrypt_pair(c1, c2, grid, pos_of):
    """Decrypt a Playfair digraph."""
    if c1 == 'J': c1 = 'I'
    if c2 == 'J': c2 = 'I'
    r1, c1p = pos_of[c1]
    r2, c2p = pos_of[c2]

    if r1 == r2:
        # Same row: shift left
        p1 = grid[r1 * 5 + (c1p - 1) % 5]
        p2 = grid[r2 * 5 + (c2p - 1) % 5]
    elif c1p == c2p:
        # Same column: shift up
        p1 = grid[((r1 - 1) % 5) * 5 + c1p]
        p2 = grid[((r2 - 1) % 5) * 5 + c2p]
    else:
        # Rectangle: swap columns
        p1 = grid[r1 * 5 + c2p]
        p2 = grid[r2 * 5 + c1p]

    return p1, p2


def check_playfair(grid, pos_of, keyword):
    """
    Decrypt the ciphertext as Playfair (taking digraphs from consecutive positions)
    and check against all cribs.
    """
    hits = []

    # Standard Playfair: consecutive pairs (0,1), (2,3), ...
    for offset in range(2):  # Try starting at position 0 and 1
        plaintext = [None] * N
        for i in range(offset, N - 1, 2):
            p1, p2 = playfair_decrypt_pair(CT[i], CT[i + 1], grid, pos_of)
            plaintext[i] = p1
            plaintext[i + 1] = p2

        matches = 0
        total = 0
        for pos in sorted_pos:
            if plaintext[pos] is not None:
                total += 1
                expected = cribs[pos]
                if expected == 'J':
                    expected = 'I'
                if plaintext[pos] == expected:
                    matches += 1

        if matches == total and total >= 15:
            hits.append(f"HIT Playfair keyword={keyword} offset={offset} "
                        f"matches={matches}/{total}")

    return hits


def check_foursquare(grid1, pos_of1, kw1, grid2, pos_of2, kw2):
    """
    Four-square cipher decrypt.
    Standard alphabet in TL and BR quadrants, keyed alphabets in TR (grid1) and BL (grid2).
    Digraphs: (PT[0],PT[1]) → look up positions in standard grid → form rectangle → CT from keyed grids.
    To decrypt: CT digraph → find CT[0] in grid1 (TR), CT[1] in grid2 (BL) → rectangle → PT from standard grid.
    """
    std_grid, std_pos = make_grid("")
    hits = []

    for offset in range(2):
        plaintext = [None] * N
        for i in range(offset, N - 1, 2):
            c1, c2 = CT[i], CT[i + 1]
            if c1 == 'J': c1 = 'I'
            if c2 == 'J': c2 = 'I'
            r1, col1 = pos_of1[c1]  # Position in keyed grid 1
            r2, col2 = pos_of2[c2]  # Position in keyed grid 2
            # Rectangle rule: PT letters come from standard grids at (r1,col2) and (r2,col1)
            plaintext[i] = std_grid[r1 * 5 + col2]
            plaintext[i + 1] = std_grid[r2 * 5 + col1]

        matches = 0
        total = 0
        for pos in sorted_pos:
            if plaintext[pos] is not None:
                total += 1
                expected = cribs[pos]
                if expected == 'J':
                    expected = 'I'
                if plaintext[pos] == expected:
                    matches += 1

        if matches == total and total >= 15:
            hits.append(f"HIT FourSquare kw1={kw1} kw2={kw2} offset={offset} "
                        f"matches={matches}/{total}")

    return hits


def load_keywords():
    extra = [
        "", "KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK", "NORTHEAST",
        "SANBORN", "SHADOW", "LUCID", "MEMORY", "VIRTUALLY", "INVISIBLE",
        "DIGETAL", "INTERPRETATION", "UNDERGRUUND", "LANGLEY", "SLOWLY",
        "IQLUSION", "ENIGMA", "COMPASS", "LODESTONE", "WEBSTER",
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
        print("  Warning: words.txt not found, using built-in keywords only.")
    return words


def main():
    t0 = time.time()
    words = load_keywords()

    # Deduplicate grids
    seen_grids = set()
    unique_kws = []
    for kw in words:
        kw = kw.strip().upper() if kw else ""
        if kw and not kw.isalpha():
            continue
        grid, pos_of = make_grid(kw if kw else "")
        gkey = "".join(grid)
        if gkey not in seen_grids:
            seen_grids.add(gkey)
            unique_kws.append((kw if kw else "(standard)", grid, pos_of))

    print(f"Unique 5x5 grids: {len(unique_kws)}")
    print(f"Crib positions: {ncrib}")
    print()

    all_hits = []

    # ── Playfair ───────────────────────────────────────────────────────
    print("Testing Playfair cipher...")
    for kw, grid, pos_of in unique_kws:
        hits = check_playfair(grid, pos_of, kw)
        all_hits += hits
    print(f"  Playfair: {len(all_hits)} hit(s)")

    # ── Four-Square (use smaller keyword set for the O(n²) search) ─────
    n_before = len(all_hits)
    kryptos_kws = [(kw, g, p) for kw, g, p in unique_kws
                   if kw in ("(standard)", "KRYPTOS", "PALIMPSEST", "ABSCISSA",
                             "BERLIN", "CLOCK", "NORTHEAST", "SANBORN", "SHADOW",
                             "LUCID", "MEMORY", "INVISIBLE", "ENIGMA", "COMPASS",
                             "LODESTONE", "EGYPT", "WEBSTER", "LANGLEY", "POSITION",
                             "MAGNETIC", "UNDERGROUND", "LIGHT", "ABSENCE",
                             "SUBTLE", "DIGITAL", "LAYER")]

    print(f"Testing Four-Square cipher ({len(kryptos_kws)} × {len(unique_kws)} grid pairs)...")
    for kw1, g1, p1 in kryptos_kws:
        for kw2, g2, p2 in unique_kws:
            hits = check_foursquare(g1, p1, kw1, g2, p2, kw2)
            all_hits += hits
    print(f"  Four-Square: {len(all_hits) - n_before} hit(s)")

    elapsed = time.time() - t0
    print(f"\nTotal: {len(all_hits)} hit(s) in {elapsed:.1f}s")

    if all_hits:
        hitfile = os.path.join(HERE, "..", "hits_playfair.txt")
        with open(hitfile, "w") as f:
            f.write("\n".join(all_hits) + "\n")
        print(f"\nHits written to {hitfile}")
        for h in all_hits[:20]:
            print(f"  {h}")
    else:
        print("\nNo hits. Playfair and Four-Square ruled out for tested keyword grids.")


if __name__ == "__main__":
    main()
