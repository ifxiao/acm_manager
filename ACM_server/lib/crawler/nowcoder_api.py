from crawler.get import *
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.abspath("../"))
from db_util import ACMdb

class Nowcoder_api:

    def __init__(self):
        self.acmdb = ACMdb()

    def get_page(self, user_id):
        url = "https://ac.nowcoder.com/acm/contest/profile/%s/practice-coding?statusTypeFilter=5" % user_id
        html = get(url)
        soup = BeautifulSoup(html.decode('utf-8'), "html.parser")
        last_page_li = soup.find('li', attrs={'class': 'txt-pager js-last-pager'})
        last_page = last_page_li.a.get('data-page')
        return int(last_page)


    def nowcoder_crawler(self, user_id):
        # user_id = 555354219
        user_id = str(user_id)
        last_page = self.get_page(user_id)
        for page in range(1, last_page+1):
            url = "https://ac.nowcoder.com/acm/contest/profile/{user_id}/practice-coding?&pageSize=10&search=&statusTypeFilter=5&languageCategoryFilter=-1&orderType=DESC&page={page}".format(user_id = user_id, page = page)
            # url = "https://ac.nowcoder.com/acm/contest/profile/%s/practice-coding?statusTypeFilter=5" % user_id
            html = get(url)
            soup = BeautifulSoup(html.decode('utf-8'), "html.parser")
            table = soup.find('table', attrs={'class': 'table-hover'})
            url_head = "https://ac.nowcoder.com"
            for row in table.find_all("tr")[1:]:
                tds = row.find_all("td")
                plaform_id = 3
                submit_id = tds[0].text
                contest_id = -1
                ans = 4
                problem_url = url_head + tds[1].a.get('href')
                problem_id = problem_url.split('/')[-1]
                problem_name = tds[1].text
                code_url = url_head + tds[0].a.get('href')
                self.acmdb.insert_submit(user_id, plaform_id, submit_id, contest_id, problem_id, problem_name, ans, problem_url, code_url)

if __name__ == '__main__':
    nowcoder_api = Nowcoder_api()
    nowcoder_api.nowcoder_crawler(555354219)
    # nowcoder_api.get_page(555354219)
