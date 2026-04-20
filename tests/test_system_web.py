from __future__ import annotations

from tests.helpers import AppTestCase


class WebSystemTests(AppTestCase):
    def test_user_can_publish_and_apply_through_html_workflow(self):
        create_response = self.client.post(
            "/opportunities/new",
            data={
                "title": "Test Lead",
                "company": "Fabrikam",
                "location": "Remote",
                "description": "Drive quality strategy across the full career application lifecycle with strong communication.",
                "closing_date": "2026-05-20",
            },
            follow_redirects=True,
        )

        self.assertEqual(create_response.status_code, 200)
        page = create_response.get_data(as_text=True)
        self.assertIn("Opportunity created successfully.", page)
        self.assertIn("Test Lead", page)

        opportunity = self.service.list_opportunities()[0]
        apply_response = self.client.post(
            f"/opportunities/{opportunity['id']}/apply",
            data={
                "applicant_name": "Margaret Hamilton",
                "applicant_email": "margaret@example.com",
                "cover_letter": "I enjoy leading test strategy while staying close to product risks and delivery outcomes.",
                "resume_url": "https://example.com/margaret.pdf",
            },
            follow_redirects=True,
        )

        self.assertEqual(apply_response.status_code, 200)
        applied_page = apply_response.get_data(as_text=True)
        self.assertIn("Application submitted successfully.", applied_page)
        self.assertIn("Margaret Hamilton", applied_page)

    def test_invalid_html_submission_shows_errors(self):
        response = self.client.post(
            "/opportunities/new",
            data={
                "title": "",
                "company": "Fabrikam",
                "location": "",
                "description": "Too short",
                "closing_date": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("Title is required.", page)
        self.assertIn("Location is required.", page)
        self.assertIn("Description must contain at least 20 characters.", page)

