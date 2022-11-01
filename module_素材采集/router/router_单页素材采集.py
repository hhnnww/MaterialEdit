from fastapi import APIRouter
from pydantic import BaseModel

from module_素材采集.core.class_单页直接采集 import SCSinglePage
from module_素材采集.core.model import fun_获取MODEL

router = APIRouter()


class ItemIn(BaseModel):
    body: str
    url: str


@router.post('/sing_page_scrapy')
def single_page_scrapy(item_in: ItemIn):
    all_post = SCSinglePage(html=item_in.body, url=item_in.url).main()

    site_name = ''
    if '58pic.com' in item_in.url:
        site_name = '千图'
    elif 'ibaotu.com' in item_in.url:
        site_name = '包图'
    elif '588ku.com' in item_in.url:
        site_name = '千库'
        
    model = fun_获取MODEL(tb_name='小夕素材', site_name=site_name)

    for ma in all_post:
        count = model.select().where(model.hash == ma.hash).count()
        if count == 0:
            obj = model.create(
                img=ma.img,
                url=ma.url,
                hash=ma.hash
            )
            print(obj)
        else:
            print(f'素材存在，不采集。')
