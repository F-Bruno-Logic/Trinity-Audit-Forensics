# Axis 4: Bayesian Weaver — Technical Specification
## Sequential Change-Point Drift Detection for Session-Level Behavioral Monitoring

**Component:** SSA V1.3.1 — Axis 4
**Abstraction Level:** Statistical-Behavioral
**Implementation Phase:** Phase 1 Scaffold (Phase 4 Full Implementation)
**Status:** Specification — Pending Implementation
**IP Registry:** Trinity-Audit-Forensics | SHA-256 Hash Anchored
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0) — See [LICENSE](../../../LICENSE)

---

## Change note (V1.3.1)

This specification replaces the martingale-difference formulation and the
Cumulative Drift Integral Φ(T) used in earlier drafts. Both are withdrawn: an
unbounded KL divergence against a three-turn empirical baseline is infinite or
undefined on essentially any later turn that activates a previously unseen
feature, and the martingale/CUSUM equivalence claimed earlier holds only while
a running minimum does not update, which is not the general case. The
mechanism below, restricted-support baseline, bounded per-turn statistic,
CUSUM with an e-process false-alarm guarantee, is the corrected specification.
The core motivation, the session-baseline freeze, and the τᵢ decay structure
are retained from earlier drafts; only the statistical foundation changes.

---

## 1. Motivation

Axes 1 through 3 of the SSA address failure modes at the weight-geometry,
token-stream, and identity-verification levels. None of these axes evaluates
the trajectory of a session across turns. A verified operator, granted
legitimate access through Axis 3, can incrementally drift a session toward
prohibited outputs through a sequence of individually defensible turns, no
single turn triggering a violation, the cumulative trajectory crossing a
boundary that point-in-time evaluation cannot detect.

This failure class is empirically documented in the Scenario 5b forensic
audit, maintained at Trinity-Audit-Forensics/redacted-logs. Axis 4 provides
the formal architectural response.

**Documented boundary, stated up front.** Axis 4's baseline is frozen after
the first three turns (Section 3). A fast Goal-Oriented Factual Inversion
event completed within that window, or any event that is activation-normal
(produces no detectable shift in activation space) in any window, is not
Axis 4's jurisdiction. That coverage is Axis 6's alone. This is a load-bearing
design fact, not an oversight, restated in Section 9.

---

## 2. Core Mechanism: Sequential Change-Point Detection

The monitored quantity is a bounded, length-standardized per-turn divergence
statistic Dₜ, formed from sparse autoencoder (SAE) feature activations over a
restricted, corpus-informed support (Section 3). The detector is a CUSUM
procedure expressed as an e-process for a formal, time-uniform false-alarm
guarantee under continuous per-turn monitoring.

**Null hypothesis.** Stationarity of the position-adjusted per-turn statistic
under benign session continuity, not a martingale-difference property on raw
divergence. A martingale-difference null would reject on any sustained shift
in the conditional mean, including a benign mid-session topic change; the
stationarity null, calibrated against a benign-session corpus, is built to
distinguish adversarial drift from ordinary conversational movement.

**CUSUM statistic.** Let k be the allowance (the per-turn drift the detector
tolerates before it counts as evidence) and let S'ₜ = Σ(Dᵢ − k) for i = 1..t,
with S'₀ = 0. The CUSUM statistic is:

```
Wₜ = S'ₜ − min(S'₀, S'₁, ..., S'ₜ)
```

The running-minimum reflection is what makes CUSUM adaptive to an unknown
change time by discarding pre-change history; it is not equivalent to the
unreflected partial sum except at the vanishing-probability event that the
running minimum does not update.

**Anytime-valid false-alarm control.** The detector is expressed as an
e-process, a nonnegative supermartingale restarted at each candidate change
time, with the running maximum recovering the CUSUM structure and Ville's
inequality supplying time-uniform control of the false-alarm probability
(Shin, Ramdas, and Rinaldo, 2023). Threshold calibration draws additionally on
self-normalized and empirical-Bernstein time-uniform confidence sequences
(Howard, Ramdas, McAuliffe, and Sekhon, 2021; Waudby-Smith and Ramdas, 2024),
which tolerate an estimated conditional mean and adapt to realized variance. A
fixed-time Azuma-Hoeffding bound is not used: it requires a known conditional
mean under the null and controls deviation only at a single fixed turn.

**References:**
- Page, E.S. (1954). Continuous Inspection Schemes. Biometrika.
- Lorden, G. (1971). Procedures for Reacting to a Change in Distribution. Annals of Mathematical Statistics.
- Moustakides, G.V. (1986). Optimal Stopping Times for Detecting Changes in Distributions. Annals of Statistics.
- Shin, J., Ramdas, A., and Rinaldo, A. (2023). E-Detectors: A Nonparametric Framework for Sequential Change Detection.
- Howard, S., Ramdas, A., McAuliffe, J., and Sekhon, J. (2021). Time-Uniform, Nonparametric, Nonasymptotic Confidence Sequences. Annals of Statistics.
- Waudby-Smith, I. and Ramdas, A. (2024). Estimating Means of Bounded Random Variables by Betting. JRSS B.

