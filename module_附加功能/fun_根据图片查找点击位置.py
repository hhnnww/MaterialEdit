from pathlib import Path
from typing import Union

import pyautogui


def fun_根据图片获取需要点击的位置(img: str) -> Union[tuple, None]:
    """
    传入图片，获取图片中心位置
    :param img:
    :return:
    """
    img = Path(__file__).parent.parent / img

    if pyautogui.locateOnScreen(img.as_posix()) is None:
        pyautogui.sleep(1)

    if pyautogui.locateOnScreen(img.as_posix()) is None:
        return None

    position = pyautogui.locateOnScreen(img.as_posix())
    cl = position.left + int(position.width / 2)
    ct = position.top + int(position.height / 2)
    return cl, ct
