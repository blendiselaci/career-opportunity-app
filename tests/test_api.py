from __future__ import annotations

from tests.helpers import AppTestCase


class ApiTests(AppTestCase):
    def test_healthcheck_returns_ok(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_create_and_fetch_opportunity_via_api(self):
        create_response = self.client.post(
            "/api/opportunities",
            json={
                "title": "Backend Developer",
                "company": "Northwind",
                "location": "Prishtina",
                "description": "Design, test, and maintain secure APIs for a customer-facing recruitment platform.",
                "closing_date": "2026-06-01",
            },
        )

        self.assertEqual(create_response.status_code, 201)
        created = create_response.get_json()

        fetch_response = self.client.get(f"/api/opportunities/{created['id']}")

        self.assertEqual(fetch_response.status_code, 200)
        fetched = fetch_response.get_json()
        self.assertEqual(fetched["title"], "Backend Developer")
        self.assertEqual(fetched["company"], "Northwind")
        self.assertEqual(fetched["application_count"], 0)

    def test_apply_to_opportunity_via_api(self):
        opportunity = self.create_opportunity()

        response = self.client.post(
            f"/api/opportunities/{opportunity['id']}/apply",
            json={
                "applicant_name": "Grace Hopper",
                "applicant_email": "grace@example.com",
                "cover_letter": "I enjoy building reliable software systems and introducing disciplined testing practices.",
                "resume_url": "https://example.com/grace.pdf",
            },
        )

        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertEqual(body["status"], "submitted")
        self.assertEqual(body["opportunity_id"], opportunity["id"])

        applications_response = self.client.get(f"/api/opportunities/{opportunity['id']}/applications")
        self.assertEqual(applications_response.status_code, 200)
        applications = applications_response.get_json()["applications"]
        self.assertEqual(len(applications), 1)
        self.assertEqual(applications[0]["applicant_name"], "Grace Hopper")

    def test_api_returns_validation_errors(self):
        response = self.client.post(
            "/api/opportunities",
            json={
                "title": "",
                "company": "Northwind",
                "location": "",
                "description": "Too short",
                "closing_date": "",
            },
        )

        self.assertEqual(response.status_code, 400)
        body = response.get_json()
        self.assertEqual(body["message"], "Validation failed")
        self.assertIn("title", body["errors"])
        self.assertIn("location", body["errors"])
        self.assertIn("description", body["errors"])

    def test_api_returns_not_found(self):
        response = self.client.get("/api/opportunities/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["message"], "Opportunity 999 was not found.")

