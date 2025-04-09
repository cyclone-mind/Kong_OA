from fastapi import APIRouter, Depends

from src.apps.system.models import Dept, UserInfo
from src.apps.system.schemas import DeptOutSchema, DeptInSchema, DeptOutTreeSchema
from src.utils.common_response import APIResponse
from ..core import get_current_user

router = APIRouter()


# 1 查询所有部门
@router.get("/depts", description="查询所有部门")
async def get_dept_list(
        user: UserInfo = Depends(get_current_user)
):
    # 部门，分父级和子级---》到时候要加过滤条件--》只查出没有父级的部门--》最顶级部门

    # 查询出来的是一个异步查询集
    depts = await Dept.filter(is_delete=False, pid=None).all().prefetch_related('children')
    dept_dicts = [await DeptOutSchema.from_orm_recursive(dept) for dept in depts]
    return APIResponse(results=dept_dicts)


"""
@router.get("/depts",description="查询所有部门")
async def get_dept_list(
        page_query: PaginationQueryParams = Depends(),  # 查询分页参数，强行转成PaginationQueryParams的对象：page,page_size...
        # user: UserInfo = Depends(get_current_user)
):
    # 部门，分父级和子级---》到时候要加过滤条件--》只查出没有父级的部门--》最顶级部门
    # 我们认为：把数据库中数据都查回来   100w条--》再去做序列化--》再分页
    # 实际上：select * from dept limit=20;--->生成器--》用多少，查多少，不会一次性查回来
    # 所有的orm框架都有这种特性
    # 查询出来的是一个异步查询集
    depts = await Dept.filter().all()
    dept_dicts = [DeptOutSchemas.from_orm(dept).dict() for dept in depts]
    return PaginationResponse(data=dept_dicts, page=page_query.page, page_size=page_query.page_size)
"""


# 2 查询单个部门
@router.get("/depts/{dept_id}", description="查询单个部门")
async def get_dept(
        dept_id: int,
        user: UserInfo = Depends(get_current_user)
):
    dept = await Dept.filter(id=dept_id).first().prefetch_related('children')
    if not dept:
        raise Exception('部门不存在')
    dept_dict = await DeptOutSchema.from_orm_recursive(dept)
    return APIResponse(result=dept_dict, msg="查询部门成功")


# 3 新增部门
@router.post("/depts", description="新增部门")
async def add_dept(
        dept: DeptInSchema,
        user: UserInfo = Depends(get_current_user)
):
    # **dept.dict()将dept对象的属性作为关键字参数传递给Dept.create方法
    dept = await Dept.create(**dept.dict(), create_by=user.username, update_by=user.username)
    if dept:
        return APIResponse(msg='新增部门成功')
    else:
        raise Exception('部门新增失败')


# 4 删除一个或多个部门
@router.delete("/depts", description="删除一个或多个部门")
async def delete_dept(
        ids: list[int],
        user: UserInfo = Depends(get_current_user)
):
    # 删除多个部门
    # await Dept.filter(id__in=ids).delete()
    # 删除单个部门
    await Dept.filter(id__in=ids).update(is_delete=True, update_by=user.username)  # 软删除
    return APIResponse(msg='删除部门成功')


# 5 修改一个部门
@router.put("/depts/{dept_id}", description="修改一个部门")
async def update_dept(
        dept_id: int,
        dept: DeptInSchema,
        user: UserInfo = Depends(get_current_user)
):
    # 修改部门
    await Dept.filter(id=dept_id).update(**dept.dict(), update_by=user.username)
    return APIResponse(msg='修改部门成功')


#### 给角色页面使用，获取部门树的接口
@router.get("/tree/depts", description="查询部门树")
async def get_dept_list_tree(
    user: UserInfo = Depends(get_current_user)
):
    menus = await Dept.filter(is_delete=False,pid=None).all().prefetch_related('children')
    menu_dicts = [await DeptOutTreeSchema.from_orm_recursive(menu) for menu in menus]
    return APIResponse(results=menu_dicts)
