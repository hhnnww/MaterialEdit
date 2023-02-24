from pathlib import Path

from PIL import Image
from tqdm import tqdm

from module_素材处理.core.setting import IMAGE_FILE_SUFFIX
from module_素材处理.core.setting import IMG_PATH
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历


def fun_素材图蜘蛛水印(in_path: Path, tb_name: str):
    water_pil = Image.open(
        (IMG_PATH / tb_name / '蜘蛛网水印.png').as_posix()
    )
    for in_file in tqdm(fun_指定遍历(in_path, IMAGE_FILE_SUFFIX),
                        desc='图片添加水印', ncols=100):

        with Image.open(in_file.as_posix()) as im:
            if 1200 not in im.size:
                wp_copy = water_pil.copy()
                im.thumbnail((1200, 1200), 1)
                wp_copy.thumbnail((im.width, 9999), 1)

                top = int((im.height - wp_copy.height) / 2)
                im.paste(wp_copy, (0, top), wp_copy)
                im.save(in_file.as_posix())

                wp_copy.close()
            else:
                print('边距 1200 不添加')


if __name__ == '__main__':
    fun_素材图蜘蛛水印(in_path=Path(r'F:\泡泡素材\10000-19999\10002\10002'), tb_name='泡泡素材')
