import util
import setting
import pymysql
from pymysql.converters import escape_string
import sys
import os
sys.path.append(os.path.abspath("../"))
from db_util import ACMdb

class HustOJ_api:
    def __init__(self):
        self.hust_db = util.getConnection(setting.HUSTOJ_ONLINE_CONF, ssh_status=True)

    def __del__(self):
        self.hust_db.close()

    def hustoj_online_crawler(self, user_id_list):
        acm_db = ACMdb()
        with self.hust_db.cursor() as hust_cursor:
            for user_ids in util.divide_list(user_id_list, 50):
                sql = '''
                    select a.solution_id, a.problem_id, b.title, a.user_id, a.contest_id, a.result
                    from 
                        jol.solution a,
                        jol.problem b
                    where a.user_id in ('{user_id}')
                    and a.result = 4
                    and a.problem_id = b.problem_id
                    '''.format(
                    user_id = escape_string(",".join(str(i) for i in user_ids))
                )
                hust_cursor.execute(sql)
                results = hust_cursor.fetchall()
                for result in results:
                    submit_id, problem_id, problem_name, user_id, contest_id, ans = result
                    problem_url = "https://acm.hdcsti.com/problem.php?id={problem_id}".format(problem_id=problem_id)
                    code_url = "https://acm.hdcsti.com/showsource.php?id={submit_id}".format(submit_id=submit_id)
                    plaform_id = 1
                    print(user_id, plaform_id, submit_id, contest_id, problem_id, problem_name, ans, problem_url, code_url)
                    acm_db.insert_submit(user_id, plaform_id, submit_id, contest_id, problem_id, problem_name, ans, problem_url, code_url)


if __name__ == '__main__':
    hust_api = HustOJ_api()
    hust_api.hustoj_online_crawler(["admin"])
