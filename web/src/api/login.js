import request from '@/utils/request'

export function login(username, password) {                                      
  return request({
    url: '/user/login',
    method: 'post',
    data: {
      "username":username,
      "password":password,
    },
    headers: {'content-type': 'application/x-www-form-urlencoded'},
    'emulateJSON': true, 'credentials': true
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'post',
    params: { token },
    data:{
      token
    },
    headers: {'content-type': 'application/x-www-form-urlencoded'},
    'emulateJSON': true, 'credentials': true
  })
}

export function logout(token) {
  return request({
    url: '/user/logout',
    method: 'post',
    data: { token },
    headers: {'content-type': 'application/x-www-form-urlencoded'},
    'emulateJSON': true, 'credentials': true
  })
}

export function test(){

}
