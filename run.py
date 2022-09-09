import uvicorn
from fastapi import FastAPI
from api import bilibili
from api import ebbinghaus

app = FastAPI()


def install_router(obj):
    child_app = obj.app
    prefix = obj.prefix
    tags = obj.tags
    app.include_router(child_app, prefix=prefix, tags=tags)


install_router(bilibili)  # 添加路由
install_router(ebbinghaus)  # 添加路由


if __name__ == '__main__':
    uvicorn.run(app='Web:app', host='127.0.0.1', port=9527, reload=True, debug=True)

