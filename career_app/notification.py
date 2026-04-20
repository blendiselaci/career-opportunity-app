from __future__ import annotations


class NotificationService:
    """Represents an external email/notification provider."""

    def send_application_received(self, application: dict) -> dict:
        return {
            "status": "sent",
            "recipient": application["applicant_email"],
            "application_id": application["id"],
        }

