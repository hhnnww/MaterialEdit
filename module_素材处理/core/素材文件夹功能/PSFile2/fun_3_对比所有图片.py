import cv2
import numpy as np
from PIL import Image
from pyzbar import pyzbar

from module_素材处理.core import PICEdit
from module_素材处理.core.setting import PIC_EDIT_IMG


def fun_cv2_to_pil(img):
    img = Image.fromarray(
        cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    )
    return img


def fun_pil_to_cv2(img):
    img = cv2.cvtColor(
        np.array(img), cv2.COLOR_RGBA2BGRA
    )
    return img


def fun_打开图片(img_path: str):
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
    return img


def fun_所有广告图片():
    ad_list = []
    ad_pic_path = PIC_EDIT_IMG / '广告图片'
    for in_file in ad_pic_path.iterdir():
        if in_file.is_file() and in_file.suffix.lower() in ['.png']:
            ad_list.append(fun_打开图片(in_file))

    return ad_list


def fun_图片边缘(img):
    img = cv2.resize(img.copy(), (100, 100), interpolation=cv2.INTER_NEAREST)
    img = cv2.Canny(img, 3, 30)
    rec, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)

    return img


def fun_获取所有白色像素(img):
    white = np.bincount(np.nditer(img))
    if len(white) == 1:
        return 0
    return white.item(-1)


def fun_判断比例(img_1, img_2):
    radio_1 = img_1.shape[0] / img_1.shape[1]
    radio_2 = img_2.shape[0] / img_2.shape[1]
    abs_radio = abs(radio_1 - radio_2)
    if abs_radio < 0.1:
        return True

    return False


def fun_叠加差异(img_1, img_2):
    # 先给第一个图片删除个边框
    img_1 = fun_cv2_to_pil(img_1)
    img_1 = PICEdit.fun_边框删除(img_1).main()
    img_1 = fun_pil_to_cv2(img_1)

    im_1 = fun_图片边缘(img_1.copy())
    im_2 = fun_图片边缘(img_2.copy())

    diff = cv2.absdiff(im_1, im_2)
    diff_white = fun_获取所有白色像素(diff)

    # 如果差异完全无白色
    # 就是完全相同的图片
    if diff_white == 0:
        return True

    # 如果差异小于最小的 0.3
    # 至少大概率相同
    im_1_white = fun_获取所有白色像素(im_1)
    im_2_white = fun_获取所有白色像素(im_2)

    if diff_white < min([im_1_white, im_2_white]) * 0.8 and abs(im_1_white - im_2_white) < 200:
        return True

    return False


def fun_单个图片对比(img_1, img_2):
    if len(pyzbar.decode(img_1)) > 0:
        return True

    if fun_判断比例(img_1, img_2) is True:
        if fun_叠加差异(img_1, img_2) is True:
            return True

    return False


def run_对比所有图片(img, ad_img_list: list):
    for ad_img in ad_img_list:
        if fun_单个图片对比(img_1=img, img_2=ad_img) is True:
            return True

    return False


if __name__ == '__main__':
    print(
        fun_单个图片对比(
            fun_打开图片(r'C:\Users\wuweihua\Desktop\OUT_PATH\小夕素材(127)\图层 34.png'),
            fun_打开图片(r'E:\MyProject\material-fastapi\core\IMG\广告图片\2 (6).png')
        )
    )

    res = run_对比所有图片(
        img=fun_打开图片(r'C:\Users\wuweihua\Desktop\OUT_PATH\小夕素材(127)\图层 34.png'),
        ad_img_list=fun_所有广告图片()
    )
    print(res)
