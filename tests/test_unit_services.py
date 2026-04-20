from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock, patch

from career_app.errors import NotFoundError, ValidationError
from career_app.services import CareerService


class CareerServiceUnitTests(TestCase):
    def setUp(self) -> None:
        self.repository = MagicMock()
        self.notifier = MagicMock()
        self.service = CareerService(self.repository, self.notifier)

    @patch("career_app.services.utcnow_iso", return_value="2026-04-18T12:00:00+00:00")
    def test_create_opportunity_adds_timestamp_before_saving(self, mocked_time):
        self.repository.create_opportunity.return_value = {"id": 1, "title": "QA Engineer"}

        result = self.service.create_opportunity(
            {
                "title": "QA Engineer",
                "company": "Pulse Labs",
                "location": "Remote",
                "description": "Design and maintain dependable testing workflows for a multi-team application.",
                "closing_date": "2026-05-01",
            }
        )

        self.assertEqual(result["id"], 1)
        self.repository.create_opportunity.assert_called_once_with(
            {
                "title": "QA Engineer",
                "company": "Pulse Labs",
                "location": "Remote",
                "description": "Design and maintain dependable testing workflows for a multi-team application.",
                "closing_date": "2026-05-01",
                "created_at": "2026-04-18T12:00:00+00:00",
            }
        )
        mocked_time.assert_called_once()

    @patch("career_app.services.utcnow_iso", return_value="2026-04-18T12:30:00+00:00")
    def test_apply_to_opportunity_sends_notification(self, mocked_time):
        self.repository.get_opportunity.return_value = {"id": 7, "title": "Test Lead"}
        self.repository.create_application.return_value = {
            "id": 99,
            "opportunity_id": 7,
            "applicant_name": "Grace Hopper",
            "applicant_email": "grace@example.com",
            "cover_letter": "I enjoy building reliable software systems and introducing disciplined testing practices.",
            "resume_url": "https://example.com/grace.pdf",
            "status": "submitted",
            "applied_at": "2026-04-18T12:30:00+00:00",
        }

        result = self.service.apply_to_opportunity(
            7,
            {
                "applicant_name": "Grace Hopper",
                "applicant_email": "grace@example.com",
                "cover_letter": "I enjoy building reliable software systems and introducing disciplined testing practices.",
                "resume_url": "https://example.com/grace.pdf",
            },
        )

        self.assertEqual(result["id"], 99)
        self.repository.create_application.assert_called_once_with(
            {
                "opportunity_id": 7,
                "applicant_name": "Grace Hopper",
                "applicant_email": "grace@example.com",
                "cover_letter": "I enjoy building reliable software systems and introducing disciplined testing practices.",
                "resume_url": "https://example.com/grace.pdf",
                "status": "submitted",
                "applied_at": "2026-04-18T12:30:00+00:00",
            }
        )
        self.notifier.send_application_received.assert_called_once_with(result)
        mocked_time.assert_called_once()

    def test_apply_to_missing_opportunity_raises_not_found(self):
        self.repository.get_opportunity.return_value = None

        with self.assertRaises(NotFoundError):
            self.service.apply_to_opportunity(
                999,
                {
                    "applicant_name": "Grace Hopper",
                    "applicant_email": "grace@example.com",
                    "cover_letter": "I enjoy building reliable software systems and introducing disciplined testing practices.",
                    "resume_url": "https://example.com/grace.pdf",
                },
            )

        self.repository.create_application.assert_not_called()
        self.notifier.send_application_received.assert_not_called()

    def test_create_opportunity_propagates_validation_errors(self):
        with self.assertRaises(ValidationError):
            self.service.create_opportunity(
                {
                    "title": "",
                    "company": "Pulse Labs",
                    "location": "Remote",
                    "description": "Too short",
                    "closing_date": "",
                }
            )

        self.repository.create_opportunity.assert_not_called()

