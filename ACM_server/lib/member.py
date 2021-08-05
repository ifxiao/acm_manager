import util
import setting
from pymysql.converters import escape_string
from submits import Submit

class Member:
    def __init__(self):
        self.acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        self.position_dict = {
            1:"管理员",
            3:"管理员",
            0:"成员"
        }

    def __del__(self):
        self.acm_db.close()

    def select_member_all(self):
        ret_list = list()
        sql = '''
        select a.Fuser_id, a.Fuser_name, a.Fposition, a.Fcontact, b.Fschool_name, Fgrade
        from 
            karl.t_user a,
            karl.t_school b
        '''
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            if len(results) == 0:
                return -1
            print(results[0])

            for result in results:
                list_node = dict()
                list_node['user_id'], list_node['user_name'], position, list_node['contact'], list_node['school'], list_node['grade'] = result
                list_node['position'] = self.position_dict.get(position, "position err [position_id : %s]" % position)
                list_node['score'] = 1000
                ret_list.append(list_node)

        return ret_list

    def select_member_by_info(self, user_id = None, user_name = None, grade = None):
        ret_list = list()
        where = "where"
        flg = False
        if user_id is not None and user_id != "":
            where += "\na.Fuser_id = {user_id}".format(user_id = user_id)
            flg = True
        if user_name is not None and user_name != "":
            if where != "where":
                where += "\n and "
            where += "\na.Fuser_name = '{user_name}'".format(user_name = user_name)
            flg = True
        if grade is not None and grade != "":
            if where != "where":
                where += "\n and "
            where += "\na.Fgrade = {grade}".format(grade = grade)
            flg = True
        if where != "where":
            where += "\n and "
        where += "\na.Fstatus > 0"
        flg = True
        sql = '''
        select a.Fuser_id, a.Fuser_name, a.Fposition, a.Fcontact, b.Fschool_name, Fgrade
        from 
            karl.t_user a,
            karl.t_school b
        
        '''
        if flg:
            sql = sql + where
        print(sql)
        submit = Submit()
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                member = dict()
                member['user_id'], member['user_name'], position, member['contact'], member['school'], member['grade'] = result
                member['position'] = self.position_dict.get(position, "position err [position_id : %s]" % position)
                member['score'] = submit.select_count_by_userid(member['user_id'])
                ret_list.append(member)

        return ret_list

    def delete_member_by_id(self, user_id):
        sql = '''
        update karl.t_user set Fstatus = -1 where Fuser_id = {user_id}
        '''.format(user_id = user_id)
        with self.acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                return "删除失败：{err}".format(err = str(e))
        return "删除成功"

    def insert_one_member(self, user_id, user_name,contact, grade):
        sql = '''
        insert into karl.t_user(Fuser_id, Fpassword, Fuser_name, Fposition, Fcontact, Fschool_id, Fgrade, Fstatus, Finsert_time, Fmodify_time)
        values({user_id}, '{user_id}', '{user_name}', 0, '{contact}', 1, {grade}, 1, NOW(), NOW())
        ON DUPLICATE KEY UPDATE Fuser_name = '{user_name}', Fcontact = '{contact}', Fgrade = {grade}, Fstatus = 1, Fmodify_time = NOW()
        '''.format(
            user_id = int(user_id),
            user_name = escape_string(user_name),
            contact = escape_string(contact),
            grade = int(grade)
        )
        with self.acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                return "添加/修改失败：{err}".format(err = str(e))
        return "保存成功"

if __name__ == '__main__':
    member = Member()
    # ans_list = member.select_member_by_info(user_id=2019471, user_name= "宋福海", grade = 2019)
    # print(ans_list)
    # for i in ans_list:
    #     print(i)
    ans = member.insert_one_member(20196126, "华业鑫", "12345678901", 2019)
    print(ans)
