import request from '@/utils/request'

export default {
    //current当前页 limit每页记录数 memberQuery条件对象
    getSubmitListPage(current, limit, submitQuery) {
        return request({
            //url: '/table/list/' + current + '/' + limit,
            url: `/submit/getsubmits/${current}/${limit}`,
            method: 'post',
            //条件对象，后端用RequestBody获取对象
            //data表示把对象转换成json传递到接口里面
            data: submitQuery,
            headers: {'content-type': 'application/x-www-form-urlencoded'},
        })
    },
    getLinkListPage(current, limit, linkQuery) {
        return request({
            //url: '/table/list/' + current + '/' + limit,
            url: `/submit/getlinks/${current}/${limit}`,
            method: 'post',
            //条件对象，后端用RequestBody获取对象
            //data表示把对象转换成json传递到接口里面
            data: linkQuery,
            headers: {'content-type': 'application/x-www-form-urlencoded'},
        })
    },
    deleteLinkById(id) {
        return request({
            url: `/submit/link/delete/${id}`,
            method: 'delete'
        })
    },
    addLink(link) {
        return request({
            url: `/submit/link/add`,
            method: 'post',
            data: link
        })
    },
    getLinkInfo(id) {
        return request({
            url: `/submit/link/getinfo/${id}`,
            method: 'get'
        })
    },
    getPlatform(){
        return request({
            url:'/submit/getoptions',
            method:'get'
        })
    }
}

