from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from app.api.v1.resp.bvideo_info_response import BVideoInfoResponse
from app.services import bilibili_service

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
        return e.args
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

@app.get("/getPlanListJson", description='通过不同计划安排视频分集列表')
async def get_plan_list_json(b_url: str, duration: int):
    try:
        b_url = format_bilibili_url(b_url)
        pan_list = bilibili_service.get_plan_list(b_url, duration)

    except Exception as e:
        return e
    return pan_list


@app.get("/getPlanListStr", description='通过秒数生成日计划列表，返回字符串形式', response_class=PlainTextResponse)
async def get_plan_list_str(b_url: str, duration: int, reverse: bool = False):
    b_url = format_bilibili_url(b_url)
    pan_list = bilibili_service.get_plan_list(b_url, duration)
    answer_str = ""
    num_list = range(len(pan_list)) if not reverse else range(len(pan_list) - 1, -1, -1)
    for i in num_list:
        answer_str += "第{}天任务\n".format(i + 1)
        day_plan_list = pan_list[i]
        for plan in day_plan_list:
            tmp_str = " - [{}]({}) {}\n".format(plan.title, plan.url, "| **" + plan.comment + "**" if plan.comment != "" else "")
            answer_str += tmp_str
        answer_str += "\n"
    return answer_str


# 返回格式最好是按天进行划分，生成每天的计划，以及最后的视频要看多长时间，直接返回字符串即可
# 例如
# 每天观看时长
# 第一天
#       Notes:

@app.get("/getSuggestionPlan", description='建议视频进度安排')
async def get_suggestion_plan(b_url: str):
    try:
        b_url = format_bilibili_url(b_url)
        plan_obj = bilibili_service.get_suggestion_plan(b_url)

    except Exception as e:
        return e
    return plan_obj
