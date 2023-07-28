import sys

import uvicorn
import logging
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from controller import bilibili
from controller import ebbinghaus

app = FastAPI(
    title="零散api python服务器",
    description="主要存放一些小的，但不得不放在云端的api",
    version="1.0",
    contact={
        "name": "小艾同学",
        "url": "http://localhost",
        "email": "1192384722@qq.com",
    },
    openapi_url="/api/v2/openapi.json",
    docs_url="/doc"
)
app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
    # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
    # expose_headers=["*"]
    # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    # max_age=1000
)

# 关闭 FastAPI 的 INFO 日志
logging.getLogger("fastapi").setLevel(logging.WARNING)


# 全局拦截
@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    global log
    try:
        log = f"{request.client.host}:{request.headers.get('User-Agent')}|{request.method}:{request.url}"
        # print(log)
        return await call_next(request)
    except Exception as e:
        logging.error(f"发生错误:{str(e)},\033[32m在请求此url时s:\033[0m:{log}")
        error_response = {"error": str(e)}
        return JSONResponse(status_code=500, content=error_response)


def install_router(obj):
    child_app = obj.app
    prefix = obj.prefix
    tags = obj.tags
    app.include_router(child_app, prefix=prefix, tags=tags)


install_router(bilibili)  # 添加路由
install_router(ebbinghaus)  # 添加路由


def equal(a, b):
    return str(a).strip(" ") == b


def main():
    host = "0.0.0.0"
    port = 9528
    if len(sys.argv) > 0:
        for i in range(1, len(sys.argv)):
            # if equal(sys.argv[i], "--debug=true"):
            #     openDebug()
            if sys.argv[i].find("--host=") != -1:
                host = sys.argv[i][7:]
            if sys.argv[i].find("--port=") != -1:
                port = int(sys.argv[i][7:])

        # myDebug('参数个数为:{}个参数。'.format(len(sys.argv)))
        # for i in range(0, len(sys.argv)):
        #     myDebug('参数 %s 为：%s' % (i, sys.argv[i]))
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - \033[32m%(levelname)s:\033[0m: %(message)s"
    # log_config["formatters"]["default"]["fmt"] = "%(asctime)s - \033[32m%(levelname)s:\033[0m: %(message)s"
    uvicorn.run(app, host=host, port=port, log_config=log_config)


if __name__ == '__main__':
    main()
