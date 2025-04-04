import request from "../http";
// 导出请求对象
export const reqLogin = (username, password) =>
  request.post("system/user/login", { username, password });

export const reqMenus = () => request.get("system/auth/menus");
