import request from '@/utils/request'

export default {
    //current当前页 limit每页记录数 memberQuery条件对象
    getMemberListPage(current, limit, memberQuery) {
        return request({
            //url: '/table/list/' + current + '/' + limit,
            url: `/member/pagememberCondition/${current}/${limit}`,
            method: 'post',
            //条件对象，后端用RequestBody获取对象
            //data表示把对象转换成json传递到接口里面
            data: memberQuery,
            headers: {'content-type': 'application/x-www-form-urlencoded'},
        })
    },

    deleteMemberById(id) {
        return request({
            url: `/member/delete/${id}`,
            method: 'delete'
        })

    },

    addMember(member) {
        return request({
            url: `/member/add`,
            method: 'post',
            data: member
        })
    },

    getMemberInfo(id) {
        return request({
            url: `/member/getMember/${id}`,
            method: 'get'
        })
    },

    updateMember(member) {
        return request({
            url: `/member/update`,
            method: 'post',
            data: member
        })
    } 
}

