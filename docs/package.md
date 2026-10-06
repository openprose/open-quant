# Contract package and runnable examples

Open Quant has two delivery scopes. The [component package](../PACKAGE.md) contains reusable requirements for authors to compose with their own evidence. The complete source repository contains those contracts plus examples, inputs, provenance and development checks. The source-clone workshop flow remains available; fetching the component package does not provide an example program.

## Component package

[prose-package.json](../prose-package.json) selects all 22 contract definitions, the consumer entry document, license and manifest: 25 files. Definitions retain their existing paths and bytes, so local adoption links resolve without rewriting. The kernel and agent harness remain supplied by the caller's runtime. No package builder, copied source tree or private dependency is required.

The proposed identity remains `openprose/open-quant@0.1.0-rc.1`, prepared for review and **not published**. This candidate changes delivery scope before any release: example exports such as `sofr-decision`, `sofr-assessment` and `monitoring-review` are absent. The default export remains full documentation; named component exports still locate their definitions. `README` points to the included consumer entry document.

After authorized publication, fetch the component package into a fresh directory using the actual publication receipt:

```sh
prose cli package fetch openprose/open-quant@0.1.0-rc.1 --output-dir open-quant --sha256 RECEIPT_SHA256 --json
```

`RECEIPT_SHA256` is a placeholder. Fetch validates the package and receipt and refuses an occupied destination. Read `open-quant/PACKAGE.md` and reference the installed contracts from your own program. That program supplies its evidence, bindings, permitted effects and output location. There is no `examples/` or `scripts/` directory in this package.

Every change to selected bytes requires a new candidate digest and package check. Offline preparation and extraction do not establish registry availability, publication authority or model execution. Maintainers publish only after explicit release authorization and review of the actual candidate and receipt.

## Versioned demonstration checkout

The self-contained SOFR and operating examples remain available at source checkpoint `6772948763b736e87d4661fd4d1565ce8e841751`. To inspect that exact candidate without installing a provider:

```sh
git clone https://github.com/openprose/open-quant.git open-quant-examples
cd open-quant-examples
git checkout --detach 6772948763b736e87d4661fd4d1565ce8e841751
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -v
```

Follow that checkout's README and runtime guide for installation, authentication, execution and assessment. Its existing commands and relative contract references remain intact. It uses its own checked-out definitions; a component package fetched elsewhere does not silently upgrade the example. A future example revision must receive its own review and qualification.

The preceding 128-file all-in-one candidate is retained for this same source checkpoint, with digest `4c436b6188d750845d0388317dfa02eed04713397205448c2b50dc2008a40cd8`. It remains unpublished. This separate packaging proposal does not overwrite its bytes or change the original SOFR agreement. That bundle reaches the inspected file limit; separating reusable requirements from source examples provides room for library growth without increasing a CLI limit.

The component-only candidate and the complete source checkout require different checks. Package checks cover selected bytes, exports and local-reference closure. Source checks additionally cover imported model evidence, examples and fixture arithmetic. The earlier bounded CLI campaign does not qualify a fresh attendee install, this delivery change or every report example. See [runtime limits](running.md) and [the qualification record](qualification.md).
