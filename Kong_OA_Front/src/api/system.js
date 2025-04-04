// 系统相关
// 登录接口
import request from "../http";
export const reqLogin=(username,password)=>request.post('system/user/login',{username,password})
export const reqAuth=()=>request.get('system/auth/auth')

// 岗位相关
export const reqJobList=()=>request.get('system/job/jobs')
export const reqJob=(job_id)=>request.get(`system/job/jobs/${job_id}`)
export const reqUpdateJob=(job_id,data)=>request.put(`system/job/jobs/${job_id}`,{...data})
export const reqDeleteJob=(ids)=>request.delete('system/job/jobs/',{data:ids})
export const reqCreateJob=(data)=>request.post('system/job/jobs',{...data})


// 角色相关
export const reqRoleList=()=>request.get('system/role/jobs')
export const reqRole=(role_id)=>request.get(`system/role/roles/${role_id}`)
export const reqUpdateRole=(role_id)=>request.put(`system/role/roles/${role_id}`)
export const reqDeleteRole=(ids)=>request.delete('system/role/roles/',{data:ids})
export const reqCreateRole=(data)=>request.post('system/role/roles',{...data})

// 部门相关
export const reqDeptList=()=>request.get('system/dept/depts')
export const reqDept=(dept_id)=>request.get(`system/dept/depts/${dept_id}`)
export const reqUpdateDept=(dept_id, data)=>request.put(`system/dept/depts/${dept_id}`,{...data})
export const reqDeleteDept=(ids)=>request.delete('system/dept/depts',{data:ids})
export const reqCreateDept=(data)=>request.post('system/dept/depts',{...data})

// 菜单相关
export const reqMenuList=()=>request.get('system/menu/menus')
export const reqMenu=(menu_id)=>request.get(`system/menu/menus/${menu_id}`)
export const reqUpdateMenu=(menu_id)=>request.put(`system/menu/menus/${menu_id}`)
export const reqDeleteMenu=(ids)=>request.delete('system/menu/menus',{data:ids})
export const reqCreateMenu=(data)=>request.post('system/menu/menus',{...data})