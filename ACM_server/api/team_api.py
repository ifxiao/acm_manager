import os
import sys
sys.path.append(os.path.abspath("../"))

import json
from team import  Team


from flask import Blueprint, request

team_api = Blueprint('team_api', __name__)


@team_api.route("/account")

def get_from_info(web_form):
    keys = list(web_form.keys())
    json_str = keys[0]
    return json.loads(json_str)


@team_api.route('/team/teamdata', methods=['get'])
def teamdata():
    print("test_from", type(request.args))

    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "items":[{
                "label": '2017级',
                "children": [{
                  "label": '17 一队',
                  "children": [{
                    "label": '杨可浩'
                  }, {
                    "label": '何文彬'
                  },
                  {
                    'label': "盛诗曼"
                  }]
                }]
              },
              {
                "id": 2,
                'label': '2018级',
                'children': [{
                  'label': '18级一队'
                }, {
                  'label': '18级2队'
                }]
              }, {
                'label': '2019级',
                'children': [{
                  'label': '19级1队'
                }, {
                  'label': '19级2队'
                }]
              }]
        }
    }

@team_api.route('/team/teams/<int:current>/<int:limit>', methods=['post'])
def getteams(current, limit):
    print(request.form)
    items = get_from_info(request.form)
    team = Team()
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
    grade = items.get("grade", None)
    if user_id_find is None and user_name_find is None:
        if int(position) == 3:
            rows = team.get_team_by_info(user_id = None, grade = grade)
        else:
            rows = team.get_team_by_info(user_id = user_id, grade = grade)

    elif user_id_find is not None and user_id_find != "":
        rows = team.get_team_by_info(user_id = user_name_find, grade = grade)
    elif user_name_find is not None and user_name_find != "":
        rows = team.get_team_by_info(user_name = user_name_find, grade = grade)
    else:
        return {
            "Success": False,
            "code": 20002,
            "message": "登录状态失效"
        }
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

@team_api.route('/team/delete/<int:Fid>', methods=['delete'])
def delete_link_by_id(Fid):
    team = Team()
    message = team.delete_team_by_id(Fid)
    return {
        "Success": True,
        "code": 20000,
        "message": message,
    }

@team_api.route('/team/add', methods=['post'])
def add_team():
    items = get_from_info(request.form)
    team_id = items.get("team_id", None)
    grade = items.get("grade", None)
    team_name = items.get("team_name", None)
    member1 = items.get("member1", None)
    member2 = items.get("member2", None)
    member3 = items.get("member3", None)
    coach = items.get("coach", None)

    if grade is None or team_name is None or member1 is None or member2 is None or member3 is None or coach is None:
        message = "请填写完整数据"
    else:
        team = Team()
        if team_id is None or team_id == "":
            message = team.insert_one_team(grade, team_name, member1, member2, member3, coach)
        else:
            message = team.update_one_item(team_id, grade, team_name, member1, member2, member3, coach)
    return {
        "Success": True,
        "code": 20000,
        "message": message,
    }

@team_api.route('/team/checkMember', methods=['post'])
def check_member():
    items = get_from_info(request.form)
    member1 = items.get("member1", -1)
    member2 = items.get("member2", -1)
    member3 = items.get("member3", -1)
    team = Team()
    ret = dict()
    ret["member1_name"] = team.get_member_name(member1)
    ret["member2_name"] = team.get_member_name(member2)
    ret["member3_name"] = team.get_member_name(member3)
    code = 20000
    message = ""
    success = True
    if ret["member1_name"] is None or ret["member2_name"] is None or ret["member3_name"] is None:
        code = 20005
        message = "学号输入错误"
        success = False
    return {
        "Success": success,
        "code": code,
        "message": message,
        "data": {
            "member": ret
        }
    }

@team_api.route('/team/getTeam/<int:team_id>', methods=['get'])
def get_team(team_id):
    team = Team()
    print(team_id)
    team_list = team.get_team_by_id(team_id)
    if len(team_list) < 1:
        return {
            "Success": False,
            "code": 20005,
            "message": "未查询到队伍",
        }
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "team": team_list[0],
        }
    }


