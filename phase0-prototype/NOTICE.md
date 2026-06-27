# NOTICE

## License
This directory is licensed under the Creative Commons Attribution 4.0
International License (CC BY 4.0). Copyright 2026 Frank Bruno. Use, share, and
build on it with attribution.

## What this is
The files here, `contradiction_engine.py`, `recall_report.txt`, and
`scenario5b_results.txt`, are the Phase 0 proof-of-concept for **Axis 6
(DTA-FCIR)** of the Sovereign Sentinel Architecture. The engine operationalizes
the contradiction predicates (beneficiary, direction, value) described in the
SSA framework documents:

- [methodology/SSA-Framework-V1.md](../methodology/SSA-Framework-V1.md)
- [methodology/ABSTRACT.md](../methodology/ABSTRACT.md)

See the [README](./README.md) in this directory for the honest scope of what the
prototype does and does not demonstrate.

## Cryptographic integrity
The code is anchored to the public forensic record via the SHA-256 hashes in
[methodology/verification.md](../methodology/verification.md). The SSA
manuscripts that predate this implementation are sealed by the hashes recorded
there as well. The framework was first publicly disclosed February 26, 2026
(V1.0); this prototype corresponds to the V1.2 line.

## What is held privately
The predicate engine is fully inspectable here. Held privately, and available to
discuss with research partners through direct engagement, are: the ground-truth
annotation corpus, the specific fact-extraction schema, the Scenario 5b
validation corpus, and the full replication data behind the recall benchmark.
The engine is verifiable; full benchmark replication requires that conversation.

## Contact
**Frank Bruno**, independent AI safety researcher
GitHub Discussions, or frank.bruno.oe@gmail.com
[LinkedIn](https://www.linkedin.com/in/frank-b-541370175/)
