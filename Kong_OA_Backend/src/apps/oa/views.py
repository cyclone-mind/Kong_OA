
from fastapi import APIRouter,Depends
from .models import Leave
from .schemas import LeaveInSchema, LeaveOutSchema
from ..system.core import get_current_user
from ..system.models import UserInfo
from src.utils.common_response import APIResponse
from typing import List
router=APIRouter()


# 1 新建请假单
@router.post('/leave', description='新增请假')
async def add_leave(
        leave: LeaveInSchema,
        user: UserInfo = Depends(get_current_user)
):
    # 请假单创建人是当前登录用户
    await Leave.create(**leave.dict(),owner_id=user.id)
    return APIResponse(msg='新增成功')
# 2 删除请假单
@router.delete('/leave', description='删除请假单')
async def delete_job(
        ids: List[int],  # [1,2,3]
        user: UserInfo = Depends(get_current_user)
):
    await Leave.filter(id__in=ids).update(is_delete=True)  # 软删除
    return APIResponse(msg='删除请假单成功')
# 3 修改请假单
@router.put('/leave/{leave_id}', description='修改请假')
async def update_leave(
        leave_id: int,
        leave: LeaveInSchema,
        user: UserInfo = Depends(get_current_user)
):
    await Leave.filter(id=leave_id).update(**leave.dict())
    return APIResponse(msg='修改成功')
# 4 查询一条请假单详情
@router.get('/leave/{leave_id}', description='查询一个请假单')
async def get_job(
        leave_id: int ,
        user: UserInfo = Depends(get_current_user)
):
    job = await Leave.filter(id=leave_id).prefetch_related('owner').first()
    job_dict = LeaveOutSchema.from_orm(job).dict()
    return APIResponse(msg='查询请假单成功', result=job_dict)

# 5 查询所有请假单-：根据传入的参数：如果传入type为1：查询当前用户的，如果传入type为2:查询所有
@router.get('/leave', description='查询本人请假单或所有请假单')
async def get_leave_list(
        q:int|None=1, # 为1时，查本人，不为1时查所有
        user: UserInfo = Depends(get_current_user)
):
    if q==1:
        leave_list = await Leave.filter(is_delete=False,owner=user).prefetch_related('owner').all()
    else:
        leave_list = await Leave.filter(is_delete=False).prefetch_related('owner').all()
    leave_dicts = [LeaveOutSchema.from_orm(leave).dict() for leave in leave_list]
    return APIResponse(results=leave_dicts)


# 6 请假单审批：无论通过或驳回，都用一个接口
@router.get('/leave/status/{leave_id}/{status_type}', description='审批请假单')
async def change_leave_status(
        leave_id: int,
        status_type:int=1, # 请假单状态，默认为1，1是通过，2 是驳回
        user: UserInfo = Depends(get_current_user)
):
    await Leave.filter(id=leave_id).update(status=status_type)
    return APIResponse(msg='修改成功')


