from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from module_素材处理.router import router_制作详情, router_制作首图, router_文件夹信息, router_文件夹操作

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
