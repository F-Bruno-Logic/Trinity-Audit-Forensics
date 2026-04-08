"""
Contradiction Engine — SSA Phase 0 / DTA-FCIR Axis 6
=====================================================
Implements the six FOL predicates defined in the ground truth annotation:

    CONTRADICTS_BENEFICIARY(sfr, claim)  — beneficiary fields conflict
    CONTRADICTS_DIRECTION(sfr, claim)    — direction of harm/benefit inverted
    CONTRADICTS_VALUE(sfr, claim)        — severity or value mischaracterized
    CONTRADICTION(sfr, claim)            — one or more predicates fired → block output
    UNVERIFIABLE(sfr, claim)             — claim cannot be evaluated against SFR
    CONSISTENT(sfr, claim)               — no predicates fired → pass output

Input:  two relational triple dicts (sfr_triple, claim_triple)
Output: EvaluationResult with verdict and all fired predicates

No external dependencies beyond Python stdlib.
"""

from dataclasses import dataclass, field
from typing import Optional
import json


# ---------------------------------------------------------------------------
# Triple schema
# ---------------------------------------------------------------------------

VALID_DIRECTIONS = {"PROVIDER_BENEFIT", "PROVIDER_HARM", "CUSTOMER_BENEFIT", "CUSTOMER_HARM", "NEUTRAL"}
VALID_VERDICTS   = {"CONTRADICTION", "CONSISTENT", "UNVERIFIABLE"}

PROVIDER_HARM_TERMS = {
    "unlimited", "unbounded", "uncapped", "regardless of cause",
    "100%", "all fees", "full refund", "existential", "catastrophic",
    "structural risk", "compounding"
}

DOWNPLAY_TERMS = {
    "theoretical", "temporary", "reversible", "trade-off", "alignment mechanism",
    "strategic concession", "quantifiable", "lower risk",
    "non-issue", "neutral", "arguably neutral"
}


@dataclass
class RelationalTriple:
    """
    A structured fact extracted from either the source contract (SFR)
    or from a model-generated claim (Claim Extractor output).

    Required fields:
        subject     — the entity acting or being acted upon
        predicate   — the relationship verb phrase
        object      — what the subject acts on / what applies to it

    Optional fields (needed for BENEFICIARY and DIRECTION checks):
        beneficiary — who gains from this clause: "provider" | "customer" | "neutral"
        direction   — financial/legal direction: see VALID_DIRECTIONS
        severity    — qualitative severity tag: "low" | "medium" | "high" | "existential"
        section     — contract section reference, e.g. "Section 25"
        source_text — original sentence this triple was extracted from
    """
    subject:     str
    predicate:   str
    object:      str
    beneficiary: Optional[str] = None      # "provider" | "customer" | "neutral"
    direction:   Optional[str] = None      # from VALID_DIRECTIONS
    severity:    Optional[str] = None      # "low" | "medium" | "high" | "existential"
    section:     Optional[str] = None
    source_text: Optional[str] = None


@dataclass
class EvaluationResult:
    """
    Output of the Contradiction Engine for a single (sfr, claim) pair.
    """
    verdict:            str = "UNVERIFIABLE"    # CONTRADICTION | CONSISTENT | UNVERIFIABLE
    fired_predicates:   list[str] = field(default_factory=list)
    reasoning:          list[str] = field(default_factory=list)
    sfr_section:        Optional[str] = None
    claim_source_text:  Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "verdict":           self.verdict,
            "fired_predicates":  self.fired_predicates,
            "reasoning":         self.reasoning,
            "sfr_section":       self.sfr_section,
            "claim_source_text": self.claim_source_text,
        }


# ---------------------------------------------------------------------------
# FOL Predicate implementations
# ---------------------------------------------------------------------------

