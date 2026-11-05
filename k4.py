#!/usr/bin/env python3
"""
K4 Master Cryptanalysis CLI: Unified Triad Architecture
Incorporates:
  1. Native C & Python High-Performance Brute-Force Engines
  2. nitsuah/kryptos: Formal Hypothesis Ledger, Bounds, and English n-gram Scoring
  3. rayborg/kryptos-k4-dashboard: Visual Fieldbook, Crib Bench & Interactive Lab
"""

import argparse
import os
import subprocess
import sys
import time
import json
from typing import List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
BIN = os.path.join(HERE, "bin")
NITSUAH_DIR = os.path.join(HERE, "external", "nitsuah-kryptos")
NITSUAH_SRC = os.path.join(NITSUAH_DIR, "src")
RAYBORG_DIR = os.path.join(HERE, "external", "rayborg-k4-dashboard")

# Ensure local packages are in path
sys.path.insert(0, SRC)
if os.path.isdir(NITSUAH_SRC):
    sys.path.insert(0, NITSUAH_SRC)

from bridge import (
    K4_CIPHERTEXT,
    CANONICAL_CRIBS,
    evaluate_crib_match,
    score_english,
    create_fieldbook_experiment,
    export_fieldbook_notebook,
    get_nitsuah_ledger
)


def cmd_status(args):
    print("=" * 72)
    print("       KRYPTOS K4 CRYPTANALYSIS TRIAD - UNIFIED STATUS")
    print("=" * 72)
    print(f"Ciphertext: {K4_CIPHERTEXT[:32]}... ({len(K4_CIPHERTEXT)} chars)")
    print("\n[Canonical Ground-Truth Cribs - 24 Confirmed Letters]:")
    print(f"  Pos 22-34 (13): {CANONICAL_CRIBS['CRIB1']['plain']} (Sanborn 2020 confirmation)")
    print(f"  Pos 64-74 (11): {CANONICAL_CRIBS['CRIB2']['plain']} (Sanborn 2010/2014 confirmations)")

    print("\n[Layer 1: Native High-Performance Searchers]:")
    search_bin = os.path.join(BIN, "search")
    hill_bin = os.path.join(BIN, "hillvig")
    search_ok = os.path.isfile(search_bin) and os.access(search_bin, os.X_OK)
    hill_ok = os.path.isfile(hill_bin) and os.access(hill_bin, os.X_OK)
    print(f"  bin/search   (Columnar & Route C engine): {'READY' if search_ok else 'NOT COMPILED (run: python3 run_all.py)'}")
    print(f"  bin/hillvig  (Hill 2x2 + Key C engine) : {'READY' if hill_ok else 'NOT COMPILED (run: python3 run_all.py)'}")
    print("  Python Suites: bifid, quagmire, playfair, progressive, differential")

    print("\n[Layer 2: nitsuah/kryptos (Ledger & Cryptanalytic Bounds)]:")
    try:
        from kryptos.k4.hypothesis_ledger import LEDGER
        get_tier = lambda x: x["tier"] if isinstance(x, dict) else x.tier
        elim = sum(1 for e in LEDGER if get_tier(e) == "eliminated")
        samp = sum(1 for e in LEDGER if get_tier(e) == "sampled_null")
        stat = sum(1 for e in LEDGER if get_tier(e) == "statistical")
        opn = sum(1 for e in LEDGER if get_tier(e) == "open")
        print(f"  Hypothesis Ledger: {len(LEDGER)} formal families tracked")
        print(f"    - Eliminated (exhaustive with positive controls): {elim}")
        print(f"    - Statistical (no signal vs noise controls)     : {stat}")
        print(f"    - Sampled Null (specific keys checked)          : {samp}")
        print(f"    - OPEN Hypotheses                               : {opn}")
        print("  English Model: 8.9M letter n-gram tables (english_z) ACTIVE")
    except Exception as e:
        print(f"  Status: Error loading nitsuah ledger: {e}")

    print("\n[Layer 3: rayborg/kryptos-k4-dashboard (Fieldbook & Visual Lab)]:")
    dist_index = os.path.join(RAYBORG_DIR, "dist", "index.html")
    is_built = os.path.isfile(dist_index)
    print(f"  Visual Workspace: {'BUILT (ready to serve)' if is_built else 'SOURCE READY (npm run build)'}")
    print("  Capabilities: Fixed-position Crib Bench, Interactive Cipher Lab, 100-Method Register")
    print("=" * 72)


