import util
import setting
import os
import contest.balloon_conf as balloon_conf
from pymysql.converters import escape_string


class Contest_balloon:
    def __init__(self):
        self.acm_db = util.getConnection(setting.HUSTOJ_ONLINE_CONF,ssh_status=True)
        # self.acm_db = util.getConnection(setting.HUSTOJ_CONTEST_CONF,
        #                                  ssh_status=True,
        #                                  SSH_TUNNEL_CONF=setting.SSH_CONNTEST_CONF)
        if os.path.exists("./ballooned_dict.pic") == False:
            self.ballooned_dict = dict()
        else:
            self.ballooned_dict = util.pickleLoad("./ballooned_dict.pic")
        # self.ballooned_dict = dict()

    def __del__(self):
        # self.acm_db.close()
        pass

    def select_ac(self):
        self.acm_db = util.getConnection(setting.HUSTOJ_ONLINE_CONF, ssh_status=True)
        contest_id = balloon_conf.contest_id
        ret_list = list()
        sql = '''
        select solution_id, problem_id, user_id, nick, ip, DATE_FORMAT(in_date,'%Y-%m-%d %H:%i:%s')
        from jol.solution
        where result = 4
        and contest_id = {contest_id}
        order by judgetime
        '''.format(contest_id = contest_id)
        print(sql)
        ip_dict = dict()
        ac_dict = dict()
        ac_list = list()
        with self.acm_db.cursor() as acm_cursor:
            acm_cursor.execute(sql)
            results = acm_cursor.fetchall()
            for result in results:
                node = dict()
                submit_id, node["problem_id"], user_id, node["nick"], ip, node["input_time"]= result
                node["colour"] = balloon_conf.colour_dict.get(node["problem_id"], "未定义")
                node["submit_id"] = submit_id
                node["comment"] = "正常"
                node["user_id"] = user_id
                node["ip"] = ip
                node["balloon"] = False

                ip_list = str(ip).split('.')
                room_number = ip_list[2]
                index = ip_list[3]
                node["index"] = "{}-{}".format(room_number, index)
                if submit_id in self.ballooned_dict.get(user_id, []):
                    node["balloon"] = True

                if user_id not in ac_dict:
                    ac_dict.setdefault(user_id, []).append(node["problem_id"])
                else:
                    if node["problem_id"] not in ac_dict[user_id]:
                        ac_dict[user_id].append(node["problem_id"])
                    else:
                        continue

                if user_id not in ip_dict:
                    ip_dict.setdefault(user_id, []).append(ip)
                else:
                    if ip not in ip_dict[user_id]:
                        ip_dict[user_id].append(ip)
                        node["comment"] = "提交ip不一致{}".format(",".join(str(i) for i in ip_dict[user_id]))

                if node["problem_id"] not in ac_list:
                    ac_list.append(node["problem_id"])
                    node["index"] += "  一血！！"

                ret_list.append(node)
        self.acm_db.close()
        return ret_list

    def add_balloon2list(self, user_id, submit_id):
        if os.path.exists("./ballooned_dict.pic") == False:
            self.ballooned_dict = dict()
        else:
            self.ballooned_dict = util.pickleLoad("./ballooned_dict.pic")
        if user_id not in self.ballooned_dict:
            self.ballooned_dict.setdefault(user_id, []).append(submit_id)
        else:
            if submit_id not in self.ballooned_dict[user_id]:
                self.ballooned_dict[user_id].append(submit_id)
        # print(self.ballooned_dict)
        util.pickleDump(self.ballooned_dict, "./ballooned_dict.pic")
        return True




if __name__ == '__main__':
    contest = Contest_balloon()

    # ans = member.select_submit_by_id([20194771])
    # ans = member.select_submit_by_name('宋福海', 3)
    # ans = member.select_platform()
    ans = contest.select_ac()
    for i in ans:
        print(i)
