from fastapi import APIRouter
from fastapi.responses import Response
from peewee import ModelSelect
from pydantic import BaseModel

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import fun_获取MODEL

router = APIRouter(prefix='/get_material')


class ItemIn(BaseModel):
    tb_name: str
    site_name: str
    page_num: int


@router.get('/img')
def get_img(img: str):
    try:
        res = Response(HTMLDown(img, use_proxy=False).content)
    except:
        return Response()

    return res


@router.post('/get')
def get_material(item_in: ItemIn):
    model = fun_获取MODEL(tb_name=item_in.tb_name, site_name=item_in.site_name)
    query: ModelSelect = model.select().where(model.state == 0)
    query = query.paginate(item_in.page_num, 80)
    query = list(query.dicts())

    if item_in.site_name == '包图':
        for obj in query:
            obj['img'] = 'http://127.0.0.1:22702/get_material/img?img=' + obj['img']

    return query
