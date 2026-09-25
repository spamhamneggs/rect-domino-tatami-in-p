# Rectangular Domino Tatami Tiling is in P

**Author:** Rifki Kusmana

**Status:** Draft for development. Not submission-ready.

---

## Abstract

A domino covering of a rectilinear region is _tatami_ if no four dominoes meet at any point. Erickson and Ruskey proved that deciding whether a general rectilinear region admits a domino tatami covering is NP-complete. They stated their belief that the problem remains NP-complete for simply connected regions. We prove RECT-DTC, the rectangular special case with dominoes only, is in P. The proof combines the block-decomposition theorems of Ruskey and Woodcock for tatami tilings of rectangles with an explicit dynamic program that decides tileability in time linear in the longer side. We also supply a short coloring proof for the untileability of staircase triangles used throughout those arguments, cover all small-height and transposed cases, and validate the decision procedure computationally against two published enumeration tables. We close by discussing where the tractability boundary lies and what would be needed to extend the result. We also give a polytime construction of a monomer-dimer tatami tiling for every rectangle, using at most $\min(r, c)$ monomers, so each domino no-instance still receives a tiling.

## 1. Introduction

Tatami tilings, domino tilings in which no four tiles meet at a point, arise both in traditional Japanese floor layouts and in the combinatorics of domino tilings. From a computational perspective, the central problem is _Domino Tatami Covering_ (DTC), which asks, given a rectilinear region, whether it can be covered by dominoes satisfying the tatami constraint. Erickson and Ruskey proved DTC NP-complete by reduction from planar 3SAT [ER13]. Their hardness construction produces regions with holes, and they explicitly leave the simply connected (no holes) case open, stating their belief that it remains NP-complete.

Known results therefore leave a gap at the simplest end. To our knowledge, the complexity of the purely rectangular case has not been stated explicitly, even though the combinatorics of rectangular tatami tilings is well developed. Ruskey and Woodcock proved that pure-domino tatami tilings of rectangles decompose into concatenations of fixed-width blocks [RW09], and Erickson et al. gave the broader T-diagram structural theory for rectangles with monomers allowed [ERWS11]. These results suggest tractability, but a formal complexity statement with a defined decision problem, input encoding, decision procedure, and runtime bound has been missing.

**Contributions.** This paper makes six contributions: it defines the decision problem RECT-DTC (rectangular domino tatami tileability) with an explicit input encoding; proves that RECT-DTC is in P via a linear-time dynamic program over the cited block decomposition; supplies a short coloring proof for the staircase-triangle lemma used by the cited arguments and covers all small-height and transposed cases; validates the procedure computationally against every entry of two published enumeration tables, [RW09, Table 2] and Hickerson's $t(r,s)$ table [Hic02]; and discusses the tractability boundary between rectangles and the conjectured hard cases while listing concrete open items; and gives, for every domino no-instance, an explicit polytime monomer-dimer tatami tiling with at most $\min(r, c)$ monomers.

**Organization.** Section 2 defines the problem. Section 3 states the structural theorems we cite, with small additions. Section 4 gives the decision procedure, correctness argument, and complexity analysis. Section 5 gives the monomer-dimer fallback construction for no-instances. Section 6 reports the computational validation. Section 7 discusses the boundary and future work. Section 8 concludes.

## 2. Problem statement

Let $G_{r,c}$ be the $r \times c$ grid graph, with cells as vertices and edges joining orthogonal neighbors. A _domino tiling_ is a perfect matching, a set of edges covering every vertex exactly once. A tiling is _tatami_ if no four dominoes meet at any single point. Equivalently, following [ER13], a tatami tiling is a perfect matching meeting every 4-cycle. Around each interior grid vertex, the four incident cells form a 4-cycle of $G_{r,c}$, and a tatami violation at that vertex is exactly the absence of any matched edge on the cycle. If some domino covers two of the four cells, the vertex lies on that domino's edge rather than its corner, so fewer than four dominoes meet there. This is the $C_4$-transverse matching formulation of [CHZ11], with the added requirement that the matching be perfect; [ER13] uses it in exactly this form.

> **Problem RECT-DTC.** _Input:_ positive integers $r, c$, with the region given explicitly in the unary encoding, so the input size is $\Theta(rc)$. _Question:_ does the $r \times c$ rectangle admit a tatami tiling using dominoes only?

