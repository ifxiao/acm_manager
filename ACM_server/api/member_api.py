import os
import sys
sys.path.append(os.path.abspath("../"))

import json
from member import Member


from flask import Blueprint, request

member_api = Blueprint('member_api', __name__)


def get_from_info(web_form):
    keys = list(web_form.keys())
    json_str = keys[0]
    return json.loads(json_str)


@member_api.route('/member/pagememberCondition/<int:current>/<int:limit>', methods=['post'])
def getmembers(current, limit):
    items = get_from_info(request.form)
    member = Member()
    rows = list()
    user_id = items.get("user_id", None)
    user_name = items.get("user_name", None)
    grade = items.get("grade", None)
    rows = member.select_member_by_info(user_id = user_id, user_name = user_name, grade = grade)
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


@member_api.route('/member/getMember/<int:user_id>', methods=['get'])
def getmember(user_id):
    member = Member()
    member_list = member.select_member_by_info(user_id = user_id)
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "member": member_list[0],
        }
    }

@member_api.route('/member/delete/<int:user_id>', methods=['delete'])
def delete_member(user_id):
    # print(user_id)
    member = Member()
    message = member.delete_member_by_id(user_id = user_id)
    return {
        "Success": True,
        "code": 20000,
        "message": message,
    }

@member_api.route('/member/add', methods=['post'])
def add_member():
    # print("test_from", request.form)
    items = get_from_info(request.form)
    # print(len(items))
    user_id = items.get("user_id", None)
    user_name = items.get("user_name", None)
    grade = items.get("grade", None)
    contact = items.get("contact", None)
    if user_id is None or user_name is None or grade is None or contact is None:
        message = "请填写完整数据"
    else:
        member = Member()
        message = member.insert_one_member(user_id, user_name, contact, grade)
    return {
        "Success": True,
        "code": 20000,
        "message": message
    }