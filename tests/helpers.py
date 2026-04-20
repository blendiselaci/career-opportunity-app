from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import TestCase

from career_app import create_app


class AppTestCase(TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "test.sqlite3")
        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE": self.db_path,
            }
        )
        self.client = self.app.test_client()
        self.service = self.app.extensions["career_service"]

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def create_opportunity(self, **overrides):
        payload = {
            "title": "QA Engineer",
            "company": "Pulse Labs",
            "location": "Remote",
            "description": "Lead the automated and exploratory testing strategy for a growing platform.",
            "closing_date": "2026-05-10",
        }
        payload.update(overrides)
        return self.service.create_opportunity(payload)

    def create_application(self, opportunity_id: int, **overrides):
        payload = {
            "applicant_name": "Ada Lovelace",
            "applicant_email": "ada@example.com",
            "cover_letter": "I bring strong quality engineering experience and a practical mindset for product delivery.",
            "resume_url": "https://example.com/resume.pdf",
        }
        payload.update(overrides)
        return self.service.apply_to_opportunity(opportunity_id, payload)

