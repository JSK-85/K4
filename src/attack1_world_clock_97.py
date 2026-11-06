#!/usr/bin/env python3
"""
Attack 1: The 97-City Erich John Alexanderplatz Weltzeituhr Keystream Runner.
Evaluates 1-to-1 keystreams derived from the Alexanderplatz World Clock cylinder:
  1. 97-character sliding windows of city initials / terminal letters.
  2. 97-character running keys from concatenated city names in cylinder order.
  3. City length sequences and time-zone shift offsets.
  4. Top-ring vs Bottom-ring vs Both across all 24 hourly rotational offsets.
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
from kryptos.k4.world_clock_faces_2017 import WORLD_CLOCK_FACES_2017
from kryptos.k4.world_clock_cities import CONFIRMED_CITIES

CT = K4_CIPHERTEXT
N = 97
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"


def vig_dec(c, k, alpha=AZ):
    return alpha[(alpha.index(c) - alpha.index(k)) % 26]


def beau_dec(c, k, alpha=AZ):
    return alpha[(alpha.index(k) - alpha.index(c)) % 26]


def varb_dec(c, k, alpha=AZ):
    return alpha[(alpha.index(c) + alpha.index(k)) % 26]


def run_attack1():
    print("=" * 70)
    print("ATTACK 1: The 97-City Alexanderplatz Weltzeituhr Keystream Runner")
    print("=" * 70)
    t0 = time.time()
    
    # Clean city names
    cleaned_confirmed = ["".join(c for c in city.upper() if c in AZ) for city in CONFIRMED_CITIES]
    cleaned_confirmed = [c for c in cleaned_confirmed if c]
    
    # Cities from WORLD_CLOCK_FACES_2017 in cylinder sequence
    tz_order = ["-12/-11/-10/-9", "-8", "-7", "-6", "-5", "-4", "-3", "-2", "-1", "0",
                "+1", "+2", "+3", "+4", "+5", "+6", "+7", "+8", "+9", "+10", "+11", "+12"]
    
    face_top_cities = []
    face_bottom_cities = []
    face_all_cities = []
    tz_shifts_per_city = []
    
    for tz_label in tz_order:
        data = WORLD_CLOCK_FACES_2017.get(tz_label, {})
        # Extract numerical offset for this timezone if possible
        try:
            tz_num = int(tz_label.replace("+", "")) % 26
        except Exception:
            tz_num = 0
            
        top_list = data.get("top") or ()
        for city in top_list:
            c_clean = "".join(ch for ch in city.upper() if ch in AZ)
            if c_clean:
                face_top_cities.append(c_clean)
                face_all_cities.append(c_clean)
                tz_shifts_per_city.append(tz_num)
                
        bottom_list = data.get("bottom") or ()
        for city in bottom_list:
            c_clean = "".join(ch for ch in city.upper() if ch in AZ)
            if c_clean:
                face_bottom_cities.append(c_clean)
                face_all_cities.append(c_clean)
                tz_shifts_per_city.append(tz_num)

    print(f"Loaded: {len(cleaned_confirmed)} confirmed cities, {len(face_all_cities)} face cities.")
    
    candidate_streams = []
    
    # 1. First letter and last letter streams
    for label, clist in [("Confirmed", cleaned_confirmed), ("FaceAll", face_all_cities), 
                         ("FaceTop", face_top_cities), ("FaceBottom", face_bottom_cities)]:
        firsts = "".join(c[0] for c in clist)
        lasts = "".join(c[-1] for c in clist)
        
        # Test full stream repeated / rotated
        for letter_mode, s in [("FirstLetters", firsts), ("LastLetters", lasts)]:
            if len(s) >= N:
                for start_idx in range(len(s) - N + 1):
                    sub = s[start_idx:start_idx + N]
                    candidate_streams.append((f"{label}_{letter_mode}_win{start_idx}", sub))
            # Rotations of length-extended stream
            ext = (s * (N // len(s) + 2))
            for rot in range(len(s)):
                sub = ext[rot:rot + N]
                candidate_streams.append((f"{label}_{letter_mode}_rot{rot}", sub))

    # 2. Continuous concatenated text of city names (running key from clock)
    for label, clist in [("Confirmed", cleaned_confirmed), ("FaceAll", face_all_cities)]:
        full_text = "".join(clist)
        # Test all starting offsets within the continuous text
        max_offsets = min(len(full_text) - N + 1, 500)
        for off in range(max_offsets):
            sub = full_text[off:off + N]
            candidate_streams.append((f"{label}_ContinuousRun_off{off}", sub))

    # 3. Numeric shifts from city lengths modulo 26 converted to letters
    for label, clist in [("Confirmed", cleaned_confirmed), ("FaceAll", face_all_cities)]:
        len_chars = "".join(AZ[len(c) % 26] for c in clist)
        ext = (len_chars * (N // len(len_chars) + 2))
        for rot in range(len(len_chars)):
            candidate_streams.append((f"{label}_CityLengths_rot{rot}", ext[rot:rot + N]))

    # 4. Time zone shift sequence
    tz_chars = "".join(AZ[shift] for shift in tz_shifts_per_city)
    ext_tz = (tz_chars * (N // len(tz_chars) + 2))
    for rot in range(len(tz_chars)):
        candidate_streams.append((f"Face_TZShifts_rot{rot}", ext_tz[rot:rot + N]))

    print(f"Generated {len(candidate_streams)} distinct candidate keystreams.")
    
    # Run evaluation across all keystreams x 2 alphabets x 3 cipher modes
    hits = []
    total_evals = 0
    
    for stream_tag, ks in candidate_streams:
        rev_ks = ks[::-1]
        for ks_mode, stream in [("fwd", ks), ("rev", rev_ks)]:
            for alpha_name, alpha in [("AZ", AZ), ("KA", KA)]:
                for dec_name, dec_fn in [("Vig", vig_dec), ("Beau", beau_dec), ("VarB", varb_dec)]:
                    total_evals += 1
                    pt = "".join(dec_fn(CT[i], stream[i], alpha) for i in range(N))
                    ev = evaluate_crib_match(pt)
                    if ev.get("total_matches", 0) >= 4:
                        z = score_english(pt)
                        hits.append({
                            "tag": f"Attack1_{stream_tag}_{ks_mode}_{dec_name}_{alpha_name}",
                            "cribs": ev["total_matches"],
                            "z": z,
                            "pt": pt,
                            "ev": ev,
                            "ks": stream
                        })

    elapsed = time.time() - t0
    print(f"Tested {total_evals:,} cipher combinations in {elapsed:.2f}s.")
    print(f"Candidates with >=4 crib matches: {len(hits)}")
    
    hits.sort(key=lambda h: (-h["cribs"], -h["z"]))
    for h in hits[:10]:
        print(f"  [{h['cribs']}/24 cribs | z={h['z']:.4f}] {h['tag']}")
        print(f"    Plaintext: {h['pt'][:60]}...")
        
    return hits


if __name__ == "__main__":
    run_attack1()
