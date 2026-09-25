# Validation for "Rectangular Domino Tatami Tiling is in P"

Supplementary material for `paper-draft`, Section 4 (decision procedure) and
Section 5 (monomer-dimer fallback).

## What it does

`validate_tatami_dp.py` implements the decision procedure of Section 4 and checks it
against two published enumeration tables: Ruskey and Woodcock Table 2 ($T(m,n)$ for
$1 \le m,n \le 16$) and Hickerson's $t(r,s)$ table ($1 \le r,s \le 15$):

1. **Existence pattern (RW09).** The program's yes/no answer matches $T(m,n) > 0$
   on all 256 entries, including every no-instance, e.g. $7 \times 10$ and
   $8 \times 11$.
2. **Exact counts (RW09).** The program's counts match all 227 entries where the
   cited theorems determine counts: odd heights with the doubling factor, even
   heights $\ge 4$ with strict $S$/$L$ alternation, and height 1. We checked the
   29 entries with $\min(m,n) = 2$ for positivity only, since the draft does not
   cite the $m = 2$ composition rule.
3. **Table symmetry (both tables).** $T(m,n) = T(n,m)$ holds on all entries of
   each table, consistent with the rotation argument of Section 2.
4. **Hickerson cross-check.** The same comparisons against Hickerson's independent
   $t(r,s)$ table for $1 \le r, s \le 15$ agree on all 225 existence entries and
   all 198 determined counts, with positivity-only checks on the 27 entries with
   $\min(m,n) = 2$.

This checks consistency between the implementation, the cited theorems, and the
published enumerations. It is evidence of correctness, not a substitute for the proof
in Section 4.

## Fallback construction

`validate_monomer_fallback.py` implements the `FALLBACK` construction of
Section 5. It restricts a running bond to the rectangle in the cheaper
orientation and verifies each emitted tiling for exact cover, the tatami
condition at every interior grid point, the orientation count formulas
with $m \le \min(r,c)$, parity $m \equiv rc \pmod 2$, and boundary
placement of all monomers. It checks all 900 tilings with
$1 \le r, c \le 30$, confirms every domino no-instance with
$1 \le r, c \le 16$ receives a tiling, and runs scaling spot checks up to
$1000 \times 999$.

## Provenance of the embedded table

We transcribed the 256 values from Table 2 of F. Ruskey and J. Woodcock,
"Counting Fixed-Height Tatami Tilings", _Electron. J. Combin._ 16(1):R126, 2009.
The transcription derives from a text extraction of the published PDF; we verified
it entry-by-entry against the PDF on 2026-09-22. We keep a copy of the source PDF
in `../Sources/`; the draft's references name the exact file.

Hickerson's 225 values come from the $t(r,s)$ table in D. Hickerson, "Filling
rectangular rooms with Tatami mats", OEIS A068920, March 2002,
https://oeis.org/A068920/a068920.txt. We generated the transcription
programmatically from `../Sources/a068920.txt` and verified it entry-by-entry
on 2026-09-24.

## How to run

Standard library only; any Python 3.6+ works:

```sh
python3 validate_tatami_dp.py
python3 validate_monomer_fallback.py
```

Expected output ends with `ALL CHECKS PASSED` and exit code 0. Any mismatch prints
the offending entries and exits nonzero.
