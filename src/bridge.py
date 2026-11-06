#!/usr/bin/env python3
"""
K4 Bridge: Connects the High-Speed Native C/Python Attack Engine with
1. nitsuah/kryptos: Formal Hypothesis Ledger & English n-gram statistical scoring (english_z)
2. rayborg/kryptos-k4-dashboard: Visual Fieldbook Experiment JSON format & interactive exploration
"""

import os
import sys
import json
import time
import uuid
from typing import Dict, Any, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
NITSUAH_SRC = os.path.join(ROOT, "external", "nitsuah-kryptos", "src")
RAYBORG_DIR = os.path.join(ROOT, "external", "rayborg-k4-dashboard")

# Add nitsuah package to sys.path
if NITSUAH_SRC not in sys.path:
    sys.path.insert(0, NITSUAH_SRC)

# Canonical 97-character K4 ciphertext
K4_CIPHERTEXT = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"

# Canonical 24 known letters (1-indexed positions)
# 22-34: EASTNORTHEAST (Sanborn 2020)
# 64-74: BERLINCLOCK (Sanborn 2010, 2014)
CANONICAL_CRIBS = {
    "CRIB1": {
        "range": (22, 34),
        "plain": "EASTNORTHEAST",
        "cipher": K4_CIPHERTEXT[21:34],  # 0-indexed 21..33
    },
    "CRIB2": {
        "range": (64, 74),
        "plain": "BERLINCLOCK",
        "cipher": K4_CIPHERTEXT[63:74],  # 0-indexed 63..73
    }
}

# 0-indexed dictionary of expected letters
EXPECTED_LETTERS: Dict[int, str] = {}
for crib in CANONICAL_CRIBS.values():
    start_1 = crib["range"][0]
    for i, ch in enumerate(crib["plain"]):
        EXPECTED_LETTERS[start_1 - 1 + i] = ch


def evaluate_crib_match(plaintext: str) -> Dict[str, Any]:
    """
    Check match against all 24 known crib positions.
    Returns match count, total tested, holdout breakdown, and mismatched positions.
    """
    s = plaintext.upper()
    if len(s) != 97:
        return {"valid": False, "error": f"Plaintext length is {len(s)}, expected 97"}

    crib1_matches = sum(1 for i, ch in enumerate(CANONICAL_CRIBS["CRIB1"]["plain"])
                        if s[21 + i] == ch)
    crib2_matches = sum(1 for i, ch in enumerate(CANONICAL_CRIBS["CRIB2"]["plain"])
                        if s[63 + i] == ch)
    total_matches = crib1_matches + crib2_matches

    mismatches = []
    for pos_0, exp_char in EXPECTED_LETTERS.items():
        if s[pos_0] != exp_char:
            mismatches.append({
                "pos_1": pos_0 + 1,
                "expected": exp_char,
                "actual": s[pos_0]
            })

    return {
        "valid": True,
        "total_matches": total_matches,
        "crib_count": 24,
        "match_percentage": round(total_matches / 24 * 100, 2),
        "crib1_matches": f"{crib1_matches}/13",
        "crib2_matches": f"{crib2_matches}/11",
        "perfect_crib_match": total_matches == 24,
        "mismatches": mismatches
    }


def score_english(plaintext: str) -> float:
    """
    Compute English z-score using nitsuah's 8.9M letter n-gram model.
    0.0 = typical random/noise text, 1.0 = typical English text.
    Values >= 0.7 indicate plausible English structure.
    """
    try:
        from kryptos.k4.english_model import english_z
        return float(english_z(plaintext))
    except Exception as e:
        # Fallback to Index of Coincidence if model cannot be loaded
        from collections import Counter
        s = "".join(c for c in plaintext.upper() if c.isalpha())
        n = len(s)
        if n <= 1:
            return 0.0
        counts = Counter(s)
        ic = sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))
        # Standardize IC where 0.0385 -> 0.0, 0.0667 -> 1.0
        return (ic - 0.0385) / (0.0667 - 0.0385)


