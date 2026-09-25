"""Validation for "Rectangular Domino Tatami Tiling is in P" (paper-draft, Section 6).

Compares the decision procedure of Section 4 against two published enumeration
tables: Ruskey and Woodcock Table 2 (T(m,n) for 1 <= m,n <= 16) and Hickerson's
t(r,s) table (1 <= r,s <= 15):

  1. Existence pattern: DECIDE(m,n) == (T(m,n) > 0) on all 256 RW09 entries
     and all 225 Hickerson entries.
  2. Exact counts where determined by the cited theorems: 227 RW09 entries
     and 198 Hickerson entries. The script checks entries with min(m,n) == 2
     for positivity only, because the draft does not cite the m = 2
     composition rule.
  3. Table symmetry on both tables, consistent with the rotation argument.

Uses only the standard library. Exit code 0 iff every check passes.

Table provenance: we transcribed the 256 values from Table 2 of F. Ruskey and
J. Woodcock, "Counting Fixed-Height Tatami Tilings", Electron. J. Combin.
16(1):R126, 2009. The transcription derives from a text extraction of the
published PDF; we verified it entry-by-entry against the PDF on 2026-09-22.

Hickerson's 225 values come from the t(r,s) table in D. Hickerson, "Filling
rectangular rooms with Tatami mats", OEIS A068920, March 2002
(https://oeis.org/A068920/a068920.txt), kept in the repo as
Sources/a068920.txt. We generated the transcription programmatically from
that file and verified it entry-by-entry on 2026-09-24.
"""

import sys

# TABLE2[m] = [T(m,1), ..., T(m,16)]. See provenance note above.
TABLE2 = {
    1: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    2: [1, 2, 3, 4, 6, 9, 13, 19, 28, 41, 60, 88, 129, 189, 277, 406],
    3: [0, 3, 0, 4, 0, 6, 0, 10, 0, 16, 0, 26, 0, 42, 0, 68],
    4: [1, 4, 4, 2, 3, 3, 3, 5, 5, 6, 8, 8, 11, 13, 14, 19],
    5: [0, 6, 0, 3, 0, 2, 0, 2, 0, 4, 0, 4, 0, 6, 0, 8],
    6: [1, 9, 6, 3, 2, 2, 2, 1, 1, 2, 3, 4, 3, 3, 3, 4],
    7: [0, 13, 0, 3, 0, 2, 0, 2, 0, 0, 0, 2, 0, 4, 0, 2],
    8: [1, 19, 10, 5, 2, 1, 2, 2, 2, 1, 0, 0, 1, 2, 3, 4],
    9: [0, 28, 0, 5, 0, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2],
    10: [1, 41, 16, 6, 4, 2, 0, 1, 2, 2, 2, 1, 0, 0, 0, 0],
    11: [0, 60, 0, 8, 0, 3, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0],
    12: [1, 88, 26, 8, 4, 4, 2, 0, 0, 1, 2, 2, 2, 1, 0, 0],
    13: [0, 129, 0, 11, 0, 3, 0, 1, 0, 0, 0, 2, 0, 2, 0, 0],
    14: [1, 189, 42, 13, 6, 3, 4, 2, 0, 0, 0, 1, 2, 2, 2, 1],
    15: [0, 277, 0, 14, 0, 3, 0, 3, 0, 0, 0, 0, 0, 2, 0, 2],
    16: [1, 406, 68, 19, 8, 4, 2, 4, 2, 0, 0, 0, 0, 1, 2, 2],
}

# HICKERSON_T[r] = [t(r,1), ..., t(r,15)]. See provenance note above.
HICKERSON_T = {
    1: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    2: [1, 2, 3, 4, 6, 9, 13, 19, 28, 41, 60, 88, 129, 189, 277],
    3: [0, 3, 0, 4, 0, 6, 0, 10, 0, 16, 0, 26, 0, 42, 0],
    4: [1, 4, 4, 2, 3, 3, 3, 5, 5, 6, 8, 8, 11, 13, 14],
    5: [0, 6, 0, 3, 0, 2, 0, 2, 0, 4, 0, 4, 0, 6, 0],
    6: [1, 9, 6, 3, 2, 2, 2, 1, 1, 2, 3, 4, 3, 3, 3],
    7: [0, 13, 0, 3, 0, 2, 0, 2, 0, 0, 0, 2, 0, 4, 0],
    8: [1, 19, 10, 5, 2, 1, 2, 2, 2, 1, 0, 0, 1, 2, 3],
    9: [0, 28, 0, 5, 0, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0],
    10: [1, 41, 16, 6, 4, 2, 0, 1, 2, 2, 2, 1, 0, 0, 0],
    11: [0, 60, 0, 8, 0, 3, 0, 0, 0, 2, 0, 2, 0, 0, 0],
    12: [1, 88, 26, 8, 4, 4, 2, 0, 0, 1, 2, 2, 2, 1, 0],
    13: [0, 129, 0, 11, 0, 3, 0, 1, 0, 0, 0, 2, 0, 2, 0],
    14: [1, 189, 42, 13, 6, 3, 4, 2, 0, 0, 0, 1, 2, 2, 2],
    15: [0, 277, 0, 14, 0, 3, 0, 3, 0, 0, 0, 0, 0, 2, 0],
}


