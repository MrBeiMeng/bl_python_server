from datetime import datetime
from utils.common.video_page import VideoPage


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