Two immediate observations. First, if $rc$ is odd, the answer is trivially no, since no domino tiling of any kind exists. Second, rotation preserves both domino tilings and the tatami property, so $T(r, c) = T(c, r)$ throughout; we always orient the rectangle with $m = \min(r, c)$ and $n = \max(r, c)$.

_Remark on encodings._ The unary (explicit-region) encoding is standard in tiling complexity. Hardness reductions in this area produce regions whose area is polynomial in the source instance [ER13]. Our main theorem uses it. For the odd-height case we also obtain a closed form decidable in polylogarithmic time, which covers the binary-coordinate encoding there. We leave the even-height binary case open (Section 4).

## 3. Structural foundations

We cite the decomposition theory of [RW09, Section 2] for $m \times n$ rectangles with $m \le n$. We restate the theorems we need and flag the points where we add to the cited proofs.

**Theorem 3.1** (Left-edge lemma [RW09, Thm. 2.2]). _In a tatami tiling of an $m \times n$ rectangle with $m \le n$, no horizontal tile touches the left edge unless it also touches the top or bottom edge._

The proof proceeds by contradiction. A middle horizontal tile on the left edge forces, via tatami-preserving cascades, either full horizontal rows or a diagonal cascade, and in every subcase leaves an untileable staircase-triangular region (see Remark 3.4).

**Theorem 3.2** (Odd heights [RW09, Thm. 2.3]). _If $m$ is odd and $m \le n$, every tatami tiling of the $m \times n$ rectangle is a concatenation of tiled $m \times (m-1)$ and $m \times (m+1)$ blocks._

**Theorem 3.3** (Even heights [RW09, Thm. 2.4]). _If $m$ is even, $m \ge 4$, and $m \le n$, every tatami tiling of the $m \times n$ rectangle is a strict alternation of width-1 all-vertical columns ($S$-blocks) and long blocks of width $m-2$ or $m$ ($L$-blocks), where the tiling may start and end with either type._

In particular, no two $S$-blocks are adjacent, since an all-vertical column forces top-and-bottom horizontals next for $m \ge 4$. No two $L$-blocks are adjacent, since a long block forces an all-vertical column next. Each valid block sequence corresponds to exactly one tiling; for odd $m \ge 3$, each composition corresponds to exactly two tilings, since the initial horizontal may sit at the top or bottom.

The following remark replaces a figure-only proof in [RW09, Thm. 2.1] with a self-contained argument covering all sizes.

**Remark 3.4** (Staircase triangles are untileable; proof ours). Let $S_k$ be the staircase region with rows of length $1, 2, \dots, k$. Under chessboard coloring with the length-1 row black, each even row has equal black and white squares while each odd row has one extra black square, so $S_k$ has black-minus-white imbalance $\lceil k/2 \rceil \ge 1$ for every $k$. Hence no staircase triangle admits a domino tiling. All triangular regions arising in the proofs of Theorems 3.1–3.3 are single-cell-step staircases, so the lemma applies everywhere it is invoked.

Small heights need no citation; both are elementary. The $m = 2$ composition rule stated in [RW09, Section 2.1] is not proved there, so we do not cite it.

**Lemma 3.5** (Small heights). _A $1 \times n$ rectangle has a tatami tiling iff $n$ is even, the unique all-horizontal tiling. A $2 \times n$ rectangle has a tatami tiling for every $n$: $n$ side-by-side vertical dominoes, whose corners meet only pairwise on the boundary._

_Notes on the cited proofs._ After the first block in Theorem 3.2 the seam mirrors from bottom to top; the mirrored forcing yields the same block widths by vertical symmetry. We also note that the caption of [RW09, Fig. 11] reads "when $n$ is even" where the proof requires "$m$ is even"; the proof text itself is correct.

## 4. Decision procedure

Orient the input with $m = \min(r, c)$, $n = \max(r, c)$ and dispatch on $m$:

- $m = 1$: answer yes iff $n$ is even (Lemma 3.5).
- $m = 2$: answer yes (Lemma 3.5).
- $m$ odd, $m \ge 3$: decide whether $n$ is a nonnegative combination of $m-1$ and $m+1$ by one-state reachability over positions $0, \dots, n$ with steps $m-1$ and $m+1$.
- $m$ even, $m \ge 4$: decide whether $n$ admits a strict $S$/$L$ alternation by two-state reachability. From state $S$ at position $i$ move to $L$ at $i + m - 2$ or $i + m$. From state $L$ move to $S$ at $i + 1$. Either state may start or finish.

