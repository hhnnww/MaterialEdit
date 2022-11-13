import io
import os

from PIL import Image
from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel

from module_素材处理.core.素材文件夹信息 import MaterialInfo
from module_素材处理.core.素材文件夹功能 import MaterialFolderStructure

router = APIRouter(prefix='/GetMaterialInfo')


class ItemIn(BaseModel):
    root_path: str


class OutModel(BaseModel):
    素材ID: str
    素材格式: str
    源文件数量: int
    源文件列表: str
    源文件大小: str

    prev_path: dict
    next_path: dict

    预览图列表: list
    效果图列表: list

    素材格式标题: str


@router.post('/base_info')
def get_base_info(item_in: ItemIn) -> OutModel:
    mfs = MaterialFolderStructure(root_path=item_in.root_path)
    os.startfile(mfs.material_path.as_posix())

    mi = MaterialInfo(in_path=mfs.material_path)

    om = OutModel(
        素材ID=mfs.root_path.stem,
        素材格式=' '.join(mi.pro_素材格式),
        源文件数量=len(mi.all_material_file),
        源文件列表=mi.pro_源文件列表,
        源文件大小=mi.pro_文件夹尺寸,

        prev_path=mfs.prev_path,
        next_path=mfs.next_path,

        预览图列表=mfs.preview_img_list,
        效果图列表=mfs.effect_img_list,

        素材格式标题=mi.pro_素材格式标题
    )

    return om


@router.get('/img_blob')
def get_img_blob(img: str):
    byte_io = io.BytesIO()
    with Image.open(img) as im:
        im.thumbnail((500, 500), 1)
        im.save(byte_io, format='png')

    return Response(byte_io.getvalue(), media_type=f'image/png')
