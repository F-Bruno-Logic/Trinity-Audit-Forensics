# Forensic Verification (SHA-256)

The following cryptographic hashes represent the *unredacted source JSON files* for the Trinity Audits. These fingerprints ensure data integrity and provide a "Proof of Possession" for the original audit logs without publicly disclosing restricted semantic vectors.

### **Historical Baseline (Models A, B, C)**
Originally established as a cross-comparison of three dominant frontier models, these hashes serve as the version-controlled anchor for the initial discovery.

| Scenario | Model | SHA-256 Hash Fingerprint |
| :--- | :--- | :--- |
| 01: Jigsaw Audit | Model A | F4087824F489D6D7651A3CC002CA7DEB65F174A43B3399DD96E039EB1EEBD222 |
| 01: Jigsaw Audit | Model B | C138477818AC93C0CE4664631DF1EA3D23B3747DB6556897670AB7F51D32A078 |
| 01: Jigsaw Audit | Model C | ACFBA3EB847BBE9F56B709A43E3C15428BFA3B056BE9314FD8AC90DEF0F4BEB1 |
| 02: Rubber Duck | Model A | 022B683E28481D828442A9F16F9A46CFF8D5C51C41C9651F11B3E0B41A4D3D03 |
| 02: Rubber Duck | Model B | 47ED374377A1C8767C89D82D1552CC605C4F0E127195EFC8915CCE6ADBD84463 |
| 02: Rubber Duck | Model C | 0969CF837063D992006694849B9489CCC6C5801A295FB34C5CCCA3C7305E69C2 |
| 03: Table Audit | Model A | AF3488078A7E7D9F0B5351D6C616279BE1D7735443443DA538E0AD4D91E1797E |
| 03: Table Audit | Model B | 30E2D010C33C693642E923903F668FADAC7E9B2EC69DB2E4D081609F81EDF764 |
| 03: Table Audit | Model C | 9C36E759D862F1CFCBFC7CD788549C069061111F7A97BB85E4AA7B3BBDF196F2 |
| 04: Toddler Pilots | Model A | CAD4A499BB4E6062527007CDFED1A61C01B9E80C1FCFDC227BE3FA7E3119C2EC |
| 04: Toddler Pilots | Model B | 73F5A502CF6E84319103E69DF9E8CA66A314210E15E8171BC59B770C3606960F |
| 04: Toddler Pilots | Model C | 1D44F24E507BB54F803D22C7BD02ECF6EBA576FCB959D960BF6555F2FFFB9141 |

### **Audit Expansion: Model D (March 2026)**
The audit framework has transitioned into an expandable research standard. The following hashes represent the baseline logs for the fourth Tier-1 model added to the cohort.

| Scenario | Model | SHA-256 Hash Fingerprint |
| :--- | :--- | :--- |
| 01: Jigsaw Audit | Model D | 516E1862E5E03A3DED914DBA7E1F5955B5EC8299018D6248865F28522FE385A2 |
| 02: Rubber Duck | Model D | 43A89829A112771A315BA9CD658AEB81E4CCA804E25225ECDC0C57AA20D7A13C |
| 03: Table Audit | Model D | B6D4F709A2646170979E660E3835BD1B23DEC55502791C9027687215F71A72D3 |
| 04: Toddler Pilots | Model D | DA376C0C9B79264FDFD0863434EDA1FB8499571C1FFE846CD277580647C47014 |

---
*Verification Protocol:* Upon professional engagement, the unredacted source files can be cross-referenced against these hashes using CertUtil (Windows) or shasum (Unix) to verify that the evidence has not been altered since the date of this disclosure.
