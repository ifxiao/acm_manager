import sys
import os
sys.path.append(os.path.abspath("../"))
import util
import setting
from pymysql.converters import escape_string


class Contest:
    def __init__(self):
        self.acm_db = util.getConnection(setting.ACM_MANAGER_CONF)

    def __del__(self):
        self.acm_db.close()

    def insert_one_contest(self, contest_name, contest_level, team_count, contest_url, years):
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        try:
            sql = '''
                    insert into karl.t_contest(Fcontest_name, Fcontest_level, Fyears, Fteam_count, Fcontest_url, Finsert_time, Fmodify_time)
                    values('{contest_name}', {contest_level}, {years}, {team_count}, '{contest_url}', NOW(), NOW())
                    ON DUPLICATE KEY UPDATE  Fcontest_name = '{contest_name}', Fcontest_level = {contest_level}, Fteam_count = {team_count}, Fcontest_url = '{contest_url}', Fmodify_time = NOW()
                    '''.format(
                contest_name=escape_string(contest_name),
                contest_level=int(contest_level),
                team_count=int(team_count),
                contest_url=escape_string(contest_url),
                years = int(years)
            )
            print(sql)
            with acm_db.cursor() as acm_cursor:
                try:
                    acm_cursor.execute(sql)
                except Exception as e:
                    acm_db.close()
                    return "添加失败：{err}".format(err = str(e))
            acm_db.close()
            return "保存成功"
        except Exception as e:
            acm_db.close()
            return "添加失败：{err}".format(err = str(e))

    def update_one_contest(self, Fid, contest_name, contest_level, team_count, contest_url, years):
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        try:
            sql = '''
                UPDATE  karl.t_contest set Fcontest_name = '{contest_name}', Fcontest_level = {contest_level}, Fteam_count = {team_count}, Fcontest_url = '{contest_url}', Fmodify_time = NOW() where Fcontest_id = {Fid}
                '''.format(
                contest_name=escape_string(contest_name),
                contest_level=int(contest_level),
                team_count=int(team_count),
                contest_url=escape_string(contest_url),
                years=int(years),
                Fid = int(Fid)
            )
            print(sql)
            with acm_db.cursor() as acm_cursor:
                try:
                    acm_cursor.execute(sql)
                except Exception as e:
                    acm_db.close()
                    return "添加/修改失败：{err}".format(err=str(e))
            acm_db.close()
            return "保存成功"
        except Exception as e:
            acm_db.close()
            return "添加/修改失败：{err}".format(err=str(e))

    def select_contest_by_info(self, contest_level = None, contest_name = None, contest_id = None, contest_ids = None, years = None):
        ret_list = list()
        where = "where"
        flg = False
        if contest_level is not None and contest_level != "":
            where += "\na.Fcontest_level = {contest_level}".format(contest_level=contest_level)
            flg = True
        if contest_name is not None and contest_name != "":
            if where != "where":
                where += "\n and "
            where += "\na.Fcontest_name = '{contest_name}'".format(contest_name=contest_name)
            flg = True
        if contest_id is not None and contest_id != "":
            if where != "where":
                where += "\n and "
            where += "\na.Fcontest_id = {contest_id}".format(contest_id=contest_id)
            flg = True
        if contest_ids is not None and contest_ids != "":
            if where != "where":
                where += "\n and "
            where += "\na.Fcontest_id in ({contest_ids})".format(contest_ids=",".join(str(i) for i in contest_ids))
            flg = True

        if years is not None and years != "":
            if where != "where":
                where += "\n and "
            where += "\na.Fyears = {years}".format(years=years)
            flg = True

        sql = '''
        select Fcontest_id, Fcontest_name, Fcontest_level, Fyears, Fteam_count, Fcontest_url, Fmodify_time
        from karl.t_contest a
        
        '''

        if flg:
            sql += where

        sql += "\norder by Fmodify_time desc"
        print(sql)
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        with acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
                results = acm_cursor.fetchall()
                for result in results:
                    contest = dict()
                    contest["contest_id"], contest["contest_name"], level, contest["years"], contest["team_count"], contest["contest_url"], contest["modify_time"] = result
                    level_dict = {
                        1:"校级",
                        2:"省级",
                        3:"国家级"
                    }
                    contest["contest_level"] = level_dict.get(level, "err level_id is {}".format(level))
                    contest["team_count_now"] = self.get_team_count(acm_db, contest["contest_id"])
                    ret_list.append(contest)
            except Exception as e:
                print(str(e))
        acm_db.close()
        return ret_list

    def get_team_count(self, acm_db, contest_id):
        sql = '''
        select count(1)
        from karl.t_contest_team
        where Fcontest_id = {contest_id}
        '''.format(contest_id = contest_id)
        print(sql)
        result = -1
        with acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
                result, = acm_cursor.fetchone()
            except Exception as e:
                print(str(e))
        return result

    def delete_contest_by_id(self, id):
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        sql = '''
        delete from karl.t_contest where Fcontest_id = {id} limit 1
        '''.format(id = int(id))
        with acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                return "删除失败：{}".format(str(e))
        acm_db.close()
        return "删除成功"

    def insert_one_team(self, contest_id, team_id):
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        contest_list = self.select_contest_by_info(contest_id=contest_id)
        if len(contest_list) == 0:
            return "添加失败：该比赛不存在"
        contest = contest_list[0]
        if int(contest["team_count"]) <= int(contest["team_count_now"]):
            return "添加失败：比赛可分配队伍数量已经达到上限"

        try:
            sql = '''
                    insert into karl.t_contest_team(Fcontest_id, Fteam_id, Finsert_time, Fmodify_time)
                    values({contest_id}, {team_id}, NOW(), NOW())
                    ON DUPLICATE KEY UPDATE  Fcontest_id = {contest_id}, Fteam_id = {team_id}, Fmodify_time = NOW()
                    '''.format(
                contest_id=int(contest_id),
                team_id=int(team_id)
            )
            print(sql)
            with acm_db.cursor() as acm_cursor:
                try:
                    acm_cursor.execute(sql)
                except Exception as e:
                    acm_db.close()
                    return "添加/修改失败：{err}".format(err = str(e))
            acm_db.close()
            return "保存成功"

        except Exception as e:
            acm_db.close()
            return "添加/修改失败：{err}".format(err = str(e))

    def select_team_by_contest_id(self, contest_id):
        ret_list = list()
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        sql = '''
                select a.Fteam_id, a.Fteam_grade, a.Fteam_name, a.Fmember1, b.Fuser_name, a.Fmember2, c.Fuser_name, a.Fmember3, d.Fuser_name, a.Fcoach, DATE_FORMAT(a.Fmodify_time,'%Y-%m-%d %H:%i:%s'), e.Fid
                from 
                    karl.t_team a,
                    karl.t_user b,
                    karl.t_user c,
                    karl.t_user d,
                    karl.t_contest_team e
                where
                    e.Fcontest_id = {contest_id}
                    and a.Fteam_id = e.Fteam_id
                    and a.Fmember1 = b.Fuser_id
                    and a.Fmember2 = c.Fuser_id
                    and a.Fmember3 = d.Fuser_id
                    and a.Fstatus = 1
                '''.format(contest_id=int(contest_id))
        print(sql)
        with acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                team = dict()
                team["team_id"], team["grade"], team["team_name"], team["member1"], team["member1_name"], team[
                    "member2"], team["member2_name"], team["member3"], team["member3_name"], team["coach"], team[
                    "modify_time"], team["Fid"] = result
                print(team)
                ret_list.append(team)
        acm_db.close()
        return ret_list


    def delete_contest_team_by_id(self, id):
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        sql = '''
        delete from karl.t_contest_team where Fid = {id} limit 1
        '''.format(id = int(id))
        with acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                return "删除失败：{}".format(str(e))
        acm_db.close()
        return "删除成功"


if __name__ == '__main__':
    team = Contest()
    ans = team.select_team_by_contest_id(4)
