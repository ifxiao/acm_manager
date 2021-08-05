import request from '@/utils/request'

export default {
    // //current当前页 limit每页记录数 memberQuery条件对象
    getLeaveListPage(current, limit, Query) {
        return request({
            //url: '/table/list/' + current + '/' + limit,
            url: `/Management/leave/getList/${current}/${limit}`,
            method: 'post',
            //条件对象，后端用RequestBody获取对象
            //data表示把对象转换成json传递到接口里面
            data: Query,
            headers: {'content-type': 'application/x-www-form-urlencoded'},
        })
    },
    updateLeave(data) {
        return request({
            //url: '/table/list/' + current + '/' + limit,
            url: `/Management/leave/update`,
            method: 'post',
            data
        })
    },
    deleteManagementById(id) {
        return request({
            url: `/Management/delete/${id}`,
            method: 'delete'
        })
    },
    addManagement(Management) {
        return request({
            url: `/Management/leave/add`,
            method: 'post',
            data: Management
        })
    },
    getManagementInfo(id) {
        return request({ 
            url: `/Management/getManagement/${id}`,
            method: 'get'
        })
    },
    saveTeam(data){
        return request({
            url: `/Management/add_team`,
            method: 'post',
            data: data
        })
    },
    getTeams(current, limit, id){
        return request({ 
            url: `/Management/getTeams/${id}/${current}/${limit}`,
            method: 'get'
        })
    },
    deleteTeamById(id){
        return request({
            url: `/Management/deleteTeam/${id}`,
            method: 'delete'
        })
    }
}

