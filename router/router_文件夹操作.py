import shutil

from fastapi import APIRouter
from pydantic import BaseModel

from core import MaterialFolderStructure, MaterialFolderFunction
from core.setting import AD_FILE_SUFFIX, IMAGE_FILE_SUFFIX

router = APIRouter(prefix='/MaterialFolder')


class ItemIn(BaseModel):
    root_path: str
    tb_name: str
    action_name: str


@router.post('/Function')
def material_folder_function(item_in: ItemIn):
    print(item_in)

    ma_path = MaterialFolderStructure(root_path=item_in.root_path)
    ma_func = MaterialFolderFunction
    content = ''

    match item_in.action_name:

        # ------------------ 基础操作 ------------------

        case "移动到根目录":
            ma_func.fun_移动到根目录(ma_path.material_path)

        case "删除广告文件":
            for in_file in ma_func.fun_指定遍历(ma_path.material_path, AD_FILE_SUFFIX):
                in_file.unlink()

        case "文件重命名":
            ma_func.fun_文件重命名(ma_path.material_path, '')
            ma_func.fun_文件重命名(ma_path.material_path, item_in.tb_name)

        case '复制到预览图':
            ma_func.fun_复制图片到指定目录(ma_path.material_path, ma_path.preview_path)

        case '复制到效果图':
            ma_func.fun_复制图片到指定目录(ma_path.material_path, ma_path.effect_path, rename=True)

        case '解压ZIP':
            ma_func.fun_解压ZIP(in_path=ma_path.material_path)

        # ------------------ 图片生成 ------------------

        case 'PSD删除广告-生成图片-添加广告':
            # TODO: 添加PSD文件处理
            pass

        case 'PSD生成图片-添加广告':
            pass

        case 'PSD生成图片':
            pass

        # ------------------ 删除图片 ------------------

        case '删除所有':
            shutil.rmtree(ma_path.root_path)

        case '删除素材内所有图片':
            for in_file in ma_func.fun_指定遍历(ma_path.material_path, IMAGE_FILE_SUFFIX):
                in_file.unlink()

        case "删除效果图":
            if ma_path.effect_path.exists() is True:
                shutil.rmtree(ma_path.effect_path)

        case "删除预览图":
            if ma_path.preview_path.exists() is True:
                shutil.rmtree(ma_path.preview_path)

    return dict(mess='OK', content=content)
