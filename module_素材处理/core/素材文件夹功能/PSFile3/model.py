from pathlib import Path

from peewee import CharField
from peewee import Model
from peewee import SqliteDatabase

db_path = Path(__file__).parent / 'db.db'
database = SqliteDatabase(db_path.as_posix())


class BaseModel(Model):
    class Meta:
        database = database


class IncludeName(BaseModel):
    name = CharField(unique=True)


class IsName(BaseModel):
    name = CharField(unique=True)


class IsPhoto(BaseModel):
    name = CharField(unique=True)


class TextReplaceName(BaseModel):
    ori_name = CharField()
    dst_name = CharField()


if __name__ == '__main__':
    database.create_tables(
        [IncludeName, IsName, TextReplaceName, IsPhoto]
    )
