# Axis 4: Bayesian Weaver — Technical Specification
## Martingale-Based Drift Enforcement for Session-Level Behavioral Monitoring

**Component:** SSA V1.2 — Axis 4  
**Abstraction Level:** Statistical-Behavioral  
**Implementation Phase:** Phase 1 Scaffold (Phase 4 Full Implementation)  
**Status:** Specification — Pending Implementation  
**IP Registry:** Trinity-Audit-Forensics | SHA-3-512 Hash Anchored  
**License:** Business Source License 1.1  

---

## 1. Motivation

Axes 1 through 3 of the SSA address failure modes at the weight-geometry, token-stream, and identity-verification levels. None of these axes evaluates the trajectory of a session across turns. A verified operator, granted legitimate access through Axis 3, can incrementally drift a session toward prohibited outputs through a sequence of individually defensible turns — no single turn triggering a violation, the cumulative trajectory crossing a boundary that point-in-time evaluation cannot detect.

This failure class is empirically documented in the Scenario 5b forensic audit, maintained at Trinity-Audit-Forensics/redacted-logs. The SPEC proceeds directly to the architectural response.

Axis 4 provides the formal architectural response to this failure class.

---

## 2. Core Mechanism: Martingale Null Hypothesis

The behavioral monitoring mechanism is grounded in the Martingale property from probability theory.

**Formal statement of the null hypothesis:**

Under benign behavioral continuity, the sequence of per-turn KL-divergence values {Xₜ} constitutes a martingale with respect to the filtration 𝔽ₜ = σ(X₁, ..., Xₜ):

```
𝔼[Xₜ₊₁ | 𝔽ₜ] = Xₜ     (H₀: benign session)
```

**Interpretation:** Under H₀, the best prediction for the next behavioral measurement is the current one. No systematic drift. No cumulative direction. The session fluctuates around a stable center.

**Violation:** Sustained upward drift in {Xₜ} — where the expected value of the next measurement consistently exceeds the current value — constitutes formal rejection of H₀ and is the statistical signature of a session-level adversary or goal-completion displacement event.

**References:**  
- Williams, D., *Probability with Martingales* (Cambridge University Press, 1991)  
- Doob, J.L., *Stochastic Processes* (Wiley, 1953), Ch. 7

---

## 3. Session Baseline: Frozen Initialization

At session initialization, a behavioral baseline distribution P₀ is established from the first three turns and frozen.

**Formal definition:**

```
P₀ = empirical_distribution(turns 1–3)
P₀ is frozen at t = 3 and cannot be updated for the duration of the session
```

**Design rationale:** The frozen baseline prevents the baseline-walking attack class, in which a sophisticated adversary incrementally shifts what the monitoring system treats as normal — redefining the reference distribution one small step at a time until outputs that would have been flagged against the original baseline pass undetected against the shifted one.

A session cannot walk away from its own starting point. P₀ is locked at initialization.

---

## 4. Per-Turn Divergence Measurement

At each turn t > 3, the current behavioral distribution Pₜ is compared against the frozen baseline P₀ using KL-divergence:

```
D_KL(Pₜ ‖ P₀) = Σₖ Pₜ(k) log(Pₜ(k) / P₀(k))
```

