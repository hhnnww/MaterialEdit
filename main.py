from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import router.router_制作详情
import router.router_制作首图
import router.router_文件夹信息
import router.router_文件夹操作

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router_文件夹操作.router)
app.include_router(router.router_文件夹信息.router)
app.include_router(router.router_制作首图.router)
app.include_router(router.router_制作详情.router)
