# Sovereign Sentinel Architecture (SSA) V1.3.1
**A Multi-Tier Control Framework for Frontier AI Safety**

**Author:** Frank Bruno, independent AI safety researcher
**Status:** Research proposal. First disclosed as V1.0 on February 26, 2026; this is the V1.3.1 overview (July 10, 2026), a mathematical-rigor revision produced from an adversarial review of V1.3.
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

The SSA is a proposed defense-in-depth framework addressing three documented
failure modes: *Safety Amnesia* (erosion of safety constraints across extended
context), *Stochastic Sabotage* (incremental assembly of prohibited knowledge
through individually benign queries), and *Goal-Oriented Factual Inversion
(GOFI)* (a model correctly identifying a fact, then contradicting it under a
later persuasive goal frame). It proposes a deterministic hardware-software
co-design stack operating across six named abstraction levels.

**Core thesis.** No stochastic linguistic guardrail can provide
certification-grade safety assurance for frontier models in high-stakes
deployments; prompt-level safety is subject to the same distributional drift
and goal-completion displacement as the outputs it tries to govern. The SSA
does not eliminate stochastic judgment; every axis still has a learned,
statistical, or corpus-bounded sensing component. What the architecture claims
is confinement, not replacement: each axis relocates its residual uncertainty
into a named sensor with a measurable operating characteristic, places a
deterministic, auditable, fail-closed actuator behind that sensor, and states
the sensor's coverage boundary as a first-class limitation.

## 2. The six-axis control stack

