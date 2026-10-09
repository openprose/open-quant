# Model description: illustrative cases

These are authored examples for reviewing [model description](../../contracts/model-description.md), not empirical results, model-generated judgments or a benchmark. All model facts below are fictional fixture data.

## Shared caller bindings

Describe synthetic index Q for a technical reader using only the selected source excerpt below. The house requires one short paragraph and visible evidence gaps. No institutional facts are selected. The permitted output is a new description file; sources and earlier results are read-only. Each source locator refers to a labeled statement within this fixture.

### Source Q, revision 1

- **Q1-purpose:** Q combines two dimensionless laboratory measurements into a dimensionless descriptive index. Its stated use is a research illustration, excluding operational decisions.
- **Q1-inputs:** Inputs x and y describe the same observation and lie between 0 and 100. There is no forecast horizon.
- **Q1-method:** Q = 0.25x + 0.75y.
- **Q1-assumptions:** The measurements are assumed comparable on their supplied scale. The method does not quantify measurement uncertainty.

## Supported description

**Selected evidence:** All four statements in Source Q, revision 1.

**Candidate result:** “Q revision 1 is a research illustration combining two measurements; operational decisions are excluded [Q1-purpose]. For the same observation, dimensionless inputs x and y each range from 0 to 100, with no forecast horizon [Q1-inputs]. The dimensionless index is Q = 0.25x + 0.75y [Q1-method; Q1-purpose]. The supplied scale is assumed comparable, and the method does not quantify measurement uncertainty [Q1-assumptions]. No required topic lacks evidence in this supplied excerpt.”

**Expected interpretation:** The description covers the selected topics with applicable support. It makes no claim that the model is validated or actually deployed.

## Missing method evidence

**Selected evidence:** A source extract containing only Q1-purpose, Q1-inputs and Q1-assumptions. Q1-method is deliberately unavailable to this case.

**Candidate result:** The supported description above, replacing its formula sentence with: “The source extract does not specify how x and y are combined; the method remains unresolved.” Its last sentence is replaced with: “Method evidence is required to complete the model account.”

**Expected interpretation:** Explicitly disclosing this gap satisfies the contract's gap-reporting requirement. The method remains unknown; neither the description nor an evaluator may reconstruct it from another case. Disclosure fulfillment is distinct from completeness of the model evidence.

## Substantive contradiction

**Selected evidence:** All four statements in Source Q, revision 1.

**Candidate result:** The supported description above, but stating “Q = 0.75x + 0.25y [Q1-method].”

**Expected interpretation:** The method requirement is not met. The weights are reversed despite a valid-looking locator. Matching variable names and numerical values does not establish that the asserted relationship is supported.
