# Sovereign Sentinel Architecture V1.3.1
## A Six-Axis Deterministic Framework for Frontier AI Safety

**Author:** Frank Bruno, independent AI safety researcher
**First disclosed:** February 26, 2026 (V1.0). This abstract: V1.3.1, July 10, 2026, a mathematical-rigor revision produced from an adversarial review of V1.3.
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0).

> A fuller technical version of this abstract is available as a PDF:
> [SSA_v1.3.1_Abstract.pdf](./SSA_v1.3.1_Abstract.pdf).
>
> This is a research proposal. The architecture has not been empirically
> validated at scale; the specifications are engineering targets whose formal
> correctness requires evaluation by researchers with the relevant expertise.

### Abstract
The Sovereign Sentinel Architecture (SSA) V1.3.1 is a proposed defense-in-depth
control framework for frontier language model deployments. It addresses three
documented failure modes:

1. **Safety Amnesia**, erosion of safety constraints across extended context.
2. **Stochastic Sabotage**, incremental assembly of prohibited knowledge
   through individually benign queries.
3. **Goal-Oriented Factual Inversion (GOFI)**, a model correctly identifying a
   fact in an early turn, then producing output contradicting it once a
   persuasive goal frame is introduced.

GOFI was identified through empirical forensic audit of four deployed frontier
models across party-inverted scenarios in English and Spanish. The
cryptographically anchored transcripts and model deliverables are publicly
archived in this repository for independent verification.

The architecture's central claim is confinement of probabilistic sensing, not
its replacement. Every axis still has a learned, statistical, or corpus-bounded
sensing component; what the architecture adds is a deterministic, auditable,
fail-closed actuator behind each sensor, with that sensor's coverage boundary
stated as a first-class limitation rather than left implicit.

### Six-axis overview

- **Axis 1, CLR-CRAE:** safety invariants as Lagrangian constraints on the
  training objective, re-instantiated as an inference-time probe ensemble.
  Robustness is specified two ways: an exact deterministic margin certificate
  where the probe geometry permits it, and an empirical adversarial-evaluation
  protocol elsewhere. One of the three probes is benign-referenced (trained
  only on benign activation statistics), giving the ensemble a mechanistically
  independent backup for gaps in the violation taxonomy.
- **Axis 2, FSA-HI:** a formally specified automaton on a dedicated FPGA
  co-processor with a non-maskable hardware interrupt, over a canonicalized
  event alphabet with a stated, non-certified boundary against novel
  encodings.
- **Axis 3, Cryptographic Expertise Attestation** (legacy label ZKP-ETV-HOA):
  deterministic verification of externally issued credentials via selective
  disclosure, rather than the withdrawn Zero-Knowledge Proof characterization
  used in earlier editions. A domain-expertise quiz is retained only as a
  secondary anti-sharing and liveness check.
- **Axis 4, Bayesian Weaver:** a sparse-autoencoder session monitor with a
  single sequential change-point statistic (CUSUM with an anytime-valid
  e-process false-alarm guarantee) over a restricted, corpus-informed
  baseline, plus a multi-scale allowance bank that narrows, without
  eliminating, the residual slow-drift evasion corridor.
- **Axis 5, CCE-RAE:** a formally verified rule-based arbitration engine for
  conflict resolution and human escalation, with disposition timing sized from
  a published reviewer-demand model rather than a fixed guarantee, fail-closed
  hold semantics, and two-person release for held contradictions.
- **Axis 6, DTA-FCIR:** the primary GOFI intervention; an isolated module
  builds an immutable Structured Fact Registry and a contradiction engine blocks
  output that inverts it, with an added hold for registry-referenced output
  lacking a verified affirmation. This is the axis with a working Phase 0
  prototype (the comparison logic; the automated extraction layer is specified
  but not yet built, see [/phase0-prototype](../phase0-prototype/) for honest
  scope).

**Tiered activation** (new in V1.3.1): disposition intensity activates by
severity tier (ORDINARY, WATCH, PROTECTED) rather than uniformly, on a
promote-only ratchet, so that ordinary traffic is not held at the same
intensity as declared high-stakes surfaces. Tiering only ever adds protection
above an always-on floor; it never subtracts from it.

### Version history
- **V1.0**, February 26, 2026 (first public disclosure).
- **V1.1**, March 13, 2026.
- **V1.2**, April 3, 2026.
- **V1.3.1**, July 10, 2026 (this abstract). Produced from an adversarial
  review of V1.3; narrows several global claims to their supported scope and
  adds tiered activation, a source-anchored fail-closed gate at Axis 6, a
  multi-scale drift bank at Axis 4, and fail-closed hold semantics with
  two-person release at Axis 5.

### Integrity and verification
This abstract describes the architecture at a level suitable for public review.
Specific implementation detail, SFR extraction parameters, probe ensemble
configurations, and audit corpus specifications, is held in the full private
specification, available to discuss through direct engagement. Document
integrity is verified by the SHA-256 records in [verification.md](./verification.md).
