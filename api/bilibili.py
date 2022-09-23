from fastapi import APIRouter

from obj.resp.classDef import BVideoInfoResponse
from service import bilibili_service

app = APIRouter()
prefix = "/bilibili"
tags = ["bilibili"]


def format_bilibili_url(b_url: str):
    if b_url != "":
        return b_url.split("?")[0]
    else:
        raise Exception("b_url 不能为空")


@app.get("/getVideoPageList", description='获取视频分集列表')
async def get_video_list(b_url: str):
    try:
        b_url = format_bilibili_url(b_url)
        video_page_list = bilibili_service.get_video_page_list(b_url)
    except Exception as e:
        return e
    return video_page_list


@app.get("/getVideoInfo", description='获取视频信息')
async def get_video_info(b_url: str):
    try:
        b_url = format_bilibili_url(b_url)
        video_info = bilibili_service.get_video_info(b_url)
        resp = BVideoInfoResponse(video_info)
    except Exception as e:
        print(e.args)
        return e.args
    return resp


@app.get("/getPlanList", description='通过不同计划安排视频分集列表')
async def get_plan_list(b_url: str, duration: int):
    try:
        b_url = format_bilibili_url(b_url)
        pan_list = bilibili_service.get_plan_list(b_url, duration)

    except Exception as e:
        return e
    return pan_list


@app.get("/getSuggestionPlan", description='建议视频进度安排')
async def get_suggestion_plan(b_url: str):
    try:
        b_url = format_bilibili_url(b_url)
        plan_obj = bilibili_service.get_suggestion_plan(b_url)

    except Exception as e:
        return e
    return plan_obj
