#!/usr/bin/env python3
"""
Attack 5: Linguistic Plaintext Reconstruction & SHA-256 HMAC Verifier Suite.
Reconstructs syntactically and historically coherent 97-character plaintexts
anchored by:
  - Pos 22-34 (1-idx): EASTNORTHEAST (13 chars)
  - Pos 64-74 (1-idx): BERLINCLOCK (11 chars)

Computes:
  1. Full 24/24 crib compliance check.
  2. English n-gram z-score using nitsuah's 8.9M model.
  3. SHA-256 hash digest (the exact input format for Paradigm's blind verifier).
"""

import sys
import os
import time
import hashlib
import itertools

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

CRIB1 = "EASTNORTHEAST"  # 13 chars (pos 22-34, 0-idx 21-33)
CRIB2 = "BERLINCLOCK"    # 11 chars (pos 64-74, 0-idx 63-73)

# Part 1: Length exactly 21 chars (pos 1-21, 0-idx 0-20)
PART1_CANDIDATES = [
    "LOOKINTOTHEDIRECTIONO",   # 21: Look into the direction o[f]
    "FINDTHEBEARINGHEADING",   # 21: Find the bearing heading
    "FROMTHECOMPASSROSELIE",   # 21: From the compass rose lie[s]
    "THEINITIALBEARINGWASA",   # 21: The initial bearing was a[t]
    "ITSLAYERTWOTOTHENORTH",   # 21: Its layer two to the north...
    "THEORIGINALDIALFACEDT",   # 21: The original dial faced t[oward]
    "SETYOURCOURSEEXACTLYT",   # 21: Set your course exactly t[o]
    "THEDIRECTIONOFSHADOWS",   # 21: The direction of shadows...
    "INTHEDIRECTIONPOINTED",   # 21: In the direction pointed...
    "BETWEENTHESCULPTUREAN",   # 21: Between the sculpture an[d]
    "STARTINGFROMTHECENTER",   # 21: Starting from the center...
    "ATFORTYFOURDEGREESAND",   # 21: At forty four degrees and...
    "FOLLOWINGTHEBEARINGOF",   # 21: Following the bearing of...
    "YOURCOORDINATESLIEATA",   # 21: Your coordinates lie at a...
    "BURIEDUNDERTHESURFACE",   # 21: Buried under the surface...
]

# Part 3: Length exactly 29 chars (pos 35-63, 0-idx 34-62)
PART3_CANDIDATES = [
    "LOOKFORTHESHADOWFALLINGONTHEB",  # 29: Look for the shadow falling on the B[erlin clock]
    "ANDFINDTHEDIALSETATTHEURANIAX",  # 29: and find the dial set at the Urania X
    "TOWARDSTHEHISTORICCYLINDEROFA",  # 29: Towards the historic cylinder of a
    "POINTINGDIRECTLYTOWARDSANOLDB",  # 29: Pointing directly towards an old B[erlin clock]
    "WHEREINTHECITYLIESAWORLDFAMOU",  # 29: Where in the city lies a world famou[s]
    "ANDMEASURETHEDISTANCEFROMTHEA",  # 29: And measure the distance from the a[lexanderplatz]
    "DEGREESMINUTESSECONDSFROMTHEA",  # 29: Degrees minutes seconds from the a
    "ALONGTHEGREATCIRCLELINETOTHEB",  # 29: Along the great circle line to the B[erlin clock]
    "ACROSSTHEOCEANLIESANHISTORICB",  # 29: Across the ocean lies an historic B[erlin clock]
    "WHICHPOINTSTOWARDSTHEFAMEDOLD",  # 29: Which points towards the famed old
    "WHEREFORTYFOURDEGREESMEETSTHE",  # 29: Where forty four degrees meets the
    "TOTHEDIVIDEDGERMANCAPITALTHEB",  # 29: To the divided German capital the B[erlin clock]
    "ANDTHEHISTORICHOURSOFTHEGREAT",  # 29: And the historic hours of the great
]

