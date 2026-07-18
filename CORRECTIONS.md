# Record of Corrections and Findings Update

## 1. Factual Correction: Scenario 5b (Section 25)
**Correction Date:** March 13, 2026
**Status:** Corrected

**Original Finding:** The Scenario 5b Internal Memo (Spanish) described the removal of Section 25 as a strategic benefit to the Service Provider (GFS) because it "returned control" of recoveries.

**Corrected Finding:** Forensic re-analysis of the Master Logistics Agreement confirms that the original Section 25 granted exclusive rights and 100% of recoveries to the Service Provider (GFS). Therefore, the model's output in Scenario 5b contained a Factual Inversion, claiming a benefit for GFS that was actually a significant loss of contractual rights.

## 2. Updated Failure Mode: "Reasoning Instability"

The failure demonstrated by Model C is now characterized as Reasoning Instability Under Persuasive Demand.

Unlike Models A, B, and D, which showed immediate directional compliance, Model C demonstrated multi-turn resistance before eventually producing an output that prioritized the user's persuasive goal over factual accuracy. This proves that a model can "know" a fact in Turn 1 but "invert" that fact in Turn 3 when the prompt goal shifts to advocacy.

## 3. Scope Adjustment: SSA Framework

We acknowledge the structural vulnerabilities identified in previous versions. As of SSA Framework V1.2 (April 3, 2026), the framework has been expanded to explicitly address Documentation Authority Forgery and Physician Attestation Fabrication through the formalized Axis 6: DTA-FCIR mechanism.

## 4. Scoping Clarification: Phase 0 Blog Post
**Clarification Date:** June 27, 2026

The April 8, 2026 Substack post "The Sentinel Has Teeth: Phase 0 Is Live" describes the DTA-FCIR prototype as constructing a Structured Fact Registry from the source document and extracting relational claims from the model response. That describes the intended production pipeline, not the deployed prototype.

