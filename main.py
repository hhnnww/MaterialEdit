from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from module_素材处理.router import router_制作详情
from module_素材处理.router import router_制作首图
from module_素材处理.router import router_字体文件生成图片
from module_素材处理.router import router_文件夹信息
from module_素材处理.router import router_文件夹操作
from module_素材处理.router import router_未使用目录
from module_素材处理.router import router_素材合并
from module_素材采集.core.model import database
from module_素材采集.router import router_下载目录移动到素材目录
from module_素材采集.router import router_单页素材采集
from module_素材采集.router import router_素材采集
from module_素材采集.router import router_获取素材

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware('http')
def auto_close_database(request: Request, call_next):
    if database.is_closed() is True:
        database.connect()

    response = call_next(request)

    if database.is_closed() is not True:
        database.close()

    return response


app.include_router(router_文件夹操作.router)
app.include_router(router_文件夹信息.router)
app.include_router(router_制作首图.router)
app.include_router(router_制作详情.router)
app.include_router(router_素材采集.router)
app.include_router(router_获取素材.router)
app.include_router(router_下载目录移动到素材目录.router)
app.include_router(router_单页素材采集.router)
app.include_router(router_未使用目录.router)
app.include_router(router_字体文件生成图片.router)
app.include_router(router_素材合并.router)

# app.mount('/static', StaticFiles(directory='static', html=True), name='static')
