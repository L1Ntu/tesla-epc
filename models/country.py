import json
from pydantic import BaseModel
from typing import Any, Dict
from db import Database

db = Database()


class CountryModel(BaseModel):
    code: str
    name: str
    data: Dict[str, Any]

    @staticmethod
    def create_table():
        db.execute("""
                CREATE TABLE IF NOT EXISTS main.country
                (
                    code TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    data TEXT NOT NULL,
                    CHECK (LENGTH(code) = 2)
                )
        """)

    @staticmethod
    def get_all():
        return db.fetchall("SELECT data FROM country")

    def save(self):
        db.execute(
            "INSERT OR REPLACE INTO country (code, name, data) VALUES (?, ?, ?)",
            (self.code, self.name, json.dumps(self.data)),
        )
