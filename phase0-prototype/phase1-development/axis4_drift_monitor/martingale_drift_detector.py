"""
martingale_drift_detector.py
============================
Specification Scaffold — Sovereign Sentinel Architecture (SSA) V1.2
Axis 4: Bayesian Weaver — Martingale-Based Drift Enforcement

STATUS: Specification scaffold. Interface and docstrings are formally specified.
        Implementation is pending Phase 4 compute infrastructure.
        See SPEC.md for full mathematical specification.

IP NOTICE: © 2026 Frank Bruno. All Rights Reserved.
           Licensed under Business Source License 1.1.
           IP anchored to Trinity-Audit-Forensics (SHA-3-512 Hash Registered).
           Full implementation details available under executed mNDA.
           Contact: frank.bruno.oe@gmail.com

MATHEMATICAL FOUNDATION:
    Martingale Null Hypothesis (H₀ — Benign Session):
        𝔼[X_{t+1} | ℱ_t] = X_t
    where {X_t} is the sequence of per-turn KL-divergence values with respect
    to the filtration ℱ_t = σ(X_1, ..., X_t).

    Systematic violation of this property — sustained upward drift in {X_t} —
    constitutes formal rejection of H₀ and is the statistical signature of a
    session-level adversary or Goal-Oriented Factual Inversion (GOFI) event.

    Cumulative Drift Integral:
        Φ(T) = Σ_{t=1}^{T} D_KL(P_t ‖ P_0)

    Session termination condition:
        Φ(T) > Φ_max

References:
    Williams, D. (1991). Probability with Martingales. Cambridge University Press.
    Doob, J.L. (1953). Stochastic Processes. Wiley. Ch. 7 (Martingales).
    Cover, T.M. & Thomas, J.A. (2006). Elements of Information Theory. Wiley. Ch. 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import numpy as np


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class SessionRecord:
    """
    Immutable record of a session's behavioral trajectory.

    Attributes
    ----------
    session_id : str
        Unique session identifier for TPM audit chain logging.
    baseline_distribution : np.ndarray
        P_0 — the frozen behavioral baseline established from turns 1–3.
        Once set, this distribution cannot be updated for the duration
        of the session. Mutation raises a RuntimeError.
    kl_divergences : list[float]
        Per-turn D_KL(P_t ‖ P_0) values. Append-only.
    cumulative_drift : float
        Φ(T) — running sum of kl_divergences. The session termination
        condition is Φ(T) > Φ_max.
    intentional_trust : float
        τ_i ∈ [0, 1] — Intentional Trust Coefficient. Decays with each
        severity-weighted adverse event: τ_i(t) = τ_i(t-1) · λ^δ(t),
        where λ = 0.95 and δ(t) is the severity-weighted event count.
        Architecturally distinct from τ_e (Epistemic Trust Coefficient,
        Axis 3). Conflating the two constitutes a privilege escalation
        vulnerability.
    novelty_flags : list[int]
        Turn indices where activation trajectories fell in the bottom
        2nd percentile of training corpus density. Contributes to τ_i
        degradation independently of Φ(T).
    terminated : bool
        True if Φ(T) > Φ_max triggered session termination.
    termination_turn : Optional[int]
        Turn index at which termination was triggered, if applicable.
    """

    session_id: str
    baseline_distribution: Optional[np.ndarray] = None
    kl_divergences: list[float] = field(default_factory=list)
    cumulative_drift: float = 0.0
    intentional_trust: float = 1.0
    novelty_flags: list[int] = field(default_factory=list)
    terminated: bool = False
    termination_turn: Optional[int] = None
    _baseline_frozen: bool = False

    def freeze_baseline(self, distribution: np.ndarray) -> None:
        """
        Freeze the session baseline distribution P_0.

        Called once after turn 3. Any subsequent call raises RuntimeError.
        The frozen baseline cannot be updated for the duration of the session.
        This precludes the baseline-walking attack class.

        Parameters
        ----------
        distribution : np.ndarray
            Empirical behavioral distribution derived from turns 1–3.

        Raises
        ------
        RuntimeError
            If called after the baseline has already been frozen.
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md §3."
        )


# ---------------------------------------------------------------------------
# Core detector
# ---------------------------------------------------------------------------

