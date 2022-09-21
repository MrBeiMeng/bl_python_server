from fastapi import APIRouter
from service import bilibili_service

app = APIRouter()
prefix = "/bilibili"
tags = ["bilibili"]


@app.get("/getVideoList", description='获取视频分集列表')
async def get_video_list(b_url: str):
    b_url = bilibiliService.remove_params(b_url)
    video_page_list = bilibiliService.generate_video_list(b_url)
    return video_page_list


@app.get("/getPlanList", description='通过不同计划安排视频分集列表')
async def get_plan_list(b_url: str, duration: int):
    b_url = bilibiliService.remove_params(b_url)
    pan_list = bilibiliService.get_plan_list(b_url, duration)
    return pan_list


@app.get("/getSuggestionPlan", description='建议视频进度安排')
async def get_suggestion_plan(b_url: str):
    b_url = bilibiliService.remove_params(b_url)
    plan_obj = bilibiliService.get_suggestion_plan(b_url)
    return plan_obj
