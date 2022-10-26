from dataclasses import asdict

from fastapi import APIRouter
from peewee import ModelSelect
from pydantic import BaseModel

from module_素材采集.core.class_包图 import SCBaoTu
from module_素材采集.core.model import fun_获取MODEL

router = APIRouter(prefix='/scrapy')


class ItemIn(BaseModel):
    url: str
    max_page: int
    cookie: str
    tb_name: str
    site_name: str


@router.post('/run')
def run_scrapy(item_in: ItemIn):
    model = fun_获取MODEL(tb_name=item_in.tb_name, site_name=item_in.site_name)

    all_material_list = None

    if item_in.site_name == '包图':
        all_material_list = SCBaoTu(start_url=item_in.url, max_page=item_in.max_page, cookie=item_in.cookie).main()

    for ma_obj in all_material_list:
        query: ModelSelect = model.select().where(model.hash == ma_obj.hash)
        count = query.count()

        if count == 0:
            res = model.create(
                **asdict(ma_obj)
            )
            print(res)
        else:
            print('素材存在，跳过。')

    return 'ok'
