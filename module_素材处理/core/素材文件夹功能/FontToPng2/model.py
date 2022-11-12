from pathlib import Path

from peewee import *

db_path = Path(__file__).parent / 'db.db'
database = SqliteDatabase(db_path.as_posix())


class BaseModel(Model):
    class Meta:
        database = database


class CiDian(BaseModel):
    ci = CharField(max_length=128, unique=True)


class ChengYu(CiDian):
    pass


class TangShi(ChengYu):
    pass


if __name__ == '__main__':
    with database:
        CiDian.create_table()
        ChengYu.create_table()
