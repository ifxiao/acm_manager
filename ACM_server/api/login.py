import os
import sys
sys.path.append(os.path.abspath("../"))
from flask_cors import CORS
# from flask import Flask, request
import json
from user import  User
import util
from datetime import timedelta

from flask import Blueprint, request

login_api = Blueprint('login_api', __name__)


@login_api.route("/account")


def get_from_info(web_form):
    keys = list(web_form.keys())
    json_str = keys[0]
    return json.loads(json_str)


@login_api.route('/user/login', methods=['POST'])
def login():
    print("test_from", type(request.form))
    items = get_from_info(request.form)
    user_id = int(items.get("username", ""))
    password = items.get("password", "")
    user = User()
    ans = user.init(user_id, password)
    if ans == -1:
        return {
            "Success": False,
            "code": 20001,
            "message": "该账号不存在",
            "data": {"token": ""}
        }
    elif ans == -2:
        return {
            "Success": False,
            "code": 20001,
            "message": "密码错误",
            "data": {"token": ""}
        }
    elif ans == -3:
        return {
            "Success": False,
            "code": 20003,
            "message": "目前为开user_id:[{user_id}]的登录权限".format(user_id = user_id),
            "data": {"token": ""}
        }
    # token = util.encode_md5(str(user.user_id))
    user.password = "就不告诉你"
    token = json.dumps(user.__dict__)
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {"token": token}
    }


@login_api.route('/user/info', methods=['POST'])
def info():
    items = get_from_info(request.form)
    token = items.get("token", None)

    if token is None:
        return {
            "Success": False,
            "code": 20002,
            "message": "登录状态失效"
        }
    user = json.loads(token)
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "name": user.get("user_name"),
            "roles": [user.get("position", 0)],
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
        }
    }


@login_api.route('/user/logout', methods=['POST'])
def logout():
    print("logout form", request.form)
    items = get_from_info(request.form)
    token = items.get("token", "")

    print("logout token: ", token)
    return {
        "Success": True,
        "code": 20000,
        "message": ""
    }

