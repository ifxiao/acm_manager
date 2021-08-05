import util
import setting
from pymysql.converters import escape_string


class Leave:
    def __init__(self):
        self.acm_db = util.getConnection(setting.ACM_MANAGER_CONF)

    def __del__(self):
        self.acm_db.close()

    def select_leave_by_id(self, user_id=None):
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        ret_list = list()
        flg = True
        sql = '''
        select a.Fid, a.Fuser_id, b.Fuser_name, a.Finfo, DATE_FORMAT(a.Fstart_time,'%Y-%m-%d %H:%i:%s'), DATE_FORMAT(a.Fend_time,'%Y-%m-%d %H:%i:%s'), a.Fstatus, DATE_FORMAT(a.Finsert_time,'%Y-%m-%d %H:%i:%s'), DATE_FORMAT(a.Fmodify_time,'%Y-%m-%d %H:%i:%s')
        from 
            karl.t_leave a,
            karl.t_user b
        where
            a.Fuser_id = b.Fuser_id
        '''
        if user_id is not None:
            sql += "\nand a.Fuser_id = {user_id}".format(user_id = int(user_id))
        status_dict = {
            0:"未审核",
            1:"审核通过",
            2:"已驳回"
        }
        with acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                leave = dict()
                leave["id"], leave["user_id"], leave["user_name"], leave["info"], leave["start_time"], leave["end_time"], status, leave["insert_time"], leave["modify_time"], = result
                leave["status"] = status_dict.get(status, "未审核")
                ret_list.append(leave)
        acm_db.close()
        return ret_list

    def delete_link_by_id(self, Fid):
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        sql = '''
        update karl.t_link set Fstatus = 0 where Fid = {Fid}
        '''.format(Fid = int(Fid))
        with acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                acm_db.close()
                return "删除失败：{err}".format(err = str(e))
        acm_db.close()
        return "删除成功"

    def insert_one_leave(self, user_id, start_time, end_time, info):
        sql = '''
        insert into karl.t_leave(Fuser_id, Finfo, Fstart_time, Fend_time, Finsert_time, Fmodify_time)
        values({user_id}, '{info}', '{start_time}', '{end_time}', NOW(), NOW())
        ON DUPLICATE KEY UPDATE Fuser_id = {user_id}, Finfo = '{info}', Fstart_time = '{start_time}', Fend_time = '{end_time}', Fmodify_time  = NOW()
        '''.format(
            user_id = int(user_id),
            info = escape_string(info),
            start_time = start_time,
            end_time = end_time
        )
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
                # print(sql)
            except Exception as e:
                return "添加/修改失败：{err}".format(err = str(e))
        return "保存成功"

    def update(self, admin_id, leave_id, flg):
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        status = 0
        if flg == True:
            status = 1
        else:
            status = 2
        sql = '''
        update karl.t_leave set Fstatus = {status}, Fadmin = {admin_id} where Fid = {id}
        '''.format(
            status = int(status),
            admin_id = int(admin_id),
            id = int(leave_id)
        )
        print(sql)
        with acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                print(str(e))
                acm_db.close()
                return "审批失败：{err}".format(err=str(e))
        acm_db.close()
        return "审批成功"


    # def get_link_info(self, Fid):
    #     ret_list = list()
    #     sql = '''
    #     select
    #         a.Fuser_id,
    #         b.Fuser_name,
    #         a.Fplatform_id,
    #         a.Flink_id
    #     from
    #         karl.t_link a,
    #         karl.t_user b
    #     where
    #         a.Fid = {Fid}
    #         and a.Fuser_id = b.Fuser_id
    #     '''.format(Fid = int(Fid))
    #     print(sql)
    #     with self.acm_db.cursor() as acm_cursor:
    #         acm_cursor.execute(sql)
    #         results = acm_cursor.fetchall()
    #         for result in results:
    #             link = dict()
    #             link["user_id"], link["user_name"], link["platform_id"], link["link_id"] = result
    #             ret_list.append(link)
    #     return ret_list


if __name__ == '__main__':
    member = Leave()

    ans = member.select_links_by_name("宋福海", 3)
    for i in ans:
        print(i)
