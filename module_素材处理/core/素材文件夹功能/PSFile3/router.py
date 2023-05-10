from fastapi import APIRouter
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from .model import IncludeName
from .model import IsName
from .model import database, TextReplaceName

router = APIRouter(prefix='/广告语管理', tags=['PS文件广告关键词管理'])


class LayerName(BaseModel):
    name: str


# ------------------ 包含关键词 ------------------


@router.get('/all_include_name')
def all_include_name():
    res = []
    with database:
        for in_item in IncludeName.select():
            res.append(model_to_dict(in_item))

    return res


@router.post('/new_include_name')
def new_include_name(item_in: LayerName):
    with database:
        IncludeName.create(name=item_in.name)

    return 'OK'


@router.post('/del_include_name')
def del_include_name(item_in: LayerName):
    with database:
        obj: IncludeName = IncludeName.select().where(IncludeName.name == item_in.name).first()
        obj.delete_instance()

    return "OK"


# ------------------ 等于关键词 ------------------

@router.get('/all_is_name')
def all_is_name():
    res = []
    with database:
        for in_item in IsName.select():
            res.append(model_to_dict(in_item))

    return res


@router.post('/new_is_name')
def new_is_name(item_in: LayerName):
    with database:
        IsName.create(name=item_in.name)

    return "OK"


@router.post('/del_is_name')
def del_is_name(item_in: LayerName):
    with database:
        obj: IsName = IsName.select().where(IsName.name == item_in.name).first()
        obj.delete_instance()

    return "OK"


# ------------------ 替换关键词 ------------------

class TextReplaceType(BaseModel):
    ori_name: str
    dst_name: str


@router.get('/all_text_replace')
def all_text_replace():
    res = []
    with database:
        for in_item in TextReplaceName.select():
            res.append(model_to_dict(in_item))

    return res


@router.post('/new_text_replace')
def new_text_replace(item_in: TextReplaceType):
    with database:
        TextReplaceName.create(
            ori_name=item_in.ori_name,
            dst_name=item_in.dst_name
        )
    return "OK"


@router.post("/del_text_replace")
def del_text_replace(item_in: TextReplaceType):
    with database:
        obj: TextReplaceName = TextReplaceName.select().where(
            (TextReplaceName.ori_name == item_in.ori_name) & (TextReplaceName.dst_name == item_in.dst_name)
        ).first()

        obj.delete_instance()

    return "OK"
