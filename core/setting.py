from pathlib import Path

# 素材图片目录
PIC_EDIT_IMG = Path(__file__).parent / 'IMAGE'

# 素材字体目录
FONT_PATH = Path(__file__).parent / 'FONTS' / 'OPPOSans'

# 源文件列表、图片列表、广告文件列表
MATERIAL_FILE_SUFFIX = ['.psd', '.psb', '.ai', '.eps']
IMAGE_FILE_SUFFIX = ['.png', '.jpg', '.jpeg']
AD_FILE_SUFFIX = ['.html', '.url', '.txt', '.exe']

# 桌面上传文件夹
UP_FOLDER = Path().home() / 'desktop' / 'UPLOAD'
