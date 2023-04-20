from dataclasses import asdict

from fastapi import APIRouter
from pydantic import BaseModel

from mod_文件夹分类.class_FolderCategory import FolderCategory
from mod_文件夹分类.class_FolderCategory import MaterialOBJ
from pprint import pprint

router = APIRouter(prefix='/folder_category', tags=['文件夹分类'])


class ItemIn(BaseModel):
    action: str

    # 素材路径
    root_path: str
    material_path: str
    preview_path: str

    # 新建文件夹
    new_category_stem: str

    # 移动素材列表
    in_folder_path: str
    in_preview_path: str
    move_material_list: list


@router.post('/')
def action(item_in: ItemIn):
    pprint(item_in)

    fc = FolderCategory(root_path=item_in.root_path)

    if item_in.action == '获取素材文件夹信息':
        return dict(root_path=fc.root_path.as_posix(), material_path=fc.material_path.as_posix(),
                    preview_path=fc.preview_path.as_posix())

    elif item_in.action == '获取所有文件夹':
        return [asdict(obj) for obj in fc.all_folder()]

    elif item_in.action == '获取所有文件':
        return [asdict(obj) for obj in fc.all_material_obj()]

    elif item_in.action == '新建文件夹':
        fc.new_folder(item_in.new_category_stem)
        return 'ok'

    elif item_in.action == '移动到文件夹':
        fc.move_material_to_folder(folder_path=item_in.in_folder_path, preview_path=item_in.preview_path,
                                   material_list=[MaterialOBJ(**obj) for obj in item_in.move_material_list])
        return 'ok'
