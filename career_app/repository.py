from __future__ import annotations

import sqlite3
from contextlib import closing


class OpportunityRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def init_schema(self) -> None:
        with closing(self._connect()) as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS opportunities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT NOT NULL,
                    description TEXT NOT NULL,
                    closing_date TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    opportunity_id INTEGER NOT NULL,
                    applicant_name TEXT NOT NULL,
                    applicant_email TEXT NOT NULL,
                    cover_letter TEXT NOT NULL,
                    resume_url TEXT NOT NULL,
                    status TEXT NOT NULL,
                    applied_at TEXT NOT NULL,
                    FOREIGN KEY(opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE
                );
                """
            )
            connection.commit()

    def list_opportunities(self) -> list[dict]:
        query = """
            SELECT
                o.*, 
                COUNT(a.id) AS application_count
            FROM opportunities o
            LEFT JOIN applications a ON a.opportunity_id = o.id
            GROUP BY o.id
            ORDER BY o.created_at DESC, o.id DESC
        """
        with closing(self._connect()) as connection:
            rows = connection.execute(query).fetchall()
        return [dict(row) for row in rows]

    def create_opportunity(self, opportunity: dict) -> dict:
        query = """
            INSERT INTO opportunities (title, company, location, description, closing_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (
            opportunity["title"],
            opportunity["company"],
            opportunity["location"],
            opportunity["description"],
            opportunity["closing_date"],
            opportunity["created_at"],
        )
        with closing(self._connect()) as connection:
            cursor = connection.execute(query, values)
            opportunity_id = cursor.lastrowid
            connection.commit()
        created = self.get_opportunity(opportunity_id)
        if created is None:
            raise LookupError("Opportunity was not created.")
        return created

    def get_opportunity(self, opportunity_id: int) -> dict | None:
        with closing(self._connect()) as connection:
            opportunity = connection.execute(
                """
                SELECT
                    o.*, 
                    COUNT(a.id) AS application_count
                FROM opportunities o
                LEFT JOIN applications a ON a.opportunity_id = o.id
                WHERE o.id = ?
                GROUP BY o.id
                """,
                (opportunity_id,),
            ).fetchone()
        if opportunity is None:
            return None
        data = dict(opportunity)
        data["applications"] = self.list_applications_for_opportunity(opportunity_id)
        return data

    def create_application(self, application: dict) -> dict:
        query = """
            INSERT INTO applications (
                opportunity_id,
                applicant_name,
                applicant_email,
                cover_letter,
                resume_url,
                status,
                applied_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            application["opportunity_id"],
            application["applicant_name"],
            application["applicant_email"],
            application["cover_letter"],
            application["resume_url"],
            application["status"],
            application["applied_at"],
        )
        with closing(self._connect()) as connection:
            cursor = connection.execute(query, values)
            application_id = cursor.lastrowid
            connection.commit()
            row = connection.execute(
                "SELECT * FROM applications WHERE id = ?",
                (application_id,),
            ).fetchone()
        if row is None:
            raise LookupError("Application was not created.")
        return dict(row)

    def list_applications_for_opportunity(self, opportunity_id: int) -> list[dict]:
        query = """
            SELECT *
            FROM applications
            WHERE opportunity_id = ?
            ORDER BY applied_at DESC, id DESC
        """
        with closing(self._connect()) as connection:
            rows = connection.execute(query, (opportunity_id,)).fetchall()
        return [dict(row) for row in rows]

