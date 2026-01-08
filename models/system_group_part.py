import json
from pydantic import BaseModel
from typing import Dict, Any
from db import Database

db = Database()


class SystemGroupPartModel(BaseModel):
    group_id: int
    is_parsed: int
    data: Dict[str, Any]

    @staticmethod
    def create_table():
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS system_group_part (
                group_id INTEGER PRIMARY KEY,
                is_parsed INTEGER DEFAULT 0 NOT NULL,
                data TEXT NOT NULL
            )
            """
        )

    @staticmethod
    def get_not_parsed(limit: int = 100) -> list:
        return db.fetchall(
            f"""
            SELECT * FROM system_group_part WHERE is_parsed = FALSE LIMIT {limit}
            """
        )

    @staticmethod
    def set_parsed(group_id):
        db.execute(
            f"UPDATE system_group_part SET is_parsed = 1 WHERE group_id={group_id}"
        )

    def save(self):
        db.execute(
            """
            INSERT OR REPLACE INTO system_group_part (group_id, data)
            VALUES (?, ?)
            """,
            (
                self.group_id,
                json.dumps(self.data),
            ),
        )
