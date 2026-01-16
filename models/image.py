from pydantic import BaseModel
from db import Database

db = Database()


class ImageModel(BaseModel):
    entity: str
    uuid: str
    uuid_link: str
    ext: str
    mimetype: str
    hash: str
    size: int
    name: str

    @staticmethod
    def create_table():
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS image
            (
                entity    TEXT NOT NULL,
                uuid      TEXT NOT NULL,
                uuid_link TEXT NOT NULL,
                ext       TEXT NOT NULL,
                mimetype  TEXT NOT NULL,
                hash      TEXT NOT NULL,
                size      INT  NOT NULL,
                name      TEXT NOT NULL,
                PRIMARY KEY (entity, uuid, ext)
            )
            """
        )

        db.execute("CREATE INDEX IF NOT EXISTS image_entity_hash ON image (entity, hash)")

    @staticmethod
    def get_image(entity, uuid, ext):
        sql = """
            SELECT
                i.entity                      AS entity,
                IIF(il.name, il.name, i.name) AS name
            FROM image i
            LEFT JOIN image il ON il.entity = i.entity AND il.uuid = i.uuid_link
            WHERE i.entity = ?
              AND i.uuid = ?
        """
        params = (entity, uuid)
        if ext:
            sql += "AND i.ext = ?"
            params = (entity, uuid, ext)

        return db.fetchone(sql, params)

    @staticmethod
    def exist_image(entity, uuid, ext):
        if ext:
            sql = "SELECT * FROM image WHERE entity = ? AND uuid = ? AND ext = ?"
            params = (entity, uuid, ext)
        else:
            sql = "SELECT * FROM image WHERE entity = ? AND uuid = ?"
            params = (entity, uuid)

        data = db.fetchone(sql, params)
        return True if data else False

    @staticmethod
    def get_by_hash(entity, hash, mimetype):
        return db.fetchone(
            """
            SELECT *
            FROM image
            WHERE
                entity = ?
                AND hash = ?
                AND mimetype = ?
                AND uuid_link = ''
            """,
            (entity, hash, mimetype)
        )

    def save(self):
        db.execute(
            """
            INSERT OR REPLACE INTO image (entity, uuid, uuid_link, ext, mimetype, hash, size, name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (self.entity, self.uuid, self.uuid_link, self.ext, self.mimetype, self.hash, self.size, self.name),
        )
