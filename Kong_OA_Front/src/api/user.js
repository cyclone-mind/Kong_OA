import request from "../http";

export const reqUserList = (params) => request.get('system/user/users', {params})
export const reqDeleteUser = (ids) => request.delete('system/user/users', {data: ids})

export const reqUser = (id) => request.get(`system/user/users/${id}`)

export const reqUpdateUser = (id, data) => request.put(`system/user/users/${id}`, {...data})
export const reqCreateUser = (data) => request.post(`system/user/users`, {...data})
export const reqResetPassword = (id) => request.post(`system/user/reset/password/${id}`)

export const reqLockUsers = (ids) => request.delete(`system/user/lock`, {data: ids})
