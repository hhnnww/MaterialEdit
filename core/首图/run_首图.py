import time
from pathlib import Path

from core.首图.布局.class_布局_1_X import STLayoutOneX
from core.首图.布局.class_布局自动 import STAutoLayout
from core.首图.布局.class_首图制作 import STMake, SmallSizeModel
from core.首图.样式.class_heijing import STHeiJingStyle

now = time.time()

img_list = []
for in_file in Path(r'E:\小夕素材\9000-9999\9055\效果图').iterdir():
    if in_file.is_file() and in_file.suffix.lower() in ['.png', '.jpg']:
        img_list.append(in_file.as_posix())

        if len(img_list) == 30:
            break

st_width = 1500
st_height = 1300

if len(img_list) >= 10:
    st_layout = STAutoLayout(
        img_list=img_list,
        st_width=st_width,
        st_height=st_height,
        st_row=3
    ).main()

    resize_model = SmallSizeModel.ALL_AUTO
else:
    st_layout = STLayoutOneX(
        pic_list=img_list,
        st_width=st_width,
        st_height=st_height
    ).main()
    resize_model = SmallSizeModel.ALL_AUTO

st = STMake(
    st_list=st_layout,
    st_width=st_width,
    st_height=st_height,
    gutter=10,
    bg_color=(255, 255, 255),
    small_pic_size_mode=resize_model
).main()

st = STHeiJingStyle(
    layout_bg=st,
    title='纸杯 水杯智能样机',
    material_format_list=['ppt']
).main()

st.show()

end = time.time()
print(end - now)
