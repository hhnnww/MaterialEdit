from pathlib import Path

from core.素材文件夹.PPTFile.fun_图片组合 import PPTPICMerge
from core.素材文件夹.PPTFile.fun_ppt处理 import PPTFile
import shutil


class PPTEdit:
    def __init__(self, ppt_path: Path):
        self.ppt_path = ppt_path

    def main(self):
        ppt_export = PPTFile(self.ppt_path)
        ppt_export.fun_导出PNG()

        ppt_dir = ppt_export.ppt_dir
        bg = PPTPICMerge(ppt_dir)
        bg = bg.main()

        ppt_png = self.ppt_path.with_suffix('.png')
        bg.save(
            ppt_png.as_posix()
        )
        shutil.rmtree(ppt_dir)


if __name__ == '__main__':
    PPTEdit(
        Path(r'X:\H000-H999\H0257\H0257\小夕素材(13).pptx')
    ).main()