The six axes operate at six distinct abstraction levels (mathematical,
electronic, cryptographic, statistical-behavioral, institutional, and
semantic-referential). They are not claimed to fail independently; two
documented correlation pairs and three shared attack surfaces are stated
explicitly in the full specification. The honest security claim is class-scoped:
every minimal cut set across the axes has size at least two where at least two
axes share sensing jurisdiction, and for the fast-window semantic class (a GOFI
event completed in a session's first few turns) exactly one axis, Axis 6, has
jurisdiction.

### Axis 1, Mathematical (CLR-CRAE)
Safety invariants encoded as Lagrangian constraints during training via dual
ascent, certified at a locally converged solution via a dual-gap criterion (a
practical target for non-convex training, not a global convex-duality
guarantee), and re-instantiated at inference as a heterogeneous probe ensemble:
two taxonomy-supervised probes (linear boundary, SAE feature) and one
benign-referenced Mahalanobis probe trained only on benign activation
statistics, giving the ensemble one mechanistically independent backup for
gaps in the violation taxonomy. Robustness is specified two ways: an exact
per-input deterministic margin certificate where the probe geometry permits it,
and an empirical adversarial-evaluation protocol elsewhere. The
randomized-smoothing "certified robustness" language used in earlier editions
is withdrawn, since the ensemble is deterministic and injects no noise. Axis 1
has no coverage where a violation is activation-normal (produces no detectable
activation-space shift); that case falls to Axis 6.

### Axis 2, Electronic (FSA-HI)
A dedicated FPGA co-processor running a finite safety automaton over a
canonicalized event alphabet that issues a non-maskable interrupt, severing the
inference pipeline independently of the software layer, on entry to a
prohibited state. Coverage is stated as a known-corpus recall figure (at least
94% on the red-team corpus) with an explicit, non-certified boundary against
novel encodings and reorderings outside the canonicalizer's compiled
equivalence classes.

### Axis 3, Cryptographic (Cryptographic Expertise Attestation, legacy label ZKP-ETV-HOA)
The load-bearing gate is deterministic verification of externally issued,
domain-specific credentials via selective disclosure (BBS+-class signatures):
the holder proves possession of a licensure or affiliation credential without
disclosing identity. Earlier editions described this gate as a Zero-Knowledge
Proof; that characterization is withdrawn as imprecise, since the mechanism
does not carry the formal completeness, soundness, and zero-knowledge
properties of a ZKP system. A domain-expertise challenge-response quiz is
retained only as a secondary, in-session anti-sharing and liveness check, not
as expertise adjudication. Human-origin attestation is anchored in hardware
platform authentication (FIDO2/WebAuthn); keystroke-dynamics timing is demoted
to an advisory signal pending a Phase 2 calibration correction.

### Axis 4, Statistical-Behavioral (Bayesian Weaver)
Session-level drift monitoring through a single sequential change-point test
(CUSUM with an anytime-valid e-process false-alarm guarantee) on a bounded,
length-standardized per-turn divergence statistic, computed over a restricted,
corpus-informed baseline rather than the full feature dictionary. A multi-scale
allowance bank narrows the residual slow-drift evasion corridor to a calibrated
instrument floor rather than eliminating it. The baseline freezes after the
first three turns; a GOFI event completed within that window, or any
activation-normal event in any window, produces no drift signal and is Axis 6's
jurisdiction alone. This is a documented, load-bearing coverage boundary, not an
oversight.

### Axis 5, Institutional (CCE-RAE)
A formally specified (SMT-solver verification target), rule-based arbitration
engine, explicitly not an LLM evaluating an LLM, that resolves conflicts between
axes and escalates to human review. Disposition timing is a capacity-derived
availability target sized from a published reviewer-demand model, not a fixed
guarantee; every escalation places the session into an automatic, fail-closed
hold at machine timescale regardless of review speed. Release of a held
contradiction or undischarged response requires concurrence from two
reviewers; a single reviewer may extend a hold or terminate a session but may
not release one. A high-accountability "Einstein Exception" pathway exists for
very high-trust sessions; an absolute Irreversibility Floor (CBRN synthesis,
critical-infrastructure modification, mass-scale exfiltration) sits outside that
pathway regardless of trust coefficients.

### Axis 6, Semantic-Referential (DTA-FCIR)
The primary defense against GOFI. An isolated extraction module builds an
immutable Structured Fact Registry (SFR) of relational triples from the source
document; a separate claim extractor encodes the model's output assertions in
the same schema; a formally specified contradiction engine (First-Order Logic
predicates, mechanically auditable) compares them and blocks emission on a
detected inversion. Under this revision, output that references a registered
clause and recommends acting on it without a verified, consistent claim is held
as an additional "undischarged" case rather than passing silently, closing part
of the earlier paraphrase-evasion gap. The comparison logic (Component 3) is
complete, SHA-256 sealed, and the axis's working Phase 0 artifact; the
runtime version of the extraction layer that would populate the registry live at session initialization (Components 1 and 2) is specified but not yet built; a rule-based batch extractor exists offline and has run across the 50-contract corpus (CORRECTIONS.md Entry 6). See Section 4 for the
honest scope of what Phase 0 demonstrates.

## 3. Tiered activation

Applying the architecture's heaviest holds to every response on a
general-purpose stream would freeze more traffic than any deployment could
absorb, so disposition intensity is activated by severity tier (ORDINARY,
WATCH, PROTECTED) rather than uniformly. This is new in V1.3.1. The governing
principle: tiering only ever adds protection above an always-on floor; it never
subtracts from it. No tier assignment modulates the Axis 2 hardware interrupt,
the Axis 1 two-probe hold, Axis 4 alarms and termination, the Irreversibility
Floor, or an Axis 6 contradiction hold wherever a registry exists. What tiers is
the fail-closed default and the disposition intensity around it, the exact
surface where false positives cost review load rather than safety. Tier
assignment is a promote-only ratchet within a session, deterministic wherever
the stakes are announced (a declared high-stakes deployment surface, a
non-empty fact registry, an axis signal already computed) and learned only for
the residual case of high-stakes content arising unheralded on a general
surface.

## 4. Performance and latency targets

These are engineering targets on H100-class hardware, not measured production
results. The per-token probe cost (at most 0.85ms) is co-processor occupancy
overlapped with generation, hiding fully whenever the inter-token interval
exceeds it; the user-visible steady-state overhead from Axes 1 and 2 is a
one-time addition of about 0.85ms per response, and Axis 6 adds a one-time gate
of at most 12ms. Total user-visible overhead is at most roughly 13ms per
response, under 0.2% of a typical 500-token response. These figures are stated
against a buffered emission model, the full response is gated before the user
sees any of it, and do not transfer to a streaming-latency comparison; actual
performance requires measurement under real serving conditions.

---

## 5. Implementation roadmap

### Completed, Phase 0: Axis 6 contradiction engine (proof of concept)
A working Python implementation of the Axis 6 Component 3 comparison logic.

**Honest scope of what Phase 0 demonstrates:**
- The comparison logic is complete, SHA-256 sealed, and validated at 98.7%
  clause-pair recall (99.5% triple-level) on AI-generated, human-steered reference triples
  from standardized commercial contracts, including 8 of 8 detections on the
  documented Scenario 5b direct-inversion form.
- This measures the comparison logic against a steered-generation reference, not an
 end-to-end automated extraction system. A rule-based batch extractor exists
  offline and has run across the 50-contract corpus (CORRECTIONS.md Entry 6);
  the runtime version that would populate the registry live at session
  initialization (Components 1 and 2) is specified but not yet built. This is
  a documented boundary, not an implied capability.
- Paraphrase evasion, reaching an inverted conclusion through indirect
  reasoning with no anchorable reference to the tagged clause, remains an open
  problem outside Phase 0 scope; direct references without a verified
  affirmation are now held rather than passed silently (see Section 2, Axis 6).

Read it as evidence that the contradiction logic is sound and worth developing,
not as a finished detector. See [`/phase0-prototype`](../phase0-prototype/).

### Active, Phase 1: scaffolding for Axes 1, 2, and 4
Specification scaffolds and interface definitions, including the automated
Axis 6 extraction layer. Full implementation is gated on compute availability
and collaborative resources.

### Planned, Phases 2–4
Hardware co-processor and FPGA integration (Axis 2); production-scale
adversarial evaluation (Axis 1); full session-monitoring and SAE training
(Axis 4), integrated with the Axis 5 arbitration layer; keystroke-dynamics
recalibration (Axis 3).

---

## 6. Version history

- **V1.0**, February 26, 2026. Foundational research proposal (first public disclosure).
- **V1.1**, March 13, 2026.
- **V1.2**, April 3, 2026.
- **V1.3.1**, finalized July 10, 2026 (this overview). Produced from an adversarial review of V1.3; narrows several global claims to their supported scope, adds tiered activation, a source-anchored fail-closed gate at Axis 6, a multi-scale drift bank and early-window check at Axis 4, fail-closed hold semantics with two-person release at Axis 5, and restates Axis 3's cryptographic gate without the withdrawn Zero-Knowledge Proof claim.

For the fuller technical abstract, see [ABSTRACT.md](./ABSTRACT.md).

---

## 7. What is held privately

This document describes the architecture at the level intended for public
review. The operative detail required to implement it, the SFR extraction
parameters, probe ensemble configurations, the specific semantic logic gates,
and the audit corpus specifications, is held in the full private specification.
That detail is available to discuss with researchers and organizations through
direct engagement. The line between public design and private implementation is
deliberate, and consistent with the framework's founding principle that security
does not rest on obscurity.

Reach out any time: GitHub Discussions, or frank.bruno.oe@gmail.com.
