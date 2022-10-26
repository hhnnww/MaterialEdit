from pathlib import Path

from win32com.client import Dispatch

from core.素材文件夹功能.AIFile.fun_删除_all_free_down_广告 import fun_删除_all_free_down_广告


class AIFile:
    app = None
    doc = None

    @classmethod
    def open(cls, file: Path):
        ai_file = cls()
        ai_file.app = Dispatch('Illustrator.Application')
        ai_file.app.Open(file.as_posix())
        ai_file.doc = ai_file.app.ActiveDocument

        return ai_file

    def fun_删除all_free_down广告(self):
        fun_删除_all_free_down_广告(self.doc)


if __name__ == '__main__':
    ai_path = r'E:\DOWN\box_icons_modern_3d_outline_6926301\Box 02.ai'
    ai = AIFile.open(Path(ai_path))
    ai.fun_删除all_free_down广告()
