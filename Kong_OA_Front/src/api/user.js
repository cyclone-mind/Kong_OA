import request from "../http";

export const reqUserList = (params) =>
  request.get("system/user/users", { params });
export const reqDeleteUser = (ids) =>
  request.delete("system/user/users", { data: ids });
