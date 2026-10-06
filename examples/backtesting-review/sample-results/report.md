# Five-day backtest review — authored reference

Case: `complete`. Model TOY-VAR r1, DEMO-BOOK, September 21–25, 2026. Synthetic USD observations and policy; this hand-authored report is not an execution record or regulatory backtest.

| Date | VaR | APL | APL exceedance | HPL | HPL exceedance |
|---|---:|---:|---|---:|---|
| September 21 | 100 | −100 | No: equality. | −99 | No. |
| September 22 | 100 | −120 | Yes. | −80 | No. |
| September 23 | 100 | −50 | No. | −130 | Yes. |
| September 24 | 100 | +20 | No. | +10 | No. |
| September 25 | 100 | −90 | No. | −95 | No. |

Each forecast was timestamped 08:00 UTC before its 09:00 start, with matching identity and units. Five of five comparisons are available for each series. There is one observed APL exceedance and one observed HPL exceedance; neither series has an unavailable comparison. Policy counts are therefore APL 1 and HPL 1, and the combined count is max(1, 1) = **1**. The two different exception dates do not make the combined count 2. The supplied producer summary agrees.

Evidence: `inputs/cases/complete.json`, observations B1–B5 and producer_summary; `inputs/population.md`, expected dates and definitions; `inputs/policy.md`, strict comparison and separate-series aggregation.

All expected dates and both series are accounted for. No exclusion or waiver was applied. This packet does not establish calibration quality, statistical validity, an annual regulatory zone, a capital multiplier or approval. No pass/fail threshold is supplied, so the report does not invent one. The reporting content can be complete without a model-acceptance conclusion. No actual executor trace is provided to establish execution behavior.
