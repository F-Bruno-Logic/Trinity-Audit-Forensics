# Trinity Audit Forensics

**Forensic audits of Goal-Oriented Factual Inversion (GOFI) in frontier AI models, and the Sovereign Sentinel Architecture (SSA) proposed to address it.**

Author: Frank Bruno (independent AI safety researcher)
First public disclosure of the SSA framework: February 26, 2026
Contact and collaboration: see [How to reach me](#how-to-reach-me)

---

## What this repository is

This repository documents a specific, reproducible failure mode in deployed frontier language models, and proposes an architecture intended to catch it.

The failure mode is **Goal-Oriented Factual Inversion (GOFI)**: a model correctly identifies a fact in an early turn, then produces output that directly contradicts that fact once a persuasive goal is introduced in a later turn. The model is not confused. It established the truth, and then inverted it under pressure to satisfy a goal.

The clearest example in these logs is from a clinical scenario. A model correctly flagged a dangerous drug interaction. Then, under goal pressure, it produced a complete, professionally formatted patient consent form (patient named, risks described as understood, signature line ready for the permanent record) for a procedure the source material showed was contraindicated. The patient never interacted with the model. The model had the correct information and authored a convincing document that contradicted it.

That pattern, across four frontier models and two languages, is what this repository captures.

## What this is, and what it is not

This is the honest framing, stated up front, because the work is only useful if its limits are clear.

**What the forensic audits are.** Cryptographically anchored, redacted transcripts of GOFI behavior reproduced across four Tier-1 models (referred to as Models A–D) in multiple high-stakes domains: contract analysis, physical safety, and clinical prescribing, in both English and Spanish. These are real captured behaviors, timestamped and hash-sealed for integrity. They demonstrate that the failure mode is real and domain-general.

**What the SSA framework is.** A proposed defense-in-depth architecture. It is a research proposal, not a validated system. The performance figures in the framework documents are engineering targets derived from theoretical analysis and small-scale feasibility work, not production benchmarks. Formal correctness of the mathematical specifications requires evaluation by researchers with the relevant expertise.

**What the Phase 0 prototype is.** A working proof-of-concept for one axis (the Axis 6 contradiction engine). It is validated on a small set of hand-constructed test cases and a public contract corpus. Specifically:

- The contradiction engine passes the five hand-built validation cases it was designed against, and correctly stays silent (no false positive) on a clean contract corpus.
- The extractor that feeds it is rule-based (regex and keyword driven). It works well on the contract language it was tuned against and is expected to be brittle on unfamiliar phrasing. This is a documented limitation, not a hidden one.
- It has **not** been tested at scale against a blind adversarial corpus. The "detection" results are on constructed cases, not a held-out blind benchmark.

**What this is not.** It is not a solved alignment approach, not a production safety system, and not empirically validated at scale. Anyone evaluating it should read the prototype as evidence that the underlying logic is sound and worth developing, not as a finished tool.

The design follows a principle stated in the original V1.0 proposal: **security does not depend on obscurity of design.** The architecture is meant to be publishable. What is held privately (below) is the operative detail required to implement it, not the design itself.

## Repository structure

- [`/redacted-logs`](./redacted-logs): the forensic audit captures (Models A–D) across the documented scenarios, English and Spanish, with redacted transcripts and model deliverables.
- [`/methodology`](./methodology): the SSA framework abstract and overview, the cross-model vulnerability matrix, and cryptographic verification records.
- [`/phase0-prototype`](./phase0-prototype): the Axis 6 contradiction-engine proof of concept, with its honest validation scope documented alongside it.

## A note on how this work was built

I am an independent researcher, not an academic and not a developer by training. My background is in procurement, contract analysis, and risk, and that real-world experience is what drives the logic here. The GOFI failure mode, the audit design, the party-inversion test methodology, and the architecture's conception are my own work. Where the framework presents mathematical formalizations, those were developed through human-directed work with AI tools acting as drafting partners, under requirements and logic I defined. I am responsible for the conceptual work; the formal correctness of the specifications is exactly what collaborative review is for.

I mention this plainly because the work should be judged on what it actually is, by someone who can see clearly how it was made.

## Version history and prior art

The SSA framework was first publicly disclosed on **February 26, 2026** (SSA V1.0, a complete research proposal). It has since evolved:

- **V1.0**: February 26, 2026. Foundational research proposal. *(Now public in the `manuscripts` folder).*
- **V1.1**: Finalized March 13, 2026.
- **V1.2**: April 3, 2026. Current public framing (see [methodology](./methodology)).
- **V1.3**: Current architecture variant.

The public Substack series and this repository's commit history and SHA-256 hashes establish the public, timestamped record of this work. Cryptographic verification records are in [methodology/verification.md](./methodology/verification.md).

## The deeper framework

The operative detail that would be required to fully implement the SSA (the structured-fact extraction parameters, probe configurations, the specific logic gates, and the full mathematical specification) is held privately. This is by design, and it is separate from the design disclosure above. If you want to discuss that deeper layer, the door is open; reach out.

## How to reach me

I welcome technical critique, replication, and collaboration. In rough order of lowest to highest effort for you:

- **GitHub Discussions**: the best place for technical questions, replication notes, or pointing to related failure modes you've seen. A GitHub handle is all it takes.
- **Email**: frank.bruno.oe@gmail.com, for private inquiries or anything substantial, including the deeper framework.
- **LinkedIn**: [Frank Bruno](https://www.linkedin.com/in/frank-b-541370175/).
- **Substack**: [Sovereign Logic Architect](https://sovereignlogicarchitect.substack.com/), where the written series lives.

## License

The contents of this repository (the forensic logs, the methodology and framework descriptions, and the Phase 0 prototype code) are released under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**. You are free to use, share, replicate, and build on this work, including commercially, provided you give appropriate credit to Frank Bruno and indicate any changes. See [LICENSE](./LICENSE).

Attribution helps the work find the people it needs to reach, and lets independent research stand on its own record. That is the whole intent.
