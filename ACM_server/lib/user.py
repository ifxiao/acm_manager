import util
import setting

class User():
    def __init__(self):
        self.user_id = -1
        self.password = ""
        self.user_name = ""
        self.position = 0
        self.contact = ""
        self.shool = ""
        self.grade = 0
        self.acm_db = None
    
    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_user_name(self, user_name):
        self.user_name = user_name
    
    def set_password(self, password):
        self.password = password

    def set_position(self, position):
        self.position = position
    
    def set_contact(self, contact):
        self.contact = contact

    def set_shool(self, shool):
        self.shool = shool

    def set_grade(self, grade):
        self.grade = grade

    def init(self, user_id, password):#返回值 -1：用户名不存在，-2：密码错误，0：登录成功
        acm_db = util.getConnection(setting.ACM_MANAGER_CONF)
        with acm_db.cursor() as acm_cursor:
            sql = '''
            select Fuser_id, Fpassword, Fposition
            from karl.t_user
            where Fuser_id = {user_id}
            '''.format(user_id = user_id)
            print(sql)
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            if len(results) == 0:
                return -1
            Fuser_id, Fpassword, position = results[0]
            # if position != 3:
            #     return -3
            if user_id != Fuser_id or password != Fpassword:
                # print(f"{user_id} : {Fuser_id}\n{password} : {Fpassword}")
                return -2
            self.user_id = user_id
            self.password = password #session中没必要保存密码，根据安全性可删除

            sql = '''
            select a.Fuser_id, a.Fuser_name, a.Fposition, a.Fcontact, b.Fschool_name, Fgrade
            from 
                karl.t_user a,
                karl.t_school b
            where 
                Fuser_id = {user_id}
                and a.Fschool_id = b.Fschool_id
            '''.format(user_id = user_id)
            # print(sql)
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            if len(results) == 0:
                return -1
            print(results[0])
            self.user_id, self.user_name, self.position, self.contact, self.school_name, self.grade = results[0]
        acm_db.close()
        return 0

if __name__ == '__main__':
    user1 = User()
    ans = user1.init(20175189, "fordream")
    print(ans)