import datetime

from utils.common.common import MyTime

detailed_ebbinghaus_duration = [  # 11
    MyTime.MINUTE * 5, MyTime.MINUTE * 30, MyTime.HOUR * 12, MyTime.DAY, MyTime.DAY * 2, MyTime.DAY * 4, MyTime.DAY * 7,
    MyTime.DAY * 15, MyTime.MOUTH * 1, MyTime.MOUTH * 3, MyTime.MOUTH * 6
]

simple_ebbinghaus_duration = [  # 9
    MyTime.MINUTE * 30, MyTime.DAY, MyTime.DAY * 2, MyTime.DAY * 4, MyTime.DAY * 7, MyTime.DAY * 15, MyTime.MOUTH * 1,
    MyTime.MOUTH * 3, MyTime.MOUTH * 6
]

shortly_ebhs_duration = [  # 6
    MyTime.MINUTE * 5, MyTime.MINUTE * 30, MyTime.HOUR * 12, MyTime.DAY, MyTime.DAY * 2, MyTime.DAY * 4,
]


class EbbinghausType:
    _type = 1

    def __init__(self, type_of_duration: int):
        self._type = type_of_duration

    def get_duration(self):
        if self._type == 0:
            return detailed_ebbinghaus_duration
        if self._type == 2:
            return shortly_ebhs_duration
        return simple_ebbinghaus_duration


def get_day_list_from_today(duration_type: EbbinghausType):
    duration_list = duration_type.get_duration()
    now_time = datetime.datetime.now()
    result_date_list = []
    for ele in duration_list:
        tmp_datetime = now_time + datetime.timedelta(seconds=ele)
        result_date_list.append(tmp_datetime.strftime("%Y年%m月%d日 %H:%M"))
    return result_date_list