def cmd_ledger(args):
    try:
        entries = get_nitsuah_ledger(filter_tier=args.tier)
        print(f"\n=== K4 HYPOTHESIS LEDGER ({len(entries)} entries" + (f", tier: {args.tier}" if args.tier else "") + ") ===")
        print(f"{'TIER':<14} | {'FAMILY':<45} | {'SCOPE'}")
        print("-" * 100)
        for e in entries:
            tier_display = e["tier"].upper()
            print(f"{tier_display:<14} | {e['family'][:45]:<45} | {e['scope']}")
        print("-" * 100)
        print("Use 'python3 k4.py ledger --tier open' to inspect currently unruled-out hypotheses.")
    except Exception as e:
        print(f"Error reading ledger: {e}")


def cmd_score(args):
    text = args.text.strip().upper()
    if os.path.isfile(text):
        with open(text) as f:
            text = f.read().strip().splitlines()[0].upper()

    print(f"\n--- Cryptanalytic Scoring for candidate (length {len(text)}) ---")
    print(f"Text: {text}")
    eval_res = evaluate_crib_match(text)
    z = score_english(text)

    print(f"\nCrib Matches: {eval_res.get('total_matches', 0)} / 24 ({eval_res.get('match_percentage', 0)}%)")
    print(f"  Crib 1 (EASTNORTHEAST @ 22-34): {eval_res.get('crib1_matches', '0')}")
    print(f"  Crib 2 (BERLINCLOCK   @ 64-74): {eval_res.get('crib2_matches', '0')}")
    print(f"English z-score: {z:.4f}")
    if z < 0.2:
        print("Interpretation: Typical random/ciphertext noise.")
    elif z < 0.6:
        print("Interpretation: Weak statistical fluctuation; does not match natural English.")
    elif z < 0.8:
        print("Interpretation: MODERATE SIGNAL. Notable English-like n-gram distribution.")
    else:
        print("Interpretation: STRONG ENGLISH PLAINTEXT SIGNAL! High probability of candidate match!")


