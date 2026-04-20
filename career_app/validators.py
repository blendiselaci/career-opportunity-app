from __future__ import annotations

from datetime import date
import re

from .errors import ValidationError

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
URL_PATTERN = re.compile(r"^https?://.+")


def _clean_required(payload: dict, field: str, label: str, errors: dict[str, str]) -> str:
    value = str(payload.get(field, "")).strip()
    if not value:
        errors[field] = f"{label} is required."
    return value


def validate_opportunity_payload(payload: dict) -> dict:
    errors: dict[str, str] = {}
    cleaned = {
        "title": _clean_required(payload, "title", "Title", errors),
        "company": _clean_required(payload, "company", "Company", errors),
        "location": _clean_required(payload, "location", "Location", errors),
        "description": _clean_required(payload, "description", "Description", errors),
        "closing_date": _clean_required(payload, "closing_date", "Closing date", errors),
    }
    if cleaned["description"] and len(cleaned["description"]) < 20:
        errors["description"] = "Description must contain at least 20 characters."
    if cleaned["closing_date"]:
        try:
            date.fromisoformat(cleaned["closing_date"])
        except ValueError:
            errors["closing_date"] = "Closing date must use YYYY-MM-DD format."
    if errors:
        raise ValidationError(errors)
    return cleaned


def validate_application_payload(payload: dict) -> dict:
    errors: dict[str, str] = {}
    cleaned = {
        "applicant_name": _clean_required(payload, "applicant_name", "Applicant name", errors),
        "applicant_email": _clean_required(payload, "applicant_email", "Applicant email", errors),
        "cover_letter": _clean_required(payload, "cover_letter", "Cover letter", errors),
        "resume_url": _clean_required(payload, "resume_url", "Resume URL", errors),
    }
    if cleaned["applicant_email"] and not EMAIL_PATTERN.match(cleaned["applicant_email"]):
        errors["applicant_email"] = "Applicant email must be a valid email address."
    if cleaned["cover_letter"] and len(cleaned["cover_letter"]) < 30:
        errors["cover_letter"] = "Cover letter must contain at least 30 characters."
    if cleaned["resume_url"] and not URL_PATTERN.match(cleaned["resume_url"]):
        errors["resume_url"] = "Resume URL must start with http:// or https://."
    if errors:
        raise ValidationError(errors)
    return cleaned

