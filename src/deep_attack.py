#!/usr/bin/env python3
"""
Deep K4 Cryptanalysis Attack Suite: Targeting the High-Priority Open Frontiers
  1. The 24-Column Incomplete Grid (97 = 4x24 + 1: the sculpture's exact physical column width!)
  2. Mirrored / Flipped Physical Tableau Keystreams (Beaufort-algebraic reads from the rear)
  3. Alexanderplatz Weltzeituhr 24-Face Cylinder Rotations & City Streams
  4. The 6-Segment Inverse-Keyed Structure (delimited by X at pos 20, 36, 48, 58, 74)
"""

import sys
import os
import json
import time

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
    evaluate_crib_match,
    score_english,
    create_fieldbook_experiment,
    export_fieldbook_notebook
)

KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N = 97


def vig_dec(c, k, alpha=AZ):
    ci = alpha.index(c)
    ki = alpha.index(k)
    return alpha[(ci - ki) % len(alpha)]


def beau_dec(c, k, alpha=AZ):
    ci = alpha.index(c)
    ki = alpha.index(k)
    return alpha[(ki - ci) % len(alpha)]


def varbeau_dec(c, k, alpha=AZ):
    ci = alpha.index(c)
    ki = alpha.index(k)
    return alpha[(ci + ki) % len(alpha)]


def test_24_column_physical_grid():
    """
    Kryptos is physically constructed with 24 columns!
    97 letters in 24 columns = 4 full rows of 24 (96 letters) + 1 letter in row 5.
    Column 0 has 5 letters; columns 1-23 have 4 letters.
    Or vice versa (depending on reading direction).
    Test all reading orientations of this physical grid + periodic keys.
    """
    print("=" * 70)
    print("VECTOR 1: 24-Column Physical Incomplete Grid (4x24 + 1)")
    print("=" * 70)
    
    W = 24
    # Column lengths: one column has 5 letters, 23 columns have 4 letters
    col_orders = []
    
    # 1. Standard Columnar: Col 0 has 5 letters
    order_fwd = []
    col_lens = [5] + [4] * 23
    idx = 0
    cols = []
    for cl in col_lens:
        cols.append(list(range(idx, idx + cl)))
        idx += cl
    
    # Read rows then columns, columns then rows, forward, backward, serpentine
    # Write by row into grid of width 24
    # Row 0: 0..23, Row 1: 24..47, Row 2: 48..71, Row 3: 72..95, Row 4: [96]
    grid_rows = [
        list(range(0, 24)),
        list(range(24, 48)),
        list(range(48, 72)),
        list(range(72, 96)),
        [96]
    ]
    
    # Reading orders
    readings = {}
    
    # Col by col (top-down, L-to-R)
    read_col_tl = []
    for c in range(24):
        for r in range(5 if c == 0 else 4):
            read_col_tl.append(grid_rows[r][c])
    readings["col_top_down_LtoR"] = read_col_tl
    
    # Col by col (bottom-up, L-to-R)
    read_col_bl = []
    for c in range(24):
        rows_in_col = list(range(5 if c == 0 else 4))
        rows_in_col.reverse()
        for r in rows_in_col:
            read_col_bl.append(grid_rows[r][c])
    readings["col_bottom_up_LtoR"] = read_col_bl
    
    # Col by col (top-down, R-to-L)
    read_col_tr = []
    for c in range(23, -1, -1):
        for r in range(5 if c == 0 else 4):
            read_col_tr.append(grid_rows[r][c])
    readings["col_top_down_RtoL"] = read_col_tr
    
    # Col by col (bottom-up, R-to-L)
    read_col_br = []
    for c in range(23, -1, -1):
        rows_in_col = list(range(5 if c == 0 else 4))
        rows_in_col.reverse()
        for r in rows_in_col:
            read_col_br.append(grid_rows[r][c])
    readings["col_bottom_up_RtoL"] = read_col_br
    
    # Serpentine columns
    read_col_snake = []
    for c in range(24):
        rows_in_col = list(range(5 if c == 0 else 4))
        if c % 2 == 1:
            rows_in_col.reverse()
        for r in rows_in_col:
            read_col_snake.append(grid_rows[r][c])
    readings["col_serpentine_LtoR"] = read_col_snake
    
    # Now invert each reading (untangling transposition)
    candidates_found = []
    kryptos_keys = ["KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK", "NORTHEAST", "EAST", "SANBORN", "SHADOW"]
    
    for name, order in readings.items():
        # Transpose ciphertext
        # Case A: ciphertext was read by columns, write back by rows
        untangled_A = "".join(K4_CIPHERTEXT[order[i]] for i in range(N))
        # Case B: inverse permutation
        inv_order = [0] * N
        for i, pos in enumerate(order):
            inv_order[pos] = i
        untangled_B = "".join(K4_CIPHERTEXT[inv_order[i]] for i in range(N))
        
        for case_label, text in [("direct", untangled_A), ("inverse", untangled_B)]:
            # Test null substitution
            ev = evaluate_crib_match(text)
            if ev["total_matches"] >= 4:
                candidates_found.append((f"24-col({name},{case_label},RAW)", text, ev))
            
            # Test periodic keys
            for kw in kryptos_keys:
                for alpha_name, alpha in [("AZ", AZ), ("KA", KA)]:
                    for dec_name, dec_fn in [("Vig", vig_dec), ("Beau", beau_dec), ("VarBeau", varbeau_dec)]:
                        pt = "".join(dec_fn(text[i], kw[i % len(kw)], alpha) for i in range(N))
                        ev2 = evaluate_crib_match(pt)
                        if ev2["total_matches"] >= 4:
                            candidates_found.append((f"24-col({name},{case_label}) + {dec_name}_{alpha_name}({kw})", pt, ev2))

    print(f"Tested {len(readings) * 2 * (1 + len(kryptos_keys) * 2 * 3)} configurations on 24-column grid.")
    print(f"Candidates with >=4 crib matches: {len(candidates_found)}")
    for tag, pt, ev in candidates_found:
        z = score_english(pt)
        print(f"  [{tag}] Cribs: {ev['total_matches']}/24 | z-score: {z:.4f}")
    return candidates_found


