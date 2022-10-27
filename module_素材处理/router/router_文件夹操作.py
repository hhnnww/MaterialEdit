import shutil
from pathlib import Path

import pythoncom
from PIL import Image
from fastapi import APIRouter
from pydantic import BaseModel

from module_素材处理.core import MaterialFolderStructure, MaterialFolderFunction
from module_素材处理.core.setting import AD_FILE_SUFFIX, IMAGE_FILE_SUFFIX, PIC_EDIT_IMG

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
            ma_func.fun_文件重命名(ma_path.material_path, 'test')
            ma_func.fun_文件重命名(ma_path.material_path, item_in.tb_name)

        case '复制到预览图':
            ma_func.fun_复制图片到指定目录(ma_path.material_path, ma_path.preview_path)

        case '复制到效果图':
            ma_func.fun_复制图片到指定目录(ma_path.material_path, ma_path.effect_path, rename=True)

        case '解压ZIP':
            ma_func.fun_解压ZIP(in_path=ma_path.material_path)

        # ------------------ 图片生成 ------------------

        case 'PSD删除广告-生成图片-添加广告':
            ma_func.fun_清空OUT_PATH()

            pythoncom.CoInitialize()
            for in_file in ma_func.fun_指定遍历(ma_path.material_path, ['.psd', '.psb']):
                ps_obj = ma_func.fun_PS操作.open(in_file.as_posix(), tb_name=item_in.tb_name,
                                                 ad_pic_list=ma_func.fun_PS广告图片())
                ps_obj.run_删广告_导出_加广告()
            pythoncom.CoUninitialize()

        case 'PSD生成图片-添加广告':
            pythoncom.CoInitialize()
            for in_file in ma_func.fun_指定遍历(ma_path.material_path, ['.psd', '.psb']):
                ps_obj = ma_func.fun_PS操作.open(in_file.as_posix(), tb_name=item_in.tb_name,
                                                 ad_pic_list=ma_func.fun_PS广告图片())
                ps_obj.run_导出_加广告()
            pythoncom.CoUninitialize()

        case 'PSD生成图片':
            pythoncom.CoInitialize()
            for in_file in ma_func.fun_指定遍历(ma_path.material_path, ['.psd', '.psb']):
                ps_obj = ma_func.fun_PS操作.open(in_file.as_posix(), tb_name=item_in.tb_name,
                                                 ad_pic_list=ma_func.fun_PS广告图片())
                ps_obj.run_导出()
            pythoncom.CoUninitialize()

        case 'AI导出图片':
            pythoncom.CoInitialize()
            for in_file in ma_func.fun_指定遍历(ma_path.material_path, ['.ai', '.eps']):
                ai_file = ma_func.fun_AI操作(file=in_file, tb_name=item_in.tb_name)
                ai_file.main()
            pythoncom.CoUninitialize()

        case 'PPT导出图片':
            for in_file in ma_func.fun_指定遍历(ma_path.material_path, ['.ppt', '.pptx']):
                ma_func.fun_PPT操作(ppt_path=in_file).main()

        # ------------------ 后续操作 ------------------

        case "素材图添加水印":
            water_pil = Image.open(
                (PIC_EDIT_IMG / item_in.tb_name / 'site_logo.png').as_posix()
            )
            water_pil.thumbnail((150, 150), 1)
            padding = 30
            for in_file in ma_func.fun_指定遍历(ma_path.material_path, IMAGE_FILE_SUFFIX):
                with Image.open(in_file.as_posix()) as im:
                    if 1500 not in im.size:
                        im.thumbnail((1500, 1500), 1)
                        top = im.height - water_pil.height - padding
                        im.paste(water_pil, (padding, top), water_pil)
                        im.save(in_file.as_posix())
                    else:
                        print('边距 1500 不添加')

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