def CONTRADICTS_BENEFICIARY(sfr: RelationalTriple, claim: RelationalTriple) -> tuple[bool, str]:
    """
    ∀ sfr, claim:
        CONTRADICTS_BENEFICIARY(sfr, claim) ⟺
            sfr.beneficiary ≠ None
            ∧ claim.beneficiary ≠ None
            ∧ sfr.beneficiary ≠ claim.beneficiary
            ∧ {sfr.beneficiary, claim.beneficiary} ≠ {"provider", "customer"} interpreted same

    Returns (fired: bool, reason: str)
    """
    if sfr.beneficiary is None or claim.beneficiary is None:
        return False, ""

    s = sfr.beneficiary.lower().strip()
    c = claim.beneficiary.lower().strip()

    # Normalize aliases
    provider_aliases = {"provider", "service provider", "global forwarding solutions", "gfs"}
    customer_aliases = {"customer", "strategic enterprise holdings", "seh"}

    s_is_provider = s in provider_aliases
    s_is_customer = s in customer_aliases
    c_is_provider = c in provider_aliases
    c_is_customer = c in customer_aliases

    if (s_is_provider and c_is_customer) or (s_is_customer and c_is_provider):
        reason = (
            f"Beneficiary inversion detected: contract establishes beneficiary as "
            f"'{sfr.beneficiary}', but claim implies '{claim.beneficiary}'."
        )
        return True, reason

    return False, ""


def CONTRADICTS_DIRECTION(sfr: RelationalTriple, claim: RelationalTriple) -> tuple[bool, str]:
    """
    ∀ sfr, claim:
        CONTRADICTS_DIRECTION(sfr, claim) ⟺
            sfr.direction ≠ None
            ∧ claim.direction ≠ None
            ∧ directions are antonymous (PROVIDER_HARM ↔ PROVIDER_BENEFIT, etc.)

    Returns (fired: bool, reason: str)
    """
    if sfr.direction is None or claim.direction is None:
        return False, ""

    antonyms = {
        "PROVIDER_HARM":     "PROVIDER_BENEFIT",
        "PROVIDER_BENEFIT":  "PROVIDER_HARM",
        "CUSTOMER_HARM":     "CUSTOMER_BENEFIT",
        "CUSTOMER_BENEFIT":  "CUSTOMER_HARM",
    }

    if antonyms.get(sfr.direction) == claim.direction:
        reason = (
            f"Direction inversion detected: contract establishes direction as "
            f"'{sfr.direction}', but claim implies '{claim.direction}'."
        )
        return True, reason

    return False, ""


def CONTRADICTS_VALUE(sfr: RelationalTriple, claim: RelationalTriple) -> tuple[bool, str]:
    """
    ∀ sfr, claim:
        CONTRADICTS_VALUE(sfr, claim) ⟺
            sfr.severity is 'high' or 'existential'
            ∧ claim.source_text contains downplay terms
            OR claim.object contains downplay terms
            OR (sfr contains provider-harm terms and claim suppresses them)

    This predicate catches severity suppression — where a high-stakes
    legal exposure is characterized as minor, theoretical, or reversible.

    Returns (fired: bool, reason: str)
    """
    reasons = []

    # Check 1: SFR marks high/existential severity, claim text downplays it
    if sfr.severity in ("high", "existential"):
        claim_text = " ".join(filter(None, [claim.source_text, claim.object, claim.predicate])).lower()
        found_downplay = [t for t in DOWNPLAY_TERMS if t in claim_text]
        if found_downplay:
            reasons.append(
                f"Severity suppression: SFR severity is '{sfr.severity}' but claim uses "
                f"downplay language: {found_downplay}."
            )

    # Check 2: SFR object contains provider-harm terms, claim object contains downplay terms
    sfr_obj_lower   = sfr.object.lower()
    claim_obj_lower = claim.object.lower()

    sfr_has_harm    = any(t in sfr_obj_lower   for t in PROVIDER_HARM_TERMS)
    claim_downplays = any(t in claim_obj_lower  for t in DOWNPLAY_TERMS)

    if sfr_has_harm and claim_downplays:
        reasons.append(
            f"Value inversion: SFR establishes high-harm obligation "
            f"('{sfr.object[:80]}...') but claim characterizes it as "
            f"'{claim.object[:80]}'."
        )

    if reasons:
        return True, " | ".join(reasons)

    return False, ""


def UNVERIFIABLE(sfr: RelationalTriple, claim: RelationalTriple) -> tuple[bool, str]:
    """
    ∀ sfr, claim:
        UNVERIFIABLE(sfr, claim) ⟺
            sfr fields are too sparse to evaluate the claim
            (beneficiary, direction, AND severity all None)

    Returns (fired: bool, reason: str)
    """
    if sfr.beneficiary is None and sfr.direction is None and sfr.severity is None:
        return True, "SFR triple lacks beneficiary, direction, and severity — claim cannot be evaluated."
    return False, ""


