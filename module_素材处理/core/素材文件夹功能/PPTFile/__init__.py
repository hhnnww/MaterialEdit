from pathlib import Path

from module_素材处理.core.素材文件夹功能.PPTFile.fun_ppt处理 import PPTFile
from module_素材处理.core.素材文件夹功能.PPTFile.fun_图片组合 import PPTPICMerge


class PPTEdit:
    def __init__(self, ppt_path: Path, ppt_export_path: Path):
        self.ppt_path = ppt_path
        self.ppt_export_path = ppt_export_path

    def main(self):
        ppt_export = PPTFile(self.ppt_path, self.ppt_export_path)
        if ppt_export.fun_导出PNG() == 'ok':
            ppt_dir = ppt_export.ppt_dir
            bg = PPTPICMerge(ppt_dir)
            bg = bg.main()

            ppt_png = self.ppt_path.with_suffix('.png')
            bg.save(
                ppt_png.as_posix()
            )

            for in_file in ppt_dir.iterdir():
                if in_file.is_file():
                    new_stem = "99" + in_file.stem
                    if in_file.with_stem(new_stem).exists() is False:
                        in_file.rename(
                            in_file.with_stem(new_stem)
                        )

            # shutil.rmtree(ppt_dir)
