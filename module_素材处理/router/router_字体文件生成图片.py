import io
from typing import Literal

from fastapi import APIRouter
from fastapi.responses import Response

from module_素材处理.core.setting import UP_FOLDER
from module_素材处理.core.图片编辑 import PICEdit

router = APIRouter()

Direction = Literal['ltr', 'ttb']


@router.get('/font_to_pil')
def font_to_pil(font_path: str, text: str, direction: Direction):
    bg = PICEdit.fun_字体文件生成图片(font_path=font_path, text=text, direction=direction).fun_单个文字生成图片()
    bg.save(
        (UP_FOLDER / '00.png').as_posix()
    )

    byte_io = io.BytesIO()
    bg.save(byte_io, format='png')
    bg.close()

    return Response(byte_io.getvalue(), media_type='image/png')
