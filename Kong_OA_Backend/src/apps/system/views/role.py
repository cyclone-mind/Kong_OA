
# 角色相关接口
from fastapi import APIRouter
from ..models import Roles,UserInfo
from ..schemas import RoleInSchema,RoleOutSchema
from ..core import get_current_user
from fastapi import Depends
from typing import List
from ..query_params import PaginationQueryParams
from src.utils.common_response import APIResponse
from src.utils.common_response import PaginationResponse
router=APIRouter()


# 角色增
@router.post('/roles', description="角色新增")
async def add_role(role: RoleInSchema,
                   # user: UserInfo = Depends(get_current_user)
                   ):
    await Roles.create(**role.dict())
    return APIResponse()


# 岗位删
@router.delete('/roles', description="删除接口，单条多条都支持")
async def delete_role(
        ids: List[int],
        # user: UserInfo = Depends(get_current_user)
):
    res = await Roles.filter(id__in=ids).update(is_delete=True)  # 软删除，字段控制
    return APIResponse(msg='角色删除成功')


# 岗位查所有
## 1 查询所有用户接口--不分页
@router.get("/roles", description="查询所有角色")
async def get_role_list(
        # user: UserInfo = Depends(get_current_user)
):
    roles = await Roles.filter(is_delete=False).all()
    # 序列化 Pydantic
    role_dicts = [RoleOutSchema.from_orm(role).dict() for role in roles]
    return APIResponse(results=role_dicts)

# 角色查一个
@router.get("/roles/{role_id}", description="查询角色详情")
async def get_role(
        role_id: int,
        #user: UserInfo = Depends(get_current_user)
):
    role = await Roles.filter(id=role_id).first()
    role_dict = RoleOutSchema.from_orm(role).dict()
    return APIResponse(result=role_dict)


# 角色修改
@router.put("/roles/{role_id}", description="查询角色详情")
async def update_role(
        role_id: int,
        role: RoleInSchema,
        #user: UserInfo = Depends(get_current_user)
):
    await Roles.filter(id=role_id).update(**role.dict())
    return APIResponse("角色修改成功")
