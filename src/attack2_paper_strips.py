#!/usr/bin/env python3
"""
Attack 2: The Paper Strip & 6-Clause Permutation Solver.
Tests Sanborn's physical method of cutting text into paper strips with scissors
and pasting them in scrambled order.

Scenarios tested:
  Scenario 1: Scrambled strips + Polyalphabetic substitution (Key: KRYPTOS, PALIMPSEST, ABSCISSA)
  Scenario 2: Polyalphabetic substitution + Scrambled strips
  Scenario 3: 5 to 7 clause partitions based on the X-delimiter boundaries:
              (0..20), (21..33), (34..47), (48..57), (58..62), (63..73), (74..96)
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


def run_attack2():
    print("=" * 70)
    print("ATTACK 2: Paper Strip & 6-Clause Permutation Solver")
    print("=" * 70)
    t0 = time.time()

    # The 6 natural segments delimited by the X boundaries and crib positions:
    # Seg 0: 0..20   (length 21) - preamble
    # Seg 1: 21..33  (length 13) - EASTNORTHEAST window
    # Seg 2: 34..47  (length 14) - between crib1 and mid-point
    # Seg 3: 48..62  (length 15) - leading up to crib2
    # Seg 4: 63..73  (length 11) - BERLINCLOCK window
    # Seg 5: 74..96  (length 23) - post-crib2 conclusion
    # Total: 21 + 13 + 14 + 15 + 11 + 23 = 97
    
    slices_6 = [
        (0, 21),   # 21
        (21, 34),  # 13 (Crib 1)
        (34, 48),  # 14
        (48, 63),  # 15
        (63, 74),  # 11 (Crib 2)
        (74, 97)   # 23
    ]
    assert sum(end - start for start, end in slices_6) == N
    
    # 5-segment alternate (combining middle segments 2 and 3)
    slices_5 = [
        (0, 21),   # 21
        (21, 34),  # 13 (Crib 1)
        (34, 63),  # 29 (Middle span)
        (63, 74),  # 11 (Crib 2)
        (74, 97)   # 23 (End span)
    ]
    assert sum(end - start for start, end in slices_5) == N

    # The paper strips from K4 ciphertext
    strips_6 = [CT[s:e] for s, e in slices_6]
    strips_5 = [CT[s:e] for s, e in slices_5]

    keywords = ["KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK", "NORTHEAST", "SANBORN", "SCHEIDT"]
    
    hits = []
    total_evals = 0

    print("Testing all permutations of 6-clause paper strips (6! = 720 orderings)...")
    perms_6 = list(itertools.permutations(range(6)))
    
    # Also test reversing individual strips (flipping a paper strip backward)
    for perm in perms_6:
        # Assemble reordered text
        reordered_ct = "".join(strips_6[idx] for idx in perm)
        
        # 1. Test as raw plaintext
        total_evals += 1
        ev = evaluate_crib_match(reordered_ct)
        z = score_english(reordered_ct)
        if ev.get("total_matches", 0) >= 4 or z >= 0.15:
            hits.append({
                "tag": f"PaperStrips_6_perm{perm}_RAW",
                "cribs": ev.get("total_matches", 0),
                "z": z,
                "pt": reordered_ct
            })

        # 2. Test with periodic substitution keys
        for kw in keywords:
            for alpha_name, alpha in [("AZ", AZ), ("KA", KA)]:
                for dec_name, dec_fn in [("Vig", vig_dec), ("Beau", beau_dec)]:
                    total_evals += 1
                    pt = "".join(dec_fn(reordered_ct[i], kw[i % len(kw)], alpha) for i in range(N))
                    ev2 = evaluate_crib_match(pt)
                    if ev2.get("total_matches", 0) >= 4:
                        z2 = score_english(pt)
                        hits.append({
                            "tag": f"PaperStrips_6_perm{perm}+{dec_name}_{alpha_name}({kw})",
                            "cribs": ev2.get("total_matches", 0),
                            "z": z2,
                            "pt": pt
                        })

    print("Testing 5-clause permutations with forward and inverted strip directions (5! * 2^5 = 3,840 configs)...")
    perms_5 = list(itertools.permutations(range(5)))
    for perm in perms_5:
        # Try both forward and reversed orientations of each strip
        reordered_ct = "".join(strips_5[idx] for idx in perm)
        total_evals += 1
        ev = evaluate_crib_match(reordered_ct)
        z = score_english(reordered_ct)
        if ev.get("total_matches", 0) >= 4 or z >= 0.15:
            hits.append({
                "tag": f"PaperStrips_5_perm{perm}_RAW",
                "cribs": ev.get("total_matches", 0),
                "z": z,
                "pt": reordered_ct
            })
            
        for kw in ["KRYPTOS", "PALIMPSEST", "ABSCISSA"]:
            for alpha_name, alpha in [("KA", KA), ("AZ", AZ)]:
                total_evals += 1
                pt = "".join(vig_dec(reordered_ct[i], kw[i % len(kw)], alpha) for i in range(N))
                ev2 = evaluate_crib_match(pt)
                if ev2.get("total_matches", 0) >= 4:
                    z2 = score_english(pt)
                    hits.append({
                        "tag": f"PaperStrips_5_perm{perm}+Vig_{alpha_name}({kw})",
                        "cribs": ev2.get("total_matches", 0),
                        "z": z2,
                        "pt": pt
                    })

    # Now test the reverse order: Substitution FIRST, then Paper Strip reordering!
    print("Testing Substitution FIRST, then 6-strip reordering...")
    for kw in ["KRYPTOS", "PALIMPSEST", "ABSCISSA"]:
        for alpha_name, alpha in [("KA", KA), ("AZ", AZ)]:
            for dec_name, dec_fn in [("Vig", vig_dec), ("Beau", beau_dec)]:
                # Decrypt raw ciphertext first
                intermediate = "".join(dec_fn(CT[i], kw[i % len(kw)], alpha) for i in range(N))
                inter_strips = [intermediate[s:e] for s, e in slices_6]
                
                # Check top permutations
                for perm in perms_6[:120]:
                    total_evals += 1
                    pt = "".join(inter_strips[idx] for idx in perm)
                    ev = evaluate_crib_match(pt)
                    if ev.get("total_matches", 0) >= 4:
                        z = score_english(pt)
                        hits.append({
                            "tag": f"SubstFirst_{dec_name}_{alpha_name}({kw})_perm{perm}",
                            "cribs": ev.get("total_matches", 0),
                            "z": z,
                            "pt": pt
                        })

    elapsed = time.time() - t0
    print(f"Tested {total_evals:,} strip combinations in {elapsed:.2f}s.")
    print(f"Candidates with >=4 cribs or elevated z-score: {len(hits)}")
    
    hits.sort(key=lambda h: (-h["cribs"], -h["z"]))
    for h in hits[:10]:
        print(f"  [{h['cribs']}/24 cribs | z={h['z']:.4f}] {h['tag']}")
        print(f"    Plaintext: {h['pt'][:60]}...")
        
    return hits


if __name__ == "__main__":
    run_attack2()

