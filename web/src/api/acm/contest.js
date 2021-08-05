import request from '@/utils/request'

export default {
    // //current当前页 limit每页记录数 memberQuery条件对象
    getContestListPage(current, limit, Query) {
        return request({
            //url: '/table/list/' + current + '/' + limit,
            url: `/contest/getList/${current}/${limit}`,
            method: 'post',
            //条件对象，后端用RequestBody获取对象
            //data表示把对象转换成json传递到接口里面
            data: Query,
            headers: {'content-type': 'application/x-www-form-urlencoded'},
        })
    },
    deleteContestById(id) {
        return request({
            url: `/contest/delete/${id}`,
            method: 'delete'
        })
    },
    addContest(contest) {
        return request({
            url: `/contest/add`,
            method: 'post',
            data: contest
        })
    },
    getcontestInfo(id) {
        return request({ 
            url: `/contest/getContest/${id}`,
            method: 'get'
        })
    },
    saveTeam(data){
        return request({
            url: `/contest/add_team`,
            method: 'post',
            data: data
        })
    },
    getTeams(current, limit, id){
        return request({ 
            url: `/contest/getTeams/${id}/${current}/${limit}`,
            method: 'get'
        })
    },
    deleteTeamById(id){
        return request({
            url: `/contest/deleteTeam/${id}`,
            method: 'delete'
        })
    }
}

