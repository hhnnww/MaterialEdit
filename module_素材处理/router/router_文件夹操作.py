from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from module_素材处理.router.class_文件夹功能 import MaterialPathAction

router = APIRouter(prefix='/MaterialFolder')


class ItemIn(BaseModel):
    root_path: str
    tb_name: str
    action_name: str


@router.get('/del_img')
def del_img(img: str):
    img_path = Path(img)
    if img_path.exists() is True:
        img_path.unlink()

    return 'success'


@router.post('/Function')
def material_folder_function(item_in: ItemIn):
    print(item_in)
    ma = MaterialPathAction(item_in)

    match item_in.action_name:

        # ------------------ 基础操作 ------------------

        case "移动到根目录":
            ma.fun_移动到根目录()

        case "删除广告文件":
            ma.fun_删除广告文件()

        case "文件重命名":
            ma.fun_文件重命名()

        case '复制到预览图':
            ma.fun_复制到预览图()

        case '复制到效果图':
            ma.fun_复制到效果图()

        case '解压ZIP':
            ma.fun_解压ZIP()

        case "删除相同文件":
            ma.fun_删除相同文件()

        case "字体文件重命名":
            ma.fun_字体重命名()

        case "按格式分类":
            ma.fun_按格式分类()

        case "字体导出PNG":
            ma.fun_字体生成图片()

        # ------------------ 图片生成 ------------------

        case 'PSD删除广告-生成图片-添加广告':
            ma.fun_PSD删广告生成图片()

        case 'PSD生成图片-添加广告':
            ma.fun_PSD添加广告生成图片()

        case 'PSD生成图片':
            ma.fun_PSD生成图片()

        case 'AI导出图片':
            ma.fun_AI导出图片()

        case 'PPT导出图片':
            ma.fun_PPT导出图片()

        # ------------------ 后续操作 ------------------
        case "删除图片边框":
            ma.fun_删除图片边框()

        case "素材图添加水印":
            ma.fun_素材图片添加水印()

        # ------------------ 删除图片 ------------------

        case '删除所有':
            ma.fun_删除所有()

        case '删除素材内所有图片':
            ma.fun_删除素材图片()

        case "删除效果图":
            ma.fun_删除效果图()

        case "删除所有EPS":
            ma.fun_删除所有EPS()

        case "删除预览图":
            ma.fun_删除预览图()

        # ------------------ 一键全自动操作 ------------------
        case "全自动一键操作":
            ma.fun_全自动一键操作()

    return dict(mess='OK')
