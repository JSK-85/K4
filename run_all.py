#!/usr/bin/env python3
import argparse, multiprocessing, os, random, subprocess, sys, tempfile, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
BIN = os.path.join(HERE, "bin")
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WORDS_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
N = 97
K4_FILE = os.path.join(HERE, "k4.txt")


def sh(cmd, env=None, cwd=HERE):
    return subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=cwd)


def compile_all():
    os.makedirs(BIN, exist_ok=True)
    for name in ("search", "hillvig"):
        r = sh(["gcc", "-O2", "-o", f"{BIN}/{name}", f"{SRC}/{name}.c"])
        if r.returncode != 0:
            sys.exit(f"Compile failed for {name}.c (is gcc/clang installed?):\n{r.stderr}")
    print("[1/7] compiled C searchers")


def crib_file(path, cipher):
    with open(path, "w") as f:
        f.write(cipher + "\n22 EASTNORTHEAST\n64 BERLINCLOCK\n")


def vig_ka(text, key):
    return [KA[(KA.index(c) + KA.index(key[i % len(key)])) % 26] for i, c in enumerate(text)]


def selftest():
    random.seed(3)
    p = [random.choice(AZ) for _ in range(N)]
    for i, ch in enumerate("EASTNORTHEAST"): p[21 + i] = ch
    for i, ch in enumerate("BERLINCLOCK"): p[63 + i] = ch
    w, perm = 7, [4, 1, 6, 0, 3, 5, 2]
    order = [x for col in perm for x in range(col, N, w)]
    y = vig_ka(p, "SHADOW")
    cipher = "".join(y[order[j]] for j in range(N))
    tmp = os.path.join(HERE, "_selftest.txt")
    crib_file(tmp, cipher)
    out = sh([f"{BIN}/search", tmp, "7", "12", "7", "7"]).stdout
    ok1 = any("key=SHADOW" in l and "w=7" in l for l in out.splitlines())
    M = [[3, 5], [7, 12]]
    idx = [KA.index(c) for c in vig_ka(p, "LIGHT")]
    h = []
    for i in range(0, N - 1, 2):
        a, b = idx[i], idx[i + 1]
        h += [KA[(a * M[0][0] + b * M[1][0]) % 26], KA[(a * M[0][1] + b * M[1][1]) % 26]]
    h.append(KA[idx[-1]])
    crib_file(tmp, "".join(h))
    out2 = sh([f"{BIN}/hillvig", tmp, "11", "7"]).stdout
    ok2 = any("key=LIGHT" in l for l in out2.splitlines())
    os.remove(tmp)
    if not (ok1 and ok2):
        sys.exit(f"SELF-TEST FAILED (transposition={ok1}, hill={ok2}) - results would be meaningless.")
    print("[2/7] self-test passed (planted transposition+key and Hill+key both recovered)")



def run_routes(cfile, jobs, double_w=0, dims=None):
    sys.path.insert(0, SRC)
    import routes
    env = dict(os.environ)
    if double_w >= 2:
        env["DOUBLE_W"] = str(double_w)
    outs, procs = [], []
    for _ in range(jobs):
        f = tempfile.NamedTemporaryFile("w+", delete=False, suffix=".hits")
        outs.append(f)
        procs.append(subprocess.Popen([f"{BIN}/search", cfile, "0", "14", "7", "2", "rawperm", "-"],
                                      stdin=subprocess.PIPE, stdout=f, stderr=subprocess.DEVNULL,
                                      text=True, env=env))
    n = 0
    for label, order in routes.route_orders(N, dims=dims):
        procs[n % jobs].stdin.write(label + " " + " ".join(map(str, order)) + "\n")
        n += 1
    hits = []
    for p, f in zip(procs, outs):
        p.stdin.close()
        p.wait()
        f.seek(0)
        hits += [l.strip() for l in f if l.startswith("HIT")]
        f.close()
        os.remove(f.name)
    return n, hits


