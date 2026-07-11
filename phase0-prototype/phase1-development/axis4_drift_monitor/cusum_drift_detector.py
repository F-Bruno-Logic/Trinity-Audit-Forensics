"""
cusum_drift_detector.py
========================
Specification Scaffold — Sovereign Sentinel Architecture (SSA) V1.3.1
Axis 4: Bayesian Weaver — Sequential Change-Point Drift Detection

STATUS: Specification scaffold. Interface and docstrings are formally specified.
        Implementation is pending Phase 4 compute infrastructure.
        See SPEC.md for full mathematical specification.

IP NOTICE: (c) 2026 Frank Bruno.
           Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
           Use, share, and build on this with attribution to Frank Bruno.
           IP anchored to Trinity-Audit-Forensics (SHA-256 Hash Registered).
           Full implementation details available under executed mNDA.
           Contact: frank.bruno.oe@gmail.com

CHANGE NOTE (V1.3.1): This replaces the earlier martingale-difference
formulation and the Cumulative Drift Integral Phi(T). Both are withdrawn:
an unbounded KL divergence against a three-turn empirical baseline is
infinite or undefined on essentially any later turn that activates a
previously unseen feature, and the martingale/CUSUM equivalence claimed
earlier holds only while a running minimum does not update. See SPEC.md
"Change note (V1.3.1)" for the full correction.

MATHEMATICAL FOUNDATION:
    Restricted-support baseline (Section 3 of SPEC.md):
        P_0(feature) = (c + beta * q) / (N + beta)
    over a restricted support S_0 plus a single OTHER aggregate bin, not the
    full 32,768-feature SAE dictionary.

    Bounded per-turn statistic D_t (Section 4): Jensen-Shannon divergence
    (bounded above by log 2) or squared Hellinger distance (bounded above
    by 1) between P_t and P_0, length-standardized.

    CUSUM statistic with allowance k (Section 2):
        S'_t = sum_{i=1}^{t} (D_i - k),  S'_0 = 0
        W_t  = S'_t - min(S'_0, S'_1, ..., S'_t)

    Session termination condition:
        W_t > h   (h is the calibrated CUSUM threshold)

    The detector is expressed as an e-process (a nonnegative supermartingale
    restarted at each candidate change time) so that Ville's inequality
    supplies a time-uniform, anytime-valid false-alarm guarantee (Shin,
    Ramdas, and Rinaldo, 2023), rather than the fixed-time martingale
    property claimed by earlier drafts.

    Multi-scale allowance bank (Section 5): the detector above is run at
    several block-length scales m, each with its own calibrated allowance
    k_m, narrowing the single-scale evasion corridor to a calibrated
    instrument floor rather than eliminating it.

References:
    Page, E.S. (1954). Continuous Inspection Schemes. Biometrika.
    Lorden, G. (1971). Procedures for Reacting to a Change in Distribution.
        Annals of Mathematical Statistics.
    Moustakides, G.V. (1986). Optimal Stopping Times for Detecting Changes
        in Distributions. Annals of Statistics.
    Shin, J., Ramdas, A., and Rinaldo, A. (2023). E-Detectors: A
        Nonparametric Framework for Sequential Change Detection.
    Howard, S., Ramdas, A., McAuliffe, J., and Sekhon, J. (2021).
        Time-Uniform, Nonparametric, Nonasymptotic Confidence Sequences.
        Annals of Statistics.
    Waudby-Smith, I. and Ramdas, A. (2024). Estimating Means of Bounded
        Random Variables by Betting. JRSS B.
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
    baseline_support : Optional[np.ndarray]
        S_0 — the restricted set of monitored SAE feature indices, fixed
        at baseline freeze. Not the full 32,768-feature dictionary.
    baseline_distribution : Optional[np.ndarray]
        P_0 — the frozen, corpus-informed baseline over S_0 plus the OTHER
        bin, established from turns 1-3. Once set, cannot be updated for
        the duration of the session. Mutation raises a RuntimeError.
    per_turn_statistics : list[float]
        D_t values, the bounded (Jensen-Shannon or Hellinger) per-turn
        divergence between P_t and P_0. Append-only.
    cusum_partial_sums : list[float]
        S'_t = sum_{i<=t} (D_i - k), the allowance-adjusted partial sum.
        Append-only; used to compute the running minimum.
    cusum_statistic : float
        W_t = S'_t - min(S'_0, ..., S'_t). The session termination
        condition is W_t > h.
    intentional_trust : float
        tau_i in [0, 1] -- Intentional Trust Coefficient. Decays with each
        severity-weighted adverse event and with sub-threshold occupancy
        (Section 6 of SPEC.md): tau_i(t) = tau_i(t-1) * lambda^delta(t),
        where lambda = 0.95 and delta(t) includes both the severity-weighted
        event count and the fraction of recent turns spent near, but not
        over, the detection surface. Architecturally distinct from tau_e
        (Epistemic Trust Coefficient, Axis 3). Conflating the two
        constitutes a privilege escalation vulnerability.
    novelty_flags : list[int]
        Turn indices flagged by any of the three novelty signals: bottom
        2nd-percentile corpus density, OTHER-bin inflation, or SAE
        reconstruction-residual excursion. Contributes to tau_i degradation
        independently of the CUSUM statistic.
    terminated : bool
        True if W_t > h triggered session termination.
    termination_turn : Optional[int]
        Turn index at which termination was triggered, if applicable.
    """

    session_id: str
    baseline_support: Optional[np.ndarray] = None
    baseline_distribution: Optional[np.ndarray] = None
    per_turn_statistics: list[float] = field(default_factory=list)
    cusum_partial_sums: list[float] = field(default_factory=list)
    cusum_statistic: float = 0.0
    intentional_trust: float = 1.0
    novelty_flags: list[int] = field(default_factory=list)
    terminated: bool = False
    termination_turn: Optional[int] = None
    _baseline_frozen: bool = False

    def freeze_baseline(
        self,
        support: np.ndarray,
        distribution: np.ndarray,
    ) -> None:
        """
        Freeze the restricted-support baseline (S_0, P_0).

        Called once after turn 3. Any subsequent call raises RuntimeError.
        The frozen baseline cannot be updated for the duration of the
        session. This precludes the baseline-walking attack class. See
        SPEC.md Section 3.

        Parameters
        ----------
        support : np.ndarray
            S_0 — the restricted monitored feature support: features active
            in the baseline window plus features above the offline-corpus
            frequency floor.
        distribution : np.ndarray
            P_0 — the Dirichlet-posterior-mean baseline over S_0 plus the
            OTHER bin, per SPEC.md Section 3.

        Raises
        ------
        RuntimeError
            If called after the baseline has already been frozen.
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md Section 3."
        )


# ---------------------------------------------------------------------------
# Core detector
# ---------------------------------------------------------------------------

class CUSUMDriftDetector:
    """
    Session-level behavioral monitor implementing sequential change-point
    drift detection for the Sovereign Sentinel Architecture (SSA) V1.3.1,
    Axis 4.

    The detector operates asynchronously in the inter-turn window, zero
    contribution to the token generation critical path.

    Architectural position
    ----------------------
    - Receives activation trajectories from the Axis 1 CLR-CRAE co-processor
      at monitored layers {L/4, L/2, 3L/4}.
    - Routes termination signals to the Axis 5 CCE-RAE arbitration engine,
      itself fail-closed under this revision.
    - Routes novelty flags to the session accounting system for tau_i
      degradation.
    - Does not make enforcement decisions. Detection and arbitration are
      architecturally separated. See SPEC.md Section 8.

    Documented boundary (see SPEC.md Section 9): this detector has no
    coverage for events completed within the three-turn baseline window
    that are activation-normal, nor for any activation-normal event in any
    window. That coverage is Axis 6's alone.

    Parameters
    ----------
    threshold_h : float
        h — the calibrated CUSUM threshold. Session termination triggers
        at W_t > threshold_h. Must be calibrated against a representative
        benign session corpus before deployment. See SPEC.md Section 9.
    allowance_k : float
        k — the per-turn allowance subtracted before accumulation in the
        CUSUM partial sum. A Phase 1 calibration target.
    decay_rate : float
        lambda = 0.95 — the Intentional Trust Coefficient decay rate.
    novelty_percentile : float
        Bottom percentile threshold for the corpus-density novelty signal.
        Default: 0.02 (2nd percentile of training corpus density).
    scale_allowances : Optional[dict[int, float]]
        Per-scale allowances {block_length: k_m} for the multi-scale
        allowance bank (SPEC.md Section 5). If None, only the single-scale
        detector above is run.
    """

    def __init__(
        self,
        threshold_h: float,
        allowance_k: float,
        decay_rate: float = 0.95,
        novelty_percentile: float = 0.02,
        scale_allowances: Optional[dict] = None,
    ) -> None:
        self.threshold_h = threshold_h
        self.allowance_k = allowance_k
        self.decay_rate = decay_rate
        self.novelty_percentile = novelty_percentile
        self.scale_allowances = scale_allowances or {}

    def initialize_session(self, session_id: str) -> SessionRecord:
        """
        Initialize a new session record.

        Called at session start, before any turns are processed. The
        restricted-support baseline (S_0, P_0) is not yet established;
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
            "Pending Phase 4 implementation. See SPEC.md Section 3."
        )

    def process_turn(
        self,
        session: SessionRecord,
        turn_index: int,
        activation_trajectory: np.ndarray,
    ) -> SessionRecord:
        """
        Process a single turn's activation trajectory.

        For turns 1-3: accumulates activation data toward the
        restricted-support baseline. At turn 3: freezes (S_0, P_0), applying
        the early-window check so that activation-visible events within the
        baseline window are not simply unmonitored (SPEC.md Section 3).
        For turns > 3: computes the bounded per-turn statistic D_t, updates
        the CUSUM statistic W_t, evaluates the termination condition, and
        runs novelty detection.

        The termination condition W_t > threshold_h reflects a running
        minimum, not a raw partial sum: a session whose per-turn readings
        are individually below the allowance but persistently drifting will
        still trigger termination, while the reflection lets the detector
        adapt to an unknown change time.

        Parameters
        ----------
        session : SessionRecord
            The current session record. Mutated in place.
        turn_index : int
            The current turn index (1-indexed).
        activation_trajectory : np.ndarray
            The current turn's residual stream activations at the monitored
            layers.

        Returns
        -------
        SessionRecord
            The updated session record.
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md Sections 3-4."
        )

    def compute_per_turn_statistic(
        self,
        p_current: np.ndarray,
        p_baseline: np.ndarray,
        method: str = "jensen_shannon",
    ) -> float:
        """
        Compute the bounded per-turn divergence statistic D_t.

        Parameters
        ----------
        p_current : np.ndarray
            P_t — the activation-mass distribution at the current turn,
            over the restricted support S_0 plus the OTHER bin. Must be a
            valid probability distribution (non-negative, sums to 1).
        p_baseline : np.ndarray
            P_0 — the frozen baseline distribution over the same support.
            Must be a valid probability distribution (non-negative, sums
            to 1).
        method : str
            "jensen_shannon" (bounded above by log 2) or "hellinger"
            (bounded above by 1). An unbounded KL divergence is deliberately
            not offered here: boundedness of D_t is the precondition for
            the false-alarm and detection-delay guarantees in SPEC.md
            Section 2.

        Returns
        -------
        float
            D_t, the bounded, length-standardized per-turn statistic.

        Raises
        ------
        ValueError
            If distributions have mismatched shapes, contain negative
            values, do not sum to approximately 1.0, or method is not one
            of the two supported bounded statistics.

        Notes
        -----
        Unlike an unbounded KL divergence, both supported statistics remain
        finite when p_current assigns mass to features absent from
        p_baseline's support; that case is exactly what the OTHER bin and
        the novelty-detection channel (SPEC.md Section 7) are for, not a
        reason to reject the computation.
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md Section 4."
        )

    def update_cusum(
        self,
        session: SessionRecord,
        per_turn_statistic: float,
    ) -> float:
        """
        Update the CUSUM statistic with the current turn's D_t.

        S'_t = S'_{t-1} + (D_t - allowance_k)
        W_t  = S'_t - min(S'_0, ..., S'_t)

        Parameters
        ----------
        session : SessionRecord
            The current session record. Mutated in place.
        per_turn_statistic : float
            D_t, from compute_per_turn_statistic.

        Returns
        -------
        float
            The updated CUSUM statistic W_t. Session termination is
            indicated by W_t > self.threshold_h; this method does not
            itself terminate the session or route to Axis 5. See
            SPEC.md Section 8.
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md Section 2."
        )

    def decay_intentional_trust(
        self,
        session: SessionRecord,
        severity_weight: float,
        sub_threshold_occupancy: float = 0.0,
    ) -> float:
        """
        Apply the Intentional Trust Coefficient decay function.

        tau_i(t) = tau_i(t-1) * lambda^delta(t)

        where:
            lambda = self.decay_rate = 0.95
            delta(t) = severity_weight + sub_threshold_occupancy

        New in V1.3.1: sub_threshold_occupancy contributes decay weight even
        when no alarm fires, so that riding just under the detection
        surface still costs standing in tau_i. See SPEC.md Section 6.

        tau_i is architecturally distinct from tau_e (Epistemic Trust
        Coefficient, Axis 3). tau_e certifies domain expertise at session
        entry and does not change during a session. tau_i tracks behavioral
        trajectory during the session and degrades with adverse events.
        Conflating the two constitutes a privilege escalation vulnerability.

        Parameters
        ----------
        session : SessionRecord
            The current session record.
        severity_weight : float
            The severity-weighted event count for the current turn.
        sub_threshold_occupancy : float
            The fraction of recent turns in which any statistic in the
            detection bank sits above a stated null quantile without
            alarming. Defaults to 0.0 (no occupancy penalty).

        Returns
        -------
        float
            Updated tau_i value after decay.
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md Section 6."
        )

    def detect_novelty(
        self,
        activation_trajectory: np.ndarray,
        training_corpus_density: np.ndarray,
        other_bin_mass: float,
        reconstruction_residual_norm: float,
    ) -> dict:
        """
        Evaluate the three novelty signals for the current turn.

        Parameters
        ----------
        activation_trajectory : np.ndarray
            Current turn's residual stream activations.
        training_corpus_density : np.ndarray
            Pre-computed density estimates over the training corpus
            activation space at monitored layers.
        other_bin_mass : float
            Activation mass assigned to the OTHER aggregate bin this turn.
        reconstruction_residual_norm : float
            The per-turn aggregate norm of the activation minus its SAE
            dictionary reconstruction.

        Returns
        -------
        dict
            {"corpus_density_flag": bool, "other_bin_flag": bool,
             "residual_flag": bool}, per SPEC.md Section 7. All three are
             blind to activation-normal events by construction; that case
             is Axis 6's jurisdiction (SPEC.md Section 9).
        """
        raise NotImplementedError(
            "Pending Phase 4 implementation. See SPEC.md Section 7."
        )

    def route_termination(self, session: SessionRecord) -> dict:
        """
        Package the session termination record for routing to Axis 5 CCE-RAE.

        Called when W_t > threshold_h. Returns a structured evidence record
        containing the full drift history, the CUSUM trajectory, and the
        tau_i history.

        Axis 4 detects. It does not decide. All termination decisions are
        routed through the Axis 5 CCE-RAE rule-based arbitration engine,
        itself fail-closed under this revision. This separation is
        architecturally mandatory. See SPEC.md Section 8.

        Parameters
        ----------
        session : SessionRecord
            The terminated session record.

        Returns
        -------
        dict
            Structured evidence package for CCE-RAE arbitration. Schema is
            defined in the Axis 5 interface specification.
        """
        raise NotImplementedError(
            "Pending Phase 5 arbitration layer integration. See SPEC.md Section 8."
        )
