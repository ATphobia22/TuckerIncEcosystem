from tuckerinc82.guardrails import (
    GuardrailDecision,
    GuardrailRequest,
    evaluate_guardrails,
)


def test_safe_low_impact_request_is_allowed():
    result = evaluate_guardrails(
        GuardrailRequest(purpose="benchmark", impact_level="low")
    )
    assert result.decision == GuardrailDecision.ALLOW


def test_unconsented_personal_data_is_denied():
    result = evaluate_guardrails(
        GuardrailRequest(
            purpose="profile a person",
            impact_level="high",
            involves_personal_data=True,
            has_consent=False,
        )
    )
    assert result.decision == GuardrailDecision.DENY


def test_unverifiable_claim_is_reviewed():
    result = evaluate_guardrails(
        GuardrailRequest(
            purpose="publish a research claim",
            impact_level="medium",
            claims_are_verifiable=False,
        )
    )
    assert result.decision == GuardrailDecision.REVIEW
