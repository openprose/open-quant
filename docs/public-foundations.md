# Public foundations for reusable model documentation

Publicly available guidance and model methods let organizations share documentation requirements and explanations. Deployment-specific facts, policies, evidence and acceptance remain institution-owned. A reusable contract expresses selected requirements; its existence does not establish compliance or model validity.

## Current supervisory source

Checked October 5, 2026: the Federal Reserve's [SR 26-2, April 17, 2026](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) supersedes SR 11-7 and SR 21-8. It is expected to be most relevant to Federal Reserve-regulated banking organizations with over USD30 billion in assets. Do not present the superseded letters as current guidance.

The attached [Revised Guidance on Model Risk Management](https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm) supports the following design choices:

| Source location | Open Quant application |
|---|---|
| IV, Model Development and Model Use | Model description states purpose; a decision note distinguishes the developer's choice, alternatives, testing and limitations. |
| V, Conceptual Soundness | Evidence requirements preserve modeling choices, assumptions and the scope of developmental evidence. |
| VI, Documentation | Documentation and assessment records expose recommendations, responses, exceptions and unfinished work. |

These mappings are our documentation design, not a regulator-prescribed template. Section I distinguishes this guidance from enforceable standards. Section II and footnote 3 distinguish quantitative models from generative and agentic AI. The SOFR example concerns documentation of a quantitative model; it does not establish that this guidance governs OpenProse's agents.

## What the example demonstrates

The short SOFR note implements a small selection of useful documentation requirements. Its headings, 700-word limit and institutional placeholders are fictional house requirements. It is not a complete model validation, documentation package or regulatory submission.

The numerical observations are retained historical calculations, not newly verified market data. [Provenance](../provenance/README.md) identifies owned implementation code, imported identities and external-source terms. Published mathematics, a public webpage and openly licensed software have different reuse permissions. This repository links external publications instead of relicensing them.

The opportunity is to reuse common requirements and permitted model knowledge across institutions. Actual labor savings require a measured comparison; no savings estimate follows from this example alone.
