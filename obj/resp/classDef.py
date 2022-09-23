from obj.classDef import VideoInfo, VideoPage


def response_conv(func):
    try:
        return func()
    except Exception as e:
        print(e.args)
        return e.args


def format_duration(duration: int) -> str:
    answer_list = []
    num: int = duration
    for i in range(3):
        if num == 0:
            break
        tmp_num = num % 60
        answer_list.append(str(tmp_num))
        num = int(num/60)
    answer_list.reverse()

    return ":".join(answer_list)


class BVideoInfoResponse:
    title: str  # 视频标题
    description: str  # 简介
    upload_time: str  # 上传时间
    video_total_duration: str  # 总时长 单位秒
    page_list = None  # 视频分集

    def __init__(self, video_info: VideoInfo):
        self.title = video_info.title
        self.description = video_info.description
        self.upload_time = video_info.upload_time.strftime("%Y-%m-%d %H:%M:%S")
        self.page_list = video_info.page_list
        if not video_info.has_page:
            self.page_list = ""
        self.video_total_duration = format_duration(video_info.video_total_duration)
