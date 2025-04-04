from fastapi import APIRouter
from fastapi import Depends
from src.apps.system.models import UserInfo
from src.apps.system.core import get_current_user
router = APIRouter()

from src.utils.common_response import APIResponse

# 不同用户登录系统以后，看到的菜单是不一样的，这个菜单是根据用户的角色来的
@router.get("/auth") # 这个接口需要登陆以后才能访问，因此我们使用依赖注入
async def get_menus(
    # user:UserInfo = Depends(get_current_user)
    ):
    # 菜单权限
    nav = [
        {
            'name': 'SysManga',
            'title': '系统管理',
            'icon': 'PieChart',
            'component': '',
            'path': '',
            'children': [
                {
                    'name': 'SysInfo',
                    'title': '服务性能',
                    'icon': 'PieChart',
                    'path': '/admin/info',
                    'component': 'admin/Info',
                    'children': []
                },
                {
                    'name': 'SysUser',
                    'title': '用户管理',
                    'icon': 'Sell',
                    'path': '/admin/user',
                    'component': 'admin/User',
                    'children': []
                },
                {
                    'name': 'SysRole',
                    'title': '角色管理',
                    'icon': 'Sell',
                    'path': '/admin/role',
                    'component': 'admin/Role',
                    'children': []
                },
                {
                    'name': 'SysMenu',
                    'title': '菜单管理',
                    'icon': 'Sell',
                    'path': '/admin/menu',
                    'component': 'admin/Menu',
                    'children': []
                },
                {
                    'name': 'SysDept',
                    'title': '部门管理',
                    'icon': 'Sell',
                    'path': '/admin/dept',
                    'component': 'admin/Dept',
                    'children': []
                },
                {
                    'name': 'SysJob',
                    'title': '岗位管理',
                    'icon': 'Sell',
                    'path': '/admin/job',
                    'component': 'admin/Job',
                    'children': []
                }
            ]
        },
        {  # 这个前端没有与之对应的，只为了演示
            'name': 'SysTools',
            'title': '自动办公',
            'icon': 'Sell',
            'path': '',
            'component': '',
            'children': [
                {
                    'name': 'SysDict',
                    'title': '数字字典',
                    'icon': 'Sell',
                    'path': '/admin/dicts',
                    'component': '/admin/Dicts',
                    'children': []
                },
            ]
        }
    ]
    # 用户权限
    authoritys = ["sys:user:list","sys:user:save","sys:user:delete"]
    return APIResponse(nav=nav,authoritys=authoritys)