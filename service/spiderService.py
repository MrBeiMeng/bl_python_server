import json
import re

import requests
from bs4 import BeautifulSoup
from obj.classDef import BilibiliVideoPage, BilibiliHtmlResult


def generateBilibiliVideoUrl(vId: str):
    return "https://www.bilibili.com/video/" + vId


def getTargetUrlHtmlPaser(url: str):
    response = requests.get(url=url)
    bs_html = BeautifulSoup(response.text, "html.parser")  # 用html.parser解析器
    return bs_html


def get_bilibili_obj(bilibili_video_url):
    bs_html = getTargetUrlHtmlPaser(bilibili_video_url)
    bilibili_obj: BilibiliHtmlResult = BilibiliHtmlResult(bilibili_video_url, bs_html)
    page_list = getBilibiliVideoPageList(bilibili_video_url)
    for item in page_list:
        bilibili_obj.videoTotalDuration += item.durationSecond
        bilibili_obj.videoPageList.append(page_list)
    bilibili_obj.videoPageSize = len(page_list)

    return bilibili_obj


def getBilibiliVideoPageList(bilibiliVideoUrl):
    bs_html = getTargetUrlHtmlPaser(bilibiliVideoUrl)
    # 创建正则表达式对象，表示规则
    find_link = re.compile(r'"pages":(.*?),"subtitle"')
    spi_result = re.findall(find_link, str(bs_html))

    if len(spi_result) != 0:
        result_list = json.loads(spi_result[0])

        b_video_list = []

        for item in result_list:
            ele = BilibiliVideoPage()
            ele.title = item.get("part")
            ele.indexInt = item.get("page")
            ele.indexStr = "P" + str(item.get("page"))
            ele.url = bilibiliVideoUrl + "?p=" + str(ele.indexInt)
            ele.durationSecond = item.get("duration")
            b_video_list.append(ele)

        return b_video_list
    return []