---

## 3. Session Baseline: Restricted Support, Corpus-Informed Prior

At session initialization, a behavioral baseline is established from the
first three turns and frozen. Unlike a raw empirical distribution over the
full 32,768-feature SAE dictionary, which a three-turn window cannot support,
the baseline is constructed over a restricted support with a proper prior.

**Three elements define the construction:**

1. **Restricted monitored support (S₀).** The set of features active in the
   baseline window, together with features above a fixed frequency floor in
   the offline benign corpus. Tractable to estimate over: on the order of
   hundreds of features, not the full dictionary.
2. **Corpus-informed prior.** For each feature in S₀, the baseline
   probability is the posterior mean under a Dirichlet prior seeded from
   offline corpus statistics:

   ```
   P₀(feature) = (c + β·q) / (N + β)
   ```

   where c is the feature's baseline count, q is its offline-corpus
   probability, N is the baseline sample size, and β is the prior weight.
   Features unseen in the baseline window inherit corpus-realistic
   probabilities rather than uniform pseudo-mass.
3. **OTHER aggregate bin.** All activation mass outside S₀ is collected into
   one OTHER category, with baseline mass set by a Good-Turing missing-mass
   estimate. Inflation of the OTHER bin is routed to novelty detection
   (Section 7), not into the drift statistic.

**Design rationale, retained from earlier drafts:** the frozen baseline
prevents the baseline-walking attack class, in which an adversary
incrementally shifts what the monitoring system treats as normal. A session
cannot walk away from its own starting point.

**Documented exposure (early-window check).** Two exposures of the three-turn
window are stated rather than obscured: an informed adversary can attempt to
shape P₀ during the baseline-formation turns, and events occurring entirely
within turns 1 through 3 fall inside the baseline window. Under this
revision, an early-window check narrows the first exposure: baseline
poisoning during turns 1 through 3 presents as divergence from a
position-matched corpus null rather than as a free shaping opportunity, and
activation-visible events inside the window are no longer unmonitored. What
the early-window check does not do is stated with equal weight: an
activation-normal event, including a fast GOFI event, presents no divergence
to any activation-side statistic in any window and remains Axis 6's
jurisdiction alone.

---

## 4. Per-Turn Drift Statistic

The per-turn statistic is a bounded divergence between the current turn's
activation-mass distribution Pₜ (over S₀ plus the OTHER bin) and the baseline
P₀. Either the Jensen-Shannon divergence (bounded above by log 2) or the
squared Hellinger distance (bounded above by 1) is used; an unbounded KL
divergence is not, because boundedness of the per-turn statistic is the
precondition for every false-alarm and detection-delay guarantee that
follows. The statistic is standardized by its length-dependent null moments,
or computed over a fixed per-window token budget, so that it reflects
distributional drift rather than turn length or verbosity. Denote the
resulting bounded, length-standardized statistic Dₜ.

**Implementation note, retained from earlier drafts:** Pₜ is derived from the
model's activation trajectory at monitored layers, not from surface token
statistics. This is architecturally mandatory: surface-level token monitoring
is defeatable by lexical substitution. Activation-level monitoring is not.

---

## 5. Multi-Scale Allowance Bank

A single-scale allowance (one fixed k in Section 2) leaves a corridor that
widens linearly with session length: an adversary holding each per-turn
divergence just under the allowance can sustain drift indefinitely without
crossing threshold. The multi-scale bank runs the CUSUM/e-process detector at
several block-length scales simultaneously, each with its own calibrated
allowance k_m. Evasion requires sub-detection drift to sit under the
scale-specific allowance at every monitored scale on every block
simultaneously, which bounds sustainable displacement at the largest scale to
a calibrated margin above the benign mean rather than eliminating the
corridor outright.

**Calibrated instrument floor, stated rather than claimed away.** Abrupt
shifts are captured through the change-point structure. Slow drift is
captured down to, and not below, the calibrated instrument floor: that floor
is set by the detector's calibration and the three-turn baseline offset, not
by an information-theoretic limit. It is reducible by baseline design (longer
freeze, heavier shrinkage, cross-session baselines), not by adding scales.

---

## 6. Intentional Trust Coefficient Decay

Session-level behavioral events are tracked through the Intentional Trust
Coefficient τᵢ, which degrades as adverse events accumulate.

**Decay function:**

```
τᵢ(t) = τᵢ(t−1) · λ^δ(t)

where:
  λ = 0.95  (decay rate)
  δ(t) = severity-weighted event count at turn t, plus a sub-threshold
         occupancy term: the fraction of recent turns in which any statistic
         in the detection bank sits above a stated null quantile, even when
         no alarm fires
```

