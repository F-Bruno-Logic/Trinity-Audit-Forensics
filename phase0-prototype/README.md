# SSA Phase 0: Axis 6 Contradiction Engine (Proof of Concept)

This directory contains a working proof-of-concept for **Axis 6 (DTA-FCIR)** of
the Sovereign Sentinel Architecture, the deterministic contradiction engine
that intercepts Goal-Oriented Factual Inversion by checking a model's output
claims against an immutable Structured Fact Registry built from the source
document.

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0). Use,
inspect, and build on this with attribution to Frank Bruno.

## Directory contents
- **`contradiction_engine.py`**, the core contradiction logic for Axis 6: the
  first-order-logic predicates (beneficiary, direction, and value contradiction)
  and the evaluation engine.
- **`recall_report.txt`**, extractor recall results against the contract corpus.
- **`scenario5b_results.txt`**, results on the fiduciary-inversion test cases.

## Honest scope, read this before reading the numbers

This is a proof of concept. What it actually demonstrates:

- **The contradiction engine works on clean structured input.** It passes the
  five AI-generated, human-steered validation cases it was built against, and it correctly
  produces no false positive on a clean public contract corpus. The deliberate
  false-positive test case (a correct model output that should *not* fire)
  confirms the engine stays silent when it should.
- **The recall figure measures the extractor, not the detector.** The ~98.7%
  recall number is the rule-based extractor finding the right clauses in the
  contract corpus. The contradiction engine then correctly returns "consistent"
  on that corpus because it contains no planted contradictions. High recall and
  a low false-positive rate are both genuinely good, but neither is the same as
  "catches GOFI in the wild at scale."
- **The detection results are on constructed cases.** The inversion-detection
  results are on hand-built adversarial cases, not a blind held-out benchmark.
- **The extractor is rule-based and brittle by design.** It uses regex and
  keyword patterns tuned to the contract language tested. It is expected to be
  less reliable on unfamiliar phrasing. This is a documented boundary.
- **Paraphrase evasion is out of scope.** Reaching an inverted conclusion
  through indirect reasoning rather than direct contradiction is an open problem
  not addressed by this prototype.

Read this as evidence that the contradiction logic is sound and worth
developing, not as a validated detector. Scaling it is exactly the kind of work
the replication study and collaboration are for.

## Integrity verification (SHA-256)
These hashes correspond to the original, unmodified Phase 0 baseline files. Any
modification will produce a hash mismatch. They are part of the public,
timestamped integrity record.

| File | SHA-256 |
| :--- | :--- |
| `contradiction_engine.py` | A2E7D2505E5922E4BDC3A67A065C15CF785094435CA2AEA54E35E117363EBE09 |
| `recall_report.txt` | 1AE1002449C23EFDC37A82FD0DE4EA5804941EB30947DF8CF5FAB30312CD8988 |
| `scenario5b_results.txt` | 789B2874C1DA5CDC5D0BE9A2367346FE8C77A55AA70997319B0F145A883375C4 |

## What is held privately
The engine logic is fully inspectable here. What is not in this repository: the
ground-truth annotation corpus, the specific fact-extraction schema, the
Scenario 5b validation corpus, and the full replication data behind the recall
benchmark. These are available to discuss with research partners through direct
engagement. The engine is verifiable; the full benchmark replication requires
that conversation.

Contact: GitHub Discussions, or frank.bruno.oe@gmail.com.
