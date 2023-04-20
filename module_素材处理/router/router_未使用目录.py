from fastapi import APIRouter
from pydantic import BaseModel

from module_素材处理.core.素材文件夹信息.fun_未使用的目录 import UnUsedPathDir

router = APIRouter(tags=['未使用的目录'])


class ItemIn(BaseModel):
    in_path: str


@router.post('/un-used-path-dir')
def unused_path_dir(item_in: ItemIn):
    upd = UnUsedPathDir(item_in.in_path)
    return list(upd.main())
