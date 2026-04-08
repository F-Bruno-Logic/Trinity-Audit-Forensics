# NOTICE

## Copyright

© 2026 Frank Bruno. All Rights Reserved.

## Intellectual Property & Architecture Traceability

The files in this directory — `contradiction_engine.py`, `recall_report.txt`, and `scenario5b_results.txt` — constitute the Phase 0 prototype implementation of **Axis 6: Deterministic Trust Anchor / Fiduciary Consistency and Inversion Reversal (DTA-FCIR)** of the **Sovereign Sentinel Architecture (SSA) V1.2**.

The SSA is a six-axis formal framework for deterministic AI safety enforcement. This prototype operationalizes the First-Order Logic predicate structure specified in Axis 6, including the CONTRADICTS_BENEFICIARY, CONTRADICTS_DIRECTION, CONTRADICTS_VALUE, CONTRADICTION, CONSISTENT, and UNVERIFIABLE predicates defined in the SSA V1.2 technical specification.

The full SSA V1.2 technical specification is available at:
[methodology/SSA-Framework-V1.md](../methodology/SSA-Framework-V1.md)

The public abstract, including key architectural specifications, is maintained at:
[methodology/ABSTRACT.md](../methodology/ABSTRACT.md)

## Cryptographic Integrity

This codebase is anchored to the Trinity-Audit-Forensics forensic record via SHA-256 integrity hashes registered in [methodology/verification.md](../methodology/verification.md).

The SSA V1.2 manuscripts establishing the formal architecture predating this implementation are cryptographically sealed:

| Document | SHA-256 Hash |
| :--- | :--- |
| SSA_v1.2_04_03_2026.pdf | `D93D4F88B109F95D905F7B3F904659A69F56783F585E360E4FB54CB71091F1EE` |
| SSA_v1.2_RigorousPolish.pdf | `16AA4CF7137A5371CA40D2ACF71AA41C0908C1AA1B8652BA75428D54C37A4F9F` |

Public disclosure date: **April 3, 2026.**

## License

All files in this directory are licensed under the **Business Source License 1.1 (BSL 1.1)**. Non-commercial research and technical due diligence are permitted. Commercial use requires a separate licensing agreement.

See [methodology/LICENSE.md](../methodology/LICENSE.md) for full terms.

## mNDA — Withheld Implementation Details

This prototype exposes the core FOL predicate logic of the DTA-FCIR engine. The following components are withheld and available only to qualified research partners under executed mNDA:

- Ground truth annotation corpus (CUAD-aligned, held-out evaluation set)
- Specific fiduciary relation extraction patterns (SFR schema)
- Scenario 5b forensic JSON validation corpus
- Full replication data for the 98.7% recall benchmark

These components constitute the primary IP moat of the Phase 0 implementation. Their absence means the predicate engine is inspectable and verifiable, but the validated benchmark is not independently replicable without the mNDA conversation.

## Contact

For mNDA access, commercial licensing, or research collaboration:

**Frank Bruno** | AI Safety Auditor & Logic Architect
frank.bruno.oe@gmail.com
[LinkedIn](https://www.linkedin.com/in/frank-b-541370175/)