```pseudocode
DECIDE(r, c):
    m, n = min(r, c), max(r, c)
    if m == 1: return (n mod 2 == 0)
    if m == 2: return True
    if m is odd:
        reach = {0}; for i in 0..n:
            if i in reach: reach += {i + m-1, i + m+1} (within bounds)
        return (n in reach)
    else:  # m even, m >= 4
        track (position, last-block-in-{S, L}) reachability as above
        return (n reachable in either state)
```

**Correctness.** _Completeness:_ if a tatami tiling exists, its block widths form a composition of the type the program accepts, by Theorems 3.2 and 3.3 for $m \ge 3$ and Lemma 3.5 for $m \le 2$. The program therefore answers yes. _Soundness:_ if the program answers yes, the accepted composition is realizable block by block. Figures 10 and 12 of [RW09] tile the long blocks, $S$-blocks are single all-vertical columns, and Lemma 3.5 covers $m \le 2$. Consecutive blocks join along forced, tatami-preserving seams. In the even case the column joints stagger by one row, so no four dominoes meet at any seam point. Hence a tatami tiling exists.

**Complexity.** The odd case scans $n + 1$ positions with two transitions each; the even case scans $n + 1$ positions times two states with at most two transitions each. Time is $O(n)$ and space is $O(m)$ with a sliding window, since transitions look back at most $m + 1$ positions. Since $n \le mn$ and the input has size $\Theta(mn)$, the procedure is polynomial. This proves the main result.

**Theorem 4.1 (Main result).** _RECT-DTC is in P._

_Remark (closed form for odd heights)._ For odd $m$, writing $k = (m-1)/2$, the parts $(m-1)/2 = k$ and $(m+1)/2 = k+1$ are consecutive, hence coprime, so by the Frobenius coin theorem every even $n \ge 2k(k-1)$ is tileable. For example with $m = 7$ and $k = 3$: for $n \ge 7$, the answer is yes iff $n$ is even and $n \ne 10$. This closed form decides the odd case in polylogarithmic time even under binary-coordinate encoding. No comparably clean closed form is known to us for the even case's alternating semigroup. We leave the binary encoding there to future work.

## 5. Monomer-dimer fallback for no-instances

When DECIDE answers no, the rectangle still admits a tatami tiling once monomers ($1 \times 1$ tiles) are allowed. A monomer-dimer tatami tiling is an exact cover by $1 \times 1$, $1 \times 2$, and $2 \times 1$ tiles with no four tiles meeting at a point [ERWS11]; in matching terms, monomers are unmatched vertices and the matching still meets every 4-cycle [ERWS11, Section 4.2]. Among the open problems of [ERSW10, Section 4], Erickson et al. note in passing that every grid graph admits such a tiling, e.g. by restricting the infinite running-bond layout to the region. The same aside appears in a later paper by the same authors [ERWS11, Section 4.2]. Neither gives more than that sketch. We prove the rectangle case here, with a monomer bound and a verified construction. What we guarantee is a valid tiling, not a minimal one; the remarks at the end of this section explain why.

**Construction.** Take the infinite horizontal running bond. In even rows dominoes cover column pairs $(2k, 2k+1)$, and in odd rows $(2k+1, 2k+2)$. Restrict it to the rectangle. Each cell whose partner falls outside becomes a monomer. The vertical bond is the transpose. Use whichever orientation yields fewer monomers (horizontal on ties). The counts are:

- horizontal: $m_H = 2\lfloor r/2 \rfloor$ if $c$ is even, else $m_H = r$;
- vertical: $m_V = 2\lfloor c/2 \rfloor$ if $r$ is even, else $m_V = c$.

```pseudocode
FALLBACK(r, c):
    compute m_H, m_V as above; pick H if m_H <= m_V else V
    emit the chosen bond restricted to the rectangle (cut cells become monomers)
```

**Theorem 5.1.** _Every $r \times c$ rectangle admits a monomer-dimer tatami tiling with $m = \min(m_H, m_V) \le \min(r, c)$ monomers, all on the boundary and $m \equiv rc \pmod 2$, constructible in $O(rc)$ time._

