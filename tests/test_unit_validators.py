from __future__ import annotations

from career_app.errors import ValidationError
from career_app.validators import validate_application_payload, validate_opportunity_payload
from unittest import TestCase


class ValidatorUnitTests(TestCase):
    def test_validate_opportunity_payload_trims_and_returns_clean_data(self):
        cleaned = validate_opportunity_payload(
            {
                "title": "  QA Engineer  ",
                "company": "  Pulse Labs ",
                "location": " Remote ",
                "description": "  Build test strategies and release confidence across multiple software deliveries.  ",
                "closing_date": "2026-05-01",
            }
        )

        self.assertEqual(cleaned["title"], "QA Engineer")
        self.assertEqual(cleaned["company"], "Pulse Labs")
        self.assertEqual(cleaned["location"], "Remote")

    def test_validate_opportunity_payload_rejects_invalid_data(self):
        with self.assertRaises(ValidationError) as context:
            validate_opportunity_payload(
                {
                    "title": "",
                    "company": "",
                    "location": "",
                    "description": "Too short",
                    "closing_date": "",
                }
            )

        self.assertIn("title", context.exception.errors)
        self.assertIn("company", context.exception.errors)
        self.assertIn("location", context.exception.errors)
        self.assertIn("description", context.exception.errors)
        self.assertIn("closing_date", context.exception.errors)

    def test_validate_application_payload_rejects_bad_email_and_resume_url(self):
        with self.assertRaises(ValidationError) as context:
            validate_application_payload(
                {
                    "applicant_name": "Ada Lovelace",
                    "applicant_email": "invalid-email",
                    "cover_letter": "This is a long enough cover letter to pass the length rule for the field.",
                    "resume_url": "resume.pdf",
                }
            )

        self.assertIn("applicant_email", context.exception.errors)
        self.assertIn("resume_url", context.exception.errors)

