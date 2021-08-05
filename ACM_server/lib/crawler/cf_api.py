import codeforces_api
import sys
import os
sys.path.append(os.path.abspath("../"))
from db_util import ACMdb

class CF_api:
    def __init__(self):
        self.acm_db = ACMdb()
        key = '4a1e08f638c0a0c5ae43b1ea7129693f98a7daaa'
        secret = 'd9b9680007a149083df97a4509339e0f9c2a4a09'
        self.cf_api = codeforces_api.CodeforcesApi(key, secret)



    def codeforces_submit_crawler(self, user_id):
        plaform_id = 2
        results = self.cf_api.user_status(user_id)
        for result in results:
            submit_id = result.id
            problem = result.problem
            contest_id = problem.contest_id
            code_url = "http://codeforces.com/problemset/submission/{contest_id}/{submit_id}".format(
                contest_id=contest_id, submit_id=submit_id)
            problem_index = problem.index
            problem_id = "{contest_id}-{problem_index}".format(contest_id=contest_id, problem_index=problem_index)
            problem_url = "http://codeforces.com/problemset/problem/{contest_id}/{problem_index}".format(
                contest_id=contest_id, problem_index=problem_index)
            problem_name = problem.name
            # print(problem)
            verdict = result.verdict
            ans = 0
            if verdict == 'OK':
                ans = 4
            else:
                continue
            self.acm_db.insert_submit(user_id, plaform_id, submit_id, contest_id, problem_id, problem_name, ans, problem_url, code_url)

if __name__ == '__main__':
    cf_api = CF_api()
    cf_api.codeforces_submit_crawler('Syins')