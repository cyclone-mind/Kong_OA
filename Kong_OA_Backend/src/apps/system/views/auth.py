from fastapi import APIRouter
from fastapi import Depends
from src.apps.system.models import UserInfo
from src.apps.system.core import get_current_user
router = APIRouter()

from src.utils.common_response import APIResponse

# 不同用户登录系统以后，看到的菜单是不一样的，这个菜单是根据用户的角色来的
# @router.get("/auth") # 这个接口需要登陆以后才能访问，因此我们使用依赖注入
# async def get_menus(
#     # user:UserInfo = Depends(get_current_user)
#     ):
#     # 菜单权限
#     nav = [
#         {
#             'name': 'SysManga',
#             'title': '系统管理',
#             'icon': 'PieChart',
#             'component': '',
#             'path': '',
#             'children': [
#                 {
#                     'name': 'SysInfo',
#                     'title': '服务性能',
#                     'icon': 'PieChart',
#                     'path': '/admin/info',
#                     'component': 'admin/Info',
#                     'children': []
#                 },
#                 {
#                     'name': 'SysUser',
#                     'title': '用户管理',
#                     'icon': 'Sell',
#                     'path': '/admin/user',
#                     'component': 'admin/User',
#                     'children': []
#                 },
#                 {
#                     'name': 'SysRole',
#                     'title': '角色管理',
#                     'icon': 'Sell',
#                     'path': '/admin/role',
#                     'component': 'admin/Role',
#                     'children': []
#                 },
#                 {
#                     'name': 'SysMenu',
#                     'title': '菜单管理',
#                     'icon': 'Sell',
#                     'path': '/admin/menu',
#                     'component': 'admin/Menu',
#                     'children': []
#                 },
#                 {
#                     'name': 'SysDept',
#                     'title': '部门管理',
#                     'icon': 'Sell',
#                     'path': '/admin/dept',
#                     'component': 'admin/Dept',
#                     'children': []
#                 },
#                 {
#                     'name': 'SysJob',
#                     'title': '岗位管理',
#                     'icon': 'Sell',
#                     'path': '/admin/job',
#                     'component': 'admin/Job',
#                     'children': []
#                 }
#             ]
#         },
#     ]
#     # 用户权限
#     authoritys = ["sys:user:list","sys:user:save","sys:user:delete"]
#     return APIResponse(nav=nav,authoritys=authoritys)


from ..models import Menu
from ..schemas import MenuPermissionSchema
@router.get('/auth')
async def menus(
    user:UserInfo=Depends(get_current_user)
):
    # 1 如果是超级用户
    if user.is_superuser:
        ## 1.1 拿到所有菜单
        menus = await Menu.filter(is_delete=False, is_menu=True).prefetch_related('children').order_by('menu_sort')
        ## 1.2 组装成字典，返回给前端
        nav = [await MenuPermissionSchema.from_orm_recursive(menu) for menu in menus]
        ## 1.3 所有按钮都查出来
        buttons = await Menu.filter(type=2)
        ## 1.4 组装成列表，返回给前端
        authoritys = [item.permission for item in buttons]
    else:
        # 2 根据当前登录用户，获得所有角色--》角色可能有多个--》每个角色有自己的权限[菜单，按钮]--》根据角色拿到所有权限去重
        roles = await user.roles.all()
        # 2.1 根据角色，取出所有菜单权限,会有重复所有用集合去重
        catalog_ids = []  # 存放所有目录id
        menus_ids = []  # 存放所有菜单id

        buttons = []  # 存放所有按钮
        for role in roles:
            # 根据角色获取所有目录
            catalog_ids += await role.menus.filter(type=0).values_list('id', flat=True)
            # 获取所有菜单
            menus_ids += await role.menus.filter(type=1).values_list('id', flat=True)
            # 根据角色获取所有按钮
            buttons += await role.menus.filter(type=2)
        # 序列化所有目录及子菜单
        menus_qs = await Menu.filter(id__in=list(set(catalog_ids)))
        # 2.2 组装成字典--》去重过的
        nav = [await MenuPermissionSchema.from_orm_recursive(menu, menus_ids) for menu in menus_qs]
        # 2.3 通过按钮拿到所有权限放到列表中
        authoritys = [item.permission for item in buttons]
        # 2.3 按钮权限去重
        authoritys = list(set(authoritys))
    return APIResponse(nav=nav,authoritys=authoritys)