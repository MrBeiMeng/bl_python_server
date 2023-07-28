class VideoPage:
    title = ""
    url = ""
    indexInt = 0
    indexStr = "P1"
    durationSecond = 0  # 表示视频的播放时间，当播放时间和实际不符时表示要看多久
    comment = ""

    def move_to_second(self, second: int):
        self.url += "&t=" + str(second)