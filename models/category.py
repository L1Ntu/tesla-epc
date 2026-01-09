import json
from pydantic import BaseModel
from typing import Dict, Any
from db import Database

db = Database()


class CategoryModel(BaseModel):
    id: int
    catalog_id: int
    name: str
    reference: str
    image: str
    data: Dict[str, Any]

    @staticmethod
    def create_table():
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY,
                catalog_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                reference TEXT NOT NULL,
                image TEXT,
                data TEXT
            )
            """
        )
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_category_catalog_id
            ON category (catalog_id)
            """
        )
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_category_reference
            ON category (reference)
            """
        )

    @staticmethod
    def get_for_image():
        return db.fetchall("SELECT reference, image FROM category")

    def save(self):
        db.execute(
            """
            INSERT OR REPLACE INTO category (id, catalog_id, name, reference, image, data)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                self.id,
                self.catalog_id,
                self.name,
                self.reference,
                self.image,
                json.dumps(self.data),
            ),
        )