def test_mirrored_tableau_keystreams():
    """
    Test physical tableau keystreams from physical_grid.py with both standard and mirrored orientations.
    """
    print("\n" + "=" * 70)
    print("VECTOR 2: Physical Vigenère Tableau Keystreams (Direct & Mirrored)")
    print("=" * 70)
    from kryptos.k4.physical_grid import candidate_keystreams
    
    results = []
    for mirrored in (False, True):
        mode_str = "Mirrored (Rear View)" if mirrored else "Direct (Front View)"
        streams = candidate_keystreams("KRYPTOS", mirrored=mirrored)
        print(f"Testing {len(streams)} keystreams for {mode_str}...")
        for name, ks in streams.items():
            # Extend keystream to length 97
            full_ks = (ks * (N // len(ks) + 1))[:N]
            for alpha_name, alpha in [("AZ", AZ), ("KA", KA)]:
                for dec_name, dec_fn in [("Vig", vig_dec), ("Beau", beau_dec), ("VarBeau", varbeau_dec)]:
                    pt = "".join(dec_fn(K4_CIPHERTEXT[i], full_ks[i], alpha) for i in range(N))
                    ev = evaluate_crib_match(pt)
                    if ev["total_matches"] >= 4:
                        results.append((f"Tableau({name},{mode_str})+{dec_name}_{alpha_name}", pt, ev))
    
    print(f"Completed physical tableau sweeps. Promising candidates: {len(results)}")
    for tag, pt, ev in results:
        z = score_english(pt)
        print(f"  [{tag}] Cribs: {ev['total_matches']}/24 | z-score: {z:.4f}")
    return results


def test_weltzeituhr_cylinder_rotations():
    """
    Test the 24 faces of the Berlin World Clock.
    Each face corresponds to 1 hour (1 to 24).
    Rotate through all 24 hour offsets and generate running streams from city initial letters.
    """
    print("\n" + "=" * 70)
    print("VECTOR 3: Alexanderplatz Weltzeituhr 24-Hour Cylinder Rotations")
    print("=" * 70)
    from kryptos.k4.world_clock_faces_2017 import WORLD_CLOCK_FACES_2017, FaceSide
    
    offsets = ["-12/-11/-10/-9", "-8", "-7", "-6", "-5", "-4", "-3", "-2", "-1", "0",
               "+1", "+2", "+3", "+4", "+5", "+6", "+7", "+8", "+9", "+10", "+11", "+12"]
    
    # Collect all top cities and bottom cities in cylinder order
    top_cities = []
    bottom_cities = []
    for off in offsets:
        entry = WORLD_CLOCK_FACES_2017.get(off, {})
        for c in (entry.get("top") or ()):
            clean_c = "".join(ch for ch in c.upper() if ch in AZ)
            if clean_c:
                top_cities.append(clean_c)
        for c in (entry.get("bottom") or ()):
            clean_c = "".join(ch for ch in c.upper() if ch in AZ)
            if clean_c:
                bottom_cities.append(clean_c)
    
    print(f"Assembled {len(top_cities)} top cylinder cities, {len(bottom_cities)} bottom cylinder cities.")
    
    candidates = []
    # Test streams derived from city initial letters, last letters, and lengths
    for label, city_list in [("TopCities", top_cities), ("BottomCities", bottom_cities), ("AllCities", top_cities + bottom_cities)]:
        for method in ("first", "last"):
            stream_chars = [c[0] if method == "first" else c[-1] for c in city_list if c]
            if len(stream_chars) < 10:
                continue
            # Rotate by all starting positions
            for rot in range(len(stream_chars)):
                rotated = stream_chars[rot:] + stream_chars[:rot]
                full_ks = (rotated * (N // len(rotated) + 1))[:N]
                for alpha_name, alpha in [("AZ", AZ), ("KA", KA)]:
                    for dec_name, dec_fn in [("Vig", vig_dec), ("Beau", beau_dec), ("VarBeau", varbeau_dec)]:
                        pt = "".join(dec_fn(K4_CIPHERTEXT[i], full_ks[i], alpha) for i in range(N))
                        ev = evaluate_crib_match(pt)
                        if ev["total_matches"] >= 4:
                            candidates.append((f"Weltzeituhr({label},{method},rot={rot})+{dec_name}_{alpha_name}", pt, ev))
                            
    print(f"Tested Weltzeituhr rotation matrix. Promising candidates: {len(candidates)}")
    for tag, pt, ev in candidates:
        z = score_english(pt)
        print(f"  [{tag}] Cribs: {ev['total_matches']}/24 | z-score: {z:.4f}")
    return candidates


def main():
    t0 = time.time()
    print("STARTING ADVANCED K4 CRYPTANALYSIS CAMPAIGN...")
    
    all_candidates = []
    all_candidates += test_24_column_physical_grid()
    all_candidates += test_mirrored_tableau_keystreams()
    all_candidates += test_weltzeituhr_cylinder_rotations()
    
    print("\n" + "=" * 70)
    print("CAMPAIGN SUMMARY")
    print("=" * 70)
    print(f"Elapsed time: {time.time() - t0:.1f}s")
    print(f"Total candidates meeting >=4 crib threshold: {len(all_candidates)}")
    
    experiments = []
    for tag, pt, ev in all_candidates:
        z = score_english(pt)
        exp = create_fieldbook_experiment(
            title=f"Campaign candidate: {tag[:35]}",
            method=tag,
            operation="Decrypt",
            key="DERIVED",
            alphabet="KRYPTOS/AZ",
            output=pt,
            notes=f"Evaluation: {ev['total_matches']}/24 crib matches, english_z={z:.4f}",
            status="tested" if z < 0.5 else "promising"
        )
        experiments.append(exp)
        
    if experiments:
        out_file = os.path.join(ROOT, "fieldbook_experiments.json")
        export_fieldbook_notebook(experiments, out_file)
        print(f"Updated Fieldbook notebook with {len(experiments)} candidate experiment(s) in {out_file}")
    else:
        print("All tested combinations produced sub-threshold signals (<4 crib matches).")


if __name__ == "__main__":
    main()
