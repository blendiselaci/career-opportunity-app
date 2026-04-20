from __future__ import annotations

from datetime import datetime, timezone

from .errors import NotFoundError
from .validators import validate_application_payload, validate_opportunity_payload


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class CareerService:
    def __init__(self, repository, notifier) -> None:
        self.repository = repository
        self.notifier = notifier

    def list_opportunities(self) -> list[dict]:
        return self.repository.list_opportunities()

    def create_opportunity(self, payload: dict) -> dict:
        cleaned = validate_opportunity_payload(payload)
        cleaned["created_at"] = utcnow_iso()
        return self.repository.create_opportunity(cleaned)

    def get_opportunity(self, opportunity_id: int) -> dict:
        opportunity = self.repository.get_opportunity(opportunity_id)
        if opportunity is None:
            raise NotFoundError(f"Opportunity {opportunity_id} was not found.")
        return opportunity

    def apply_to_opportunity(self, opportunity_id: int, payload: dict) -> dict:
        opportunity = self.repository.get_opportunity(opportunity_id)
        if opportunity is None:
            raise NotFoundError(f"Opportunity {opportunity_id} was not found.")

        cleaned = validate_application_payload(payload)
        cleaned["opportunity_id"] = opportunity_id
        cleaned["status"] = "submitted"
        cleaned["applied_at"] = utcnow_iso()
        application = self.repository.create_application(cleaned)
        self.notifier.send_application_received(application)
        return application