def tileable(r, c):
    """Section 4 decision procedure: does an r x c rectangle admit a
    pure-domino tatami tiling?"""
    m, n = min(r, c), max(r, c)
    if m == 1:
        return n % 2 == 0
    if m == 2:
        return True
    if m % 2 == 1:
        reach = [False] * (n + 1)
        reach[0] = True
        for i in range(n + 1):
            if reach[i]:
                for w in (m - 1, m + 1):
                    if i + w <= n:
                        reach[i + w] = True
        return reach[n]
    # m even, m >= 4: strict S/L alternation, either state may start/finish.
    reach_s = [False] * (n + 1)
    reach_l = [False] * (n + 1)
    reach_s[1] = True
    for w in (m - 2, m):
        if w <= n:
            reach_l[w] = True
    for i in range(n + 1):
        if reach_s[i]:
            for w in (m - 2, m):
                if i + w <= n:
                    reach_l[i + w] = True
        if reach_l[i] and i + 1 <= n:
            reach_s[i + 1] = True
    return reach_s[n] or reach_l[n]


def count_tilings(r, c):
    """Exact tiling count, or None where not determined by the cited theorems
    (min(r,c) == 2)."""
    m, n = min(r, c), max(r, c)
    if m == 1:
        return 1 if n % 2 == 0 else 0
    if m == 2:
        return None
    if m % 2 == 1:
        dp = [0] * (n + 1)
        dp[0] = 1
        for i in range(n + 1):
            for w in (m - 1, m + 1):
                if i + w <= n:
                    dp[i + w] += dp[i]
        return 2 * dp[n]
    num_s = [0] * (n + 1)
    num_l = [0] * (n + 1)
    num_s[1] = 1
    for w in (m - 2, m):
        if w <= n:
            num_l[w] += 1
    for i in range(n + 1):
        if num_s[i]:
            for w in (m - 2, m):
                if i + w <= n:
                    num_l[i + w] += num_s[i]
        if num_l[i] and i + 1 <= n:
            num_s[i + 1] += num_l[i]
    return num_s[n] + num_l[n]


def check_table(table, size):
    """Compare tileable() and count_tilings() against table[m][n-1] for
    1 <= m, n <= size. Returns (exist_bad, count_bad, count_ok,
    positivity_ok)."""
    exist_bad, count_bad = [], []
    count_ok = positivity_ok = 0
    for m in range(1, size + 1):
        for n in range(1, size + 1):
            published = table[m][n - 1]
            if tileable(m, n) != (published > 0):
                exist_bad.append((m, n, published))
            count = count_tilings(m, n)
            if count is None:
                if published > 0:
                    positivity_ok += 1
                else:
                    count_bad.append((m, n, "non-positive", published))
            elif count != published:
                count_bad.append((m, n, count, published))
            else:
                count_ok += 1
    return exist_bad, count_bad, count_ok, positivity_ok


def check_symmetric(table, size):
    """Pairs (m, n) with table[m][n] != table[n][m], for 1 <= m, n <= size."""
    return [
        (m, n)
        for m in range(1, size + 1)
        for n in range(1, size + 1)
        if table[m][n - 1] != table[n][m - 1]
    ]


def main():
    failed = False
    for name, table, size in (("RW09", TABLE2, 16), ("Hickerson", HICKERSON_T, 15)):
        total = size * size
        exist_bad, count_bad, count_ok, positivity_ok = check_table(table, size)
        asymmetric = check_symmetric(table, size)
        print(
            f"{name} existence: {total - len(exist_bad)}/{total} match "
            f"(mismatches: {exist_bad[:8]})"
        )
        print(
            f"{name} counts: {count_ok} exact matches, "
            f"{positivity_ok} positivity-only (min(m,n) == 2), "
            f"mismatches: {count_bad[:8]}"
        )
        print(
            f"{name} table symmetric: {not asymmetric} "
            f"({asymmetric[:8] if asymmetric else 'ok'})"
        )
        failed = failed or bool(exist_bad or count_bad or asymmetric)
    if failed:
        print("VALIDATION FAILED")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
