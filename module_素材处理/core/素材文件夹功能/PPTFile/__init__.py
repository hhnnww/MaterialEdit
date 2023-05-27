from pathlib import Path

from module_素材处理.core.素材文件夹功能.PPTFile.fun_ppt处理 import PPTFile
from module_素材处理.core.素材文件夹功能.PPTFile.fun_图片组合 import PPTPICMerge


class PPTEdit:
    def __init__(self, ppt_path: Path, xgt_path: Path):
        self.ppt_path = ppt_path
        self.xgt_path = xgt_path

    def main(self):
        # TODO: 需要把导出的文件夹改为效果图
        # 这样可以把导出的图片保存下来，用来制作单独的首图和详情。

        ppt_export = PPTFile(self.ppt_path, self.xgt_path)
        if ppt_export.fun_导出PNG() == 'ok':
            ppt_dir = ppt_export.ppt_dir
            bg = PPTPICMerge(ppt_dir)
            bg = bg.main()

            ppt_png = self.ppt_path.with_suffix('.png')
            bg.save(
                ppt_png.as_posix()
            )
            # shutil.rmtree(ppt_dir)


if __name__ == '__main__':
    PPTEdit(
        Path(r'X:\H000-H999\H0257\H0257\小夕素材(13).pptx'),
        xgt_path=Path('')
    ).main()