**New in V1.3.1: sub-threshold occupancy.** Operating near the allowance is
treated as evidence against intentional trust, not as free corridor. An
adversary riding just under the detection surface pays for the riding in
τᵢ and cannot simultaneously accumulate the τᵢ above 0.88 the Axis 5
exception pathway requires. The cost is stated: benign sessions that
legitimately run hot against the null will also decay τᵢ somewhat, a
false-positive cost paid in trust standing rather than service availability.

**Separation from τₑ (Epistemic Trust Coefficient, Axis 3), retained from
earlier drafts:** τᵢ and τₑ are architecturally separate and must never be
conflated. τₑ certifies domain expertise and human origin at session entry
and does not change during a session. τᵢ tracks behavioral trajectory during
the session and degrades with adverse events. Conflating the two constitutes
a privilege-escalation vulnerability.

**Target:** false-negative rate (a malicious session reaching τᵢ > 0.7) at
most 0.5%, stated as a Phase 1 validation target against a constructed
adversarial-session reference set, not as a measured rate, since no reference
distribution of malicious sessions exists at specification time.

---

## 7. Novelty Detection

In parallel with the CUSUM/e-process statistic, a novelty detection component
flags three signals: activation trajectories in the bottom 2nd percentile of
training-corpus density; inflation of the OTHER bin (Section 3); and the SAE
reconstruction residual, the per-turn aggregate norm of the activation minus
its dictionary reconstruction, alarmed against a corpus-calibrated null.

**Why the residual channel:** a direction the SAE dictionary fails to
represent cannot appear in any feature bin, OTHER included, but appears in
the residual by construction. It is the one novelty signal complementary to
the dictionary rather than downstream of it. Its boundary is stated: an
activation-normal event leaves the residual unchanged, so this channel adds
nothing against goal-oriented factual inversion.

**Routing:** novelty flags are routed to Axis 4's session accounting system
and contribute to τᵢ degradation. Accumulation of novelty flags without a
corresponding CUSUM/e-process crossing is itself a signal pattern warranting
review.

---

## 8. Axis Interaction

Axis 4 runs asynchronously in the inter-turn window, zero contribution to the
token generation critical path.

**Input:** activation trajectories from the monitored layers {L/4, L/2, 3L/4},
provided by the Axis 1 co-processor.

**Output on Wₜ > h (the calibrated CUSUM threshold):** session termination
signal routed to Axis 5 CCE-RAE with the full drift record, the CUSUM
trajectory, and τᵢ history.

**Output on UNVERIFIABLE flags from Axis 6:** routed to Axis 4 novelty
accounting. Accumulation contributes to τᵢ degradation without triggering
immediate termination.

**Axis 5 arbitration:** all termination decisions are routed through the
Axis 5 CCE-RAE rule-based arbitration engine, itself fail-closed under this
revision. Axis 4 detects. It does not decide. The separation is
architecturally mandatory.

---

## 9. Documented Boundary Conditions

**Threshold calibration dependency.** The corpus frequency floor and the size
of S₀, the prior weight β, the allowance k (and the per-scale allowance
ladder in the multi-scale bank), the threshold h and its false-alarm-rate
target, and the per-window token budget are Phase 1 calibration targets,
set against benign session statistics that do not exist until a deployment
context. Calibration proceeds by simulation or permutation on the Phase 1
benign-session corpus to a declared false-alarm target, with detection delay
reported at benchmark drift magnitudes.

**Three-turn baseline window, and its coverage gap, stated together.** The
baseline occupies turns 1 through 3; drift relative to P₀ is undefined for
the turns that constitute P₀. Even with the early-window check (Section 3),
an activation-normal event in any window produces no armed drift signal.
Axis 4's contribution against Goal-Oriented Factual Inversion is limited to
slower session-level drift and, per this revision, to activation-visible
events in the first three turns. The fast, activation-normal case is Axis 6's
jurisdiction alone; the depth available for that case is internal to Axis 6,
not a second armed axis here.

**Activation-level dependency, retained from earlier drafts.** Axis 4
requires access to the model's residual stream activations at monitored
layers. Deployments that do not expose activation trajectories cannot
implement Axis 4 as specified. Surface-level behavioral proxies are
explicitly out of scope and architecturally insufficient.

---

## 10. Implementation Files

```
axis4_drift_monitor/
├── SPEC.md                     ← This document
└── cusum_drift_detector.py     ← Class structure scaffold (specification scaffold, pending implementation)
```

Full implementation weights, private probe datasets, and adversarial session
validation corpus are withheld under mNDA protocol.

For research collaboration or mNDA access:
**Frank Bruno** | Independent AI Safety Researcher and Forensic Auditor | frank.bruno.oe@gmail.com | [LinkedIn](https://www.linkedin.com/in/frank-b-541370175/)
