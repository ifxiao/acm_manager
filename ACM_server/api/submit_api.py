import os
import sys
sys.path.append(os.path.abspath("../"))

import json
from submits import Submit


from flask import Blueprint, request

submit_api = Blueprint('submit_api', __name__)


def get_from_info(web_form):
    keys = list(web_form.keys())
    json_str = keys[0]
    return json.loads(json_str)


@submit_api.route('/submit/getsubmits/<int:current>/<int:limit>', methods=['post'])
def getsubmits(current, limit):
    print(request.form)
    items = get_from_info(request.form)
    submit = Submit()
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
    user_name = user.get("user_name", None)
    position = user.get("position", 0)
    user_id_find = items.get("user_id", None)
    user_name_find = items.get("user_name", None)
    platform_id = items.get("platform_id", None)
    if user_id_find is None and user_name_find is None:
        if position == 3:
            rows = submit.select_submit_by_id(None, platform_id)
        else:
            rows = submit.select_submit_by_id([user_id], platform_id)
    elif user_id_find is not None and user_id_find != "":
        rows = submit.select_submit_by_id([user_id_find], platform_id)
    elif user_name_find is not None and user_name_find != "":
        rows = submit.select_submit_by_name(user_name_find, platform_id)
    else:
        return {
            "Success": False,
            "code": 20002,
            "message": "登录状态失效"
        }
    platforms = submit.get_platform()
    ret_rows = rows[(current - 1) * limit:min(current * limit, len(rows))]
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "rows": ret_rows,
            "total": len(rows),
            "options": platforms
        }
    }


@submit_api.route('/submit/getlinks/<int:current>/<int:limit>', methods=['post'])
def getlinks(current, limit):
    print(request.form)
    items = get_from_info(request.form)
    submit = Submit()
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
    user_name = user.get("user_name", None)

    user_id_find = items.get("user_id", None)
    user_name_find = items.get("user_name", None)
    platform_id = items.get("platform_id", None)
    if user_id_find is None and user_name_find is None:
        rows = submit.select_links_by_id(None, platform_id)
    elif user_id_find is not None and user_id_find != "":
        rows = submit.select_links_by_id([user_id_find], platform_id)
    elif user_name_find is not None and user_name_find != "":
        rows = submit.select_links_by_name(user_name_find, platform_id)
    else:
        return {
            "Success": False,
            "code": 20002,
            "message": "登录状态失效"
        }

    platforms = submit.get_platform()
    ret_rows = rows[(current - 1) * limit:min(current * limit, len(rows))]
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "rows": ret_rows,
            "total": len(rows),
            "options": platforms
        }
    }

@submit_api.route('/submit/link/delete/<int:Fid>', methods=['delete'])
def delete_link_by_id(Fid):
    submit = Submit()
    message = submit.delete_link_by_id(Fid)
    return {
        "Success": True,
        "code": 20000,
        "message": message,
    }

@submit_api.route('/submit/link/add', methods=['post'])
def add_link():
    # print("test_from", request.form)
    items = get_from_info(request.form)
    # print(len(items))
    Fid = items.get("Fid", None)
    user_id = items.get("user_id", None)
    user_name = items.get("user_name", None)
    platform_id = items.get("platform_id", None)
    link_id = items.get("link_id", None)
    if user_id is None or user_name is None or platform_id is None or link_id is None:
        message = "请填写完整数据"
    else:
        submit = Submit()
        if Fid is None:
            message = submit.insert_one_link(user_id, platform_id, link_id)
        else:
            message = submit.update_one_link(Fid, platform_id, link_id)
    return {
        "Success": True,
        "code": 20000,
        "message": message,
    }

@submit_api.route('/submit/link/getinfo/<int:Fid>', methods=['get'])
def get_link_idfo(Fid):
    submit = Submit()
    link_list = submit.get_link_info(Fid)
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "link": link_list[0],
        }
    }

@submit_api.route('/submit/getoptions', methods=['get'])
def get_options():
    submit = Submit()
    platforms = submit.get_platform()
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "options": platforms
        }
    }
