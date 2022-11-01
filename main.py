from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from module_素材处理.router import router_制作详情, router_制作首图, router_文件夹信息, router_文件夹操作
from module_素材采集.router import router_素材采集, router_获取素材, router_下载目录移动到素材目录,router_单页素材采集

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_文件夹操作.router)
app.include_router(router_文件夹信息.router)
app.include_router(router_制作首图.router)
app.include_router(router_制作详情.router)
app.include_router(router_素材采集.router)
app.include_router(router_获取素材.router)
app.include_router(router_下载目录移动到素材目录.router)
app.include_router(router_单页素材采集.router)

app.mount('/static', StaticFiles(directory='static', html=True), name='static')
