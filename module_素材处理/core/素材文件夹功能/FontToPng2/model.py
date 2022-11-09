from peewee import *
from pathlib import Path

db_path = Path(__file__).parent / 'db.db'
database = SqliteDatabase(db_path.as_posix())


class BaseModel(Model):
    class Meta:
        database = database


class CiDian(BaseModel):
    ci = CharField(max_length=128, unique=True)


class ChengYu(BaseModel):
    ci = CharField(max_length=128, unique=True)


if __name__ == '__main__':
    with database:
        CiDian.create_table()
        ChengYu.create_table()
