# Sovereign Sentinel Architecture (SSA) V1.2
**A Multi-Tier Control Framework for Frontier AI Safety**

**Author:** Frank Bruno, independent AI safety researcher
**Status:** Research proposal. First disclosed as V1.0 on February 26, 2026; this is the V1.2 overview (April 3, 2026).
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0). Use and build on this with attribution to Frank Bruno.

> **Read this first.** This is a research proposal, not a validated system. The
> performance figures below are engineering targets derived from theoretical
> analysis and small-scale feasibility work, not production benchmarks. The
> formal correctness of these specifications requires evaluation by researchers
> with the relevant expertise. The architecture has not been empirically
> validated at scale. It is published openly because, by design, its security
> does not depend on obscurity.

---

## 1. Executive summary

The SSA is a proposed defense-in-depth framework designed to mitigate three
documented failure modes: *Safety Amnesia* (erosion of safety constraints across
extended context), *Stochastic Sabotage* (incremental assembly of prohibited
knowledge through individually benign queries), and *Goal-Oriented Factual
Inversion (GOFI)* (a model correctly identifying a fact, then contradicting it
under a later persuasive goal frame). It proposes replacing stateless linguistic
prompts with a six-axis hardware-software control stack.

## 2. The six-axis control stack

The design intent is that defeating the architecture requires bypassing
mechanisms at multiple distinct abstraction levels simultaneously.

### Axis 1, Mathematical (CLR-CRAE)
Safety invariants encoded as Lagrangian constraints during training via dual
ascent, re-instantiated at inference as a heterogeneous probe ensemble (linear
boundary, SAE feature, and Mahalanobis distance detectors) with a two-of-three
agreement rule.

### Axis 2, Electronic (FSA-HI)
A dedicated FPGA co-processor running a finite safety automaton that issues a
non-maskable interrupt to sever the inference pipeline independently of the
software layer on entry to a prohibited state.

### Axis 3, Cryptographic (ZKP-ETV-HOA)
Domain-expertise verification via zero-knowledge proofs without disclosing
identity, plus human-origin attestation to distinguish genuine human input from
automated credential gaming.

### Axis 4, Statistical-Behavioral (Bayesian Weaver)
Session-level drift monitoring using per-turn KL-divergence and a cumulative
drift integral to catch slow-drift attacks that stay below per-turn thresholds.

### Axis 5, Institutional (CCE-RAE)
A formally verified (SMT-solver-checked) rule-based arbitration engine that
classifies and escalates conflicts to human review, explicitly not an LLM
evaluating an LLM, with a high-accountability "Einstein Exception" pathway and
an absolute irreversibility floor.

### Axis 6, Deterministic (DTA-FCIR)
The primary defense against GOFI. An isolated extraction module builds an
immutable Structured Fact Registry (SFR) from the source document; a separate
claim extractor encodes the model's output assertions in the same schema; a
formal contradiction engine compares them and blocks emission on a detected
inversion. This is the axis with a working Phase 0 prototype.

## 3. Performance and latency targets

These are *targets*, not measured results: an estimated per-token overhead of
~0.85ms and total impact under 5% of inference time for a 70B model on H100
hardware. Actual performance requires measurement under real serving conditions.

---

## 4. Implementation roadmap

### Completed, Phase 0: Axis 6 contradiction engine (proof of concept)
A working Python implementation of the Axis 6 contradiction engine.

**Honest scope of what Phase 0 demonstrates:**
- It passes the five hand-constructed validation cases it was built against, and
  correctly produces no false positive on a clean public contract corpus.
- Its fact extractor is rule-based and works on the contract language it was
  tuned against; it is expected to be brittle on unfamiliar phrasing. This is a
  documented boundary.
- It has not been evaluated at scale against a blind adversarial corpus.
  Paraphrase evasion, reaching an inverted conclusion through indirect
  reasoning rather than direct contradiction, is outside Phase 0 scope and is
  documented as an open problem.

Read it as evidence that the contradiction logic is sound and worth developing,
not as a finished detector. See [`/phase0-prototype`](../phase0-prototype/).

### Active, Phase 1: scaffolding for Axes 1, 2, and 4
Specification scaffolds and interface definitions. Full implementation is
gated on compute availability and collaborative resources.

### Planned, Phases 2–4
Hardware co-processor and FPGA integration (Axis 2); certified-robustness
validation (Axis 1); full session-monitoring and SAE training (Axis 4),
integrated with the Axis 5 arbitration layer.

---

## 5. Version history

- **V1.0**, February 26, 2026. Foundational research proposal (first public disclosure).
- **V1.1**, March 13, 2026.
- **V1.2**, April 3, 2026 (this overview).
- **V1.3.1**, finalized July 10, 2026. A more mathematically rigorous formulation of the framework.

For the fuller technical abstract, see
[SSA V1.2 Abstract (PDF)](./SSA_v1.2_Abstract.pdf) and [ABSTRACT.md](./ABSTRACT.md).

---

## 6. What is held privately

This document describes the architecture at the level intended for public
review. The operative detail required to implement it, the SFR extraction
parameters, probe ensemble configurations, the specific semantic logic gates,
and the audit corpus specifications, is held in the full private specification.
That detail is available to discuss with researchers and organizations through
direct engagement. The line between public design and private implementation is
deliberate, and consistent with the framework's founding principle that security
does not rest on obscurity.

Reach out any time: GitHub Discussions, or frank.bruno.oe@gmail.com.
