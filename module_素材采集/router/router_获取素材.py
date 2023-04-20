import math
import re

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.responses import Response
from peewee import ModelDelete
from peewee import ModelSelect
from pydantic import BaseModel

from module_素材采集.core.class_envato_素材图片下载 import SCEnvatoPICDown
from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import fun_获取MODEL

router = APIRouter(prefix='/get_material', tags=['获取素材'])


class ItemIn(BaseModel):
    tb_name: str
    site_name: str
    page_num: int


@router.get('/img')
def get_img(img: str):
    # 获取图片
    try:
        res = Response(HTMLDown(img, use_proxy=False).content)
    except:
        return Response()

    return res


@router.post('/get_list')
def get_material_list(item_in: ItemIn):
    """
    获取素材列表
    :param item_in:
    :return:
    """

    single_pate_material_num = 160

    model = fun_获取MODEL(tb_name=item_in.tb_name, site_name=item_in.site_name)
    query: ModelSelect = model.select().where(model.state == 0)
    ma_list = query.paginate(item_in.page_num, single_pate_material_num)
    ma_list = list(ma_list.dicts())

    if item_in.site_name == '包图':
        for obj in ma_list:
            obj['img'] = 'http://127.0.0.1:22702/get_material/img?img=' + obj['img']

    resp_dict = {
        'material_list': ma_list,
        'count':         query.count(),
        'all_page':      math.ceil(query.count() / single_pate_material_num)
    }

    return resp_dict


@router.get('/get_material/{tb_name}/{site_name}/{material_id}')
def get_material(tb_name: str, site_name: str, material_id: int):
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

    elif site_name == 'envato':
        SCEnvatoPICDown(url).main()

    elif site_name == 'allfreedown':
        # https://all-free-download.com/free-vector/download/christmas_seamless_pattern_template_illusive_snowflakes_shapes_decor_elegant_design_6928013.html
        # https://files.all-free-download.com/free_download_graphic_6928013.html
        sc_id = re.findall(r'_(\d+)?\.html', url)[0]
        url = f'https://files.all-free-download.com/free_download_graphic_{sc_id}.html'

    obj.state = 1
    obj.save()

    return RedirectResponse(url)


@router.get('/cut/{tb_name}/{site_name}/{material_id}')
def cut_material(tb_name: str, site_name: str, material_id: int):
    model = fun_获取MODEL(tb_name=tb_name, site_name=site_name)
    query: ModelDelete = model.delete().where((model.state == 0) & (model.id <= material_id))
    query.execute()

    return 'ok'


@router.get('/clear_db/{tb_name}/{site_name}')
def clear_db(tb_name: str, site_name: str):
    model = fun_获取MODEL(tb_name=tb_name, site_name=site_name)
    query: ModelDelete = model.delete().where(model.state == 0)
    query.execute()

    return 'ok'


@router.post('/get_already_downloaded')
def get_already_downloaded(item_in: ItemIn):
    """
    获取已经下载了的素材
    :param item_in:
    :return:
    """
    model = fun_获取MODEL(tb_name=item_in.tb_name, site_name=item_in.site_name)
    query: ModelSelect = model.select().where(model.state == 1).order_by(model.id.desc()).paginate(item_in.page_num,
                                                                                                   120)
    query = list(query.dicts())

    if item_in.site_name == '包图':
        for obj in query:
            obj['img'] = 'http://127.0.0.1:22702/get_material/img?img=' + obj['img']

    resp_dict = {
        'material_list': query,
    }

    return resp_dict
