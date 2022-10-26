from PIL import Image
from fastapi import APIRouter
from pydantic import BaseModel

from core import XQEffectPIC, XQInfoPic, XQPreviewPic, MaterialFolderStructure, MaterialFolderFunction
from core.setting import IMAGE_FILE_SUFFIX
from core.setting import UP_FOLDER, PIC_EDIT_IMG

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
            ('素材标题', item_in.首图标题),
            ('素材ID', item_in.素材ID),
            ('素材格式', item_in.素材格式),
            ('素材数量', item_in.源文件列表),
            ('素材大小', item_in.源文件大小),
            ('* 购买须知', '本店都是设计师专用素材，非设计师请勿购买，本店不提供任何使用教程。'),
            ('* 样机须知', '本店均为白膜样机，不提供样机内贴图！'),
            ('* 海报须知', '本店海报均不提供字体。')
        ]
    ).main()

    effect_pil = XQEffectPIC(
        img_list=mff.fun_指定遍历(mfs.effect_path, IMAGE_FILE_SUFFIX)
    ).main()

    preview_pil = XQPreviewPic(
        img_list=mff.fun_指定遍历(mfs.preview_path, IMAGE_FILE_SUFFIX),
        material_path=mfs.material_path
    ).main()

    all_pil = [
        Image.open(
            (PIC_EDIT_IMG / item_in.tb_name / '素材信息.png').as_posix()
        ),
        info_pil,
        Image.open(
            (PIC_EDIT_IMG / item_in.tb_name / '效果图.png').as_posix()
        ),
        effect_pil,
        Image.open(
            (PIC_EDIT_IMG / item_in.tb_name / '预览图.png').as_posix()
        ),
        preview_pil
    ]
    bg_width = 750
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

    water_mark = Image.open(
        (PIC_EDIT_IMG / item_in.tb_name / '蜘蛛网水印.png').as_posix()
    )
    while True:
        if bottom > bg.height:
            bottom = bg.height

        crop_im = bg.crop((0, top, bg.width, bottom))

        if num > 1:
            water_mark.thumbnail((750, 9999))
            w_left = int((crop_im.width - water_mark.width) / 2)
            w_top = int((crop_im.height - water_mark.height) / 2)
            crop_im.paste(water_mark, (w_left, w_top), water_mark)

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
    water_mark.close()
