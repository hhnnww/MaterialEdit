from dataclasses import asdict
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from module_素材采集.core.class_包图 import SCBaoTu
from module_素材采集.core.class_千图 import SCQianTu
from module_素材采集.core.class_千库 import SCQianKu
from module_素材采集.core.class_摄图 import SCSheTu
from module_素材采集.core.model import fun_获取MODEL, database

router = APIRouter(prefix='/scrapy')


class ItemIn(BaseModel):
    url: str
    max_page: int
    cookie: str
    tb_name: str
    site_name: str


@router.post('/run')
def run_scrapy(item_in: ItemIn):
    with database:
        model = fun_获取MODEL(tb_name=item_in.tb_name, site_name=item_in.site_name)

        all_material_list = None

        if item_in.site_name == '包图':
            all_material_list = SCBaoTu(start_url=item_in.url, max_page=item_in.max_page, cookie=item_in.cookie).main()
        elif item_in.site_name == '千图':
            all_material_list = SCQianTu(start_url=item_in.url, max_page=item_in.max_page, cookie=item_in.cookie).main()
        elif item_in.site_name == '摄图':
            all_material_list = SCSheTu(start_url=item_in.url, max_page=item_in.max_page, cookie=item_in.cookie).main()
        elif item_in.site_name == '千库':
            all_material_list = SCQianKu(start_url=item_in.url, max_page=item_in.max_page, cookie=item_in.cookie).main()

        for ma_obj in all_material_list:
            count = model.select().where(model.hash == ma_obj.hash).count()
            if count == 0:
                res = model.create(
                    **asdict(ma_obj)
                )
                print(res)
            else:
                print('素材存在，跳过。')

    return 'ok'


@router.get('/down_path_cate')
def down_path_cate(down_path: str):
    down_path = Path(down_path)

    file_list = []
    for in_file in down_path.iterdir():
        if in_file.is_file():
            file_list.append(in_file)

    if len(file_list) > 0:
        new_path = down_path / '新建文件夹'

        num = 1
        while new_path.exists() is True:
            new_path = down_path / f'新建文件夹 ({num})'
            num += 1

        new_path.mkdir()

        for in_file in file_list:
            new_name = new_path / in_file.name
            if new_name.exists() is False:
                in_file.rename(new_name)

    return '归类完成 OK'
