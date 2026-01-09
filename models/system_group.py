import json
from pydantic import BaseModel
from typing import Dict, Any
from db import Database

db = Database()


class SystemGroupModel(BaseModel):
    id: int
    subcategory_id: int
    is_parsed: int
    name: str
    reference: str
    data: Dict[str, Any]

    @staticmethod
    def create_table():
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS system_group (
                id INTEGER PRIMARY KEY,
                subcategory_id INTEGER NOT NULL,
                is_parsed INTEGER NOT NULL DEFAULT 0,
                name TEXT NOT NULL,
                reference TEXT NOT NULL,
                data TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_system_group_subcategory_id
            ON system_group (subcategory_id)
            """
        )
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_system_group_reference
            ON system_group (reference)
            """
        )
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_system_group_is_parsed
            ON system_group (is_parsed)
            """
        )

    @staticmethod
    def get_for_image():
        return db.fetchall("SELECT sg.reference, sg.data FROM system_group sg")

    @staticmethod
    def get_not_parsed(limit: int = 1000):
        return db.fetchall(
            f"""
            SELECT
                sg.id         AS group_id,
                sg.reference  AS group_reference,
                sub.reference AS sub_reference,
                cat.reference AS category_reference,
                c.reference   AS catalog_reference
            FROM system_group sg
            JOIN subcategory sub ON sg.subcategory_id = sub.id
            JOIN category cat ON sub.category_id = cat.id
            JOIN catalog c ON cat.catalog_id = c.id
            WHERE sg.id > 0
            AND (sg.is_parsed = 0 OR sg.is_parsed IS NULL)
            LIMIT {limit}
            """
        )

    @staticmethod
    def set_parsed(group_id):
        db.execute(f"UPDATE system_group SET is_parsed = 1 WHERE id={group_id}")

    def save(self):
        db.execute(
            """
            INSERT OR REPLACE INTO system_group (id, subcategory_id, name, reference, data)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                self.id,
                self.subcategory_id,
                self.name,
                self.reference,
                json.dumps(self.data),
            ),
        )
