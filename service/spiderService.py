import json
import re
from typing import List

import requests
from bs4 import BeautifulSoup
from obj.classDef import VideoPage, BilibiliHtmlResult, VideoInfo


def generate_bilibili_video_url(vId: str):
    return "https://www.bilibili.com/video/" + vId


def get_target_url_html_paser(url: str):
    response = requests.get(url=url)
    bs_html = BeautifulSoup(response.text, "html.parser")  # 用html.parser解析器
    return bs_html


def get_bilibili_obj(bilibili_video_url):
    bs_html = get_target_url_html_paser(bilibili_video_url)
    bilibili_obj: BilibiliHtmlResult = BilibiliHtmlResult(bilibili_video_url, bs_html)
    page_list = get_bilibili_video_page_list(bilibili_video_url)
    for item in page_list:
        bilibili_obj.videoTotalDuration += item.durationSecond
        bilibili_obj.videoPageList.append(page_list)
    bilibili_obj.videoPageSize = len(page_list)

    return bilibili_obj


def get_bilibili_video_page_list(bilibili_video_url) -> Exception | list[VideoPage]:
    bs_html = get_target_url_html_paser(bilibili_video_url)
    # 创建正则表达式对象，表示规则
    find_link = re.compile(r'"pages":(.*?),"subtitle"')
    spi_result = re.findall(find_link, str(bs_html))

    if len(spi_result) == 0:
        return Exception("爬虫查询失败")
    result_list = json.loads(spi_result[0])

    b_video_list = []

    for item in result_list:
        ele = VideoPage()
        ele.title = item.get("part")
        ele.indexInt = item.get("page")
        ele.indexStr = "P" + str(item.get("page"))
        ele.url = bilibili_video_url + "?p=" + str(ele.indexInt)
        ele.durationSecond = item.get("duration")
        b_video_list.append(ele)

    return b_video_list


def get_bilibili_video_info(b_url) -> Exception | VideoInfo:
    bs_html = get_target_url_html_paser(b_url)
    # 创建正则表达式对象，表示规则
    find_link = re.compile(r'"pages":(.*?),"subtitle"')
    find_upload_time = re.compile(r'"thumbnailUrl"/><meta content="(.*?)"')
    find_title = re.compile(r'<title data-vue-meta="true">(.*?)_哔哩哔哩_bilibili')
    find_desc = re.compile(r'"desc":"(.*?)","desc_v2":')

    pages = re.findall(find_link, str(bs_html))  # 进行异常判断

    upload_time_list = re.findall(find_upload_time, str(bs_html))
    if len(upload_time_list) == 0:
        return Exception("上传时间查询失败")
    upload_time = upload_time_list[0]

    title_list = re.findall(find_title, str(bs_html))
    if len(title_list) == 0:
        return Exception("标题查询失败")
    title = title_list[0]
    description_list = re.findall(find_desc, str(bs_html))
    if len(description_list) == 0:
        return Exception("描述查询失败")
    description = description_list[0]

    b_video_list = []

    for item in json.loads(pages[0]):
        ele = VideoPage()
        ele.title = item.get("part")
        ele.indexInt = item.get("page")
        ele.indexStr = "P" + str(item.get("page"))
        ele.url = b_url + "?p=" + str(ele.indexInt)
        ele.durationSecond = item.get("duration")
        b_video_list.append(ele)

    video_info = VideoInfo(title, description, upload_time, b_video_list)
    return video_info
