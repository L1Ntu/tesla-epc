from pydantic import BaseModel
from db import Database

db = Database()


class ImageModel(BaseModel):
    entity: str
    uuid: str
    ext: str
    mimetype: str
    size: int
    name: str

    @staticmethod
    def create_table():
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS image
            (
                entity   TEXT NOT NULL,
                uuid     TEXT NOT NULL,
                ext      TEXT NOT NULL,
                mimetype TEXT NOT NULL,
                size     INT  NOT NULL,
                name     TEXT NOT NULL,
                PRIMARY KEY (entity, uuid, ext)
            )
            """
        )

    def save(self):
        db.execute(
            """
            INSERT OR REPLACE INTO image (entity, uuid, ext, mimetype, size, name)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (self.entity, self.uuid, self.ext, self.mimetype, self.size, self.name),
        )
