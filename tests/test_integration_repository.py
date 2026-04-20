from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import TestCase

from career_app.repository import OpportunityRepository


class RepositoryIntegrationTests(TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "repository.sqlite3")
        self.repository = OpportunityRepository(self.db_path)
        self.repository.init_schema()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_repository_persists_opportunity_and_application(self):
        opportunity = self.repository.create_opportunity(
            {
                "title": "Product Tester",
                "company": "Contoso",
                "location": "Hybrid",
                "description": "Coordinate manual and automated tests across web application releases.",
                "closing_date": "2026-07-15",
                "created_at": "2026-04-18T12:00:00+00:00",
            }
        )

        application = self.repository.create_application(
            {
                "opportunity_id": opportunity["id"],
                "applicant_name": "Alan Turing",
                "applicant_email": "alan@example.com",
                "cover_letter": "I want to contribute practical testing insight and careful analytical thinking to the team.",
                "resume_url": "https://example.com/alan.pdf",
                "status": "submitted",
                "applied_at": "2026-04-18T12:30:00+00:00",
            }
        )

        loaded = self.repository.get_opportunity(opportunity["id"])

        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["title"], "Product Tester")
        self.assertEqual(loaded["application_count"], 1)
        self.assertEqual(len(loaded["applications"]), 1)
        self.assertEqual(loaded["applications"][0]["id"], application["id"])

    def test_list_opportunities_orders_most_recent_first(self):
        older = self.repository.create_opportunity(
            {
                "title": "QA Analyst",
                "company": "Older Corp",
                "location": "On-site",
                "description": "Support release validation with test cases, defect tracking, and reporting metrics.",
                "closing_date": "2026-06-05",
                "created_at": "2026-04-17T08:00:00+00:00",
            }
        )
        newer = self.repository.create_opportunity(
            {
                "title": "Automation Engineer",
                "company": "Newer Corp",
                "location": "Remote",
                "description": "Build maintainable regression suites for the hiring platform and surrounding services.",
                "closing_date": "2026-06-10",
                "created_at": "2026-04-18T08:00:00+00:00",
            }
        )

        opportunities = self.repository.list_opportunities()

        self.assertEqual([item["id"] for item in opportunities], [newer["id"], older["id"]])

