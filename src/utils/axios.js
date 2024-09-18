// src/utils/axios.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5000', // 你 Flask API 的地址
  withCredentials: false, // 跨域请求时是否发送 cookies
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
});

export default apiClient;
