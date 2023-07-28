from datetime import datetime
import json
import time
from uuid import UUID

import numpy as np


class MyTime:
    SECOND = 1
    MINUTE = SECOND * 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24
    MOUTH = DAY * 30


class HtmlResult:
    title = None  # 页面标题
    html_content = None  # 抓取结果
    create_at = None
    saving_file_name = None

    def __init__(self, title, html_content):
        self.title = title
        self.html_content = html_content
        self.create_at = datetime.now().strftime("%y-%m-%d %H:%M")
        self.saving_file_name = "抓取结果" + self.title + self.create_at + ".html"

    def save(self):
        file = open(self.saving_file_name, "w", encoding="utf-8")
        file.write(self.html_content)
        file.close()


class VideoPage:
    title = ""
    url = ""
    indexInt = 0
    indexStr = "P1"
    durationSecond = 0  # 表示视频的播放时间，当播放时间和实际不符时表示要看多久
    comment = ""

    def move_to_second(self, second: int):
        self.url += "&t=" + str(second)


class VideoInfo:
    title: str  # 视频标题
    description: str  # 简介
    upload_time: datetime  # 上传时间
    has_page: bool  # 存在分集
    video_total_duration = 0  # 总时长 单位秒
    video_total_duration_1_25 = 0  # 总时长 单位秒
    video_total_duration_1_5 = 0  # 总时长 单位秒
    video_total_duration_2 = 0  # 总时长 单位秒
    page_list: list[VideoPage]  # 视频分集

    def __init__(self, title: str, description: str, upload_time: str, page_list: list) -> None:
        self.title = title
        self.description = description
        self.upload_time = datetime.strptime(upload_time, "%Y-%m-%d %H:%M:%S")
        self.page_list = page_list
        self.has_page = True
        if len(page_list) == 0:
            self.has_page = False
        for item in self.page_list:
            self.video_total_duration += item.durationSecond
        self.video_total_duration_1_25 = int(0.8 * self.video_total_duration)
        self.video_total_duration_1_5 = int(0.667 * self.video_total_duration)
        self.video_total_duration_2 = int(0.5 * self.video_total_duration)


class BilibiliHtmlResult(HtmlResult):
    videoPageList = []
    videoPageSize = None
    videoTotalDuration = 0

    def __init__(self, title, html_content):
        super().__init__(title, html_content)


class VideoPlan:
    SECOND = 60
    MINUTE = SECOND * 60
    BY_FIFTEEN_MINUTE = MINUTE * 15
    BY_ONE_HOUR = MINUTE * 60

    duration: int
    videoNum: int
    VideoList: list[VideoPage]


def generate_plan_list(list: list[VideoPage], plan: int):
    pass


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, VideoPage):
            return {"title": obj.title, "url": obj.url, "indexInt": obj.indexInt, "indexStr": obj.indexStr,
                    "duration": obj.durationSecond}
        # elif isinstance(obj, array):
        #    return obj.tolist()
        else:
            return json.JSONEncoder.default(self, obj)
