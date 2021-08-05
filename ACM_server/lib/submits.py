import util
import setting
from pymysql.converters import escape_string


class Submit:
    def __init__(self):
        self.acm_db = util.getConnection(setting.ACM_MANAGER_CONF)

    def __del__(self):
        self.acm_db.close()

    def select_submit_by_id(self, user_ids, platform = None):
        ret_list = list()
        flg = True
        sql = '''
        select a.Fuser_id, d.Fuser_name, b.Flink_id, c.Fplatform_name, b.Fsubmit_id_link, b.Fcontest_id, b.Fproblem_id, b.Fproblem_name, b.Fresult, b.Fproblem_url, b.Fcode_url, DATE_FORMAT(b.Finsert_time,'%Y-%m-%d %H:%i:%s')
        from 
            karl.t_link a,
            karl.t_submit b,
            karl.t_platform c,
            karl.t_user d
        where 
            a.Flink_id = b.Flink_id
            and b.Fplatform_id = c.Fplatform_id
            and a.Fuser_id = d.Fuser_id
        '''
        if user_ids is not None:
            sql += "\n and a.Fuser_id in ({user_ids})".format(user_ids = ",".join(str(i) for i in user_ids))
        if platform != None and platform != "":
            sql += "\n and a.Fplatform_id = {platform}".format(platform = platform)
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                submit = dict()
                submit["user_id"],submit["user_name"],submit["link_id"],submit["platform_name"],submit["submit_id_link"],submit["contest_id"],submit["problem_id"],submit["problem_name"],submit["result"],submit["problem_url"],submit["code_url"], submit["insert_time"] = result
                ret_list.append(submit)
        return ret_list

    def select_submit_by_name(self, user_name, platform = None):
        ret_list = list()
        sql = '''
        select a.Fuser_id, d.Fuser_name, b.Flink_id, c.Fplatform_name, b.Fsubmit_id_link, b.Fcontest_id, b.Fproblem_id, b.Fproblem_name, b.Fresult, b.Fproblem_url, b.Fcode_url, DATE_FORMAT(b.Finsert_time,'%Y-%m-%d %H:%i:%s')
        from 
            karl.t_link a,
            karl.t_submit b,
            karl.t_platform c,
            karl.t_user d
        where 
            d.Fuser_name = '{user_name}'
            and a.Flink_id = b.Flink_id
            and b.Fplatform_id = c.Fplatform_id
            and a.Fuser_id = d.Fuser_id
        '''.format(user_name = user_name)
        if platform != None and platform != "":
            sql += "\n and a.Fplatform_id = {platform}".format(platform = platform)
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                submit = dict()
                submit["user_id"],submit["user_name"],submit["link_id"],submit["platform_name"],submit["submit_id"], submit["contest_id"],submit["problem_id"],submit["problem_name"],submit["result"],submit["problem_url"],submit["code_url"], submit["insert_time"] = result
                ret_list.append(submit)
        return ret_list

    def get_platform(self):
        ret_list = list()
        sql = '''
        select Fplatform_id, Fplatform_name
        from karl.t_platform
        '''
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                platform = dict()
                platform["value"], platform["label"] = result
                ret_list.append(platform)
        return ret_list

    def select_links_by_id(self, user_ids, platform = None):
        ret_list = list()
        sql = '''
        select a.Fid, a.Fuser_id, b.Fuser_name, c.Fplatform_name, a.Flink_id, DATE_FORMAT(a.Fmodify_time,'%Y-%m-%d %H:%i:%s')
        from 
            karl.t_link a,
            karl.t_user b,
            karl.t_platform c
        where 
            a.Fuser_id = b.Fuser_id
            and a.Fplatform_id = c.Fplatform_id
            and a.Fstatus = 1
        '''
        if platform != None and platform != "":
            sql += "\n and a.Fplatform_id = {platform}".format(platform = platform)

        if user_ids is not None:
            sql += "\nand  a.Fuser_id in ({user_ids})".format(user_ids = ",".join(str(i) for i in user_ids))
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                link = dict()
                link["link"], link["user_id"], link["user_name"], link["platform_name"], link["link_id"], link["modify_time"] = result
                ret_list.append(link)
        return ret_list

    def select_links_by_name(self, user_name, platform = None):
        ret_list = list()
        sql = '''
        select a.Fid, a.Fuser_id, b.Fuser_name, c.Fplatform_name, a.Flink_id, DATE_FORMAT(a.Fmodify_time,'%Y-%m-%d %H:%i:%s')
        from 
            karl.t_link a,
            karl.t_user b,
            karl.t_platform c
        where 
            b.Fuser_name = '{user_name}'
            and a.Fuser_id = b.Fuser_id
            and a.Fplatform_id = c.Fplatform_id
            and a.Fstatus = 1
        '''.format(user_name = user_name)
        if platform != None and platform != "":
            sql += "\n and a.Fplatform_id = {platform}".format(platform = platform)
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                link = dict()
                link["link"], link["user_id"], link["user_name"], link["platform_name"], link["link_id"], link["modify_time"] = result
                ret_list.append(link)
        return ret_list

    def delete_link_by_id(self, Fid):
        sql = '''
        update karl.t_link set Fstatus = 0 where Fid = {Fid}
        '''.format(Fid = int(Fid))
        with self.acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                return "删除失败：{err}".format(err = str(e))
        return "删除成功"

    def insert_one_link(self, user_id, platform_id, link_id):
        sql = '''
        insert into karl.t_link(Fuser_id, Fplatform_id, Flink_id, Fstatus, Finsert_time, Fmodify_time)
        values({user_id}, {platform_id}, '{link_id}', 1, NOW(), NOW())
        ON DUPLICATE KEY UPDATE Fuser_id = {user_id}, Fplatform_id = {platform_id}, Flink_id = '{link_id}', Fmodify_time  = NOW(), Fstatus = 1
        '''.format(
            user_id = int(user_id),
            platform_id = int(platform_id),
            link_id = escape_string(link_id)
        )
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                return "添加/修改失败：{err}".format(err = str(e))
        return "保存成功"

    def update_one_link(self, Fid, platform_id, link_id):
        sql = '''
        update karl.t_link set Fplatform_id = {platform_id}, Flink_id = '{link_id}' where Fid = {Fid}
        '''.format(
            Fid = int(Fid),
            platform_id = int(platform_id),
            link_id = escape_string(link_id)
        )
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                return "添加/修改失败：{err}".format(err=str(e))
        return "保存成功"



    def get_link_info(self, Fid):
        ret_list = list()
        sql = '''
        select 
            a.Fuser_id,
            b.Fuser_name,
            a.Fplatform_id,
            a.Flink_id
        from 
            karl.t_link a,
            karl.t_user b
        where 
            a.Fid = {Fid}
            and a.Fuser_id = b.Fuser_id
        '''.format(Fid = int(Fid))
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                link = dict()
                link["user_id"], link["user_name"], link["platform_id"], link["link_id"] = result
                ret_list.append(link)
        return ret_list

    def select_count_by_userid(self, user_id):
        sql = '''
        select count(1)
        from 
            karl.t_link a,
            karl.t_submit b
        where
            a.Flink_id = b.Flink_id
            and a.Fuser_id = {user_id}
        '''.format(user_id = user_id)
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            return results[0][0]

if __name__ == '__main__':
    member = Submit()

    # ans = member.select_submit_by_id([20194771])
    # ans = member.select_submit_by_name('宋福海', 3)
    # ans = member.select_platform()
    ans = member.select_links_by_name("宋福海", 3)
    for i in ans:
        print(i)
