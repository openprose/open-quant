# Offline controls

The fixtures are authored examples with explicit field and unit bindings. Two supported numerical claims and five deliberately defective bindings cover absent evidence, a conflicting value, swapped methods, wrong units and stale source identity. Their labels were supplied by the author, not produced by a model. They are not a benchmark of executor or evaluator accuracy.

The checker compares the bindings to the retained JSON. It cannot infer a sentence's meaning, discover the correct field for an arbitrary claim, or verify the claimed source unit independently. A numerical match alone does not establish that a sentence is supported. Mutation tests demonstrate detection of changed imported bytes and changed evidence; reproduction controls reject material changes in values, dates, keys and list length.
