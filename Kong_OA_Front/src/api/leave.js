import request from "../http/index.js";


export const reqLeaveList=(q)=>request.get(`oa/leave/leave?q=${q}`)
export const reqLeave=(leave_id)=>request.get(`oa/leave/leave/${leave_id}`)
export const reqUpdateLeave=(leave_id,data)=>request.put(`oa/leave/leave/${leave_id}`,{...data})
export const reqDeleteLeave=(ids)=>request.delete('oa/leave/leave',{data:ids})
export const reqCreateLeave=(data)=>request.post('oa/leave/leave',{...data})

export const reqChangeLeaveStatus=(leave_id,status)=>request.get(`oa/leave/leave/status/${leave_id}/${status}`)