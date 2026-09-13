from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class GuardrailDecision(StrEnum):
    ALLOW = "allow"
    REVIEW = "review"
    DENY = "deny"


class GodIsLovePrinciple(StrEnum):
    HUMAN_DIGNITY = "human_dignity"
    NON_MALEFICENCE = "non_maleficence"
    TRUTHFULNESS = "truthfulness"
    CONSENT = "consent"
    PRIVACY = "privacy"
    FAIRNESS = "fairness"
    TRANSPARENCY = "transparency"
    ACCOUNTABILITY = "accountability"
    HUMAN_OVERSIGHT = "human_oversight"


class GuardrailRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    purpose: str = Field(min_length=1, max_length=1000)
    impact_level: str = Field(min_length=1, max_length=32)
    involves_personal_data: bool = False
    has_consent: bool = True
    can_harm: bool = False
    claims_are_verifiable: bool = True
    provides_explanation: bool = True
    has_human_oversight: bool = True
    fairness_risk: bool = False


class GuardrailResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: GuardrailDecision
    triggered_principles: list[GodIsLovePrinciple]
    rationale: list[str]


def evaluate_guardrails(request: GuardrailRequest) -> GuardrailResult:
    triggered: list[GodIsLovePrinciple] = []
    rationale: list[str] = []

    if request.can_harm:
        triggered.append(GodIsLovePrinciple.NON_MALEFICENCE)
        rationale.append("Potential harm requires a safety review.")

    if request.involves_personal_data and not request.has_consent:
        triggered.extend(
            [GodIsLovePrinciple.PRIVACY, GodIsLovePrinciple.CONSENT]
        )
        rationale.append("Personal-data processing without consent is denied.")
        return GuardrailResult(
            decision=GuardrailDecision.DENY,
            triggered_principles=triggered,
            rationale=rationale,
        )

    if not request.claims_are_verifiable:
        triggered.append(GodIsLovePrinciple.TRUTHFULNESS)
        rationale.append("Unverifiable claims require human review.")

    if not request.provides_explanation:
        triggered.append(GodIsLovePrinciple.TRANSPARENCY)
        rationale.append("Opaque consequential behavior requires review.")

    if request.fairness_risk:
        triggered.append(GodIsLovePrinciple.FAIRNESS)
        rationale.append("Potential fairness risk requires review.")

    if request.impact_level.lower() in {"high", "critical"}:
        triggered.extend(
            [GodIsLovePrinciple.HUMAN_DIGNITY, GodIsLovePrinciple.HUMAN_OVERSIGHT]
        )
        if not request.has_human_oversight:
            rationale.append("High-impact actions require human oversight.")
        else:
            rationale.append("High-impact action is gated by human oversight.")

    if triggered:
        return GuardrailResult(
            decision=GuardrailDecision.REVIEW,
            triggered_principles=list(dict.fromkeys(triggered)),
            rationale=rationale,
        )

    return GuardrailResult(
        decision=GuardrailDecision.ALLOW,
        triggered_principles=[],
        rationale=["No configured guardrail condition blocks execution."],
    )