_Proof._ Tatami: in the infinite horizontal bond, the two rows incident to any grid point use opposite pairing parity. Exactly one of the two pairings contains the horizontal edge $\{j-1, j\}$ of the point's 4-cycle, namely the even pairing when $j$ is odd and the odd pairing when $j$ is even. So every 4-cycle has a matched edge. Restriction deletes only dominoes crossing the rectangle boundary; each 4-cycle fully inside keeps all four edges and hence its matched edge. Boundary points touch at most two tiles of the rectangle. The vertical case is symmetric.

Count: if $c$ is even, even rows tile fully while odd rows lose cells $0$ and $c-1$, giving $m_H = 2\lfloor r/2 \rfloor$. If $c$ is odd, every row loses exactly one cell, cell $c-1$ in even rows and cell $0$ in odd rows, so $m_H = r$. Since $m_H \le r$ and, symmetrically, $m_V \le c$, the minimum is at most $\min(r, c)$. All monomers lie in the outer rows or columns by construction. Parity: if $c$ is even, $rc$ is even and $m_H = 2\lfloor r/2 \rfloor$ is even; if $c$ is odd, $m_H = r \equiv rc \pmod 2$; symmetrically for $m_V$. Each orientation is correct on its own, so the chosen one is too. The construction visits each cell once, so it runs in $O(rc)$ time. Q.E.D.

Combined with Section 4, every rectangle is now covered. Yes-instances are certified domino-tileable, and each no-instance receives an explicit tiling. For example the no-instances $7 \times 10$, $8 \times 11$, and $9 \times 13$ receive tilings with $6$, $8$, and $9$ monomers respectively, all in the horizontal orientation.

_Remarks._ The bound is consistent with the necessary condition $m \le \max(r+1, c+1)$ of [ERWS11, Thm. 1]. It is not minimal in general. The rectangle $9 \times 13$ has odd area, so parity allows a single monomer, yet no $1$-monomer tatami tiling exists, since $T(9,13,1) = 0$ [ERWS11]. Our construction uses $9$ monomers and claims no optimality. ERWS11 assert without proof that the least monomer count for rectangular grids is computable in polynomial time with T-diagrams [ERWS11, Section 4.2]. Minimal monomer counts, fixed-count decidability, and explicit domino tilings for yes-instances all remain open (Section 7).

## 6. Computational validation

We implemented the procedure of Section 4 in plain Python, included as supplementary material in `validation/validate_tatami_dp.py`, and compared it against two published tables: [RW09, Table 2] for all $1 \le m, n \le 16$ and Hickerson's $t(r,s)$ table for $1 \le r, s \le 15$ [Hic02]:

- on the RW09 table, the existence pattern agrees on all 256 entries, including all no-instances such as $7 \times 10$ and $8 \times 11$;
- on the RW09 table, exact tiling counts agree on all 227 entries where the cited theorems determine counts, namely odd heights with the doubling factor, even heights $\ge 4$ with strict alternation, and height 1. We checked the 29 entries with $\min(m, n) = 2$ for positivity only, since we do not cite the $m = 2$ composition rule;
- both published tables are symmetric, with $T(m,n) = T(n,m)$, consistent with the rotation argument of Section 2;
- Hickerson's independent $t(r,s)$ table gives the same result. All 225 existence entries and all 198 determined counts agree, with positivity-only checks on the 27 entries with $\min(m,n) = 2$ [Hic02];
- on the fallback construction of Section 5, all 900 tilings for $1 \le r, c \le 30$ satisfy exact cover, tatami, the count bound, parity, and boundary placement, as do all 92 domino no-instances with $1 \le r, c \le 16$ and scaling spot checks up to $1000 \times 999$.

This validation checks consistency between our implementation, the cited theorems, and the published enumerations; it is evidence of correctness, not a substitute for the proof in Section 4. A second script, `validation/validate_monomer_fallback.py`, checks the Section 5 construction as described in the last bullet above.

## 7. Discussion

