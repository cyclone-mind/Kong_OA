# 菜单相关接口
from typing import List

from fastapi import APIRouter

from src.utils.common_response import APIResponse
from ..models import Menu
from ..schemas import MenuInSchema, MenuOutSchema, MenuOutTreeSchema

router = APIRouter()


# 1 菜单增
@router.post('/menus', description="菜单新增")
async def add_menu(
        menu: MenuInSchema,
        # user: UserInfo = Depends(get_current_user)
):
    await Menu.create(**menu.dict())
    return APIResponse()


# 2 菜单删
@router.delete('/menus', description="删除接口，单条多条都支持")
async def delete_menu(
        ids: List[int],
        # user: UserInfo = Depends(get_current_user)
):
    res = await Menu.filter(id__in=ids).update(is_delete=True)  # 软删除，字段控制
    return APIResponse(msg='菜单删除成功')


# 3 菜单查所有
## 1 查询所有menu接口----不分页
@router.get("/menus", description="查询所有菜单")
async def get_menu_list():
    menus = await Menu.filter(is_delete=False,pid=None).all().prefetch_related('children')
    menu_dicts = [await MenuOutSchema.from_orm_recursive(menu) for menu in menus]
    return APIResponse(results=menu_dicts)


# 4 菜单查一个
@router.get("/menus/{menu_id}", description="查询菜单详情")
async def get_menu(
        menu_id: int,
        # user: UserInfo = Depends(get_current_user)
):
    menu = await Menu.filter(id=menu_id).first()
    menu_dict = await MenuOutSchema.from_orm_recursive(menu)
    return APIResponse(result=menu_dict)


# 5 菜单修改
@router.put("/menus/{menu_id}", description="查询菜单详情")
async def update_menu(
        menu_id: int,
        menu: MenuInSchema,
        # user: UserInfo = Depends(get_current_user)
):
    await Menu.filter(id=menu_id).update(**menu.dict())
    return APIResponse()


# 6 查询菜单树
@router.get('/tree/menus',description="查询所有菜单")
async def get_tree_list_menu(
     # user: UserInfo = Depends(get_current_user)
):
    menus = await Menu.filter(is_delete=False,pid=None).all().prefetch_related("children")
    menu_dicts = [await MenuOutTreeSchema.from_orm_recursive(menu) for menu in menus]
    return APIResponse(results=menu_dicts)
