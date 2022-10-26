from PIL import Image
from fastapi import APIRouter
from pydantic import BaseModel

from module_素材处理.core import XQEffectPIC, XQInfoPic, XQPreviewPic, MaterialFolderStructure, MaterialFolderFunction, \
    XQTitlePic
from module_素材处理.core.setting import IMAGE_FILE_SUFFIX
from module_素材处理.core.setting import UP_FOLDER

router = APIRouter(prefix='/make_xq')


class ItemIn(BaseModel):
    root_path: str
    tb_name: str

    首图标题: str
    素材ID: str
    素材格式: str
    源文件列表: str
    源文件大小: str


@router.post('/make_xq')
def make_xq(item_in: ItemIn):
    mfs = MaterialFolderStructure(root_path=item_in.root_path)
    mff = MaterialFolderFunction

    for in_file in UP_FOLDER.iterdir():
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_FILE_SUFFIX:
            if 'xq_' in in_file.stem:
                in_file.unlink()

    info_pil = XQInfoPic(
        text_list=[
            ('素材标题', item_in.首图标题 + f' [{item_in.tb_name}]'),
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

    if mfs.effect_path.exists() is True:
        effect_pil = XQEffectPIC(
            img_list=mff.fun_指定遍历(mfs.effect_path, IMAGE_FILE_SUFFIX), tb_name=item_in.tb_name
        ).main()

        all_pil.append(
            XQTitlePic(title='效果图', sec_title='此效果图素材内不提供').main()
        )
        all_pil.append(
            effect_pil
        )

    if mfs.preview_path.exists() is True:
        preview_pil = XQPreviewPic(
            img_list=mff.fun_指定遍历(mfs.preview_path, IMAGE_FILE_SUFFIX),
            material_path=mfs.material_path,
            tb_name=item_in.tb_name
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
    for pil in all_pil:
        bg.paste(pil, (0, top), pil)
        top += pil.height
        pil.close()

    line_height = 2000
    top = 0
    bottom = 2000
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