**Where the boundary lies.** General rectilinear DTC is NP-complete [ER13], and the authors of [ER13] state their belief that hardness persists without holes. Pak and Yang proved hardness for simply connected regions with _other_ fixed tile sets [PY13], which lends plausibility to that conjecture. Our result establishes the tractable base of this hierarchy. Full rectangles are in P. As an interpretation, not a theorem, what makes rectangles easy is the absence of inner corners. With no notches, the T-diagram structure of [ERWS11] collapses to a one-dimensional block concatenation, a regular language decided by a one- or two-phase automaton, whereas inner corners supply the feature sources around which complexity can accumulate: vortices, bidimers, vees, and loners. Formalizing that intuition, e.g. by showing bounded-height rectilinear strips remain tractable while general no-hole regions do not, is the natural next step.

**Finite automaton and 2-SAT viewpoints.** For each fixed $m$, the procedure is a finite automaton over the one-letter alphabet $\{1\}$, reading the width $n$ in unary. Each block-width jump expands into a chain of single-symbol steps. The total is $O(m)$ states. Odd $m$ needs one phase; even $m$ needs the two $S$/$L$ phases. The tileable widths therefore form a regular language. For odd $m$ the regular expression is $(1^{m-1} \mid 1^{m+1})*$. (The even case has one as well. With $s$ a width-$1$ block and $L$ a long block, the alternating sequences are $\epsilon \mid s(Ls)*(\epsilon \mid L) \mid L(sL)*(\epsilon \mid s)$, where $s$ expands to $1$ and each $L$ expands to one of the two long widths. The two-state automaton states this more clearly than the expression does.) This also explains the rational generating functions of [RW09]. A unary language is regular exactly when its counting sequence has a rational ordinary generating function. A 2-CNF encoding is not immediate. The successor-choice clause ($y_i \to y_{i+m-1} \lor z_{i+m-1}$) is ternary, so the automaton does not translate directly into 2-SAT. The dynamic program is simpler and faster.

**Limitations.** The proof depends on the cited decomposition theorems. Our verification of them, in the Section 3 notes, is a careful reading, not a machine-checked proof. The main theorem uses the unary region encoding; the binary-coordinate even case is open. The domino decision procedure certifies yes-instances without emitting an explicit tiling. Section 5 shows a free-monomer tiling always exists; minimal- and fixed-monomer-count questions remain open.

**Future work.** (1) Closed form for even-height tileability under binary encoding. (2) Bounded-height or bounded-notch rectilinear strips. (3) A scoped formalization of the decision procedure and its runtime bound, taking the decomposition theorems as axioms. (4) Minimal- and fixed-monomer-count tiling: characterization, decision, and construction; explicit domino tilings for yes-instances.

## 8. Conclusion

Rectangular domino tatami tileability is in P. The block structure of rectangular tatami tilings reduces the decision to a linear-time reachability problem. The result complements the known NP-completeness for general rectilinear regions and narrows the open question to where, between rectangles and arbitrary simply connected regions, hardness begins.

## Acknowledgments

[DRAFT NOTE: to be completed by the authors. Thank the authors of the cited works as appropriate. Add funding, disclosures, and a data/code-availability statement for the validation script and draft per venue policy. Do not submit with this placeholder.]

## References

- [ER13] A. Erickson and F. Ruskey. Domino tatami covering is NP-complete. In Proc. 24th Int. Workshop on Combinatorial Algorithms (IWOCA 2013), LNCS 8288, pp. 140–149, Springer, 2013.
- [RW09] F. Ruskey and J. Woodcock. Counting fixed-height tatami tilings. Electron. J. Combin. 16(1):R126, 2009.
- [ERWS11] A. Erickson, F. Ruskey, J. Woodcock, and M. Schurch. Monomer-dimer tatami tilings of rectangular regions. Electron. J. Combin. 18(1):P109, 2011.
- [CHZ11] R. Churchley, J. Huang, and X. Zhu. Complexity of cycle transverse matching problems. In Combinatorial Algorithms (IWOCA), LNCS 7056, pp. 135–143, Springer, 2011.
- [Hic02] D. Hickerson. Filling rectangular rooms with tatami mats. OEIS A068920, March 2002. <https://oeis.org/A068920/a068920.txt>
- [PY13] I. Pak and J. Yang. Tiling simply connected regions with rectangles. J. Combin. Theory Ser. A 120(7):1804–1816, 2013.
- [ERSW10] A. Erickson, F. Ruskey, M. Schurch, and J. Woodcock. Auspicious tatami mat arrangements. In Proc. 16th Ann. Int. Computing and Combinatorics Conf. (COCOON 2010), LNCS 6196, pp. 288–297, Springer, 2010.
