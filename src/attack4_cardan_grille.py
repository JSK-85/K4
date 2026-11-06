#!/usr/bin/env python3
"""
Attack 4: Physical Stencil Aperture & Cardan Grille Suite.
Tests the 4-turn rotating Cardan Grille:
  97 = 4 * 24 + 1
  A stencil with 24 apertures rotated four times (0 deg, 90 deg, 180 deg, 270 deg)
  to write or read 96 characters, plus 1 fixed aperture for the 97th character.

Combines geometric grille apertures with periodic substitution keys.
"""

import sys
import os
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
    evaluate_crib_match,
    score_english,
    create_fieldbook_experiment,
    export_fieldbook_notebook
)

CT = K4_CIPHERTEXT
N = 97
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"


def vig_dec(c, k, alpha=AZ):
    return alpha[(alpha.index(c) - alpha.index(k)) % 26]


def beau_dec(c, k, alpha=AZ):
    return alpha[(alpha.index(k) - alpha.index(c)) % 26]


def run_attack4():
    print("=" * 70)
    print("ATTACK 4: Physical Stencil Aperture & Cardan Grille (4 * 24 + 1)")
    print("=" * 70)
    t0 = time.time()

    # Model a 10x10 grid (100 cells), where 97 cells are used and 3 are blocked nulls
    # Or a 7x14 grid (98 cells, 1 blocked), or 24x4 grid (96 cells + 1 extra)
    
    # 1. Test 4 quarter-turns of 24 characters:
    # Quadrant 1: 0..23
    # Quadrant 2: 24..47
    # Quadrant 3: 48..71
    # Quadrant 4: 72..95
    # Extra: 96
    
    q_len = 24
    quads = [CT[i*q_len : (i+1)*q_len] for i in range(4)]
    extra = CT[96]

    hits = []
    total_evals = 0

    # Test reading patterns across the 4 quarter-turns:
    # A. Interleaved reading: letter 0 from q0, q1, q2, q3; letter 1 from q0, q1, q2, q3...
    # B. Reverse interleaved: q3, q2, q1, q0...
    # C. Diagonal spiral across the 4 turns
    
    orders = {}
    
    # Interleaved L-to-R
    inter_fwd = []
    for pos in range(24):
        for q in range(4):
            inter_fwd.append(quads[q][pos])
    inter_fwd.append(extra)
    orders["Interleaved_0123"] = "".join(inter_fwd)

    # Interleaved R-to-L
    inter_rev = []
    for pos in range(24):
        for q in [3, 2, 1, 0]:
            inter_rev.append(quads[q][pos])
    inter_rev.append(extra)
    orders["Interleaved_3210"] = "".join(inter_rev)

    # Alternating Serpentine Interleave
    snake = []
    for pos in range(24):
        q_order = [0, 1, 2, 3] if pos % 2 == 0 else [3, 2, 1, 0]
        for q in q_order:
            snake.append(quads[q][pos])
    snake.append(extra)
    orders["Serpentine_4Turns"] = "".join(snake)

    # Block rotations (0 deg, 90 deg, 180 deg, 270 deg)
    for q_perm in [(0, 1, 2, 3), (1, 2, 3, 0), (2, 3, 0, 1), (3, 0, 1, 2),
                  (3, 2, 1, 0), (2, 1, 0, 3), (1, 0, 3, 2), (0, 3, 2, 1)]:
        block_text = "".join(quads[q] for q in q_perm) + extra
        orders[f"QuarterTurn_perm{q_perm}"] = block_text

    keywords = ["KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK", "SANBORN", "SCHEIDT", "SHADOW"]

    for name, candidate_text in orders.items():
        total_evals += 1
        ev = evaluate_crib_match(candidate_text)
        z = score_english(candidate_text)
        if ev.get("total_matches", 0) >= 4 or z >= 0.15:
            hits.append({
                "tag": f"Grille_{name}_RAW",
                "cribs": ev.get("total_matches", 0),
                "z": z,
                "pt": candidate_text
            })

        for kw in keywords:
            for alpha_name, alpha in [("KA", KA), ("AZ", AZ)]:
                for dec_name, dec_fn in [("Vig", vig_dec), ("Beau", beau_dec)]:
                    total_evals += 1
                    pt = "".join(dec_fn(candidate_text[i], kw[i % len(kw)], alpha) for i in range(N))
                    ev2 = evaluate_crib_match(pt)
                    if ev2.get("total_matches", 0) >= 4:
                        z2 = score_english(pt)
                        hits.append({
                            "tag": f"Grille_{name}+{dec_name}_{alpha_name}({kw})",
                            "cribs": ev2.get("total_matches", 0),
                            "z": z2,
                            "pt": pt
                        })

    elapsed = time.time() - t0
    print(f"Tested {total_evals:,} Cardan grille combinations in {elapsed:.2f}s.")
    print(f"Candidates with >=4 crib matches: {len(hits)}")

    hits.sort(key=lambda h: (-h["cribs"], -h["z"]))
    for h in hits[:10]:
        print(f"  [{h['cribs']}/24 cribs | z={h['z']:.4f}] {h['tag']}")
        print(f"    Plaintext: {h['pt'][:60]}...")

    return hits


if __name__ == "__main__":
    run_attack4()