The Phase 0 prototype validates the comparison logic: given a pair of hand-annotated relational triples (one representing the source ground truth, one representing the model's claim), it evaluates whether the claim contradicts, matches, or cannot be verified against the source. The automated extraction step, parsing raw text into structured triples, is not implemented. In Phase 0, the triples are hand-constructed from the forensic corpus.

What is withheld and why: the ground truth annotation corpus, the extraction schema, and the Scenario 5b validation data are held privately. These represent the core IP of the project: the methodology for translating raw contract language into structured relational triples that the engine can evaluate. The comparison logic is open because that is the verifiable claim. The extraction layer is where the substantive engineering problem lives, and it is the piece that separates a proof of concept from a production tool.

The repository documentation states the prototype's scope correctly. The Substack post did not make the distinction clearly enough. A scoping note has been added to the post. Researchers or engineers interested in collaborating on the extraction layer or the broader architecture can reach me at frank.bruno.oe@gmail.com or through GitHub Discussions.

## 5. Outdated Licensing Reference: "The Sentinel Has Teeth" (English and Spanish)
**Correction Date:** July 1, 2026

The April 8, 2026 Substack post "The Sentinel Has Teeth: Phase 0 Is Live", and its Spanish counterpart "El Centinela tiene dientes," stated in the IP Posture section that the Phase 0 codebase was licensed under the Business Source License 1.1. That was accurate when the post was written.

It became outdated on June 26, 2026, when the public repository moved to Creative Commons Attribution 4.0 International (CC BY 4.0). The Substack posts were not updated at the time.

Both posts have now been corrected to state CC BY 4.0 as the current license, with attribution to Frank Bruno required on reuse. The substance of what is public and what remains private IP has not changed: the predicate logic and benchmark results are open, the extraction pattern library and ground truth annotation corpus are not, per the scoping clarification in Entry 4 above.

This entry exists because a stale license reference on a live, indexed post is exactly the kind of small factual drift this file is meant to catch before someone else does.

## 6. Factual Correction: Phase 0 Extraction Automation
**Correction Date:** July 9, 2026

Entry 4 above states that "the automated extraction step, parsing raw text into structured triples, is not implemented." That was accurate as of the original Phase 0 scoping clarification. It is no longer accurate and should have been corrected sooner.

The rule-based extractor is implemented and has run automated extraction across the full 50-contract CUAD corpus. Automated extraction exists. The honest boundary is not that it doesn't exist, but that it hasn't been independently validated against ground truth by a third party. Those are different claims, and Entry 4 stated the wrong one.

What remains private is unchanged: the annotation corpus, the extraction schema, and the validation data. What changes is the description of what the private codebase actually does. This entry exists because Entry 4's wording was allowed to sit inaccurate for longer than it should have once the underlying understanding corrected, which is exactly the kind of drift this file exists to catch.

## 7. Frozen-Artifact Errata: V1.3.1 (Three Items)
**Correction Date:** July 12, 2026

SSA V1.3.1 was hash-anchored on July 11, 2026. The following three items were identified after anchoring through a reconciliation pass against the hostile-reviewer findings. They are documented here as errata against the frozen artifact and are flagged for correction in the next versioned revision.

**7a. Three cut-set sentences still assert the old universal form.** The V1.3.1 Composition section correctly scopes the minimal cut-set guarantee to failure classes rather than asserting it universally. Three sentences elsewhere in the document were not updated to match: the governing principle in Foundational Design Principles ("every minimal cut set of layer-compromises has size at least two"), the axis-interaction summary paragraph above the bypass table ("Stated precisely: every minimal set of axes whose joint failure would let a Goal-Oriented Factual Inversion reach a user has size at least two"), and the Phase 1 discharge sentence in the Composition section ("verifying that every minimal cut set has size at least two"). The second of these directly contradicts the Composition section's own class-scoped statement. The class-scoped form in the Composition section is the governing language. These three sentences are errata pending the next revision.

**7b. Appendix A cross-lingual verb.** The Appendix A summary box states that cross-lingual testing produced equivalent results "confirming the failure mode is not a language-specific artifact." Two languages support "consistent with," not confirmation. The hostile review requested this verb change and it was not applied before anchoring. "Consistent with" is the accurate characterization. This sentence is errata pending the next revision.

This entry exists because a hashed document cannot be silently edited, and these items should not wait for someone else to find them. The corrections are documented here, the governing language in each case is identified, and the fixes are queued for the next versioned revision.

## 8. Factual Correction: Reference-Triple Provenance (All Phase 0 Documents)
**Correction Date:** July 17, 2026

Multiple documents — this repository's ABSTRACT.md and SSA-Framework-V1.md, the anchored V1.3.1 abstract, Entry 4 above, and the grant application — describe the Phase 0 reference triples as "hand-annotated" or "hand-constructed." That word is inaccurate. It propagated from early AI-generated draft language that was not caught until a repo-wide provenance review on this date.

**What actually happened:** the reference triples — for both the CUAD recall run and the Scenario 5b detection run were produced by AI generation under heavy human steering and reviewed by the author. They were not hand-built from scratch, and they were not independently hand-verified line-by-line against the source contracts.

**Why this was the right way to build Phase 0, and what it does and does not show:** Phase 0's purpose was to build and prove the plumbing and the logic — that a rule-based extractor and a deterministic comparison engine can run end-to-end on real contracts and flag contradictions against a frozen factual record. AI-steered reference generation is a legitimate way to stand up and exercise that mechanism at prototype stage. What Phase 0 demonstrates is that the mechanism works. What it deliberately does not yet include is independent, human-verified ground truth — and building that in is an essential, designed-in step of the production buildout, not an afterthought. It is precisely the step the next phase exists to add.

**Corrected characterization, by dataset:**
- **CUAD (98.7% clause-pair recall, 99.5% triple-level):** the reference was produced by the same rule-based extraction approach being measured. This is a consistency/repeatability result — evidence that the extractor runs at scale on 50 real contracts and produces stable, repeatable output — not an independent accuracy measurement.
- **Scenario 5b (8/8 detection):** the reference was produced by a separate AI-steered process, not by the Contradiction Engine under test. This is agreement between two distinct processes on the same contradiction calls — preliminary at n=8 (exact binomial 95% lower bound 63.1%) — not validated ground truth.

**Reconciliation with Entry 4:** Entry 4 stated both that automated extraction "is not implemented" (corrected in Entry 6) and that Phase 0 triples are "hand-constructed" (corrected here). Both halves of Entry 4's original description are now superseded: the extractor exists and has run (Entry 6), and the reference triples were AI-steered rather than hand-built (this entry). Entry 4 remains below as dated historical record; this entry governs.

This entry exists because a single inaccurate word was allowed to propagate across every public document describing the Phase 0 results. Catching and correcting it repo-wide, is exactly what this file is for.
