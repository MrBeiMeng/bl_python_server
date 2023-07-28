from utils.common.video_page import VideoPage


class VideoPlan:
    SECOND = 60
    MINUTE = SECOND * 60
    BY_FIFTEEN_MINUTE = MINUTE * 15
    BY_ONE_HOUR = MINUTE * 60

    duration: int
    videoNum: int
    VideoList: list[VideoPage]