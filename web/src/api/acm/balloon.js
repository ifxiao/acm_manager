import request from '@/utils/request'

export default {
    getballoonListPage(current, limit, balloonQuery) {
        return request({
            //url: '/table/list/' + current + '/' + limit,
            url: `/contest/balloon/${current}/${limit}`,
            method: 'post',
            //条件对象，后端用RequestBody获取对象
            //data表示把对象转换成json传递到接口里面
            data: balloonQuery,
            headers: {'content-type': 'application/x-www-form-urlencoded'},
        })
    },
    addBalloonById(balloonQuery){
        return request({
            //url: '/table/list/' + current + '/' + limit,
            url: `/contest/addballoon`,
            method: 'post',
            //条件对象，后端用RequestBody获取对象
            //data表示把对象转换成json传递到接口里面
            data: balloonQuery,
            headers: {'content-type': 'application/x-www-form-urlencoded'},
        
        })
    }
}

