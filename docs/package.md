# Package candidate

Open Quant has a directory-package manifest, [prose-package.json](../prose-package.json), with explicitly selected files and exports. It includes the contracts, SOFR, monitoring and valuation examples, source notices and offline checks. The kernel is supplied separately by the caller's runtime; the package does not bundle a kernel or an executor.

The operating-work expansion changes the selected bytes and therefore requires a new candidate digest and package round trip before publication. The retained earlier preparation evidence applies to the preceding SOFR-only package selection, not these expanded bytes.

The proposed candidate identity is `openprose/open-quant@0.1.0-rc.1`. It is prepared for review, **not published**. Do not expect a registry fetch to succeed until a publisher has released this exact version and retained its receipt.

The manifest uses the Prose CLI's documented directory-package format. Its `default` export is the full-document contract; `sofr-decision` selects the smaller example, and `sofr-assessment` selects its assessment. Export names locate files; they do not create new language semantics or run those files automatically.

After authorized publication, fetch the package into a fresh directory using the publication receipt's actual digest:

```sh
prose cli package fetch openprose/open-quant@0.1.0-rc.1 --output-dir open-quant --sha256 RECEIPT_SHA256 --json
cd open-quant
python3 scripts/check_repository.py
```

`RECEIPT_SHA256` is a placeholder, not a published hash. Fetch verifies the package and receipt and refuses an existing destination. Follow [runtime setup](running.md) before invoking the example. Registry delivery and model execution are separate operations.

Maintainers publish with the documented `prose cli package publish` command only after release review and explicit publication authority. The earlier candidate's offline check used the CLI source's actual package preparation, receipt matching and materialization functions with a synthetic test receipt. It establishes byte-preserving local packaging, not a production registry round trip, authorization or availability.
