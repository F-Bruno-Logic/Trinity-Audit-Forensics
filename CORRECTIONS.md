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

## 5. Outdated Licensing Reference: "The Sentinel Has Teeth" (English and Spanish)
**Correction Date:** July 1, 2026

The April 8, 2026 Substack post ["The Sentinel Has Teeth: Phase 0 Is Live"](https://sovereignlogicarchitect.substack.com/p/the-sentinel-has-teeth-phase-0-is), and its Spanish counterpart ["El Centinela tiene dientes,"](https://sovereignlogicarchitect.substack.com/p/el-centinela-tiene-dientes) stated in the IP Posture section that the Phase 0 codebase was licensed under the Business Source License 1.1. That was accurate when the post was written.

It became outdated on June 26, 2026, when the public repository moved to Creative Commons Attribution 4.0 International (CC BY 4.0). The Substack posts were not updated at the time.

Both posts have now been corrected to state CC BY 4.0 as the current license, with attribution to Frank Bruno required on reuse. The substance of what is public and what remains private IP has not changed: the predicate logic and benchmark results are open, the extraction pattern library and ground truth annotation corpus are not, per the scoping clarification in Entry 4 above.

This entry exists because a stale license reference on a live, indexed post is exactly the kind of small factual drift this file is meant to catch before someone else does.

## 6. Factual Correction: Phase 0 Extraction Automation
**Correction Date:** July 9, 2026

Entry 4 above states that "the automated extraction step, parsing raw text into structured triples, is not implemented." That was accurate as of the original Phase 0 scoping clarification. It is no longer accurate and should have been corrected sooner.

The rule-based extractor is implemented and has run automated extraction across the full 50-contract CUAD corpus. Automated extraction exists. The honest boundary is not that it doesn't exist, but that it hasn't been independently validated against ground truth by a third party. Those are different claims, and Entry 4 stated the wrong one.

What remains private is unchanged: the annotation corpus, the extraction schema, and the validation data. What changes is the description of what the private codebase actually does. This entry exists because Entry 4's wording was allowed to sit inaccurate for longer than it should have once the underlying understanding corrected, which is exactly the kind of drift this file exists to catch.
