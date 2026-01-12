from pydantic import BaseModel
from db import Database

db = Database()


class ImageLinkModel(BaseModel):
    entity: str
    mimetype: str
    hash: str
    uuid_org: str
    uuid_link: str

    @staticmethod
    def create_table():
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS image_link (
                entity TEXT NOT NULL,
                mimetype TEXT NOT NULL,
                hash TEXT NOT NULL,
                uuid_org TEXT NOT NULL,
                uuid_link TEXT NOT NULL,
                PRIMARY KEY (entity, mimetype, hash, uuid_org)
            )
            """
        )

        db.execute("CREATE INDEX IF NOT EXISTS image_link_uuid_org ON image_link (entity, uuid_org)")

    @staticmethod
    def isset_image_hash(entity, sha1_hash) -> str | bool:
        result = db.fetchone(
            """
            SELECT uuid_org
            FROM image_link
            WHERE entity = ?
              AND hash = ?
              AND uuid_org = uuid_link
            LIMIT 1
            """,
            (entity, sha1_hash)
        )

        if result:
            return result["uuid_org"]
        return False

    @staticmethod
    def isset_image_uuid(entity, uuid, mimetype = None) -> bool:
        if mimetype:
            sql = "SELECT * FROM image_link WHERE entity = ? AND uuid_org = ? AND mimetype = ?"
            params = (entity, uuid, mimetype)
        else:
            sql = "SELECT * FROM image_link WHERE entity = ? AND uuid_org = ?"
            params = (entity, uuid)

        result = db.fetchone(sql, params)

        if result:
            return True
        return False

    def save(self):
        db.execute(
            """
            INSERT OR REPLACE INTO image_link (entity, mimetype, hash, uuid_org, uuid_link)
            VALUES (?, ?, ?, ?, ?)
            """,
            (self.entity, self.mimetype, self.hash, self.uuid_org, self.uuid_link),
        )
