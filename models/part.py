import json
from pydantic import BaseModel
from typing import Dict, Any
from db import Database

db = Database()


class PartModel(BaseModel):
    id: int
    part_number: str
    catalog_number: str
    name: str

    @staticmethod
    def create_table():
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS part (
                id INTEGER PRIMARY KEY NOT NULL,
                part_number TEXT NOT NULL ,
                catalog_number TEXT NOT NULL ,
                name TEXT
            )
            """
        )

    @staticmethod
    def isset_part(id: int) -> bool:
        data = db.fetchone(f"SELECT * FROM part WHERE id = {id}")
        if data is None:
            return False
        return True

    def save(self):
        db.execute(
            """
            INSERT OR REPLACE INTO part (id, part_number, catalog_number, name)
            VALUES (?, ?, ?, ?)
            """,
            (self.id, self.part_number, self.catalog_number, self.name),
        )
