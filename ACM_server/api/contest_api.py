import os
import sys
sys.path.append(os.path.abspath("../"))

import json
from lib.contest.contest import Contest
from flask import Blueprint, request

contest_api = Blueprint('contest_api', __name__)

contest = Contest()

def get_from_info(web_form):
    keys = list(web_form.keys())
    json_str = keys[0]
    return json.loads(json_str)

def func(dic):
    return dic["submit_id"]

@contest_api.route('/contest/add', methods=['post'])
def add_contest():
    items = get_from_info(request.form)
    Fid = items.get("Fid", None)
    contest_name = items.get("contest_name", None)
    contest_level = items.get("contest_level", None)
    years = items.get("years", None)
    team_count = items.get("team_count", None)
    contest_url = items.get("contest_url", None)
    print(items, contest_name, contest_level, team_count, contest_url)
    message = ""
    if Fid is None:
        message = contest.insert_one_contest(contest_name, contest_level, team_count, contest_url, years)
    else:
        message = contest.update_one_contest(Fid, contest_name, contest_level, team_count, contest_url, years)
    return {
        "Success": True,
        "code": 20000,
        "message": message
    }

@contest_api.route('/contest/getList/<int:current>/<int:limit>', methods=['post'])
def get_contest_list(current, limit):
    items = get_from_info(request.form)
    contest_name = items.get("contest_name", None)
    contest_level = items.get("contest_level", None)
    years = items.get("years", None)
    rows = contest.select_contest_by_info(contest_name=contest_name, contest_level=contest_level, years=years)
    for row in rows:
        print(row)
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


@contest_api.route('/contest/delete/<int:Fid>', methods=['delete'])
def delete_contest_by_id(Fid):
    message = contest.delete_contest_by_id(Fid)
    return {
        "Success": True,
        "code": 20000,
        "message": message,
    }

@contest_api.route('/contest/getContest/<int:id>', methods=['get'])
def get_contest(id):
    contest_list = contest.select_contest_by_info(contest_id=id)
    if len(contest_list) == 0:
        return {
            "Success": False,
            "code": 20005,
            "message": "未查询到比赛",
        }
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "contest": contest_list[0],
        }
    }

@contest_api.route('/contest/add_team', methods=['post'])
def add_team():
    items = get_from_info(request.form)
    contest_id = items.get("contest_id", None)
    team_id = items.get("team_id", None)
    message = contest.insert_one_team(contest_id, team_id)
    return {
        "Success": True,
        "code": 20000,
        "message": message
    }

@contest_api.route('/contest/getTeams/<int:id>/<int:current>/<int:limit>', methods=['get'])
def get_teams(id, current, limit):
    rows = contest.select_team_by_contest_id(id)
    for i in rows:
        print(i)
    if len(rows) == 0:
        return {
            "Success": True,
            "code": 20000,
            "message": "",
            "data": {
                "rows": [],
                "total": 0
            }
        }
    ret_rows = rows[(current - 1) * limit:min(current * limit, len(rows))]
    for i in ret_rows:
        print(i)
    return {
        "Success": True,
        "code": 20000,
        "message": "",
        "data": {
            "rows": ret_rows,
            "total": len(rows)
        }
    }

@contest_api.route('/contest/deleteTeam/<int:Fid>', methods=['delete'])
def delete_contest_team_by_id(Fid):
    message = contest.delete_contest_team_by_id(Fid)
    return {
        "Success": True,
        "code": 20000,
        "message": message,
    }