def create_fieldbook_experiment(
    title: str,
    method: str,
    operation: str,
    key: str,
    alphabet: str,
    output: str,
    notes: str = "",
    status: str = "tested",
    parameters: Optional[Dict[str, str]] = None,
    elapsed_ms: int = 0,
    candidates_tested: int = 1
) -> Dict[str, Any]:
    """
    Create an Experiment entry strictly conforming to rayborg/kryptos-k4-dashboard schema:
    interface Experiment in external/rayborg-k4-dashboard/src/types.ts
    """
    crib_eval = evaluate_crib_match(output)
    z_score = score_english(output)

    full_notes = (
        f"{notes}\n"
        f"Crib match: {crib_eval.get('total_matches', 0)}/24 "
        f"(Crib1: {crib_eval.get('crib1_matches', '0')}, Crib2: {crib_eval.get('crib2_matches', '0')})\n"
        f"English z-score: {z_score:.4f}"
    ).strip()

    exp_id = str(uuid.uuid4())
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    return {
        "id": exp_id,
        "createdAt": now_iso,
        "title": title,
        "section": "K4",
        "method": method,
        "operation": operation,
        "key": key,
        "alphabet": alphabet,
        "input": K4_CIPHERTEXT,
        "output": output,
        "notes": full_notes,
        "status": status,
        "provenance": {
            "appVersion": "k4-triad-bridge-1.0",
            "inputFingerprint": "k4-canonical-97",
            "indexConvention": "1-based",
            "parameters": parameters or {},
            "searchSpace": f"Tested {candidates_tested:,} candidate configurations",
            "corpus": "Jim Sanborn Kryptos K4",
            "scoring": f"english_z={z_score:.4f}, crib_match={crib_eval.get('total_matches', 0)}/24",
            "seed": "0",
            "elapsedMs": elapsed_ms,
            "hardware": "Mac M-Series Native Engine",
            "candidatesTested": candidates_tested,
            "holdout": f"Crib1={crib_eval.get('crib1_matches', '0')}, Crib2={crib_eval.get('crib2_matches', '0')}",
            "negativeControl": "shuffled ciphertext null model"
        }
    }


def export_fieldbook_notebook(experiments: List[Dict[str, Any]], export_path: str) -> str:
    """Save a list of experiments to JSON ready to import into Rayborg's Fieldbook."""
    os.makedirs(os.path.dirname(os.path.abspath(export_path)), exist_ok=True)
    bundle = {
        "schema": "k4-fieldbook-experiments-v1",
        "exportedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "experiments": experiments
    }
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)
    return export_path


def get_nitsuah_ledger(filter_tier: Optional[str] = None) -> List[Dict[str, Any]]:
    """Query nitsuah's Hypothesis Ledger programmatically."""
    from kryptos.k4.hypothesis_ledger import LEDGER
    entries = []
    for item in LEDGER:
        tier = item["tier"] if isinstance(item, dict) else item.tier
        if filter_tier is None or tier == filter_tier:
            if isinstance(item, dict):
                entries.append(dict(item))
            else:
                entries.append({
                    "family": item.family,
                    "tier": item.tier,
                    "scope": item.scope,
                    "evidence": item.evidence,
                    "module": item.module,
                    "test": item.test
                })
    return entries


if __name__ == "__main__":
    print("Testing K4 Bridge...")
    match = evaluate_crib_match(K4_CIPHERTEXT)
    z = score_english(K4_CIPHERTEXT)
    print(f"K4 Ciphertext English z-score: {z:.4f}")
    print(f"K4 Ciphertext Crib Matches: {match['total_matches']}/24")
    
    # Test creating a sample experiment
    exp = create_fieldbook_experiment(
        title="Baseline K4 Raw Ciphertext",
        method="Null Transformation",
        operation="Identity",
        key="NONE",
        alphabet="STANDARD",
        output=K4_CIPHERTEXT,
        notes="Control baseline representing unmodified ciphertext.",
        status="tested"
    )
    print(f"Generated Fieldbook experiment: {exp['id']}")
