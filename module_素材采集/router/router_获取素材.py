from fastapi import APIRouter
from fastapi.responses import Response, RedirectResponse
from peewee import ModelSelect, ModelDelete
from pydantic import BaseModel
import re
from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import fun_获取MODEL, database

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


@router.post('/get_list')
def get_material_list(item_in: ItemIn):
    with database:
        model = fun_获取MODEL(tb_name=item_in.tb_name, site_name=item_in.site_name)
        query: ModelSelect = model.select().where(model.state == 0).paginate(item_in.page_num, 80)
        query = list(query.dicts())

        if item_in.site_name == '包图':
            for obj in query:
                obj['img'] = 'http://127.0.0.1:22702/get_material/img?img=' + obj['img']

    return query


@router.get('/get_material/{tb_name}/{site_name}/{material_id}')
def get_material(tb_name: str, site_name: str, material_id: int):
    with database:
        model = fun_获取MODEL(tb_name=tb_name, site_name=site_name)
        obj = model.get_by_id(pk=material_id)
        url = obj.url

        if site_name == '包图':
            ma_id = re.findall(r'/(\d+)\.html', url)
            if len(ma_id) > 0:
                url = 'https://ibaotu.com/?m=download&id=' + ma_id[0]

        elif site_name == '千图':
            ma_id = re.findall(r'/(\d+)\.html', url)
            if len(ma_id) > 0:
                url = f'https://dl.58pic.com/{ma_id[0]}.html'

        obj.state = 1
        obj.save()

    return RedirectResponse(url)


@router.get('/cut/{tb_name}/{site_name}/{material_id}')
def cut_material(tb_name: str, site_name: str, material_id: int):
    with database:
        model = fun_获取MODEL(tb_name=tb_name, site_name=site_name)
        query: ModelDelete = model.delete().where((model.state == 0) & (model.id <= material_id))
        query.execute()

    return 'ok'


@router.get('/clear_db/{tb_name}/{site_name}')
def clear_db(tb_name: str, site_name: str):
    with database:
        model = fun_获取MODEL(tb_name=tb_name, site_name=site_name)
        query: ModelDelete = model.delete().where(model.state == 0)
        query.execute()
    return 'ok'
