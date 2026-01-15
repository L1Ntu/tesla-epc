import json
from pydantic import BaseModel
from typing import Any, Dict
from db import Database

db = Database()


class CatalogModel(BaseModel):
    id: int
    name: str
    description: str
    country_code: str
    reference: str
    data: Dict[str, Any]

    @staticmethod
    def create_table():
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS catalog(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                country_code TEXT NOT NULL,
                reference TEXT NOT NULL,
                data TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_catalog_country_code
            ON catalog (country_code)
            """
        )
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_catalog_reference
            ON catalog (reference)
            """
        )

    @staticmethod
    def get_by_country_code(code):
        return db.fetchall("SELECT data FROM catalog c WHERE c.country_code = ?", (code,))

    def save(self):
        db.execute(
            "INSERT OR REPLACE INTO catalog VALUES (?, ?, ?, ?, ?, ?)",
            (
                self.id,
                self.name,
                self.description,
                self.country_code,
                self.reference,
                json.dumps(self.data),
            ),
        )