class MartingaleDriftDetector:
    """
    Session-level behavioral monitor implementing Martingale-based drift
    detection for the Sovereign Sentinel Architecture (SSA) V1.2, Axis 4.

    The detector operates asynchronously in the inter-turn window — zero
    contribution to the token generation critical path.

    Architectural position
    ----------------------
    - Receives activation trajectories from the Axis 1 CLR-CRAE co-processor
      at monitored layers {L/4, L/2, 3L/4}.
    - Routes termination signals to the Axis 5 CCE-RAE arbitration engine.
    - Routes novelty flags to the session accounting system for τ_i degradation.
    - Does not make enforcement decisions. Detection and arbitration are
      architecturally separated. See SPEC.md §8.

    Parameters
    ----------
    phi_max : float
        Φ_max — the Cumulative Drift Integral termination threshold.
        Must be calibrated against a representative benign session corpus
        before deployment. See SPEC.md §9 (Boundary Conditions).
    decay_rate : float
        λ = 0.95 — the Intentional Trust Coefficient decay rate.
    novelty_percentile : float
        Bottom percentile threshold for novelty detection.
        Default: 0.02 (2nd percentile of training corpus density).
    """

    def __init__(
        self,
        phi_max: float,
        decay_rate: float = 0.95,
        novelty_percentile: float = 0.02,
    ) -> None:
        self.phi_max = phi_max
        self.decay_rate = decay_rate
        self.novelty_percentile = novelty_percentile

    def initialize_session(self, session_id: str) -> SessionRecord:
        """
        Initialize a new session record.

        Called at session start, before any turns are processed.
        The baseline distribution P_0 is not yet established —
        it will be frozen after turn 3.

        Parameters
        ----------
        session_id : str
            Unique session identifier for TPM audit chain logging.

        Returns
        -------
        SessionRecord
            A new, unfrozen session record.
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md §3."
        )

    def process_turn(
        self,
        session: SessionRecord,
        turn_index: int,
        activation_trajectory: np.ndarray,
    ) -> SessionRecord:
        """
        Process a single turn's activation trajectory.

        For turns 1–3: accumulates activation data for baseline establishment.
        At turn 3: freezes the baseline distribution P_0.
        For turns > 3: computes D_KL(P_t ‖ P_0), updates Φ(T), evaluates
        the termination condition, and runs novelty detection.

        The termination condition Φ(T) > Φ_max is a trajectory threshold,
        not a per-turn threshold. A session whose per-turn readings are
        individually below threshold but cumulatively directional will
        still trigger termination.

        Parameters
        ----------
        session : SessionRecord
            The current session record. Mutated in place.
        turn_index : int
            The current turn index (1-indexed).
        activation_trajectory : np.ndarray
            Residual stream activations at monitored layers {L/4, L/2, 3L/4},
            provided by the Axis 1 CLR-CRAE co-processor. Surface-level
            token statistics are explicitly insufficient and out of scope.

        Returns
        -------
        SessionRecord
            Updated session record. If Φ(T) > Φ_max, session.terminated
            is True and session.termination_turn is set.

        Raises
        ------
        RuntimeError
            If called on a session that has already been terminated.
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md §§4–5."
        )

    def compute_kl_divergence(
        self,
        p_current: np.ndarray,
        p_baseline: np.ndarray,
    ) -> float:
        """
        Compute D_KL(P_t ‖ P_0).

        D_KL(P_t ‖ P_0) = Σ_k P_t(k) log(P_t(k) / P_0(k))

        Direction is architecturally significant: divergence is measured
        from the current distribution to the frozen baseline, not the
        reverse. The asymmetry of KL-divergence is a feature, not a bug —
        it measures how surprising the current distribution is relative
        to the baseline, which is the correct framing for drift detection.

        Parameters
        ----------
        p_current : np.ndarray
            P_t — the behavioral distribution at the current turn.
            Must be a valid probability distribution (non-negative, sums to 1).
        p_baseline : np.ndarray
            P_0 — the frozen baseline distribution.
            Must be a valid probability distribution (non-negative, sums to 1).

        Returns
        -------
        float
            D_KL(P_t ‖ P_0) ≥ 0. Returns 0.0 if and only if P_t = P_0.

        Raises
        ------
        ValueError
            If distributions have mismatched shapes, contain negative values,
            or do not sum to approximately 1.0.
        RuntimeError
            If p_baseline contains zeros where p_current is non-zero.
            This indicates a support mismatch — the current distribution
            assigns probability mass to events the baseline considers
            impossible, which is itself a strong drift signal and should
            be routed to novelty detection rather than KL computation.

        Notes
        -----
        Numerical stability: a small epsilon is added to p_baseline before
        the log computation to avoid division by zero in near-zero regions.
        Entries where p_current is zero contribute 0 to the sum by
        convention (0 * log(0) = 0, consistent with information theory).
        """
        p_current = np.asarray(p_current, dtype=np.float64)
        p_baseline = np.asarray(p_baseline, dtype=np.float64)

        # Shape validation
        if p_current.shape != p_baseline.shape:
            raise ValueError(
                f"Distribution shape mismatch: p_current {p_current.shape} "
                f"vs p_baseline {p_baseline.shape}."
            )

        # Non-negativity validation
        if np.any(p_current < 0) or np.any(p_baseline < 0):
            raise ValueError(
                "Distributions must be non-negative. "
                "Negative values indicate a malformed activation projection."
            )

        # Normalization validation — tolerant to floating point rounding
        if not np.isclose(p_current.sum(), 1.0, atol=1e-6):
            raise ValueError(
                f"p_current does not sum to 1.0 (got {p_current.sum():.8f}). "
                "Normalize before computing KL-divergence."
            )
        if not np.isclose(p_baseline.sum(), 1.0, atol=1e-6):
            raise ValueError(
                f"p_baseline does not sum to 1.0 (got {p_baseline.sum():.8f}). "
                "The frozen baseline may have been corrupted."
            )

        # Support mismatch check — p_current non-zero where p_baseline is exactly zero
        # Only raises if p_current assigns positive mass to an impossible event
        support_mismatch = np.any((p_current > 1e-10) & (p_baseline < 1e-10))
        if support_mismatch:
            raise RuntimeError(
                "Support mismatch: p_current assigns probability mass to "
                "events p_baseline considers impossible. This is a strong "
                "drift signal. Route to novelty detection rather than "
                "KL computation. See SPEC.md §7."
            )

        # Numerical stability: epsilon floor on baseline to avoid log(0)
        epsilon = 1e-10
        p_baseline_stable = np.where(p_baseline > 0, p_baseline, epsilon)

        # Compute D_KL(P_t ‖ P_0) = Σ_k P_t(k) log(P_t(k) / P_0(k))
        # Entries where p_current == 0 contribute 0 by convention (0 log 0 = 0)
        with np.errstate(divide="ignore", invalid="ignore"):
            log_ratio = np.where(
                p_current > 0,
                np.log(p_current / p_baseline_stable),
                0.0,
            )

        kl = float(np.sum(p_current * log_ratio))

        # Gibbs' inequality: D_KL >= 0 always. Clamp numerical noise.
        return max(kl, 0.0)

    def decay_intentional_trust(
        self,
        session: SessionRecord,
        severity_weight: float,
    ) -> float:
        """
        Apply the Intentional Trust Coefficient decay function.

        τ_i(t) = τ_i(t-1) · λ^δ(t)

        where:
            λ = self.decay_rate = 0.95
            δ(t) = severity_weight (severity-weighted event count at turn t)

        τ_i is architecturally distinct from τ_e (Epistemic Trust Coefficient,
        Axis 3). τ_e certifies domain expertise at session entry and does not
        change during a session. τ_i tracks behavioral trajectory during the
        session and degrades with adverse events. Conflating the two constitutes
        a privilege escalation vulnerability. See SPEC.md §6.

        Parameters
        ----------
        session : SessionRecord
            The current session record.
        severity_weight : float
            δ(t) — the severity-weighted event count for the current turn.

        Returns
        -------
        float
            Updated τ_i value after decay.
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md §6."
        )

    def detect_novelty(
        self,
        activation_trajectory: np.ndarray,
        training_corpus_density: np.ndarray,
    ) -> bool:
        """
        Flag activation trajectories in the bottom 2nd percentile of
        training corpus density.

        A session that produces individually plausible turn-level behavior
        while navigating the model toward rarely-visited capability regions
        may not trigger the Cumulative Drift Integral. Novelty detection
        provides the orthogonal signal: not how far the session has moved
        from its starting point, but how far it has moved from the model's
        training distribution.

        Novelty flags are routed to the session accounting system and
        contribute to τ_i degradation. Accumulation of novelty flags without
        a corresponding Φ(T) crossing is itself a signal pattern warranting
        review. See SPEC.md §7.

        Parameters
        ----------
        activation_trajectory : np.ndarray
            Current turn's residual stream activations.
        training_corpus_density : np.ndarray
            Pre-computed density estimates over the training corpus
            activation space at monitored layers.

        Returns
        -------
        bool
            True if activation_trajectory falls below self.novelty_percentile
            of training_corpus_density. False otherwise.
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md §7."
        )

    def route_termination(self, session: SessionRecord) -> dict:
        """
        Package the session termination record for routing to Axis 5 CCE-RAE.

        Called when Φ(T) > Φ_max. Returns a structured evidence record
        containing the full drift history, cumulative integral value,
        τ_i trajectory, and novelty flag record.

        Axis 4 detects. It does not decide. All termination decisions are
        routed through the Axis 5 CCE-RAE rule-based arbitration engine.
        This separation is architecturally mandatory. See SPEC.md §8.

        Parameters
        ----------
        session : SessionRecord
            The terminated session record.

        Returns
        -------
        dict
            Structured evidence package for CCE-RAE arbitration.
            Schema is defined in the Axis 5 interface specification.
        """
        raise NotImplementedError(
            "Pending Phase 5 arbitration layer integration. See SPEC.md §8."
        )
