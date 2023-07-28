from datetime import datetime
import json

from utils.common.video_page import VideoPage


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


class BilibiliHtmlResult(HtmlResult):
    videoPageList = []
    videoPageSize = None
    videoTotalDuration = 0

    def __init__(self, title, html_content):
        super().__init__(title, html_content)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, VideoPage):
            return {"title": obj.title, "url": obj.url, "indexInt": obj.indexInt, "indexStr": obj.indexStr,
                    "duration": obj.durationSecond}
        # elif isinstance(obj, array):
        #    return obj.tolist()
        else:
            return json.JSONEncoder.default(self, obj)
