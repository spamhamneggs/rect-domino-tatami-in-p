"""Monomer-dimer fallback for rectangles with no domino-only tatami tiling.

Companion to paper-draft, Section 5. For every r x c rectangle this module
constructs a monomer-dimer tatami tiling by restricting an infinite
running-bond layout to the rectangle. Cells whose partner falls outside
become monomers, and the script uses the cheaper of the two bond
orientations. It then verifies each tiling independently:

  1. Exact cover: every cell is covered exactly once; every domino covers
     two orthogonally adjacent cells.
  2. Tatami: every interior grid point has a domino covering two of its
     four incident cells; equivalently, the matching meets every 4-cycle.
  3. Monomer bound: m <= min(r, c), with m = min over the two
     orientations, all monomers on the boundary.
  4. Parity: m has the same parity as r*c.
  5. No-instance coverage: every (r, c) with 1 <= r, c <= 16 for which
     validate_tatami_dp.tileable() answers no gets a verified tiling.

Uses only the standard library. Exit code 0 iff every check passes.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_tatami_dp import tileable


def orientation_counts(r, c):
    """Monomer counts of the horizontal (h) and vertical (v) bond layouts."""
    h = 2 * (r // 2) if c % 2 == 0 else r
    v = 2 * (c // 2) if r % 2 == 0 else c
    return h, v


def construct(r, c):
    """Return (placements, orientation) for an r x c monomer-dimer tatami tiling.

    placements is a list of ('M', i, j) monomers and ('D', i0, j0, i1, j1)
    dominoes. orientation is 'H' or 'V'.
    """
    if r < 1 or c < 1:
        raise ValueError("dimensions must be positive")
    h, v = orientation_counts(r, c)
    placements = []
    if h <= v:
        for i in range(r):
            if i % 2 == 0:  # pairs (2k, 2k+1); cell c-1 is a monomer if c is odd
                j = 0
                while j + 1 < c:
                    placements.append(("D", i, j, i, j + 1))
                    j += 2
                if j < c:
                    placements.append(("M", i, j))
            else:  # pairs (2k+1, 2k+2); cell 0 is a monomer, and cell c-1 too if c is even
                placements.append(("M", i, 0))
                j = 1
                while j + 1 < c:
                    placements.append(("D", i, j, i, j + 1))
                    j += 2
                if j < c:
                    placements.append(("M", i, j))
        return placements, "H"
    for j in range(c):
        if j % 2 == 0:  # pairs (2k, 2k+1); cell r-1 is a monomer if r is odd
            i = 0
            while i + 1 < r:
                placements.append(("D", i, j, i + 1, j))
                i += 2
            if i < r:
                placements.append(("M", i, j))
        else:  # pairs (2k+1, 2k+2); cell 0 is a monomer, and cell r-1 too if r is even
            placements.append(("M", 0, j))
            i = 1
            while i + 1 < r:
                placements.append(("D", i, j, i + 1, j))
                i += 2
            if i < r:
                placements.append(("M", i, j))
    return placements, "V"


def check_cover(r, c, placements):
    """Verify exact cover; return (pair, monomers) or raise AssertionError."""
    cover = [[0] * c for _ in range(r)]
    pair = {}
    monomers = set()
    for p in placements:
        if p[0] == "M":
            _, i, j = p
            assert 0 <= i < r and 0 <= j < c, f"monomer {(i, j)} out of range"
            cover[i][j] += 1
            monomers.add((i, j))
        else:
            _, i0, j0, i1, j1 = p
            for (i, j) in ((i0, j0), (i1, j1)):
                assert 0 <= i < r and 0 <= j < c, f"domino {p} out of range"
                cover[i][j] += 1
            assert abs(i0 - i1) + abs(j0 - j1) == 1, f"domino {p} not adjacent"
            assert (i0, j0) not in pair and (i1, j1) not in pair, (
                f"domino {p} overlaps"
            )
            pair[(i0, j0)] = (i1, j1)
            pair[(i1, j1)] = (i0, j0)
    for i in range(r):
        for j in range(c):
            assert cover[i][j] == 1, f"cell {(i, j)} covered {cover[i][j]} times"
    assert not (set(pair) & monomers), "cell is both monomer and domino"
    return pair, monomers


def check_tatami(r, c, pair):
    """Verify no interior grid point has four tiles meeting."""
    for i in range(1, r):
        for j in range(1, c):
            a, b = (i - 1, j - 1), (i - 1, j)
            d, e = (i, j - 1), (i, j)
            assert (
                pair.get(a) == b
                or pair.get(d) == e
                or pair.get(a) == d
                or pair.get(b) == e
            ), f"tatami violation at interior point {(i, j)}"


def check_monomers(r, c, monomers, orientation):
    """Verify count, bound, parity, and boundary placement."""
    m = len(monomers)
    h, v = orientation_counts(r, c)
    assert m == (h if orientation == "H" else v), (
        f"count {m} != orientation formula {(h, v)} {orientation}"
    )
    assert m == min(h, v), f"count {m} is not minimal over orientations"
    assert m <= min(r, c), f"count {m} exceeds min(r, c)"
    assert m % 2 == (r * c) % 2, f"count {m} parity vs area {r * c}"
    for (i, j) in monomers:
        assert i in (0, r - 1) or j in (0, c - 1), (
            f"interior monomer {(i, j)}"
        )
    return m


def verify(r, c):
    """Construct and fully verify the fallback tiling; return (m, orientation)."""
    placements, orientation = construct(r, c)
    pair, monomers = check_cover(r, c, placements)
    check_tatami(r, c, pair)
    m = check_monomers(r, c, monomers, orientation)
    return m, orientation


def main():
    if not __debug__:
        print("refusing to run with assertions disabled (python -O)")
        return 2
    failed = False

    # 1. Exhaustive verification on 1 <= r, c <= 30 (900 tilings).
    bad = []
    worst_m = 0
    t0 = time.time()
    for r in range(1, 31):
        for c in range(1, 31):
            try:
                m, _ = verify(r, c)
                worst_m = max(worst_m, m - min(r, c))
            except AssertionError as e:
                bad.append((r, c, str(e)))
    dt = time.time() - t0
    print(f"exhaustive 1..30: {900 - len(bad)}/900 verified in {dt:.2f}s "
          f"(max m - min(r,c) = {worst_m}; failures: {bad[:4]})")
    failed = failed or bool(bad)

    # 2. Every domino no-instance at 1 <= r, c <= 16 gets a tiling.
    no_instances = []
    uncovered = []
    examples = {}
    for r in range(1, 17):
        for c in range(1, 17):
            if not tileable(r, c):
                no_instances.append((r, c))
                try:
                    m, o = verify(r, c)
                    if (r, c) in ((7, 10), (8, 11), (9, 13), (3, 3)):
                        examples[(r, c)] = (m, o)
                except AssertionError as e:
                    uncovered.append((r, c, str(e)))
    print(f"no-instances 1..16: {len(no_instances)} found, "
          f"{len(no_instances) - len(uncovered)} tiled "
          f"(uncovered: {uncovered[:4]})")
    for k in sorted(examples):
        print(f"  example {k[0]}x{k[1]}: m={examples[k][0]} "
              f"orientation={examples[k][1]}")
    failed = failed or bool(uncovered) or not no_instances

    # 3. Scaling spot checks.
    for (r, c) in ((100, 101), (97, 53), (200, 301), (1000, 999)):
        t0 = time.time()
        try:
            m, o = verify(r, c)
            print(f"  {r}x{c}: m={m} orientation={o} "
                  f"in {time.time() - t0:.2f}s")
        except AssertionError as e:
            print(f"  {r}x{c}: FAILED {e}")
            failed = True

    # 4. Invalid input rejected.
    for (r, c) in ((0, 5), (5, 0), (-1, 3)):
        try:
            construct(r, c)
            print(f"  invalid {(r, c)}: NOT REJECTED")
            failed = True
        except ValueError:
            pass
    print("invalid inputs rejected: ok")

    if failed:
        print("VALIDATION FAILED")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
