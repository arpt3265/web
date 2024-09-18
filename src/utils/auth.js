import Cookies from 'js-cookie'

const TokenKey = 'token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
    Cookies.set(TokenKey, token) // 设置 token 有效期为7天
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
