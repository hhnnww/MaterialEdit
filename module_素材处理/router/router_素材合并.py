from fastapi import APIRouter
from pydantic import BaseModel
from module_素材处理.router.class_文件夹合并 import MaterialDirMerge


class StoreType(BaseModel):
    tb_name: str
    dst_path: str
    ori_path: str


router = APIRouter(prefix='/material_merge')


@router.post('/merge')
def material_merge(item_in: StoreType):
    md = MaterialDirMerge(
        ori_path=item_in.ori_path,
        dst_path=item_in.dst_path,
        tb_name=item_in.tb_name
    )
    md.main()

    return 'OK'
