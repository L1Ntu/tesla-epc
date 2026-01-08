from pydantic import BaseModel
from db import Database

db = Database()


class PartImageModel(BaseModel):
    part_id: int
    is_parsed: int
    uuid: str
    url: str

    @staticmethod
    def create_table():
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS part_image (
                part_id INTEGER PRIMARY KEY NOT NULL,
                is_parsed INTEGER NOT NULL DEFAULT 0,
                uuid TEXT NOT NULL ,
                url TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_part_image_is_parsed
            ON part_image (is_parsed)
            """
        )

    def save(self):
        db.execute(
            """
            INSERT OR REPLACE INTO part_image (part_id, uuid, url)
            VALUES (?, ?, ?)
            """,
            (self.part_id, self.uuid, self.url),
        )
