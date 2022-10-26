from PIL import Image
from fastapi import APIRouter
from pydantic import BaseModel

from core import STAutoLayout, STMake, STHeiJingStyle, SmallSizeModel, STLayoutOneX
from core.setting import UP_FOLDER

router = APIRouter(prefix='/make_st')


class ItemIn(BaseModel):
    material_id: str
    title: str
    img_list: list
    st_row: int
    st_style: str
    small_pic_mode: str
    material_format_list: str
    tb_name: str
    gutter: int
    首图名称: int


@router.post('/make_st')
def make_st(item_in: ItemIn):
    st_width, st_height = 1500, 1500
    small_pic_mode = 1

    if item_in.small_pic_mode == '全自动适应':
        small_pic_mode = SmallSizeModel.ALL_AUTO
    elif item_in.small_pic_mode == '单行自适应':
        small_pic_mode = SmallSizeModel.AUTO
    elif item_in.small_pic_mode == '固定尺寸':
        small_pic_mode = SmallSizeModel.AVERAGE

    if item_in.st_style == '黑鲸':
        st_width = 1500
        st_height = 1300

    # 构建布局
    if len(item_in.img_list) > 10:
        layout = STAutoLayout(
            img_list=item_in.img_list,
            st_width=st_width,
            st_height=st_height,
            st_row=item_in.st_row
        ).main()
    else:
        layout = STLayoutOneX(
            pic_list=item_in.img_list,
            st_height=st_height,
            st_width=st_width
        ).main()

    # 制作背景图
    bg = STMake(st_list=layout, st_width=st_width, st_height=st_height, gutter=item_in.gutter, bg_color=(255, 255, 255),
                small_pic_size_mode=small_pic_mode).main()

    # 制作首图样式图
    if item_in.st_style == '黑鲸':
        bg = STHeiJingStyle(layout_bg=bg, material_format_list=item_in.material_format_list.split(' '),
                            tb_name=item_in.tb_name, title=item_in.title, material_id=item_in.material_id).main()

    # 保存首图
    if UP_FOLDER.exists() is False:
        UP_FOLDER.mkdir(parents=True)

    st_path = (UP_FOLDER / f'{item_in.首图名称}.jpg').as_posix()
    new_bg = Image.new('RGB', bg.size, (255, 255, 255))
    new_bg.paste(bg, (0, 0), bg)
    bg.close()

    new_bg.save(st_path, quality=80)
    new_bg.close()