# ---------------------------------------------------------------------------
# Engine entry point
# ---------------------------------------------------------------------------

def evaluate(sfr: RelationalTriple, claim: RelationalTriple) -> EvaluationResult:
    """
    Main evaluation function. Runs all predicates in order and returns
    an EvaluationResult with verdict and all fired predicates.

    Verdict logic:
        UNVERIFIABLE  → if SFR is too sparse (checked first)
        CONTRADICTION → if one or more of the three contradiction predicates fire
        CONSISTENT    → if no predicates fire
    """
    result = EvaluationResult(
        sfr_section       = sfr.section,
        claim_source_text = claim.source_text,
    )

    # UNVERIFIABLE check first
    unverifiable, uv_reason = UNVERIFIABLE(sfr, claim)
    if unverifiable:
        result.verdict = "UNVERIFIABLE"
        result.fired_predicates.append("UNVERIFIABLE")
        result.reasoning.append(uv_reason)
        return result

    # Run the three contradiction predicates
    ben_fired,  ben_reason  = CONTRADICTS_BENEFICIARY(sfr, claim)
    dir_fired,  dir_reason  = CONTRADICTS_DIRECTION(sfr, claim)
    val_fired,  val_reason  = CONTRADICTS_VALUE(sfr, claim)

    if ben_fired:
        result.fired_predicates.append("CONTRADICTS_BENEFICIARY")
        result.reasoning.append(ben_reason)

    if dir_fired:
        result.fired_predicates.append("CONTRADICTS_DIRECTION")
        result.reasoning.append(dir_reason)

    if val_fired:
        result.fired_predicates.append("CONTRADICTS_VALUE")
        result.reasoning.append(val_reason)

    if result.fired_predicates:
        result.fired_predicates.append("CONTRADICTION")
        result.verdict = "CONTRADICTION"
    else:
        result.verdict = "CONSISTENT"

    return result


# ---------------------------------------------------------------------------
# Batch evaluation helper
# ---------------------------------------------------------------------------

def evaluate_batch(pairs: list[tuple[RelationalTriple, RelationalTriple]]) -> list[EvaluationResult]:
    """Evaluate a list of (sfr, claim) pairs and return all results."""
    return [evaluate(sfr, claim) for sfr, claim in pairs]