# Part 5: Length exactly 23 chars (pos 75-97, 0-idx 74-96)
PART5_CANDIDATES = [
    "ATALEXANDERPLATZBERLINX",  # 23
    "INEASTBERLINONTHEPLATZX",  # 23
    "DESIGNEDBYERICHJOHNINDR",  # 23
    "SHOWINGWORLDTIMETOALLME",  # 23
    "ONTHECOMPASSROSEMOSAICX",  # 23
    "WITHNINETYSEVENCITIESON",  # 23
    "WHERETIMEROLLSONTHEWALL",  # 23
    "RECORDINGEVERYTIMEZONEX",  # 23
    "ATTHEHISTORICURANIASITE",  # 23
    "MARKINGTHEHOURSANDMINSX",  # 23
    "TOREVEALTHELASTSECRETSX",  # 23
    "THEORIGINALWELTZEITUHRX",  # 23
]


def run_attack5():
    print("=" * 70)
    print("ATTACK 5: Linguistic Plaintext Reconstruction & SHA-256 Verifier")
    print("=" * 70)
    t0 = time.time()

    # Validate candidate lengths
    for p in PART1_CANDIDATES:
        assert len(p) == 21, f"Part 1 length error: {p} is {len(p)}"
    for p in PART3_CANDIDATES:
        assert len(p) == 29, f"Part 3 length error: {p} is {len(p)}"
    for p in PART5_CANDIDATES:
        assert len(p) == 23, f"Part 5 length error: {p} is {len(p)}"

    print(f"Combinatorial search space: {len(PART1_CANDIDATES)} x {len(PART3_CANDIDATES)} x {len(PART5_CANDIDATES)} = {len(PART1_CANDIDATES) * len(PART3_CANDIDATES) * len(PART5_CANDIDATES):,} candidates")
    print(f"Every candidate is guaranteed 24/24 (100%) confirmed crib alignment.")

    evaluated = []
    
    for p1 in PART1_CANDIDATES:
        for p3 in PART3_CANDIDATES:
            for p5 in PART5_CANDIDATES:
                full_pt = p1 + CRIB1 + p3 + CRIB2 + p5
                assert len(full_pt) == 97
                
                # Verify crib match strictly
                ev = evaluate_crib_match(full_pt)
                assert ev["total_matches"] == 24
                
                # Compute English z-score
                z = score_english(full_pt)
                
                # Compute SHA-256 hash
                sha256 = hashlib.sha256(full_pt.encode("utf-8")).hexdigest()
                
                evaluated.append({
                    "plaintext": full_pt,
                    "z": z,
                    "sha256": sha256,
                    "p1": p1,
                    "p3": p3,
                    "p5": p5
                })

    evaluated.sort(key=lambda x: -x["z"])
    elapsed = time.time() - t0
    print(f"Evaluated {len(evaluated):,} linguistic plaintexts in {elapsed:.2f}s.\n")

    print("TOP 10 LINGUISTIC RECONSTRUCTIONS (By English z-score):")
    print("-" * 70)
    for rank, cand in enumerate(evaluated[:10], start=1):
        print(f"#{rank} [English z-score: {cand['z']:.4f} | Cribs: 24/24 (100%)]")
        print(f"  Plaintext: {cand['plaintext']}")
        print(f"  P1 (1-21) : {cand['p1']}")
        print(f"  Crib 1    : {CRIB1}")
        print(f"  P3 (35-63): {cand['p3']}")
        print(f"  Crib 2    : {CRIB2}")
        print(f"  P5 (75-97): {cand['p5']}")
        print(f"  SHA-256   : {cand['sha256']}")
        print()

    # Save to a dedicated file for the user and verifier
    out_json = os.path.join(ROOT, "k4_linguistic_candidates.json")
    import json
    with open(out_json, "w") as f:
        json.dump(evaluated[:50], f, indent=2)
    print(f"Saved top 50 candidates with SHA-256 digests to {out_json}")

    return evaluated


if __name__ == "__main__":
    run_attack5()
