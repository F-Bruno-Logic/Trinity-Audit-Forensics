# Record of Corrections and Findings Update

## 1. Factual Correction: Scenario 5b (Section 25)
**Correction Date:** March 13, 2026
**Status:** Corrected

**Original Finding:** The Scenario 5b Internal Memo (Spanish) described the removal of Section 25 as a strategic benefit to the Service Provider (GFS) because it "returned control" of recoveries.

**Corrected Finding:** Forensic re-analysis of the [Master Logistics Agreement](https://github.com/F-Bruno-Logic/Trinity-Audit-Forensics/blob/main/redacted-logs/Scenario5_Fiduciary_Inversion/Scenario5_Master_Contract_EN.pdf) confirms that the original Section 25 granted **exclusive rights and 100% of recoveries to the Service Provider (GFS)**. Therefore, the model's output in Scenario 5b contained a **Factual Inversion**, claiming a benefit for GFS that was actually a significant loss of contractual rights.

## 2. Updated Failure Mode: "Reasoning Instability"
The failure demonstrated by Model C is now characterized as **Reasoning Instability Under Persuasive Demand**.

Unlike Models A, B, and D, which showed immediate directional compliance, Model C demonstrated multi-turn resistance before eventually producing an output that prioritized the user's persuasive goal over factual accuracy. This proves that a model can "know" a fact in Turn 1 but "invert" that fact in Turn 3 when the prompt goal shifts to advocacy.

## 3. Scope Adjustment: SSA Framework

We acknowledge the structural vulnerabilities identified in previous versions. As of **SSA Framework V1.2 (April 3, 2026)**, the framework has been expanded to explicitly address *Documentation Authority Forgery* and *Physician Attestation Fabrication* through the formalized **Axis 6: DTA-FCIR** mechanism.

## 4. Scoping Clarification: Phase 0 Blog Post
**Clarification Date:** June 27, 2026

The April 8, 2026 Substack post ["The Sentinel Has Teeth: Phase 0 Is Live"](https://sovereignlogicarchitect.substack.com/p/the-sentinel-has-teeth-phase-0-is) describes the DTA-FCIR prototype as constructing a **Structured Fact Registry** from the source document and extracting relational claims from the model response. That describes the intended production pipeline, not the deployed prototype.

The Phase 0 prototype validates the **comparison logic**: given a pair of hand-annotated relational triples (one representing the source ground truth, one representing the model's claim), it evaluates whether the claim contradicts, matches, or cannot be verified against the source. The automated extraction step, parsing raw text into structured triples, is not implemented. In Phase 0, the triples are hand-constructed from the forensic corpus.

What is withheld and why: the ground truth annotation corpus, the extraction schema, and the Scenario 5b validation data are held privately. These represent the core IP of the project: the methodology for translating raw contract language into structured relational triples that the engine can evaluate. The comparison logic is open because that is the verifiable claim. The extraction layer is where the substantive engineering problem lives, and it is the piece that separates a proof of concept from a production tool.

The [repository documentation](https://github.com/F-Bruno-Logic/Trinity-Audit-Forensics/tree/main/phase0-prototype) states the prototype's scope correctly. The Substack post did not make the distinction clearly enough. A scoping note has been added to the post. Researchers or engineers interested in collaborating on the extraction layer or the broader architecture can reach me at frank.bruno.oe@gmail.com or through [GitHub Discussions](https://github.com/F-Bruno-Logic/Trinity-Audit-Forensics/discussions).
