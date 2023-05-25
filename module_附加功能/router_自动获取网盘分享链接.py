from pathlib import Path
from typing import Union

import pyautogui
import pyperclip
from fastapi import APIRouter
from pydantic import BaseModel

from module_附加功能.fun_根据图片查找点击位置 import fun_根据图片获取需要点击的位置

pyautogui.PAUSE = .01

router = APIRouter(prefix='/自动分享网盘链接', tags=['自动分享网盘链接'])


class ItemIn(BaseModel):
    start_num: str
    end_num: str


@router.post('/')
def fun_自动分享网盘链接(item_in: ItemIn):
    AutoGetBaiDuYunShareLink(
        start_num=int(item_in.start_num),
        end_num=int(item_in.end_num)
    ).run()


class AutoGetBaiDuYunShareLink:
    def __init__(self, start_num: int, end_num: int):
        self.start_num = start_num
        self.end_num = end_num

    @staticmethod
    def fun_处理网盘分享内容(bd_share_content: str) -> str:
        """
        删除网盘分享链接的广告语
        :param bd_share_content:
        :return:
        """
        bd_share_content = bd_share_content.split('\n')[:-1]
        bd_share_content = '\n'.join(bd_share_content)
        bd_share_content = bd_share_content.rstrip()

        return bd_share_content

    def fun_获取百度网盘地址(self, ma_id: str) -> Union[str, None]:
        """
        自动从百度网盘获取分享链接
        :param ma_id:
        :return:
        """

        # 点击搜搜框
        res = fun_根据图片获取需要点击的位置("IMG/bd-search.png")

        if res is None:
            cl, ct = fun_根据图片获取需要点击的位置("IMG/bd-search-close.png")
            pyautogui.click(cl, ct)

        cl, ct = fun_根据图片获取需要点击的位置("IMG/bd-search.png")
        pyautogui.click(cl, ct)

        # 全选并删除
        # pyautogui.hotkey('ctrl', 'a')
        # pyautogui.hotkey('del')

        # 输入文字
        pyautogui.write(ma_id)
        pyautogui.hotkey('enter')

        # 找到文件夹
        while fun_根据图片获取需要点击的位置('IMG/bd-folder.png') is None:
            pyautogui.sleep(.01)

        cl, ct = fun_根据图片获取需要点击的位置('IMG/bd-folder.png')
        pyautogui.click(cl, ct)

        # 分享按钮
        cl, ct = fun_根据图片获取需要点击的位置('IMG/bd-share.png')
        pyautogui.click(cl, ct)

        # 永久有效
        cl, ct = fun_根据图片获取需要点击的位置('IMG/bd-time.png')
        pyautogui.click(cl, ct)

        # 创建连接
        cl, ct = fun_根据图片获取需要点击的位置('IMG/bd-getlink.png')
        pyautogui.click(cl, ct)

        # 关闭
        while fun_根据图片获取需要点击的位置('IMG/bd-close.png') is None:
            pyautogui.sleep(.01)

        cl, ct = fun_根据图片获取需要点击的位置('IMG/bd-close.png')
        pyautogui.click(cl, ct)

        bd_share = self.fun_处理网盘分享内容(pyperclip.paste())

        print(
            f'{ma_id}\t"{bd_share}"\n'
        )

        return f'{ma_id}\t"{bd_share}"\n\n'

    def run(self):
        output = Path().home() / 'Desktop' / 'output.txt'

        f = open(file=output.as_posix(), mode='w+', encoding="UTF-8")
        f.close()

        # 打开百度网盘在任务栏的位置
        c_l, c_t = fun_根据图片获取需要点击的位置('IMG/bd-icon.png')
        pyautogui.click(c_l, c_t)

        with open(file=output.as_posix(), mode='a+', encoding='UTF-8') as f:
            for x in range(self.start_num, self.end_num + 1):
                res = self.fun_获取百度网盘地址(str(x))

                if res is not None:
                    f.write(res)

        pyautogui.alert('自动获取百度网盘链接已经处理完成！', "素材全自动处理程序")


if __name__ == '__main__':
    AutoGetBaiDuYunShareLink(
        start_num=2406,
        end_num=2416
    ).run()
