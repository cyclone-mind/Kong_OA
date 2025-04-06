
# 角色相关接口
from fastapi import APIRouter
from ..models import Roles,UserInfo,Menu
from ..schemas import RoleInSchema,RoleOutSchema
from ..core import get_current_user
from fastapi import Depends
from typing import List

from src.utils.common_response import APIResponse
router=APIRouter()


# 1 角色增
@router.post('/roles', description="角色新增")
async def add_role(role: RoleInSchema,
                   user: UserInfo = Depends(get_current_user)
                   ):
    menus = role.menus
    del role.menus
    single_role=await Roles.create(**role.dict())
    if menus:
        await single_role.menus.clear()
        for menu_id in menus:
            menu = await Menu.get(id=menu_id)
            await single_role.menus.add(menu)
    return APIResponse()


# 2 角色删
@router.delete('/roles', description="删除接口，单条多条都支持")
async def delete_role(
        ids: List[int],
        user: UserInfo = Depends(get_current_user)
):
    res = await Roles.filter(id__in=ids).update(is_delete=True)
    return APIResponse(msg='角色删除成功')


# 3 所有角色
@router.get("/roles", description="查询所有角色")
async def get_role_list(
        user: UserInfo = Depends(get_current_user)
):
    roles = await Roles.filter(is_delete=False).all()
    role_dicts = [await RoleOutSchema.from_orm_recursive(role) for role in roles]
    return APIResponse(results=role_dicts)

# 4 角色查一个
@router.get("/roles/{role_id}", description="查询角色详情")
async def get_role(
        role_id: int,
        user: UserInfo = Depends(get_current_user)
):
    role = await Roles.filter(id=role_id).prefetch_related('menus').prefetch_related('depts').first()
    role_dict = await RoleOutSchema.from_orm_recursive(role)
    return APIResponse(result=role_dict)

# 5 角色修改
@router.put("/roles/{role_id}", description="角色修改")
async def update_role(
        role_id: int,
        role: RoleInSchema,
        user: UserInfo = Depends(get_current_user)
):
    menus=role.menus
    del role.menus
    await Roles.filter(id=role_id).update(**role.dict())
    if menus:
        single_role=await Roles.filter(id=role_id).first()
        await single_role.menus.clear()
        for menu_id in menus:
            menu = await Menu.get(id=menu_id)
            await single_role.menus.add(menu)
    return APIResponse()
