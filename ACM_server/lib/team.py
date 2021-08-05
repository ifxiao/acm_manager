import util
import setting
from pymysql.converters import escape_string


class Team:
    def __init__(self):
        self.acm_db = util.getConnection(setting.ACM_MANAGER_CONF)

    def __del__(self):
        self.acm_db.close()

    def get_team_by_info(self, user_id = None, user_name = None, grade = None):
        ret_list = list()
        sql = '''
        select a.Fteam_id, a.Fteam_grade, a.Fteam_name, a.Fmember1, b.Fuser_name, a.Fmember2, c.Fuser_name, a.Fmember3, d.Fuser_name, a.Fcoach, DATE_FORMAT(a.Fmodify_time,'%Y-%m-%d %H:%i:%s')
        from 
            karl.t_team a,
            karl.t_user b,
            karl.t_user c,
            karl.t_user d
        where
            a.Fmember1 = b.Fuser_id
            and a.Fmember2 = c.Fuser_id
            and a.Fmember3 = d.Fuser_id
            and a.Fstatus = 1
        '''
        if user_id is not None and user_id != "" and (user_name is None or user_name == ""):
            sql += "\nand (a.Fmember1 = {user_id} or a.Fmember2 = {user_id} or a.Fmember3 = {user_id})".format(user_id = user_id)
        elif user_name is not None and user_name != "" and (user_id is None or user_id == ""):
            sql += "\nand (b.Fuser_name = '{user_name}' or c.Fuser_name = '{user_name}' or d.Fuser_name = '{user_name}')".format(user_name = user_name)
        elif user_id is not None and user_id != "" and user_name is not None and user_name != "":
            sql += '''\nand ((b.Fuser_name = '{user_name}' and a.Fmember1 = {user_id})
            or (c.Fuser_name = '{user_name}' and a.Fmember2 = {user_id})
            or (d.Fuser_name = '{user_name}' and a.Fmember3 = {user_id}))'''.format(user_id = user_id, user_name = user_name)
        if grade is not None and grade != "":
            sql += "\nand a.Fteam_grade = {grade}".format(grade = grade)
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                team = dict()
                team["team_id"], team["grade"], team["team_name"], team["member1"], team["member1_name"], team["member2"], team["member2_name"], team["member3"], team["member3_name"], team["coach"], team["modify_time"] = result
                ret_list.append(team)
        return ret_list

    def delete_team_by_id(self, team_id):
        sql = '''
                update karl.t_team set Fstatus = -1 where Fteam_id = {team_id}
                '''.format(team_id=team_id)
        with self.acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                return "删除失败：{err}".format(err=str(e))
        return "删除成功"

    def insert_one_team(self, team_grade, team_name, member1, member2, member3, coach):
        sql = '''
                insert into karl.t_team(Fteam_grade, Fteam_name, Fmember1, Fmember2, Fmember3, Fcoach, Fstatus, Finsert_time, Fmodify_time)
                values({team_grade}, '{team_name}', {member1}, {member2}, {member3}, '{coach}', 1, NOW(), NOW())
                ON DUPLICATE KEY UPDATE  Fteam_grade = {team_grade}, Fteam_name = '{team_name}', Fmember1 = {member1}, Fmember2 = {member2}, Fmember3 = {member3}, Fcoach = '{coach}', Fstatus = 1, Fmodify_time = NOW()
                '''.format(
            team_grade=int(team_grade),
            team_name=escape_string(team_name),
            member1=int(member1),
            member2=int(member2),
            member3=int(member3),
            coach=escape_string(coach)
        )
        with self.acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                return "添加/修改失败：{err}".format(err = str(e))
        return "保存成功"

    def update_one_item(self, team_id, team_grade, team_name, member1, member2, member3, coach):
        sql = '''
        update karl.t_team set  Fteam_grade = {team_grade}, Fteam_name = '{team_name}', Fmember1 = {member1}, Fmember2 = {member2}, Fmember3 = {member3}, Fcoach = '{coach}', Fmodify_time = NOW()
        where Fteam_id = {team_id}
        '''.format(
            team_grade=int(team_grade),
            team_name=escape_string(team_name),
            member1=int(member1),
            member2=int(member2),
            member3=int(member3),
            coach=escape_string(coach),
            team_id = int(team_id)
        )
        with self.acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                return "修改失败：{err}".format(err = str(e))
        return "保存成功"

    def get_team_by_id(self, team_id):
        ret_list = list()
        sql = '''
        select a.Fteam_id, a.Fteam_grade, a.Fteam_name, a.Fmember1, b.Fuser_name, a.Fmember2, c.Fuser_name, a.Fmember3, d.Fuser_name, a.Fcoach, DATE_FORMAT(a.Fmodify_time,'%Y-%m-%d %H:%i:%s')
        from 
            karl.t_team a,
            karl.t_user b,
            karl.t_user c,
            karl.t_user d
        where
            a.Fteam_id = {team_id}
            and a.Fmember1 = b.Fuser_id
            and a.Fmember2 = c.Fuser_id
            and a.Fmember3 = d.Fuser_id
            and a.Fstatus = 1
        '''.format(team_id = team_id)
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                team = dict()
                team["team_id"], team["grade"], team["team_name"], team["member1"], team["member1_name"], team[
                    "member2"], team["member2_name"], team["member3"], team["member3_name"], team["coach"], team[
                    "modify_time"] = result

                ret_list.append(team)
        return ret_list

    def get_member_name(self, member_id):
        sql = '''
        select Fuser_name
        from karl.t_user
        where Fuser_id = {member_id}
        '''.format(member_id = member_id)
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            user_dict = dict()
            if len(results) == 0:
                return None
            user_dict["name"], = results[0]
        return user_dict["name"]

if __name__ == '__main__':
    team = Team()
    ans = team.get_team_by_info(user_id = 20196126)
    # ans = team.get_team_by_info(user_id = 20196917,user_name = "丁浩康", grade = 2019)
    # team.delete_team_by_id(1)
    # ans = team.get_team_by_info(grade=2019)
    for i in ans:
        print(i)
    # ans = team.insert_one_team(2017, 'test_team3', 20175189, 20172777, 20194771, '金虎')
    # print(ans)