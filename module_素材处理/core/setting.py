from pathlib import Path

# 素材图片目录
IMG_PATH = Path(__file__).parent / 'IMAGE'

# 素材字体目录
FONT_PATH = Path(__file__).parent / 'FONTS'

# 源文件列表、图片列表、广告文件列表
MATERIAL_FILE_SUFFIX = ['.psd', '.psb', '.ai', '.eps', '.otf', '.ttf']
IMAGE_FILE_SUFFIX = ['.png', '.jpg', '.jpeg']
AD_FILE_SUFFIX = ['.html', '.url', '.txt', '.exe', '.pdf']
FONT_SUFFIX = ['.otf', '.ttf']

# 桌面上传文件夹
UP_FOLDER = Path().home() / 'desktop' / 'UPLOAD'
if UP_FOLDER.exists() is False:
    UP_FOLDER.mkdir()

OUT_PATH = Path().home() / 'desktop' / 'OUT_PATH'
if OUT_PATH.exists() is False:
    OUT_PATH.mkdir()

TEXT_COLOR = (90, 90, 120)
