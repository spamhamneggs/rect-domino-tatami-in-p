# Validation for "Arithmetic criteria for domino tatami tilings of rectangles"

Supplementary material for `paper-draft`, Section 3.1 on the decision
procedures, Section 3.2 on correctness, Section 3.3 on complexity and
tiling certificates, Section 4 on the running-bond construction, and
Section 5 on computational verification.
All three scripts use only the Python 3 standard library and run without
the source PDFs or the internal review directory.

## What it does

`validate_tatami_dp.py` contains `arithmetic_tileable(r, c)`, the binary-input
procedure `DECIDE` of Section 3.1, and retains Hickerson's Boolean block
recurrence as `tileable(r, c)`. The arithmetic procedure uses a constant number
of integer operations with polynomial bit cost. The DP scans the longer side
`n`, using `O(n)` Boolean entries. The possible `O(m)` sliding window is not
implemented. Both procedures are checked against Ruskey and Woodcock Table 2 ($T(m,n)$ for
$1 \le m,n \le 16$) and Hickerson's $t(r,s)$ table ($1 \le r,s \le 15$):

1. **Existence pattern (RW09).** The program's yes/no answer matches $T(m,n) > 0$
   on all 256 entries, including every no-instance, e.g. $7 \times 10$ and
   $8 \times 11$.
2. **Exact counts (RW09).** The program's counts match all 227 entries where the
   cited theorems determine counts: odd heights with the doubling factor, even
   heights $\ge 4$ with strict $S$/$L$ alternation, and height 1. The 29 entries with $\min(m,n) = 2$ were checked
   for tileability only, since the draft does not
   cite the $m = 2$ composition rule.
3. **Table symmetry (both tables).** $T(m,n) = T(n,m)$ holds on all entries of
   each table, consistent with the rotation argument of Section 2.
4. **Hickerson cross-check.** The same comparisons against Hickerson's
   $t(r,s)$ table for $1 \le r, s \le 15$ agree on all 225 existence entries and
   all 198 determined counts, with existence-only checks on the 27 entries with
   $\min(m,n) = 2$.

Both tables derive from the same decomposition, and Hickerson's 225 entries
are a subset of the RW09 table. These are consistency checks, rather than
independent validation of the decomposition.

## Independent matching enumeration

`validate_matching_enumeration.py` generates exact covers directly by row profiles.
It considers every filling of each row and requires a matched edge on every
four-cell cycle. Block widths and table values are not used to generate counts.
The profile width is the shorter side, after rotation.

The script checks all 276 distinct normalized rectangles in the union of
`1 <= m <= 10, m <= n <= 30` and `1 <= m <= n <= 16`:

- Direct existence agrees with both decision procedures in both input orders.
- Direct exact counts match all 256 RW09 and 225 Hickerson entries, including
  height two. Counts also match the block counter on its 247 determined cases
  in the normalized search set.
- Arithmetic criteria agree with Boolean block recurrences in 162,752
  comparisons. The first sweep covers `1 <= m <= 100, m <= n <= 500`.
  The second covers `m <= n <= 10000` at heights
  `3, 5, 7, 8, 10, 16, 31, 32, 99, 100, 999, 1000`.
  Some pairs occur in both sweeps.
- Four examples with 101-digit dimensions exercise the binary-input procedure without
  arrays indexed by the dimensions.
- The examples `7 x 10`, `8 x 11`, and `9 x 13` have minimum monomer counts
  2, 2, and 3, respectively, with 36, 34, and 80 tilings at those counts.
  All smaller counts of the required area parity give zero.
- Both decision implementations and the enumerator reject nonpositive dimensions.

Enumeration is bounded computational evidence. It does not replace the proofs
or establish a general bound of three monomers.

## Fallback construction

`validate_monomer_fallback.py` implements the running-bond construction of
Section 4. It restricts a running bond to the rectangle in the cheaper
orientation and verifies each emitted tiling for exact cover, the tatami
condition at every interior grid point, the orientation count formulas
with $\mu \le \min(r,c)$, parity $\mu \equiv rc \pmod 2$, and boundary
placement of all monomers. Here $\mu$ is the monomer count, written `mu`
in the script. It checks all 900 tilings with
$1 \le r, c \le 30$, confirms every domino no-instance with
$1 \le r, c \le 16$ receives a tiling, and runs scaling spot checks up to
$1000 \times 999$. This is not a minimum-monomer algorithm.

## Provenance of the embedded table

The 256 values were transcribed from Table 2 of F. Ruskey and J. Woodcock,
"Counting Fixed-Height Tatami Tilings", _Electron. J. Combin._ 16(1):R126, 2009.
The transcription derives from a text extraction of the published PDF and was verified
entry-by-entry against the PDF. The local reference copy is
`../Sources/215-PDF file-275-1-10-20120107.pdf`. That filename is recorded
here, rather than in the manuscript's bibliography. Source copies are not
required to run the supplementary scripts.

Hickerson's 225 values come from the $t(r,s)$ table in D. Hickerson, "Filling
rectangular rooms with Tatami mats", OEIS A068920, March 2002,
<https://oeis.org/A068920/a068920.txt>. The transcription was generated
programmatically from `../Sources/a068920.txt` and verified entry-by-entry.

## How to run

From the repository root, with the Python 3 standard library:

```sh
python3 validation/validate_tatami_dp.py
python3 validation/validate_matching_enumeration.py
python3 validation/validate_monomer_fallback.py
```

Expected output ends with `ALL CHECKS PASSED` and exit code 0. Any mismatch prints
the offending entries and exits nonzero. Keep assertions enabled; the independent
and fallback verifiers refuse to run under `python -O`. From inside this directory,
omit the `validation/` prefix in the commands above.
