import axios from "axios";
import { ElMessage } from "element-plus";
import $cookies from "vue-cookies";
// 请求的1 基本配置
const request = axios.create({
  baseURL: "http://127.0.0.1:8080/api/v1",
  timeout: 5000,
  headers:{
    "content-Type":"application/json; charset=utf-8"
  }
});

// 2 请求拦截器

request.interceptors.request.use((config) => {
    // 从cookie中取出用户登录信息，如果有，就放在请求头中。
    let token = $cookies.get("token");
    if (token) {
      config.headers["Authorization"] = "Bearer " + token;
    }
    return config;
})

// 3 响应拦截器
request.interceptors.response.use(
    //  请求成功和请求失败的情况（业务逻辑错误）比如后端规定成功和失败
    //response是后端接口返回的响应对象：响应头、响应体（响应体从response.data中取到）
  (response) => {
    let res = response.data;
    if(res.code==100){
        // 100表示成功,正常返回
        return res;
    }else {
        // 200表示失败
        ElMessage({
            message: !res.msg?'服务器异常':res.msg, 
            type: 'error',
            plain: true,
          })
        return Promise.reject(response.data.msg);
    }
  },
//   HTTP 错误的情况（网络或服务器错误）
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          ElMessage.error("未登录，请先登录");
          break;
        case 403:
          ElMessage.error("权限不足，无法访问");
          break;
        case 404:
          ElMessage.error("请求的资源不存在");
          break;
        case 500:
          ElMessage.error("服务器错误");
          break;
        default:
          ElMessage.error("未知错误");
          break;
      }
    }
    return Promise.reject(new Error(error.message));
  }
);

/*


业务成功
	
response.data.code == 100
	
直接返回
response.data
，调用方可以通过
.then
获取数据。
业务失败
	
response.data.code != 100
	
显示错误提示，返回被拒绝的 Promise，调用方可以通过
.catch
捕获错误信息。
HTTP 错误（401、403 等）
	
error.response.status
存在
	
根据状态码显示对应提示，返回被拒绝的 Promise。
网络错误或其他异常
	
error.response
不存在
	
提示“未知错误”，返回被拒绝的 Promise。
*/


// 导出请求对象
export default request;