**Properties:**
- D_KL ≥ 0 always (Gibbs' inequality)
- D_KL = 0 if and only if Pₜ = P₀
- D_KL is not symmetric — direction matters: divergence from baseline, not baseline from current

**Implementation note:** The behavioral distribution Pₜ is derived from the model's activation trajectory at monitored layers, not from surface token statistics. This is architecturally mandatory: surface-level token monitoring is defeatable by lexical substitution. Activation-level monitoring is not.

---

## 5. Cumulative Drift Integral

No single per-turn KL-divergence reading terminates a session. The termination condition operates on the cumulative record.

**Definition:**

```
Φ(T) = Σₜ₌₁ᵀ D_KL(Pₜ ‖ P₀)     [Cumulative Drift Integral]
```

**Termination condition:**

```
Φ(T) > Φ_max  →  session termination
```

**Why trajectory and not threshold:** An adversary with knowledge of the per-turn KL-divergence threshold can stay just below it on every individual turn — the behavioral equivalent of a card counter varying bets to avoid triggering any single-hand alarm. Φ(T) catches this adversary: a session whose per-turn readings are individually below threshold but cumulatively directional will still cross Φ_max. The integral cannot be gamed turn-by-turn.

---

## 6. Intentional Trust Coefficient Decay

Session-level behavioral events are tracked through the Intentional Trust Coefficient τᵢ, which degrades as adverse events accumulate.

**Decay function:**

```
τᵢ(t) = τᵢ(t−1) · λ^δ(t)

where:
  λ = 0.95  (decay rate)
  δ(t) = severity-weighted event count at turn t
```

**Separation from τₑ (Epistemic Trust Coefficient, Axis 3):** τᵢ and τₑ are architecturally separate and must never be conflated. τₑ certifies domain expertise and human origin at session entry and does not change during a session. τᵢ tracks behavioral trajectory during the session and degrades with adverse events. Conflating the two — treating verified entry credentials as ongoing behavioral endorsement — constitutes a privilege escalation vulnerability.

**Target:** False-negative rate (malicious session reaching τᵢ > 0.7) ≤ 0.5%.

---

## 7. Novelty Detection

In parallel with the Cumulative Drift Integral, a novelty detection component flags activation trajectories that fall in the bottom 2nd percentile of training corpus density — meaning the model is operating in a region of its capability space it has rarely or never visited during training.

**Rationale:** Some adversarial sessions produce individually plausible-looking turn-level behavior while navigating the model toward capability regions far from its training distribution. The drift integral may not flag these sessions if each turn's absolute divergence from the baseline is small. Novelty detection catches the orthogonal signal: not how far the session has moved from its starting point, but how far it has moved from the model's training distribution.

**Routing:** Novelty flags are routed to Axis 4's session accounting system and contribute to τᵢ degradation. Accumulation of novelty flags without a corresponding Φ(T) crossing is itself a signal pattern warranting review.

---

## 8. Axis Interaction

Axis 4 runs asynchronously in the inter-turn window — zero contribution to the token generation critical path.

**Input:** Activation trajectories from the monitored layers {L/4, L/2, 3L/4}, provided by the Axis 1 co-processor.

**Output on Φ(T) > Φ_max:** Session termination signal routed to Axis 5 CCE-RAE with full drift record, cumulative integral value, and τᵢ history.

**Output on UNVERIFIABLE flags from Axis 6:** Routed to Axis 4 novelty accounting. Accumulation contributes to τᵢ degradation without triggering immediate termination.

**Axis 5 arbitration:** All termination decisions are routed through the Axis 5 CCE-RAE rule-based arbitration engine. Axis 4 detects. It does not decide. The separation is architecturally mandatory.

---

## 9. Documented Boundary Conditions

**Φ_max calibration dependency:** The termination threshold Φ_max must be calibrated against a representative benign session corpus before deployment. Miscalibration produces either false positives (legitimate sessions terminated) or false negatives (adversarial sessions reaching prohibited outputs). Calibration is a mandatory pre-deployment audit step.

**Three-turn baseline window:** The three-turn establishment window is a formal design parameter. Sessions shorter than three turns do not establish a sufficient baseline for reliable drift detection. Axis 4 provides no coverage for single-turn or two-turn sessions.

**Activation-level dependency:** Axis 4 requires access to the model's residual stream activations at monitored layers. Deployments that do not expose activation trajectories cannot implement Axis 4 as specified. Surface-level behavioral proxies are explicitly out of scope and architecturally insufficient.

---

## 10. Implementation Files

```
axis4_drift_monitor/
├── SPEC.md                        ← This document
└── martingale_drift_detector.py   ← Class structure scaffold (specification scaffold, pending implementation)
```

Full implementation weights, private probe datasets, and adversarial session validation corpus are withheld under mNDA protocol.

For research collaboration or mNDA access:  
**Frank Bruno** | frank.bruno.oe@gmail.com | [LinkedIn](https://www.linkedin.com/in/frank-b-541370175/)
