import request from '@/utils/request'



export function register(data) {
  return request({
    url: '/users/register',
    method: 'post',
    data
  })
}
