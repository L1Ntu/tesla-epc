import json
from pydantic import BaseModel
from typing import Dict, Any
from db import Database

db = Database()


class SubcategoryModel(BaseModel):
    id: int
    category_id: int
    name: str
    reference: str
    data: Dict[str, Any]

    @staticmethod
    def create_table():
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS subcategory (
                id INTEGER PRIMARY KEY,
                category_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                reference TEXT NOT NULL,
                data TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_subcategory_catalog_id
            ON subcategory (category_id)
            """
        )
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_subcategory_reference
            ON subcategory (reference)
            """
        )

    def save(self):
        db.execute(
            """
            INSERT OR REPLACE INTO subcategory (id, category_id, name, reference, data)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                self.id,
                self.category_id,
                self.name,
                self.reference,
                json.dumps(self.data),
            ),
        )
