import service from '@/utils/request'
import { getToken } from '@/utils/auth'


export function addPatient(data) {
  return service({
    url: '/patient/',
    method: 'post',
    data
  });
}

export function getPatients(doctor_id) {
    return service({
      url: `/users/${doctor_id}/patients`, // 在 URL 中添加 doctor_id 参数
      method: 'get'
    });
  }


export function getPatient(id) {
  return service({
    url: `/patient/${id}`,
    method: 'get'
  });
}

export function updatePatient(id, data) {
  return service({
    url: `/patient/${id}`,
    method: 'put',
    data
  });
}

export function deletePatient(id) {
  return service({
    url: `/patient/${id}`,
    method: 'delete',
  });
}

export function searchPatients(doctorId, name) {
    return service({
      url: '/users/search',
      method: 'get',
      params: {
        doctor_id: doctorId, // 确保这些参数与后端接口一致
        name: name
      }
    });
  }

export function getPatientById(id) {
  return service({
    url: `/patient/${id}`,
    method: 'get'
  })
}

// 更新患者状态
export function updatePatientStatus(id, status) {
    return service({
      url: `/patient/${id}`,
      method: 'patch',
      data: { status }
    });
}