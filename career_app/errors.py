from __future__ import annotations


class AppError(Exception):
    pass


class ValidationError(AppError):
    def __init__(self, errors: dict[str, str]) -> None:
        super().__init__("Validation failed")
        self.errors = errors


class NotFoundError(AppError):
    pass