def selftest_routes():
    sys.path.insert(0, SRC)
    import routes
    assert routes.spiral_path(3, 3, (0, 0), [(0, 1), (1, 0), (0, -1), (-1, 0)], 0) == [0, 1, 2, 5, 8, 7, 6, 3, 4]
    random.seed(21)
    p = [random.choice(AZ) for _ in range(N)]
    for i, ch in enumerate("EASTNORTHEAST"): p[21 + i] = ch
    for i, ch in enumerate("BERLINCLOCK"): p[63 + i] = ch
    y = vig_ka(p, "ABSCISSA")
    tmp = os.path.join(HERE, "_selftest_routes.txt")

    items = [it for it in routes.route_orders(N, dims=[11]) if ">sp" in it[0]]
    label, order = items[len(items) // 2]
    crib_file(tmp, "".join(y[order[j]] for j in range(N)))
    n, hits = run_routes(tmp, 1, dims=[11])
    ok_a = any(label in h and "key=ABSCISSA" in h for h in hits)

    label2, A = list(routes.route_orders(N, dims=[13]))[200]
    w, perm = 5, [3, 0, 4, 1, 2]
    B = [x for col in perm for x in range(col, N, w)]
    T = [A[B[j]] for j in range(N)]
    crib_file(tmp, "".join(y[T[j]] for j in range(N)))
    n2, hits2 = run_routes(tmp, 1, double_w=5, dims=[13])
    ok_b = any(label2 in h and "route-then-col(w=5,perm=30412)" in h and "key=ABSCISSA" in h for h in hits2)
    os.remove(tmp)
    if not (ok_a and ok_b):
        sys.exit(f"ROUTE SELF-TEST FAILED (route={ok_a}, route+columnar={ok_b}).")
    print("[2b]  route self-test passed (planted spiral-type route and route+columnar both recovered)")


def run_python_tests():
    for name in ("tests.py", "hill.py"):
        r = sh([sys.executable, f"{SRC}/{name}"], cwd=HERE)
        print(f"[3/7] {name}:")
        print("   " + r.stdout.strip().replace("\n", "\n   "))
        if r.returncode != 0:
            print("   (skipped/failed:", r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "?", ")")


def search_job(args):
    part, nparts, maxw, minw = args
    env = dict(os.environ, PART=str(part), NPARTS=str(nparts))
    r = sh([f"{BIN}/search", os.path.join(HERE, "k4.txt"), str(maxw), "12", "7", str(minw)], env=env)
    return [l for l in r.stdout.splitlines() if l.startswith("HIT")]


def run_transposition(maxw, jobs):
    hits = []
    t0 = time.time()
    with multiprocessing.Pool(jobs) as pool:
        for hs in pool.imap_unordered(search_job, [(j, jobs, maxw, 2) for j in range(jobs)]):
            hits += hs
    print(f"[4/7] columnar transposition (all permutations, widths 2-{maxw}) x periodic key: "
          f"{len(hits)} hit(s) in {time.time() - t0:.0f}s")
    return hits


def run_keywords(skip):
    if skip:
        print("[5/7] keyword-transposition search skipped")
        return []
    words = os.path.join(SRC, "words.txt")
    if not os.path.exists(words):
        try:
            print("      downloading wordlist ...")
            urllib.request.urlretrieve(WORDS_URL, words)
        except Exception as e:
            print(f"[5/7] could not download wordlist ({e}); skipping keyword search")
            return []
    sh([sys.executable, f"{SRC}/mkperms.py"], cwd=SRC)
    r = sh([f"{BIN}/search", os.path.join(HERE, "k4.txt"), "0", "14", "7", "2", "permfile",
            os.path.join(SRC, "perms.txt")])
    hits = [l for l in r.stdout.splitlines() if l.startswith("HIT")]
    print(f"[5/7] keyword-derived columnar transpositions (dictionary, widths up to 25): {len(hits)} hit(s)")
    return hits


def run_hill():
    r = sh([f"{BIN}/hillvig", os.path.join(HERE, "k4.txt"), "11", "7"])
    hits = [l for l in r.stdout.splitlines() if l.startswith("HIT")]
    print(f"[6/7] Hill 2x2 + periodic key (every invertible matrix, both orders): {len(hits)} hit(s)")
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxwidth", type=int, default=10)
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--skip-wordlist", action="store_true")
    ap.add_argument("--double", type=int, default=6)
    ap.add_argument("--skip-routes", action="store_true")
    a = ap.parse_args()
    print(f"K4 search | cores used: {a.jobs} | max width: {a.maxwidth}\n")
    compile_all()
    selftest()
    selftest_routes()
    run_python_tests()
    hits = run_transposition(a.maxwidth, a.jobs)
    hits += run_keywords(a.skip_wordlist)
    hits += run_hill()
    if not a.skip_routes:
        t0 = time.time()
        n, rh = run_routes(K4_FILE, a.jobs, double_w=a.double)
        extra = f" + route x columnar double transposition (columnar width <= {a.double}, both orders)" if a.double >= 2 else ""
        print(f"[7/7] route transpositions ({n} distinct: spirals, snakes, diagonals, row/col reads){extra} x keyed periodic key: "
              f"{len(rh)} hit(s) in {time.time() - t0:.0f}s")
        hits += rh
    with open(os.path.join(HERE, "hits.txt"), "w") as f:
        f.write("\n".join(hits) + ("\n" if hits else ""))
    print()
    if hits:
        print(f"*** {len(hits)} CANDIDATE(S) FOUND - see hits.txt. Decrypt with that key/transposition and read the result.")
        print("    (A hit means the key stream is consistent with the cribs; it is not proof until the text reads as English.)")
        for h in hits[:10]: print("   ", h)
    else:
        print("No candidates. Everything tested is ruled out (assuming the cribs sit where Sanborn said).")


if __name__ == "__main__":
    main()
