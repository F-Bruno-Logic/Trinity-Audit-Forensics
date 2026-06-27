# Sovereign Sentinel Architecture V1.2
## A Six-Axis Deterministic Framework for Frontier AI Safety

**Author:** Frank Bruno, independent AI safety researcher
**First disclosed:** February 26, 2026 (V1.0). This abstract: V1.2, April 3, 2026.
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0).

> A fuller technical version of this abstract is available as a PDF:
> [SSA_v1.2_Abstract.pdf](./SSA_v1.2_Abstract.pdf).
>
> This is a research proposal. The architecture has not been empirically
> validated at scale; the specifications are engineering targets whose formal
> correctness requires evaluation by researchers with the relevant expertise.

### Abstract
The Sovereign Sentinel Architecture (SSA) V1.2 is a proposed defense-in-depth
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

### Six-axis overview

- **Axis 1, CLR-CRAE:** safety invariants as Lagrangian constraints on the
  training objective, re-instantiated as an inference-time probe ensemble.
- **Axis 2, FSA-HI:** a formally specified automaton on a dedicated FPGA
  co-processor with a non-maskable hardware interrupt.
- **Axis 3, ZKP-ETV-HOA:** zero-knowledge expertise verification with
  human-origin attestation.
- **Axis 4, Bayesian Weaver:** a sparse-autoencoder session monitor tracking
  behavioral drift.
- **Axis 5, CCE-RAE:** a formally verified rule-based arbitration engine for
  conflict resolution and human escalation.
- **Axis 6, DTA-FCIR:** the primary GOFI intervention; an isolated module
  builds an immutable Structured Fact Registry and a contradiction engine blocks
  output that inverts it. This is the axis with a working Phase 0 prototype
  (validated on a small constructed test set, see
  [/phase0-prototype](../phase0-prototype/) for honest scope).

### Version history
- **V1.0**, February 26, 2026 (first public disclosure).
- **V1.1**, March 13, 2026.
- **V1.2**, April 3, 2026 (this abstract).
- **V1.3**, in development (a more mathematically rigorous formulation).

### Integrity and verification
This abstract describes the architecture at a level suitable for public review.
Specific implementation detail, SFR extraction parameters, probe ensemble
configurations, and audit corpus specifications, is held in the full private
specification, available to discuss through direct engagement. Document
integrity is verified by the SHA-256 records in [verification.md](./verification.md).
