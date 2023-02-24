from pathlib import Path
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历


def fun_生成SKP批量导出脚本(in_path: Path):
    cmd_path = Path.home() / 'Desktop' / 'auto_export_png.rb'
    start_args = """def save_view_to_png(file_path, img_path)
  Sketchup.open_file(file_path)
  model = Sketchup.active_model
  model.rendering_options["DisplayWatermarks"]= false
  view = model.active_view
  view.write_image(
    filename: img_path,
    width: 2000,
    height: 1500,
    antialias: true,
    transparent: false
  )
  model.save
end\n\n"""

    all_file = fun_指定遍历(folder=in_path, suffix=['.skp'])
    for in_file in all_file:
        png_path = in_file.with_suffix('.png')
        if png_path.exists() is False:
            file_args = f"save_view_to_png '{in_file.as_posix()}','{png_path.as_posix()}'\n"
            start_args += file_args

    start_args += '\n\nUI.messagebox("图片已经全部导出完成!~")'

    cmd_path.write_text(start_args, encoding='utf-8')


if __name__ == '__main__':
    fun_生成SKP批量导出脚本(
        in_path=Path(r'F:\泡泡素材\10000-19999\10003\10003')
    )
