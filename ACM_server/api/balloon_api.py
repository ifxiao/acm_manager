import os
import sys
sys.path.append(os.path.abspath("../"))

import json
from contest.balloon import Contest_balloon


from flask import Blueprint, request

balloon_api = Blueprint('balloon_api', __name__)
balloon = Contest_balloon()


def get_from_info(web_form):
    keys = list(web_form.keys())
    json_str = keys[0]
    return json.loads(json_str)

def func(dic):
    return dic["submit_id"]

@balloon_api.route('/contest/balloon/<int:current>/<int:limit>', methods=['post'])
def getmembers(current, limit):
    print(request.form)
    items = get_from_info(request.form)
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
    print(user_id, user_name)
    rows = balloon.select_ac()

    rows = sorted(rows, key=func, reverse=True)
    # for i in rows:
    #     print(i)
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

@balloon_api.route('/contest/addballoon', methods=['post'])
def addballoon():
    print(request.form)
    items = get_from_info(request.form)
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
    submit_user_id = items.get("user_id", None)
    submit_id = items.get("submit_id")

    balloon.add_balloon2list(submit_user_id, submit_id)
    return {
        "Success": True,
        "code": 20000,
        "message": "",
    }
