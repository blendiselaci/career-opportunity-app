from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for

from .errors import NotFoundError, ValidationError
from .notification import NotificationService
from .repository import OpportunityRepository
from .services import CareerService


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    default_db_path = Path(app.instance_path) / "career_app.sqlite3"
    app.config.from_mapping(
        SECRET_KEY="career-app-secret-key",
        DATABASE=os.environ.get("CAREER_APP_DATABASE", str(default_db_path)),
    )

    if test_config:
        app.config.update(test_config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    repository = OpportunityRepository(app.config["DATABASE"])
    repository.init_schema()
    notifier = app.config.get("NOTIFICATION_SERVICE", NotificationService())
    service = CareerService(repository, notifier)
    app.extensions["career_service"] = service

    @app.get("/")
    def index():
        opportunities = service.list_opportunities()
        return render_template("index.html", opportunities=opportunities)

    @app.route("/opportunities/new", methods=["GET", "POST"])
    def create_opportunity():
        errors = {}
        form_data = {
            "title": "",
            "company": "",
            "location": "",
            "description": "",
            "closing_date": "",
        }
        if request.method == "POST":
            form_data = request.form.to_dict()
            try:
                opportunity = service.create_opportunity(form_data)
                return redirect(url_for("opportunity_detail", opportunity_id=opportunity["id"], created=1))
            except ValidationError as exc:
                errors = exc.errors

        return render_template("opportunity_form.html", errors=errors, form_data=form_data)

    @app.get("/opportunities/<int:opportunity_id>")
    def opportunity_detail(opportunity_id: int):
        created = request.args.get("created") == "1"
        applied = request.args.get("applied") == "1"
        try:
            opportunity = service.get_opportunity(opportunity_id)
        except NotFoundError:
            return render_template("not_found.html"), 404

        return render_template(
            "opportunity_detail.html",
            opportunity=opportunity,
            created=created,
            applied=applied,
            errors={},
            form_data={"applicant_name": "", "applicant_email": "", "cover_letter": "", "resume_url": ""},
        )

    @app.post("/opportunities/<int:opportunity_id>/apply")
    def apply_to_opportunity(opportunity_id: int):
        form_data = request.form.to_dict()
        try:
            service.apply_to_opportunity(opportunity_id, form_data)
            return redirect(url_for("opportunity_detail", opportunity_id=opportunity_id, applied=1))
        except ValidationError as exc:
            opportunity = service.get_opportunity(opportunity_id)
            return (
                render_template(
                    "opportunity_detail.html",
                    opportunity=opportunity,
                    created=False,
                    applied=False,
                    errors=exc.errors,
                    form_data=form_data,
                ),
                400,
            )
        except NotFoundError:
            return render_template("not_found.html"), 404

    @app.get("/api/health")
    def api_health():
        return jsonify({"status": "ok"})

    @app.get("/api/opportunities")
    def api_list_opportunities():
        return jsonify({"items": service.list_opportunities()})

    @app.post("/api/opportunities")
    def api_create_opportunity():
        payload = request.get_json(silent=True) or {}
        try:
            opportunity = service.create_opportunity(payload)
            return jsonify(opportunity), 201
        except ValidationError as exc:
            return jsonify({"message": "Validation failed", "errors": exc.errors}), 400

    @app.get("/api/opportunities/<int:opportunity_id>")
    def api_get_opportunity(opportunity_id: int):
        try:
            return jsonify(service.get_opportunity(opportunity_id))
        except NotFoundError as exc:
            return jsonify({"message": str(exc)}), 404

    @app.post("/api/opportunities/<int:opportunity_id>/apply")
    def api_apply_to_opportunity(opportunity_id: int):
        payload = request.get_json(silent=True) or {}
        try:
            application = service.apply_to_opportunity(opportunity_id, payload)
            return jsonify(application), 201
        except ValidationError as exc:
            return jsonify({"message": "Validation failed", "errors": exc.errors}), 400
        except NotFoundError as exc:
            return jsonify({"message": str(exc)}), 404

    @app.get("/api/opportunities/<int:opportunity_id>/applications")
    def api_list_applications(opportunity_id: int):
        try:
            opportunity = service.get_opportunity(opportunity_id)
            return jsonify({"opportunity_id": opportunity_id, "applications": opportunity["applications"]})
        except NotFoundError as exc:
            return jsonify({"message": str(exc)}), 404

    return app

