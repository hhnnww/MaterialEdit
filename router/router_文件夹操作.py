from fastapi import APIRouter
from pydantic import BaseModel

from core import MaterialFolderStructure

router = APIRouter(prefix='/MaterialFOlder')


class ItemIn(BaseModel):
    root_path: str
    tb_name: str
    action_name: str


@router.post('/Function')
def material_folder_function(item_in: ItemIn):
    mafs = MaterialFolderStructure(root_path=item_in.root_path)
