from pathlib import Path
from tqdm import tqdm
from PIL import Image
from fastapi import APIRouter
from pydantic import BaseModel

from module_素材处理.core.setting import IMAGE_FILE_SUFFIX
from module_素材处理.core.setting import UP_FOLDER
from module_素材处理.core.制作详情 import XQInfoPic
from module_素材处理.core.制作详情 import XQMakePIC
from module_素材处理.core.制作详情 import XQTitlePic
from module_素材处理.core.素材文件夹功能 import MaterialFolderFunction
from module_素材处理.core.素材文件夹功能 import MaterialFolderStructure

router = APIRouter(prefix='/make_xq')


class ItemIn(BaseModel):
    root_path: str
    tb_name: str
    单排图片数量: int
    素材ID: str
    素材格式: str
    源文件列表: str
    源文件大小: str

    制作效果图: bool
    制作预览图: bool

    详情使用图片: str
    img_list: list
    详情水印: bool

    详情素材信息: bool
    详情使用图片数量: int
    详情使用图片排序: bool


@router.post('/make_xq')
def make_xq(item_in: ItemIn):
    print(item_in)
    mfs = MaterialFolderStructure(root_path=item_in.root_path)
    mff = MaterialFolderFunction

    for in_file in UP_FOLDER.iterdir():
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_FILE_SUFFIX:
            if 'xq_' in in_file.stem:
                in_file.unlink()

    # 制作数据图
    info_pil = XQInfoPic(
        text_list=[
            ('素材ID', item_in.素材ID),
            ('素材格式', item_in.素材格式),
            ('素材数量', item_in.源文件列表),
            ('素材大小', item_in.源文件大小),
            ('* 购买须知', '本店都是设计师专用素材，不是图片，非设计师请勿购买，本店不提供任何使用教程。'),
            ('* 样机须知', '本店均为白膜样机，不提供样机内贴图！'),
            ('* 海报须知', '本店海报均不提供字体！')
        ]
    ).main()

    all_pil = [
        XQTitlePic(title='素材信息', sec_title='购买前请务必仔细阅读购买须知').main(),
        info_pil
    ]

    # 制作效果图
    effect_pic_list = mff.fun_指定遍历(mfs.effect_path, IMAGE_FILE_SUFFIX)
    if mfs.effect_path.exists() is True and len(effect_pic_list) > 0 and item_in.制作效果图 is True:
        effect_pil = XQMakePIC(
            img_list=effect_pic_list,
            material_path=mfs.material_path,
            single_pic_num=item_in.单排图片数量,
            has_material_info=False,
            tb_name=item_in.tb_name,
            pic_water_market=item_in.详情水印
        ).main()

        all_pil.append(
            XQTitlePic(title='效果图', sec_title='此效果图素材内不提供').main()
        )
        all_pil.append(
            effect_pil
        )

    # 制作预览图
    if item_in.详情使用图片 == '所有图片':
        preview_pic_list = mff.fun_指定遍历(mfs.preview_path, IMAGE_FILE_SUFFIX)
        if item_in.详情使用图片排序 is False:
            preview_pic_list.reverse()

        preview_pic_list = preview_pic_list[:item_in.详情使用图片数量]
    else:
        preview_pic_list = [Path(img) for img in item_in.img_list]

    if mfs.preview_path.exists() is True and len(preview_pic_list) > 0 and item_in.制作预览图 is True:
        preview_pil = XQMakePIC(
            img_list=preview_pic_list,
            material_path=mfs.material_path,
            has_material_info=item_in.详情素材信息,
            single_pic_num=item_in.单排图片数量,
            tb_name=item_in.tb_name,
            pic_water_market=item_in.详情水印
        ).main()
        all_pil.append(
            XQTitlePic(title='预览图', sec_title='素材源文件和图片对应').main()
        )
        all_pil.append(
            preview_pil
        )

    bg_width = 1500
    bg_height = sum([pil.height for pil in all_pil])
    bg = Image.new('RGBA', (bg_width, bg_height), (255, 255, 255))

    top = 0
    for pil in tqdm(all_pil, ncols=100, desc='制作详情'):
        bg.paste(pil, (0, top), pil)
        top += pil.height
        pil.close()

    line_height = 2500
    top = 0
    bottom = line_height
    num = 1

    while True:
        if bottom > bg.height:
            bottom = bg.height

        crop_im = bg.crop((0, top, bg.width, bottom))

        crop_im = crop_im.convert('RGB')
        crop_im.save(
            (UP_FOLDER / f'xq_{num}.jpg').as_posix(), quality=90
        )
        crop_im.close()
        top += line_height
        bottom += line_height

        num += 1

        if bottom == bg.height:
            break

        if top >= bg.height:
            break

    bg.close()
