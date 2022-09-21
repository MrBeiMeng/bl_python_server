import copy
import datetime

from service import spiderService
from obj.classDef import BilibiliVideoPage, MyTime


def remove_params(b_url: str):
    if b_url != "":
        return b_url.split("?")[0]
    else:
        raise Exception("b_url 不能为空")


# 获取b站视频列表
def generate_video_list(bUrl: str):
    # targetUrl = spiderService.generateBilibiliVideoUrl(vId)
    video_page_list = spiderService.getBilibiliVideoPageList(bUrl)

    return video_page_list


# 按不同的计划生成对应的plan
def generate_plan_video_list(video_page_list: list[BilibiliVideoPage], duration: int):
    answer_list: list[list[BilibiliVideoPage]] = []
    video_duration = 0

    per_plan_list: list[BilibiliVideoPage] = []

    i = 0
    while i < len(video_page_list):
        item = video_page_list[i]
        video_duration += item.durationSecond

        per_plan_list.append(copy.copy(item))
        i += 1

        if video_duration >= duration:
            answer_list.append(copy.copy(per_plan_list))
            per_plan_list.clear()
            tmp_duration = video_duration - duration
            while tmp_duration > 0:
                video_second = item.durationSecond - tmp_duration  # 视频应当放映位置
                item.moveToSecond(video_second)

                per_plan_list.append(copy.copy(item))
                if tmp_duration > duration:
                    answer_list.append(copy.copy(per_plan_list))
                    per_plan_list.clear()
                    tmp_duration -= duration
                else:
                    video_duration = tmp_duration
                    tmp_duration = 0

    for item in video_page_list:
        video_duration += item.durationSecond
        per_plan_list.append(item)

        if video_duration + item.durationSecond > video_duration:
            video_duration = item.durationSecond
            answer_list.append(copy.copy(per_plan_list))
            per_plan_list.clear()
            per_plan_list.append(item)

    return answer_list


def get_plan_list(b_url: str, plan_duration: int):
    video_page_list = spiderService.getBilibiliVideoPageList(b_url)
    return generate_plan_video_list(video_page_list, plan_duration)


def get_suggestion_plan(b_url):
    bilibili_obj = spiderService.get_bilibili_obj(b_url)
    key_list = ["每天10分钟 要看", "每天15分钟 需要", "每天30分钟 需要", "每天一小时  要看", "每天两小时  则需要"]
    value_list = [MyTime.MINUTE * 10, MyTime.MINUTE * 15, MyTime.MINUTE * 30, MyTime.HOUR, MyTime.HOUR * 2]

    for i in range(len(value_list)):
        duration = value_list[i]
        days = int(bilibili_obj.videoTotalDuration / duration)
        now_time = datetime.datetime.now()
        to_time = now_time + datetime.timedelta(days=days)

        key_list[i] += str(days) + "天\t直到" + to_time.strftime("%y年%m月%d日") + "\t计划代码@" + str(duration)

    key_str = "|".join(key_list)

    return {"key": key_str}


def _anal_duration(duration_total: int, duration_per: int):
    return int(duration_total / duration_per)
