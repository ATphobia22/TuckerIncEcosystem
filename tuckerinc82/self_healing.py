from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RemediationAction(StrEnum):
    RETRY = "retry"
    REFETCH = "refetch"
    QUARANTINE = "quarantine"
    HUMAN_REVIEW = "human_review"
    NO_ACTION = "no_action"


class RemediationProposal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    proposal_id: str = Field(min_length=1)
    target: str = Field(min_length=1)
    action: RemediationAction
    reason: str = Field(min_length=1)
    evidence: dict[str, Any]
    created_at: datetime
    automated: bool = False


def propose_remediation(target: str, error: Exception, *, retryable: bool = False) -> RemediationProposal:
    action = RemediationAction.RETRY if retryable else RemediationAction.HUMAN_REVIEW
    timestamp = datetime.now(timezone.utc)
    proposal_id = f"rem-{timestamp.strftime('%Y%m%dT%H%M%S%fZ')}"
    return RemediationProposal(
        proposal_id=proposal_id,
        target=target,
        action=action,
        reason=f"{type(error).__name__}: {error}",
        evidence={"exception_type": type(error).__name__, "retryable": retryable},
        created_at=timestamp,
        automated=False,
    )
