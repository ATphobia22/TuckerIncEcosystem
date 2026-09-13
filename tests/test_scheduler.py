from datetime import datetime, timedelta, timezone

from tuckerinc82.scheduler import is_due


def test_disabled_source_is_never_due():
    assert is_due({"enabled": False, "ttl_seconds": 60}, last_retrieved_at=None) is False


def test_source_without_previous_retrieval_is_due():
    assert is_due({"enabled": True, "ttl_seconds": 60}, last_retrieved_at=None) is True


def test_source_becomes_due_after_ttl():
    now = datetime.now(timezone.utc)
    previous = now - timedelta(seconds=61)
    assert is_due({"enabled": True, "ttl_seconds": 60}, last_retrieved_at=previous, now=now) is True