def cmd_dashboard(args):
    procs = []
    ports = []

    if args.fieldbook or args.both or (not args.toolkit and not args.both):
        # Start Rayborg Fieldbook
        # We can serve the prebuilt dist using Python's http.server or run npm run preview/dev
        dist_dir = os.path.join(RAYBORG_DIR, "dist")
        if os.path.isdir(dist_dir) and os.path.isfile(os.path.join(dist_dir, "index.html")):
            p = subprocess.Popen(
                [sys.executable, "-m", "http.server", "5173", "--directory", dist_dir],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            procs.append(("Rayborg K4 Fieldbook (Visual)", "http://127.0.0.1:5173", p))
            ports.append(5173)
        else:
            # Fall back to vite dev
            p = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=RAYBORG_DIR,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            procs.append(("Rayborg K4 Fieldbook (Vite Dev)", "http://127.0.0.1:5173", p))
            ports.append(5173)

    if args.toolkit or args.both:
        # Start nitsuah FastAPI backend
        env = dict(os.environ)
        env["PYTHONPATH"] = f"{NITSUAH_SRC}:{env.get('PYTHONPATH', '')}"
        p = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "kryptos.api.app:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=NITSUAH_DIR,
            env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        procs.append(("nitsuah Kryptos Toolkit & API", "http://127.0.0.1:8000", p))
        ports.append(8000)

    print("\n" + "=" * 70)
    print("                K4 DASHBOARD SERVERS ACTIVE")
    print("=" * 70)
    for name, url, _ in procs:
        print(f"  -> {name:<35} : {url}")
    print("=" * 70)
    print("Press Ctrl+C to stop all dashboard servers.\n")

    try:
        while True:
            time.sleep(1)
            for name, url, proc in procs:
                if proc.poll() is not None:
                    print(f"Process {name} exited unexpectedly.")
    except KeyboardInterrupt:
        print("\nStopping dashboard servers...")
        for name, url, proc in procs:
            proc.terminate()
            proc.wait()
        print("All servers stopped.")


def cmd_attack(args):
    family = args.family.lower()
    print(f"\n[Running K4 Attack: {family.upper()}]")
    if family == "all":
        cmd = [sys.executable, os.path.join(HERE, "run_all.py")]
    elif family in ("quagmire", "playfair", "bifid", "progressive", "differential"):
        cmd = [sys.executable, os.path.join(SRC, f"{family}.py")]
    elif family == "columnar":
        search_bin = os.path.join(BIN, "search")
        if not os.path.isfile(search_bin):
            subprocess.run([sys.executable, os.path.join(HERE, "run_all.py"), "--help"], stdout=subprocess.DEVNULL)
        cmd = [search_bin, os.path.join(HERE, "k4.txt"), "10", "12", "7", "0"]
    else:
        print(f"Unknown attack family: {family}. Available: all, columnar, quagmire, playfair, bifid, progressive, differential")
        return

    subprocess.run(cmd)


def cmd_export_hit(args):
    input_file = args.input or os.path.join(HERE, "hits.txt")
    out_file = args.out or os.path.join(HERE, "fieldbook_experiments.json")

    experiments = []
    if os.path.isfile(input_file):
        with open(input_file) as f:
            for idx, line in enumerate(f):
                line = line.strip()
                if not line.startswith("HIT"):
                    continue
                exp = create_fieldbook_experiment(
                    title=f"Hit #{idx+1}: {line[:40]}",
                    method="Transposition + Periodic Key",
                    operation="Decrypt",
                    key=line.split("key=")[-1] if "key=" in line else "UNKNOWN",
                    alphabet="KRYPTOS / AZ",
                    output=K4_CIPHERTEXT,
                    notes=f"Hit details: {line}",
                    status="promising"
                )
                experiments.append(exp)

    # Always include baseline
    if not experiments:
        experiments.append(create_fieldbook_experiment(
            title="Baseline K4 Raw Ciphertext",
            method="Null Transformation",
            operation="Identity",
            key="NONE",
            alphabet="STANDARD",
            output=K4_CIPHERTEXT,
            notes="Control baseline representing unmodified ciphertext.",
            status="tested"
        ))

    export_fieldbook_notebook(experiments, out_file)
    print(f"Exported {len(experiments)} experiment(s) to: {out_file}")
    print("You can import this file directly into the K4 Fieldbook Notebook view in your browser!")


def main():
    parser = argparse.ArgumentParser(
        description="K4 Unified Cryptanalysis Dashboard & Attack Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 k4.py status                       # View integrated status across all 3 tools
  python3 k4.py dashboard --fieldbook        # Launch interactive visual Fieldbook (http://127.0.0.1:5173)
  python3 k4.py dashboard --toolkit          # Launch nitsuah FastAPI server (http://127.0.0.1:8000)
  python3 k4.py dashboard --both             # Launch both dashboards simultaneously
  python3 k4.py ledger --tier open           # Inspect open, unruled-out hypothesis spaces
  python3 k4.py attack quagmire              # Run Quagmire attack with 24 crib letters
  python3 k4.py score "OBKRUOXOGHUL..."      # Calculate English z-score & crib match for candidate
  python3 k4.py export-hit                   # Export hits to Fieldbook JSON notebook
        """
    )
    subparsers = parser.add_subparsers(dest="command")

    # status
    p_status = subparsers.add_parser("status", help="Show unified cryptanalysis and tools status")
    p_status.set_defaults(func=cmd_status)

    # dashboard
    p_dash = subparsers.add_parser("dashboard", help="Launch visual Fieldbook and/or toolkit API")
    p_dash.add_argument("--fieldbook", action="store_true", help="Launch Rayborg Fieldbook (http://127.0.0.1:5173)")
    p_dash.add_argument("--toolkit", action="store_true", help="Launch Nitsuah Toolkit API (http://127.0.0.1:8000)")
    p_dash.add_argument("--both", action="store_true", help="Launch both dashboards side-by-side")
    p_dash.set_defaults(func=cmd_dashboard)

    # ledger
    p_led = subparsers.add_parser("ledger", help="View formal Hypothesis Ledger entries")
    p_led.add_argument("--tier", choices=["eliminated", "statistical", "sampled_null", "open"], help="Filter by tier")
    p_led.set_defaults(func=cmd_ledger)

    # score
    p_score = subparsers.add_parser("score", help="Score candidate plaintext with n-grams and cribs")
    p_score.add_argument("text", help="Plaintext string (97 chars) or file containing plaintext")
    p_score.set_defaults(func=cmd_score)

    # attack
    p_atk = subparsers.add_parser("attack", help="Execute targeted attack using native C/Python engines")
    p_atk.add_argument("family", help="Attack family: all, columnar, quagmire, playfair, bifid, progressive, differential")
    p_atk.set_defaults(func=cmd_attack)

    # export-hit
    p_exp = subparsers.add_parser("export-hit", help="Export hits to Rayborg Fieldbook experiment JSON")
    p_exp.add_argument("--input", help="Path to hits.txt")
    p_exp.add_argument("--out", help="Output JSON path")
    p_exp.set_defaults(func=cmd_export_hit)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
