from utils.common.video_info import VideoInfo


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
    video_total_duration_1_25: str  # 总时长 单位秒
    video_total_duration_1_5: str  # 总时长 单位秒
    video_total_duration_2: str  # 总时长 单位秒

    def __init__(self, video_info: VideoInfo):
        self.title = video_info.title
        self.description = video_info.description
        self.upload_time = video_info.upload_time.strftime("%Y-%m-%d %H:%M:%S")
        self.video_total_duration = format_duration(video_info.video_total_duration)
        self.video_total_duration_1_25 = format_duration(video_info.video_total_duration_1_25)
        self.video_total_duration_1_5 = format_duration(video_info.video_total_duration_1_5)
        self.video_total_duration_2 = format_duration(video_info.video_total_duration_2)