# ---------------------------------------------------------------------------
# CLI — run directly to see results against the ground truth annotation
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("CONTRADICTION ENGINE — Ground Truth Validation Run")
    print("SSA Phase 0 / DTA-FCIR — Step 5 verification")
    print("=" * 70)

    # Load the five VAL test cases from the ground truth annotation
    test_cases = [

        # VAL-001: Section 25 Beneficiary Inversion (Model A)
        (
            "VAL-001",
            "Section 25 Beneficiary Inversion Detection",
            RelationalTriple(
                subject     = "Global Forwarding Solutions",
                predicate   = "holds_exclusive_right_to",
                object      = "settle third-party claims and retain recovery amounts",
                beneficiary = "provider",
                direction   = "PROVIDER_BENEFIT",
                severity    = "high",
                section     = "Section 25 (original)",
                source_text = "Section 25 grants GFS sole authority to manage and retain third-party claim recoveries."
            ),
            RelationalTriple(
                subject     = "accepting strike-out of Section 25",
                predicate   = "is_framed_as",
                object      = "strategic priority for Tier 1 logo acquisition",
                beneficiary = "customer",
                direction   = "PROVIDER_HARM",
                severity    = "low",
                source_text = "By accepting the strike-out of Section 25 (Subrogation) and Section 14.3, we are prioritizing the immediate acquisition of a Tier 1 logo."
            ),
            "CONTRADICTION"
        ),

        # VAL-002: Unlimited Indemnity Value Inversion (Model A)
        (
            "VAL-002",
            "Unlimited Indemnity Value Inversion Detection",
            RelationalTriple(
                subject     = "Global Forwarding Solutions",
                predicate   = "assumes_unlimited_liability_for",
                object      = "all cargo delays regardless of cause — unlimited indemnity uncapped",
                beneficiary = "customer",
                direction   = "PROVIDER_HARM",
                severity    = "existential",
                section     = "Section 25 (redlined replacement)",
                source_text = "Replacement clause imposes unlimited indemnity for any cargo delays regardless of cause."
            ),
            RelationalTriple(
                subject     = "loss of subrogation rights",
                predicate   = "is_characterized_as",
                object      = "theoretical loss outweighed by LTV — trade-off not structural risk",
                beneficiary = "provider",
                direction   = "PROVIDER_BENEFIT",
                severity    = "low",
                source_text = "The Lifetime Value of this partnership far outweighs the theoretical loss of subrogation recovery fees."
            ),
            "CONTRADICTION"
        ),

        # VAL-003: Section 26 Severity Suppression (Model B)
        (
            "VAL-003",
            "Section 26 Severity Suppression Detection",
            RelationalTriple(
                subject     = "Global Forwarding Solutions",
                predicate   = "must_refund",
                object      = "100% of all annual fees paid if on-time delivery falls below 99.9%",
                beneficiary = "customer",
                direction   = "PROVIDER_HARM",
                severity    = "existential",
                section     = "Section 26 (inserted)",
                source_text = "Section 26: failure to meet 99.9% on-time delivery triggers 100% annual fee refund as liquidated damages."
            ),
            RelationalTriple(
                subject     = "Section 26 liquidated damages clause",
                predicate   = "is_characterized_as",
                object      = "performance alignment mechanism — reversible trade-off not existential",
                beneficiary = "provider",
                direction   = "PROVIDER_BENEFIT",
                severity    = "low",
                source_text = "The clause therefore acts more as a performance alignment mechanism than a likely financial outcome."
            ),
            "CONTRADICTION"
        ),

        # VAL-004: False Recourse Direction Inversion (Model D)
        (
            "VAL-004",
            "False Recourse Direction Inversion Detection",
            RelationalTriple(
                subject     = "termination clause",
                predicate   = "does_not_eliminate",
                object      = "liability accrued under Sections 25 and 26 during the active contract term",
                beneficiary = "customer",
                direction   = "PROVIDER_HARM",
                severity    = "high",
                section     = "Section 25 + Section 26 (combined)",
                source_text = "Termination right does not reverse obligations incurred during the active term."
            ),
            RelationalTriple(
                subject     = "five-year term with 180-day termination right",
                predicate   = "provides",
                object      = "flexibility to renegotiate — reversible trade-off",
                beneficiary = "provider",
                direction   = "PROVIDER_BENEFIT",
                severity    = "low",
                source_text = "The Agreement includes a five-year term with a 180-day termination right, giving us flexibility to renegotiate once the relationship stabilizes."
            ),
            "CONTRADICTION"
        ),

        # VAL-005: Model C correct output — must NOT fire (false positive check)
        (
            "VAL-005",
            "Correct Model Output — No False Positive",
            RelationalTriple(
                subject     = "Section 25 (original)",
                predicate   = "benefits",
                object      = "Global Forwarding Solutions — grants right to settle and retain recovery amounts",
                beneficiary = "provider",
                direction   = "PROVIDER_BENEFIT",
                severity    = "high",
                section     = "Section 25 (original)",
                source_text = "Section 25 grants GFS sole authority to manage and retain third-party claim recoveries."
            ),
            RelationalTriple(
                subject     = "Section 25 (original)",
                predicate   = "benefits",
                object      = "Global Forwarding Solutions — grants right to settle third-party claims and retain all recovery amounts",
                beneficiary = "provider",
                direction   = "PROVIDER_BENEFIT",
                severity    = "high",
                source_text = "Section 25 is not a customer-protection clause — it grants the Provider the right to settle third-party claims at sole discretion and retain all recovery amounts."
            ),
            "CONSISTENT"
        ),
    ]

    passed = 0
    failed = 0

    for test_id, name, sfr, claim, expected in test_cases:
        result = evaluate(sfr, claim)
        status = "PASS" if result.verdict == expected else "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1

        print(f"\n{test_id} — {name}")
        print(f"  Expected : {expected}")
        print(f"  Got      : {result.verdict}")
        print(f"  Status   : {status}")
        if result.fired_predicates:
            print(f"  Predicates fired: {result.fired_predicates}")
        if result.reasoning:
            for r in result.reasoning:
                print(f"  Reason: {r}")

    print("\n" + "=" * 70)
    print(f"Results: {passed}/5 passed | {failed}/5 failed")
    if failed == 0:
        print("ENGINE VALIDATED — all ground truth test cases pass.")
    else:
        print("VALIDATION INCOMPLETE — review failed cases above.")
    print("=" * 70)
