import request from '@/utils/request'

export default {
    //current当前页 limit每页记录数 teamQuery条件对象
    getTeamListPage(current, limit, teamQuery) {
        return request({
            //url: '/table/list/' + current + '/' + limit,
            url: `/team/teams/${current}/${limit}`,
            method: 'post',
            //条件对象，后端用RequestBody获取对象
            //data表示把对象转换成json传递到接口里面
            data: teamQuery,
            headers: {'content-type': 'application/x-www-form-urlencoded'},
        })
    },

    deleteTeamById(id) {
        return request({
            url: `/team/delete/${id}`,
            method: 'delete'
        })
    },

    addTeam(team) {
        return request({
            url: `/team/add`,
            method: 'post',
            data: team
        })
    },

    getTeamInfo(id) {
        return request({ 
            url: `/team/getTeam/${id}`,
            method: 'get'
        })
    },

    updateTeam(team) {
        return request({
            url: `/team/update`,
            method: 'post',
            data: team
        })
    },

    checkMember(data) {
        return request({
            url: `/team/checkMember`,
            method: 'post',
            data: data
        })
    },

}


