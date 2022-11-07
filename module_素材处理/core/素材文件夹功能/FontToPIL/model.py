from peewee import *

database = SqliteDatabase('./db.db')


class BaseModel(Model):
    class Meta:
        database = database


class Page(BaseModel):
    url = CharField(max_length=512, unique=True)
    state = IntegerField(default=0)


class Single(BaseModel):
    url = CharField(max_length=512, unique=True)
    state = IntegerField(default=0)


class Content(BaseModel):
    single = CharField(max_length=512, unique=True)


if __name__ == '__main__':
    with database:
        database.create_tables(
            [Page, Single, Content]
        )
