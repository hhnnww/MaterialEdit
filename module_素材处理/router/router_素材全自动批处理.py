from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from module_素材处理.router.class_文件夹功能 import ItemIn
from module_素材处理.router.class_文件夹功能 import MaterialPathAction

router = APIRouter(prefix='/material_all_auto_edit', tags=['全自动批处理'])


def get_path_num(in_path: Path):
    stem = in_path.stem
    return int(stem)


def get_all_path(in_path: Path):
    start_stem = get_path_num(in_path)

    for in_path in in_path.parent.iterdir():
        if in_path.is_dir() and get_path_num(in_path) >= start_stem:
            yield in_path


class ItemRouterIn(BaseModel):
    tb_name: str
    start_path: str


@router.post('')
def fun_素材全自动批处理(item_in: ItemRouterIn):
    start_path = Path(item_in.start_path)
    tb_name = item_in.tb_name

    for in_path in get_all_path(in_path=start_path):
        print(f'处理 \t {in_path.as_posix()}')
        item_in = ItemIn(
            root_path=in_path.as_posix(),
            tb_name=tb_name,
            action_name='全自动'
        )

        mac = MaterialPathAction(item_in=item_in)
        mac.fun_全自动一键操作()
