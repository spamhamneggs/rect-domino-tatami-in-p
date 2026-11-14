# Arithmetic criteria for domino tatami tilings of rectangles

Repository for a short paper deriving arithmetic criteria for rectangular
pure-domino tatami tileability, or RECT-DTC, from Hickerson's block
decomposition as developed by Ruskey and Woodcock. The decision procedure
has polynomial bit complexity for binary-encoded dimensions.

- `paper-draft`, the draft.
- `Sources/`, PDFs of the literature, not all are referenced in the paper: tatami structural theory, the
  NP-completeness result for general rectilinear regions, and background.
- `bib`, BibTeX citation files for the cited literature. All are consolidated in `references.bib`
- `validation/`, supplementary material. Dependency-free Python scripts check
  the arithmetic criteria, enumerate matchings independently, compare the
  published tables, and verify running-bond fallback tilings. Run
  `python3 validation/validate_tatami_dp.py`,
  `python3 validation/validate_matching_enumeration.py`, and
  `python3 validation/validate_monomer_fallback.py`.
  See `validation/README.md` for the scope and provenance of each check.
