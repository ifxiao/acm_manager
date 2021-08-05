import util
import setting
from pymysql.converters import escape_string

class ACMdb:
    def __init__(self):
        self.acm_db = util.getConnection(setting.ACM_MANAGER_CONF)

    def __del__(self):
        self.acm_db.close()

    def insert_submit(self, user_id, plaform_id, submit_id, contest_id, problem_id, problem_name, ans, problem_url, code_url):
        sql = '''
        insert into karl.t_submit(Flink_id, Fplatform_id, Fsubmit_id_link, Fcontest_id, Fproblem_id, Fproblem_name, Fresult, Fproblem_url, Fcode_url, Finsert_time, Fmodify_time)
        values('{user_id}', {plaform_id}, {submit_id}, {contest_id}, '{problem_id}', '{problem_name}', {ans}, '{problem_url}', '{code_url}', NOW(), NOW())
        '''.format(
            user_id = escape_string(user_id),
            plaform_id = int(plaform_id),
            submit_id = int(submit_id),
            contest_id = int(contest_id),
            problem_id = escape_string(str(problem_id)),
            problem_name = escape_string(problem_name),
            ans = int(ans),
            problem_url = escape_string(problem_url),
            code_url = escape_string(code_url)
        )
        print(sql)
        with self.acm_db.cursor() as acm_cursor:
            try:
                acm_cursor.execute(sql)
            except Exception as e:
                print(e)

