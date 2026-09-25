# Rectangular Domino Tatami Tiling is in P

Working repository for a short paper proving that rectangular pure-domino tatami
tileability, or RECT-DTC, is decidable in polynomial time.

- `paper-draft`, the draft. Still in development, not submission-ready.
- `Sources/`, PDFs of the cited literature: tatami structural theory, the
  NP-completeness result for general rectilinear regions, and background.
- `validation/`, supplementary material. Dependency-free Python scripts check
  the decision procedure against the published enumeration tables and verify
  the monomer-dimer fallback tilings. Run them with
  `python3 validation/validate_tatami_dp.py` and
  `python3 validation/validate_monomer_fallback.py`. See
  `validation/README.md` for details.
