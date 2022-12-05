from dataclasses import dataclass

from peewee import *

database = MySQLDatabase('ftdesign', user='root', password='', host='192.168.0.101', port=3306)


class BaseModel(Model):
    class Meta:
        database = database


class MaterialList(BaseModel):
    url = CharField(max_length=512, unique=True)
    img = CharField(max_length=512, unique=True)
    state = IntegerField(default=0)

    hash = CharField(max_length=512, unique=True)


@dataclass
class MaterialType:
    url: str
    img: str
    hash: str


def fun_获取MODEL(tb_name: str, site_name: str) -> MaterialList:
    obj: MaterialList = type(tb_name + '-' + site_name, (MaterialList,), {})
    if obj.table_exists() is False:
        obj.create_table()

    return obj


__all__ = ['fun_获取MODEL', 'MaterialType', 'database']

if __name__ == '__main__':
    database.connect()
    print(database.is_closed())

    database.close()
    print(database.is_closed())

    model = fun_获取MODEL('饭桶设计', '包图')
    print(model.table_exists())
