import request from '@/utils/request'

export function getDiagnoses(params) {
  return request({
    url: '/diagnosis/',
    method: 'get',
    params
  })
}
