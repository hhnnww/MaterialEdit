from fastapi import APIRouter
from pydantic import BaseModel

from module_素材采集.core.class_下载目录移动到素材目录 import SCDownPathMoveMaterialPath

router = APIRouter(prefix='/down_path_move_material_path', tags=['下载目录移动到素材目录'])


class MoveType(BaseModel):
    tb_name: str
    down_path: str
    material_path: str


@router.post('/move')
def move(item_in: MoveType):
    SCDownPathMoveMaterialPath(
        tb_name=item_in.tb_name,
        down_path=item_in.down_path,
        material_path=item_in.material_path
    ).main()
