import copy
import datetime

from service import spiderService
from obj.classDef import VideoPage, MyTime, VideoInfo


# 获取b站视频列表
def get_video_page_list(b_url: str):
    video_page_list = spiderService.get_bilibili_video_page_list(b_url)
    return video_page_list

def seconds_to_hh_mm_ss(seconds):
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    answer_str = ""

    if hours > 0:
        answer_str += f"{int(hours):02d}:"
    if minutes >0:
        answer_str += f"{int(minutes):02d}:"

    answer_str += f"{int(seconds):02d}"
    return answer_str


# 按不同的计划生成对应的plan
def generate_plan_video_list_v2(video_page_list: list[VideoPage], duration: int):
    answer_list: list[list[VideoPage]] = []
    video_duration = 0  # 表示每次计划的视频时长，而duration是预期的时长

    per_plan_list: list[VideoPage] = []

    pointer: int = 0  # 指向爬取来的video_p_l的索引指针

    # 每次循环都要分一个组出来，直到pointer越界
    while True:
        if pointer >= len(video_page_list):
            break
        item = video_page_list[pointer]

        if video_duration + item.durationSecond < duration:  # 算上这个视频，总时长不足分段时长
            per_plan_list.append(copy.copy(item))
            video_duration += item.durationSecond
            pointer += 1
        else:
            total_duration = (video_duration + item.durationSecond)  # 表示距离目标相差的时间
            if total_duration > duration:
                item.comment = "看到{}就可以啦".format(seconds_to_hh_mm_ss(item.durationSecond - (total_duration - duration)))
                per_plan_list.append(copy.copy(item))
                item.comment = ""
                item.move_to_second(item.durationSecond - (total_duration - duration))  # 这是下一次要从哪开始看的标志，也是本次要看到哪里的时长
                item.durationSecond = total_duration - duration  # 超出的时间也表示下次要看多久
            else:
                item.comment = "要把这一集看完"
                per_plan_list.append(copy.copy(item))
                item.durationSecond = 0
                pointer += 1  # 所有视频分配完成，表示结束循环
            video_duration = 0
            # 下面是每次计划录入最终结果中
            answer_list.append(copy.copy(per_plan_list))
            per_plan_list.clear()

    if len(per_plan_list) > 0:
        answer_list.append(copy.copy(per_plan_list))
    return answer_list


# 按不同的计划生成对应的plan
def generate_plan_video_list(video_page_list: list[VideoPage], duration: int):
    answer_list: list[list[VideoPage]] = []
    video_duration = 0

    per_plan_list: list[VideoPage] = []

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
                item.move_to_second(video_second)

                per_plan_list.append(copy.copy(item))
                if tmp_duration > duration:
                    answer_list.append(copy.copy(per_plan_list))
                    per_plan_list.clear()
                    tmp_duration -= duration
                else:  # 比如时间剩下五分钟，而视频还有半小时，后面的的在这个item上就不算了
                    video_duration = tmp_duration
                    tmp_duration = 0

    for item in video_page_list:
        video_duration += item.durationSecond
        per_plan_list.append(item)

        if video_duration > duration:
            video_duration = item.durationSecond
            answer_list.append(copy.copy(per_plan_list))
            per_plan_list.clear()
            per_plan_list.append(item)

    return answer_list


def get_plan_list(b_url: str, plan_duration: int):
    video_page_list = spiderService.get_bilibili_video_page_list(b_url)
    return generate_plan_video_list_v2(video_page_list, plan_duration)


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


def get_video_info(b_url) -> Exception | VideoInfo:
    return spiderService.get_bilibili_video_info(b_url)
