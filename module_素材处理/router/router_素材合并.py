from fastapi import APIRouter
from pydantic import BaseModel


class StoreType(BaseModel):
    tb_name: str
    dst_path: str
    ori_path: str


router = APIRouter(prefix='/material_merge')


@router.post('/merge')
def material_merge(item_in: StoreType):
    pass
