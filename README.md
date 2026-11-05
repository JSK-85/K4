# Kryptos K4 Cryptanalysis Program (Triad Edition)

An integrated, end-to-end research and cryptanalysis suite for Jim Sanborn's unsolved **Kryptos K4** (97 characters, CIA Headquarters).

This project integrates three complementary cryptanalytic systems into a unified architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      K4 CRYPTANALYTIC TRIAD                            │
├────────────────────────────────┬───────────────────────────────────────┤
│ 1. VISUAL FIELDBOOK            │ rayborg/kryptos-k4-dashboard          │
│    (Interactive Browser Lab)   │ - Live 24-char Crib Bench             │
│                                │ - Interactive Cipher & Route Lab      │
│                                │ - 100-Method Research Register        │
│                                │ - Schema-validated Experiment Ledger  │
├────────────────────────────────┼───────────────────────────────────────┤
│ 2. RESEARCH TOOLKIT & LEDGER   │ nitsuah/kryptos                       │
│    (Scientific Rigor & Bounds) │ - Formal 46-family Hypothesis Ledger  │
│                                │ - Elimination Bounds & Controls       │
│                                │ - 8.9M-letter English n-gram Model    │
│                                │ - FastAPI REST API & GIDC Dashboard   │
├────────────────────────────────┼───────────────────────────────────────┤
│ 3. HIGH-SPEED NATIVE ENGINES   │ Local C & Multicore Python            │
│    (Raw Computational Muscle)  │ - bin/search (billions of ops/sec)    │
│                                │ - bin/hillvig (Hill 2x2 + key search) │
│                                │ - Route x Columnar double transp.     │
│                                │ - Quagmire, Bifid, Progressive suites │
└────────────────────────────────┴───────────────────────────────────────┘
```

---

## Ground-Truth Public Cribs (24 Letters)

All searchers and diagnostic tools lock into the canonical 24 public plaintext letters:

| Block | 1-based Pos | 0-based Pos | Cipher Segment | Plaintext Crib | Announcement |
|---|---|---|---|---|---|
| **Crib 1** | 22–34 (13 letters) | 21–33 | `FLRVQQPRNGKSS` | `EASTNORTHEAST` | Sanborn 2020 (`EAST` + `NORTHEAST`) |
| **Crib 2** | 64–74 (11 letters) | 63–73 | `NYPVTTMZFPK` | `BERLINCLOCK` | Sanborn 2010 (`BERLIN`) + 2014 (`CLOCK`) |

---

## Quickstart

### 1. Check Unified Status
```bash
python3 k4.py status
```
Displays current state across all 3 layers: native C binaries, nitsuah ledger counts, and rayborg visual workspace build status.

### 2. Launch Dashboards
You can launch either or both dashboards with one command:

```bash
# Launch Rayborg's Visual Fieldbook (http://127.0.0.1:5173)
python3 k4.py dashboard --fieldbook

# Launch Nitsuah's FastAPI Toolkit & Dashboard (http://127.0.0.1:8000)
python3 k4.py dashboard --toolkit

# Launch both side-by-side
python3 k4.py dashboard --both
```

### 3. Query the Hypothesis Ledger
```bash
# View all hypotheses that remain OPEN (uneliminated)
python3 k4.py ledger --tier open

# View all formally eliminated families (with positive controls)
python3 k4.py ledger --tier eliminated
```

### 4. Run High-Speed Attacks
```bash
# Run all native attacks across CPU cores (columnar, routes, Hill, Quagmire, progressive)
python3 k4.py attack all

# Or run specific attack families
python3 k4.py attack columnar      # Columnar permutations x periodic keys in C
python3 k4.py attack quagmire      # Quagmire I-IV across full dictionary
python3 k4.py attack bifid         # Bifid/Trifid Polybius square tests
python3 k4.py attack progressive   # Linear, quadratic, Gromark, running keys
```

### 5. Cryptanalytically Score Any Candidate Plaintext
Evaluates any 97-character candidate against both the 24 crib positions and the 8.9M-letter English n-gram statistical model (`english_z`):
```bash
python3 k4.py score "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
```
- `z ≈ 0.0`: Random ciphertext noise
- `z ≈ 1.0`: Genuine English text
- `z >= 0.7`: Notable signal warranting deep investigation

### 6. Export Hits to Fieldbook
Export candidate results into `fieldbook_experiments.json`:
```bash
python3 k4.py export-hit
```
Import this file into the **K4 Fieldbook Notebook** view in your browser for immediate visual inspection, matrix manipulation, and holdout validation.

---

## Directory Structure

```text
K4/
├── k4.py                           # Master Unified CLI & Triad Orchestrator
├── run_all.py                      # Multicore attack runner & test suite
├── k4.txt                          # Canonical ciphertext + 24-letter cribs
├── fieldbook_experiments.json      # Schema-compliant Fieldbook notebook export
├── bin/
│   ├── search                      # Compiled C columnar + route searcher
│   └── hillvig                     # Compiled C Hill 2x2 + key searcher
├── src/
│   ├── bridge.py                   # Triad bridge (scoring, cribs, JSON export)
│   ├── search.c                    # Ultra-fast native C searcher
│   ├── hillvig.c                   # Native C Hill searcher
│   ├── routes.py                   # Geometric route generator (spiral/snake/diag)
│   ├── quagmire.py                 # Quagmire I-IV dictionary search
│   ├── bifid.py                    # Bifid / Trifid search
│   ├── playfair.py                 # Playfair / Two-Square / Four-Square search
│   ├── progressive.py              # Progressive, Gromark, and running keys
│   └── differential.py             # Differential and IC analysis
└── external/
    ├── nitsuah-kryptos/            # Formal Hypothesis Ledger, FastAPI, n-grams
    │   ├── src/kryptos/            # Python cryptanalysis package
    │   ├── frontend/               # Single-page React dashboard
    │   └── docs/                   # Methodological proofs and elimination specs
    └── rayborg-k4-dashboard/       # Local-First Visual Fieldbook
        ├── src/                    # React 19 + TypeScript + Vite UI
        ├── dist/                   # Built production bundle (ready to serve)
        └── docs/                   # Historical dossier & Smithsonian research
```

---

## Cryptanalytic Workflow to Break K4

1. **Exploration & Hypothesis Formulation**:
   Use **Rayborg's Fieldbook** (`python3 k4.py dashboard --fieldbook`) to interactively test grid geometries, rotation routes, and cipher combinations against the 24 fixed letters.
2. **Heavy-Duty Elimination**:
   Execute the bounded parameter spaces in our **Native C/Multicore Engine** (`python3 k4.py attack all`) to test billions of permutations per second with zero false negatives.
3. **Statistical Auditing & Ledger Registration**:
   Pass candidates through the **Bridge** to compute `english_z` and holdout scores. Formally update the **Nitsuah Hypothesis Ledger** with reproducible positive-control bounds.
