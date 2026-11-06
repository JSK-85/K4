#!/usr/bin/env python3
"""
Attack 3: The Courtyard Morse Code Binary Mask Suite.
Converts the verified Morse code inscriptions on the Kryptos entrance slabs (K0)
into binary masks and multi-layer control streams:
  Phrases:
    - LUCID MEMORY
    - SHADOW FORCES
    - VIRTUALLY INVISIBLE
    - DIGITAL INTERPRETATION
    - WHAT IS YOUR POSITION / T IS YOUR POSITION
    - SOS RQ

Modes applied:
  1. Dual-Cipher Modulation: bit 0 -> Vigenere, bit 1 -> Beaufort (or VarBeau)
  2. Dual-Alphabet Modulation: bit 0 -> Standard AZ, bit 1 -> KRYPTOS-keyed KA
  3. Binary Shift Offset: bit 0 -> shift 0, bit 1 -> shift by keyword or +1/+13
  4. Null-Masking: strip ciphertext characters corresponding to bit 1
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

MORSE_TABLE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..'
}

MORSE_PHRASES = [
    "LUCID MEMORY",
    "SHADOW FORCES",
    "VIRTUALLY INVISIBLE",
    "DIGITAL INTERPRETATION",
    "WHAT IS YOUR POSITION",
    "T IS YOUR POSITION",
    "SOS RQ",
    "SOS",
    "LUCIDMEMORYSHADOWFORCESVIRTUALLYINVISIBLE",
    "VIRTUALLYINVISIBLEDIGITALINTERPRETATION"
]


def text_to_morse_bits(phrase: str) -> list[int]:
    """Convert text phrase into a list of 0s (dots) and 1s (dashes)."""
    bits = []
    for ch in phrase.upper():
        if ch in MORSE_TABLE:
            for symbol in MORSE_TABLE[ch]:
                bits.append(0 if symbol == '.' else 1)
    return bits


def vig_dec(c, k, alpha=AZ):
    return alpha[(alpha.index(c) - alpha.index(k)) % 26]


def beau_dec(c, k, alpha=AZ):
    return alpha[(alpha.index(k) - alpha.index(c)) % 26]


def varb_dec(c, k, alpha=AZ):
    return alpha[(alpha.index(c) + alpha.index(k)) % 26]


def run_attack3():
    print("=" * 70)
    print("ATTACK 3: Courtyard Morse Code Binary Mask Suite")
    print("=" * 70)
    t0 = time.time()

    masks = {}
    for phrase in MORSE_PHRASES:
        bits = text_to_morse_bits(phrase)
        if not bits:
            continue
        tag = phrase.replace(" ", "_")
        # Extended to length 97 with all circular rotations
        ext_bits = (bits * (N // len(bits) + 2))
        for rot in range(len(bits)):
            mask_97 = ext_bits[rot:rot + N]
            masks[f"{tag}_rot{rot}"] = mask_97
            # Also inverted mask (dots become 1, dashes become 0)
            inv_mask_97 = [1 - b for b in mask_97]
            masks[f"{tag}_inv_rot{rot}"] = inv_mask_97

    print(f"Generated {len(masks)} distinct Morse binary masks from courtyard inscriptions.")

    keywords = ["KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK", "SANBORN", "SCHEIDT", "SHADOW"]
    
    hits = []
    total_evals = 0

    for mask_name, mask in masks.items():
        # Mode 1: Dual-Cipher Modulation (bit 0 -> Vigenere, bit 1 -> Beaufort)
        for kw in keywords:
            for alpha_name, alpha in [("KA", KA), ("AZ", AZ)]:
                total_evals += 1
                pt = []
                for i in range(N):
                    k = kw[i % len(kw)]
                    if mask[i] == 0:
                        pt.append(vig_dec(CT[i], k, alpha))
                    else:
                        pt.append(beau_dec(CT[i], k, alpha))
                pt_str = "".join(pt)
                ev = evaluate_crib_match(pt_str)
                if ev.get("total_matches", 0) >= 4:
                    z = score_english(pt_str)
                    hits.append({
                        "tag": f"MorseDualCipher_{mask_name}+{alpha_name}({kw})",
                        "cribs": ev["total_matches"],
                        "z": z,
                        "pt": pt_str
                    })

        # Mode 2: Dual-Alphabet Modulation (bit 0 -> Standard AZ, bit 1 -> KRYPTOS KA)
        for kw in keywords:
            for dec_name, dec_fn in [("Vig", vig_dec), ("Beau", beau_dec)]:
                total_evals += 1
                pt = []
                for i in range(N):
                    k = kw[i % len(kw)]
                    alpha = AZ if mask[i] == 0 else KA
                    pt.append(dec_fn(CT[i], k, alpha))
                pt_str = "".join(pt)
                ev = evaluate_crib_match(pt_str)
                if ev.get("total_matches", 0) >= 4:
                    z = score_english(pt_str)
                    hits.append({
                        "tag": f"MorseDualAlpha_{mask_name}+{dec_name}({kw})",
                        "cribs": ev["total_matches"],
                        "z": z,
                        "pt": pt_str
                    })

        # Mode 3: Additive Masking (bit 1 adds offset +1, +13, or +25)
        for offset in [1, 13, 25]:
            for kw in ["KRYPTOS", "PALIMPSEST"]:
                total_evals += 1
                pt = []
                for i in range(N):
                    k = kw[i % len(kw)]
                    ki = (KA.index(k) + (offset if mask[i] == 1 else 0)) % 26
                    ci = KA.index(CT[i])
                    pt.append(KA[(ci - ki) % 26])
                pt_str = "".join(pt)
                ev = evaluate_crib_match(pt_str)
                if ev.get("total_matches", 0) >= 4:
                    z = score_english(pt_str)
                    hits.append({
                        "tag": f"MorseAdditive_{mask_name}_off{offset}({kw})",
                        "cribs": ev["total_matches"],
                        "z": z,
                        "pt": pt_str
                    })

    elapsed = time.time() - t0
    print(f"Tested {total_evals:,} Morse mask cipher combinations in {elapsed:.2f}s.")
    print(f"Candidates with >=4 crib matches: {len(hits)}")

    hits.sort(key=lambda h: (-h["cribs"], -h["z"]))
    for h in hits[:10]:
        print(f"  [{h['cribs']}/24 cribs | z={h['z']:.4f}] {h['tag']}")
        print(f"    Plaintext: {h['pt'][:60]}...")

    return hits


if __name__ == "__main__":
    run_attack3()

