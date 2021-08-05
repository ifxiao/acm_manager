import os
import sys
sys.path.append(os.path.abspath("../"))

import json
# from lib.contest.contest import Contest
from flask import Blueprint, request
from lib.leave import Leave
management_api = Blueprint('management_api', __name__)

leave = Leave()

def get_from_info(web_form):
    keys = list(web_form.keys())
    json_str = keys[0]
    return json.loads(json_str)

def func(dic):
    return dic["submit_id"]

@management_api.route('/Management/leave/add', methods=['post'])
def add_management():
    items = get_from_info(request.form)
    for key, value in items.items():
        print("{key}: {value}   {type_value}".format(
            key = key,
            value = value,
            type_value = type(value)
        ))
    token = items.get("token", None)
    times = items.get("time", None)
    info = items.get("info", None)
    message = ""
    flg = True
    if token is None or token == "":
        message += "用户登录状态失效，请重新登录"
        flg = False
    user = json.loads(token)
    # print(user)
    user_id = user.get('user_id', None)
    if user_id is None:
        message = " 获取用户id失败，请联系管理员"
        return {
            "Success": False,
            "code": 20005,
            "message": message
        }
    if times is None:
        message += " 请假时间不可为空"
        flg = False
    if info is None or info == "":
        message += " 请假原因不可为空"
        flg = False
    if flg is False:
        return {
            "Success": False,
            "code": 20005,
            "message": message
        }
    start_time, end_time = times
    start_time = str(start_time).replace("T", ' ')
    start_time = start_time[:-5]
    end_time = str(end_time).replace("T", ' ')
    end_time = end_time[:-5]
    message = leave.insert_one_leave(user_id, start_time, end_time, info)
    return {
        "Success": True,
        "code": 20000,
        "message": message
    }

@management_api.route('/Management/leave/getList/<int:current>/<int:limit>', methods=['post'])
def getLeave(current, limit):
    print(request.form)
    items = get_from_info(request.form)
    # submit = Submit()
    rows = list()
    token = items.get("token", None)

    if token is None:
        return {
            "Success": False,
            "code": 20002,
            "message": "登录状态失效"
        }
    user = json.loads(token)
    user_id = user.get("user_id", None)
    position = int(user.get("position", 0))
    user_name = user.get("user_name", None)
    user_id_find = items.get("user_id", None)
    if user_id_find is None:
        if position == 3:
            rows = leave.select_leave_by_id()
        else:
            rows = leave.select_leave_by_id(user_id)
    else:
        rows = leave.select_leave_by_id(user_id_find)
    # 这里写获取部分请假列表
    ret_rows = rows[(current - 1) * limit:min(current * limit, len(rows))]
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "rows": ret_rows,
            "total": len(rows)
        }
    }

@management_api.route('/Management/leave/update', methods=['post'])
def update_Leave():
    items = get_from_info(request.form)
    token = items.get("token", None)
    flg = items.get("flg", None)
    id = items.get("id", None)
    message = ""
    if token is None or token == "":
        return {
            "Success": False,
            "code": 20005,
            "message": "用户登录状态失效，请重新登录"
        }
    user = json.loads(token)
    admin_id = user.get('user_id', None)
    if admin_id is None:
        message = " 获取用户id失败，请联系管理员"
        return {
            "Success": False,
            "code": 20005,
            "message": message
        }
    message = leave.update(admin_id, id, flg)

    return {
            "Success": True,
            "code": 20000,
            "message": message
        }

