import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'

// 设置默认头像 URL
const DEFAULT_AVATAR = 'https://ts1.cn.mm.bing.net/th/id/R-C.b3201c2151a76f084a29f648ce604579?rik=RvrqbIDiwdTwIw&riu=http%3a%2f%2fimg.yipic.cn%2fthumb%2f63722c77%2f4e8ef61d%2fb6faf940%2f3c7b7441%2fbig_63722c774e8ef61db6faf9403c7b7441.jpg%3fx-oss-process%3dimage%2fformat%2cwebp%2fsharpen%2c100&ehk=7bn3F38ju2bkqvz%2b7mtg9xnvHDxIqgGXPxWOEOI5q4o%3d&risl=&pid=ImgRaw&r=0'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: DEFAULT_AVATAR, // 使用默认头像
    doctor_id: localStorage.getItem('doctor_id') || null  // 从 localStorage 获取
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar || DEFAULT_AVATAR // 使用默认头像
  },
  SET_DOCTOR_ID: (state, doctor_id) => {
    state.doctor_id = doctor_id
    localStorage.setItem('doctor_id', doctor_id)  // 存储到 localStorage
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        
        //const { data } = response
        commit('SET_TOKEN', response.access_token)
        commit('SET_NAME', response.name)
        // 使用默认头像
        commit('SET_AVATAR', DEFAULT_AVATAR)
        commit('SET_DOCTOR_ID', response.id)
        setToken(response.access_token)
        //commit('SET_TOKEN', data.token)
        //setToken(data.token)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        const { data } = response

        if (!data) {
          return reject('Verification failed, please Login again.')
        }

        const { name ,id } = data

        commit('SET_NAME', name)
        // 使用默认头像
        commit('SET_AVATAR', DEFAULT_AVATAR)
        commit('SET_DOCTOR_ID', id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    // return new Promise((resolve, reject) => {
    //   logout(state.token).then(() => {
        removeToken() // must remove token first
        resetRouter()
        commit('RESET_STATE')
    //     resolve()
    //   }).catch(error => {
    //     reject(error)
    //   })
    // })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove token first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
