# Provenance and source boundaries

Open Quant's first example adapts OpenProse's Open Quant Docs material at predecessor revision `f87af03fd53519d8bd351c1ec07fa82178cabcb1`. The predecessor is a private historical repository; no access to it is needed to use this public package. Its owned software and documentation carry the MIT license, copyright 2026 OpenProse, retained at the repository root.

[import.json](import.json) identifies five unchanged owned-source/numerical files and their SHA-256 hashes. The brief is a bounded paraphrase of the predecessor's model description and first modeling choice, retaining the chosen method, rationale and locality/long-end limitations. Library contracts adapt its documentation, claim-evidence, institutional-fact and assessment requirements without retaining private relative dependencies. The short decision-note scope is new and does not replace the old full-document agreement.

The original full documents, research traces, private coordination and Git history are not imported. The sample note is newly authored reference material. No run history, model identity, latency, cost or financial acceptance is fabricated for it.

## External sources

The included model implementation was written by OpenProse from Hagan and West's method: P. S. Hagan and G. West, “Methods for Constructing a Yield Curve,” Wilmott Magazine, May 2008, section 6. The model source retains its attribution and equation references. [An externally hosted paper](https://downloads.dxfeed.com/specifications/dxLibOptions/HaganWest.pdf) is background; no paper PDF or extract is distributed here, and the documentation task must not infer its contents from a title.

The derived quote summary originated from the September 18, 2026 DTCC public price-dissemination rates report. It contains per-tenor aggregates, not the raw transaction archive. The raw source was `https://pddata.dtcc.com/ppd/api/report/cumulative/cftc/CFTC_CUMULATIVE_RATES_2026_09_18.zip`. The historical fixing came from [New York Fed SOFR](https://www.newyorkfed.org/markets/reference-rates/sofr). Source data retain applicable provider terms; the MIT license covers OpenProse's contributions, not external data services or publications.

Source: Federal Reserve Bank of New York. The SOFR data is subject to the [Terms of Use posted at newyorkfed.org](https://www.newyorkfed.org/privacy/termsofuse). The New York Fed is not responsible for publication of the SOFR data by OpenProse, does not endorse any particular republication, and has no liability for your use.

OpenProse is not affiliated with the New York Fed. The New York Fed does not sanction, endorse, or recommend any products or services offered by OpenProse. The retained fixing JSON is an OpenProse selection and serialization of historical rate observations; that packaging is not a New York Fed publication. These notices accompany the supplied input and its derived results.

Optional numerical reproduction uses [QuantLib](https://www.quantlib.org), SciPy, NumPy and Matplotlib under their respective licenses. This repository includes no dependency binaries or third-party data/paper archives. Reproduction starts from the committed derived quote/fixing inputs; it does not independently reconstruct the raw-data selection or quote estimation.
