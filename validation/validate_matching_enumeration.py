"""Direct matching enumeration and arithmetic checks for paper-draft, Section 5.2.

The enumerator generates exact covers and checks the local tatami condition.
It does not use the block decomposition or published tables to generate counts.
Python 3 standard library only; no source PDFs or review files are required.
"""

import json
from collections import defaultdict
from functools import cache

from validate_tatami_dp import (
    HICKERSON_T,
    TABLE2,
    arithmetic_tileable,
    count_tilings,
    tileable,
)


def direct_count(r, c, monomer_target=0):
    """Enumerate row profiles, allowing exactly monomer_target monomers.

    Rotate to minimize profile width. incoming marks vertical dominoes from
    the preceding row. horizontal marks horizontal dominoes by their left
    cells. A seam vertex needs a horizontal edge in either incident row or
    a vertical edge between the two rows on its four-cell cycle.
    """
    if r < 1 or c < 1 or monomer_target < 0:
        raise ValueError("dimensions must be positive and monomer count nonnegative")
    r, c = max(r, c), min(r, c)
    full = (1 << c) - 1

    @cache
    def row_options(incoming, previous_horizontal, first, last, budget):
        options = defaultdict(int)

        def fill(occupied, outgoing, horizontal, used):
            if occupied == full:
                if not first:
                    for j in range(c - 1):
                        if not (
                            (previous_horizontal | horizontal) & (1 << j)
                            or incoming & (3 << j)
                        ):
                            return
                options[(outgoing, horizontal, used)] += 1
                return
            free = full ^ occupied
            bit = free & -free
            j = bit.bit_length() - 1
            if j + 1 < c and free & (bit << 1):
                fill(occupied | bit | (bit << 1), outgoing, horizontal | bit, used)
            if not last:
                fill(occupied | bit, outgoing | bit, horizontal, used)
            if used < budget:
                fill(occupied | bit, outgoing, horizontal, used + 1)

        fill(incoming, 0, 0, 0)
        return tuple((*key, value) for key, value in options.items())

    profiles = {(0, 0, 0): 1}
    for i in range(r):
        next_profiles = defaultdict(int)
        for (incoming, previous_horizontal, used), count in profiles.items():
            for outgoing, horizontal, added, ways in row_options(
                incoming, previous_horizontal, i == 0, i == r - 1, monomer_target - used
            ):
                next_profiles[(outgoing, horizontal, used + added)] += count * ways
        profiles = next_profiles
    return sum(
        count
        for (outgoing, horizontal, used), count in profiles.items()
        if outgoing == 0 and used == monomer_target
    )


def reachable_widths(m, limit):
    """Evaluate the block recurrence once for all widths up to limit."""
    if m % 2:
        reach = [False] * (limit + 1)
        reach[0] = True
        for i in range(limit + 1):
            if reach[i]:
                for w in (m - 1, m + 1):
                    if i + w <= limit:
                        reach[i + w] = True
        return reach
    short = [False] * (limit + 1)
    long = [False] * (limit + 1)
    short[1] = True
    long[m - 2] = long[m] = True
    for i in range(limit + 1):
        if short[i]:
            for w in (m - 2, m):
                if i + w <= limit:
                    long[i + w] = True
        if long[i] and i < limit:
            short[i + 1] = True
    return [s or ell for s, ell in zip(short, long)]


def main():
    if not __debug__:
        raise RuntimeError("Run without -O; validation requires assertions")
    rectangles = {(m, n) for m in range(1, 11) for n in range(m, 31)}
    rectangles.update((m, n) for m in range(1, 17) for n in range(m, 17))
    counts = {}
    determined_counts = 0
    for m, n in sorted(rectangles):
        count = direct_count(m, n)
        counts[(m, n)] = count
        for r, c in ((m, n), (n, m)):
            assert arithmetic_tileable(r, c) == (count > 0), (r, c, count)
            assert tileable(r, c) == (count > 0), (r, c, count)
        expected = count_tilings(m, n)
        if expected is not None:
            assert count == expected, (m, n, count, expected)
            determined_counts += 1
    table_checks = {}
    for name, table, size in (("RW09", TABLE2, 16), ("Hickerson", HICKERSON_T, 15)):
        for r in range(1, size + 1):
            for c in range(1, size + 1):
                count = counts[(min(r, c), max(r, c))]
                assert count == table[r][c - 1], (name, r, c, count)
        table_checks[name] = size * size

    arithmetic_cases = 0
    for m in range(1, 101):
        for n in range(m, 501):
            assert arithmetic_tileable(m, n) == tileable(m, n), (m, n)
            arithmetic_cases += 1
    for m in (3, 5, 7, 8, 10, 16, 31, 32, 99, 100, 999, 1000):
        limit = 10000
        reach = reachable_widths(m, limit)
        for n in range(m, limit + 1):
            assert arithmetic_tileable(m, n) == reach[n], (m, n)
            arithmetic_cases += 1

    huge_cases = [
        (10**100, 10**100),
        (10**100, 10**100 + 3),
        (10**100 + 1, 10**100 + 1),
        (10**100 + 1, 2 * 10**100),
    ]
    huge_results = [arithmetic_tileable(*case) for case in huge_cases]
    assert huge_results == [True, False, False, True], huge_results

    monomer_examples = {}
    for r, c, minimum, count in ((7, 10, 2, 36), (8, 11, 2, 34), (9, 13, 3, 80)):
        for q in range((r * c) % 2, minimum, 2):
            assert direct_count(r, c, q) == 0, (r, c, q)
        assert direct_count(r, c, minimum) == count, (r, c, minimum)
        monomer_examples[f"{r}x{c}"] = {"minimum": minimum, "count": count}
    for r, c in ((0, 5), (5, 0), (-1, 3)):
        for decide in (tileable, arithmetic_tileable, direct_count):
            try:
                decide(r, c)
            except ValueError:
                pass
            else:
                raise AssertionError(f"invalid dimensions accepted: {(r, c)}")
    print(
        json.dumps(
            {
                "direct_matching_rectangles": len(rectangles),
                "direct_matching_range": "shorter side <= 10, longer side <= 30; all sides <= 16",
                "block_count_comparisons": determined_counts,
                "direct_counts_vs_tables": table_checks,
                "arithmetic_vs_dp_comparisons": arithmetic_cases,
                "large_integer_examples": huge_results,
                "monomer_examples": monomer_examples,
                "status": "ALL CHECKS PASSED",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
