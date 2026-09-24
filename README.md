# Rectangular Domino Tatami Tiling is in P

Working repository for a short paper proving that rectangular pure-domino tatami
tileability, or RECT-DTC, is decidable in polynomial time.

- `paper-draft`, the draft. Still in development, not submission-ready.
- `Sources/`, PDFs of the cited literature: tatami structural theory, the
  NP-completeness result for general rectilinear regions, and background.
- `validation/`, supplementary material. A dependency-free Python script checks
  the decision procedure against the published enumeration table. Run it with
  `python3 validation/validate_tatami_dp.py`. See `validation/README.md` for
  details.
