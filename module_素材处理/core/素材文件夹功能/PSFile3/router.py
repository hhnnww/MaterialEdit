from typing import Optional
from typing import Union

from fastapi import APIRouter
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from .model import IncludeName
from .model import IsName
from .model import IsPhoto
from .model import TextReplaceName
from .model import database

from typing import Literal

router = APIRouter(prefix='/广告语管理', tags=['PS文件广告关键词管理'])


class ItemIn(BaseModel):
    model_name: str
    id: Optional[int]
    name: Optional[str]
    ori_name: Optional[str]
    dst_name: Optional[str]


model_name_literal = Literal["is_name", "include_name", "text_replace_name", "is_photo"]


def get_model(model_name: model_name_literal) -> Union[IncludeName, IsName, TextReplaceName]:
    if model_name == 'include_name':
        return IncludeName
    elif model_name == 'is_name':
        return IsName
    elif model_name == 'text_replace_name':
        return TextReplaceName
    elif model_name == 'is_photo':
        return IsPhoto


@router.get('/get_all_item/{model_name}')
def get_all_item(model_name: str):
    res = []
    model = get_model(model_name)
    with database:
        for in_item in model.select():
            res.append(
                model_to_dict(in_item)
            )
    return res


@router.post('/new_item')
def new_item(item_in: ItemIn):
    model = get_model(item_in.model_name)
    item_in.id = None
    with database:
        model.create(
            **item_in.dict()
        )
    return "OK"


@router.post('/del_item')
def del_item(item_in: ItemIn):
    model = get_model(item_in.model_name)
    with database:
        obj = model.get_by_id(pk=item_in.id)
        obj.delete_instance()

    return "OK"
