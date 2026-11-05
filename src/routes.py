def rowcol_paths(R, C):
    out = {}
    for major in ("row", "col"):
        n_outer, n_inner = (R, C) if major == "row" else (C, R)
        for outer_rev in (0, 1):
            for inner_rev in (0, 1):
                for snake in (0, 1):
                    outer = list(range(n_outer))
                    if outer_rev:
                        outer.reverse()
                    cells = []
                    for k, o in enumerate(outer):
                        inner = list(range(n_inner))
                        if inner_rev ^ (snake and k % 2 == 1):
                            inner.reverse()
                        for i in inner:
                            cells.append(o * C + i if major == "row" else i * C + o)
                    out[f"{major}{'U' if outer_rev else ''}{'i' if inner_rev else ''}{'S' if snake else ''}"] = cells
    return out


def spiral_path(R, C, start, dirs, d0):
    seen, cells = set(), []
    r, c = start
    d = d0
    for _ in range(R * C):
        cells.append(r * C + c)
        seen.add((r, c))
        moved = False
        for _turn in range(2):
            dr, dc = dirs[d]
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen:
                r, c = nr, nc
                moved = True
                break
            d = (d + 1) % 4
        if not moved:
            break
    return cells if len(cells) == R * C else None


def spiral_paths(R, C):
    cw = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    ccw = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    corners = {"TL": (0, 0), "TR": (0, C - 1), "BR": (R - 1, C - 1), "BL": (R - 1, 0)}
    out, seen = {}, set()
    for cname, st in corners.items():
        for sense, dirs in (("cw", cw), ("ccw", ccw)):
            for d0 in range(4):
                p = spiral_path(R, C, st, dirs, d0)
                if p and tuple(p) not in seen:
                    seen.add(tuple(p))
                    out[f"sp{cname}{sense}"] = p
    return out


def diag_paths(R, C):
    out = {}
    for fr in (0, 1):
        for fc in (0, 1):
            for rev in (0, 1):
                for snake in (0, 1):
                    cells = []
                    for d in range(R + C - 1):
                        rs = [r for r in range(R) if 0 <= d - r < C]
                        if rev:
                            rs.reverse()
                        if snake and d % 2 == 1:
                            rs.reverse()
                        for r in rs:
                            c = d - r
                            rr = R - 1 - r if fr else r
                            cc = C - 1 - c if fc else c
                            cells.append(rr * C + cc)
                    out[f"dg{'V' if fr else ''}{'H' if fc else ''}{'r' if rev else ''}{'S' if snake else ''}"] = cells
    return out


def all_paths(R, C):
    base = {}
    base.update(rowcol_paths(R, C))
    base.update(spiral_paths(R, C))
    base.update(diag_paths(R, C))
    paths, seen = {}, set()
    for name, cells in base.items():
        for tag, p in ((name, cells), (name + "~", cells[::-1])):
            t = tuple(p)
            if t not in seen:
                seen.add(t)
                paths[tag] = p
    return paths


def route_orders(N, dims=None, min_cols=2, max_cols=None):
    max_cols = max_cols or (N - 1)
    seen = set()
    cols = dims if dims is not None else range(min_cols, max_cols + 1)
    for C in cols:
        R = -(-N // C)
        if R < 2:
            continue
        paths = all_paths(R, C)
        for wname, wp in paths.items():
            widx = [-1] * (R * C)
            for k in range(N):
                widx[wp[k]] = k
            for rname, rp in paths.items():
                order = [widx[c] for c in rp if widx[c] >= 0]
                key = bytes(order)
                if key in seen:
                    continue
                seen.add(key)
                yield f"{R}x{C}:{wname}>{rname}", order


if __name__ == "__main__":
    assert spiral_path(3, 3, (0, 0), [(0, 1), (1, 0), (0, -1), (-1, 0)], 0) == [0, 1, 2, 5, 8, 7, 6, 3, 4]
    assert rowcol_paths(2, 3)["rowS"] == [0, 1, 2, 5, 4, 3]
    n = sum(1 for _ in route_orders(97))
    print("distinct route transpositions for N=97:", n)
