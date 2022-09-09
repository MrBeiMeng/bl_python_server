from fastapi import APIRouter

from service import ebbinghaus_service
from service.ebbinghaus_service import EbbinghausType

app = APIRouter()
prefix = "/ebhs"
tags = ["艾宾浩斯"]


@app.get("/getDayList")
def get_day_list(type_num: int):
    duration_type = EbbinghausType(type_num)
    date_list = ebbinghaus_service.get_day_list_from_today(duration_type)
    data_list_str = "|".join(date_list)
    return data_list_str
