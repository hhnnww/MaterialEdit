import pyautogui
from PIL import Image
from fastapi import APIRouter
from pydantic import BaseModel

from module_素材处理.core.setting import UP_FOLDER
from module_素材处理.core.制作首图 import STAutoLayout
from module_素材处理.core.制作首图 import STHeiJingStyle
from module_素材处理.core.制作首图 import STLayoutOneX
from module_素材处理.core.制作首图 import STMake
from module_素材处理.core.制作首图 import SmallSizeModel
from module_素材处理.core.制作首图.样式.class_t500 import STT500
from module_素材处理.core.制作首图.样式.class_巴扎嘿 import STBaZhaHeiStyle

# 错落首图
# from module_素材处理.core.制作首图.布局.class_错落布局 import STLayoutScat

router = APIRouter(prefix='/make_st', tags=['制作首图'])


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
    素材格式标题: str
    源文件数量: int


@router.post('/make_st')
def make_st(item_in: ItemIn):
    print(f'制作首图: {item_in.title}')

    # 删除附图
    # ft_path = (UP_FOLDER / f'ft.jpg')
    # if ft_path.exists() is True:
    #     ft_path.unlink()

    # 删除UP文件夹里面的JPG图片
    for in_file in UP_FOLDER.iterdir():
        if in_file.is_file() and in_file.suffix.lower() in ['.jpg']:
            if in_file.stem in [str(i) for i in range(0, 9)]:
                in_file.unlink()

    small_pic_mode = 1

    # 构建首图的小图缩小模式
    if item_in.small_pic_mode == '全自动适应':
        small_pic_mode = SmallSizeModel.ALL_AUTO
    elif item_in.small_pic_mode == '单行自适应':
        small_pic_mode = SmallSizeModel.AUTO
    elif item_in.small_pic_mode == '固定尺寸':
        small_pic_mode = SmallSizeModel.AVERAGE
    elif item_in.small_pic_mode == 'OneAndX':
        small_pic_mode = SmallSizeModel.ALL_AUTO

    # 构建首图尺寸
    st_width, st_height = 1500, 1500
    if item_in.st_style == '黑鲸':
        st_height = 1300
    elif item_in.st_style == '巴扎嘿':
        st_width = 1000

    if item_in.small_pic_mode == '竖排自适应':
        from module_素材处理.core.制作首图.布局.class_竖排图片 import VerticalImages
        bg = VerticalImages(pic_list=item_in.img_list[:30], st_width=st_width, st_height=st_height,
                            gutter=item_in.gutter).main()

    elif item_in.small_pic_mode == '横排自适应':
        from module_素材处理.core.制作首图.布局.class_横排错乱布局自适应 import HorizontalImageAuto
        bg = HorizontalImageAuto(pic_list=item_in.img_list[:30], st_width=st_width, st_height=st_height,
                                 gutter=item_in.gutter).main()
    else:
        # 构建布局
        if item_in.small_pic_mode == 'OneAndX':
            # 构建1-X布局
            layout = STLayoutOneX(
                pic_list=item_in.img_list,
                st_height=st_height,
                st_width=st_width
            ).main()

            # 直接构建首图
            # bg = STLayoutScat(
            #     img_list=item_in.img_list,
            #     st_width=st_width,
            #     st_height=st_height,
            #     gutter=item_in.gutter,
            #     st_row=item_in.st_row
            # ).main()

        else:
            # 构建根据行数的布局
            layout = STAutoLayout(
                img_list=item_in.img_list[:30],
                st_width=st_width,
                st_height=st_height,
                st_row=item_in.st_row
            ).main()

        bg = STMake(st_list=layout, st_width=st_width, st_height=st_height, gutter=item_in.gutter,
                    bg_color=(255, 255, 255),
                    small_pic_size_mode=small_pic_mode).main()

    # 制作首图样式图
    if item_in.st_style == '黑鲸':
        bg = STHeiJingStyle(layout_bg=bg, material_format_list=item_in.material_format_list.split(' '),
                            tb_name=item_in.tb_name, title=item_in.title.upper(),
                            material_id=item_in.material_id).main()
    elif item_in.st_style == 'T500':
        bg = STT500(st=bg, title=item_in.title, sc_id=item_in.material_id, tb_name=item_in.tb_name,
                    type_title=item_in.素材格式标题).main()
    elif item_in.st_style == '巴扎嘿':
        bg = STBaZhaHeiStyle(st_layout=bg, title=item_in.title, material_num=str(item_in.源文件数量),
                             material_format_title=item_in.素材格式标题, material_id=item_in.material_id,
                             tb_name=item_in.tb_name).main()

    # 保存首图
    if UP_FOLDER.exists() is False:
        UP_FOLDER.mkdir(parents=True)

    st_path = (UP_FOLDER / f'{item_in.首图名称}.jpg').as_posix()
    new_bg = Image.new('RGB', bg.size, (255, 255, 255))
    new_bg.paste(bg, (0, 0), bg)
    bg.close()

    new_bg.save(st_path, quality=80)
    new_bg.close()

    pyautogui.alert("首图制作完成", "素材全自动处理程序")

    # 制作附图
    # if item_in.small_pic_mode in ['竖排自适应', '横排自适应']:
    #     small_pic_mode = SmallSizeModel.AVERAGE
    #     layout = STAutoLayout(
    #         img_list=item_in.img_list[:30],
    #         st_width=st_width,
    #         st_height=st_height,
    #         st_row=item_in.st_row
    #     ).main()
    #
    # bg = STMake(
    #     st_list=layout, st_width=600, st_height=800, gutter=item_in.gutter, bg_color=(255, 255, 255),
    #     small_pic_size_mode=small_pic_mode
    # ).main()

    # bg = bg.convert('RGB')
    # bg.save(ft_path.as_posix(), quality=80)
    # bg.close()
