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
    htmlContent = None  # 抓取结果
    createAt = None
    savingFileName = None

    def __init__(self, title, htmlContent):
        self.title = title
        self.htmlContent = htmlContent
        self.createAt = datetime.now().strftime("%y-%m-%d %H:%M")
        self.savingFileName = "抓取结果" + self.title + self.createAt + ".html"

    def save(self):
        file = open(self.savingFileName, "w", encoding="utf-8")
        file.write(self.htmlContent)
        file.close()


class BilibiliVideoPage:
    title = ""
    url = ""
    indexInt = 0
    indexStr = "P1"
    durationSecond = 0

    def moveToSecond(self, second: int):
        self.url += "&t=" + str(second)


class BilibiliHtmlResult(HtmlResult):
    videoPageList = []
    videoPageSize = None
    videoTotalDuration = 0

    def __init__(self, title, htmlContent):
        super().__init__(title, htmlContent)


class VideoPlan:
    SECOND = 60
    MINUTE = SECOND * 60
    BY_FIFTEEN_MINUTE = MINUTE * 15
    BY_ONE_HOUR = MINUTE * 60

    duration: int
    videoNum: int
    VideoList: list[BilibiliVideoPage]


def generatePlanList(list: list[BilibiliVideoPage], plan: int):
    pass


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BilibiliVideoPage):
            return {"title": obj.title, "url": obj.url, "indexInt": obj.indexInt, "indexStr": obj.indexStr,
                    "duration": obj.durationSecond}
        # elif isinstance(obj, array):
        #    return obj.tolist()
        else:
            return json.JSONEncoder.default(self, obj)
