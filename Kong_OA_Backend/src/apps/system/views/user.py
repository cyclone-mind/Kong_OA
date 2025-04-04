from fastapi import APIRouter
from fastapi import Depends

from src.utils.common_exception import LoginException
from src.utils.common_response import APIResponse
from src.utils.common_response import PaginationResponse
from ..core import authenticate_user, create_access_token, get_current_user
from ..models import UserInfo
from ..query_params import PaginationQueryParams, UserQueryParams
from ..schemas import LoginRequest, UserSchema

# pip install PyJWT[crypto]
# pip install python-jose[cryptography]

router = APIRouter()


@router.post('/login')
async def login(login_request: LoginRequest):
    """
    处理用户登录请求

    参数:
    login_request (LoginRequest): 包含用户名和密码的登录请求对象

    返回:
    APIResponse: 包含用户信息和登录令牌的响应对象

    异常:
    LoginException: 当用户名或密码验证失败时抛出
    """
    # login_request 包含了用户名和密码，格式是 json
    # 1. 验证用户名和密码是否正确
    user: UserInfo = await authenticate_user(login_request.username, login_request.password)
    if not user:
        raise LoginException()
    # 2. 生成token
    token = create_access_token(data={"username": user.username})
    # 3. 返回给前端
    return APIResponse(data={'username': user.username, 'avatar': user.avatar, 'token': token})


# 1 查询所有用户的接口--带分页
@router.get('/users', description='查询所有用户的接口--带分页')
async def get_user_list(
        page_query: PaginationQueryParams = Depends(),  # 查询分页参数，强行转成PaginationQueryParams的对象：page,page_size...
        user_query: UserQueryParams = Depends(),  # 查询用户参数:根据用户名，用户中文名，是否活跃状态 去查询用户
        # user: UserInfo = Depends(get_current_user)
):
    search = user_query.to_query_params()  # {nick_name__icontains:刘}
    users=await UserInfo.filter(**search).filter(is_delete=False).all().prefetch_related("roles") # users=await UserInfo.filter(nick_name__contains='刘').all()
    # 序列化 Pydantic
    user_dicts = [UserSchema.from_orm(user).dict() for user in users]
    # 返给前端(分页的响应对象)
    return PaginationResponse(data=user_dicts, page=page_query.page, page_size=page_query.page_size)

# 2 根据用户ID 查询用户详情接口
@router.get('/users/{user_id}', description='查询单个用户详情接口')
async def get_user_info(
        user_id: int,
        # user:UserInfo = Depends(get_current_user)
):
    # 根据用户ID，拿到用户
    user = await UserInfo.filter(id=user_id).first()
    # 序列化 Pydantic
    if user:
        user_dict = UserSchema.from_orm(user).dict()
        return APIResponse(data=user_dict)
    else:
        return APIResponse(msg='用户不存在')

# 3 删除用户：单删和多删--请求体中数据格式  [2,3]
@router.delete("/user",description='删除用户：单删和多删')
async def delete_user(
        ids: list[int],
        # user: UserInfo = Depends(get_current_user)
):
    # res=await UserInfo.filter(id__in=ids).delete() # 硬删除，数据库就没了
    res = await UserInfo.filter(id__in=ids).update(is_delete=True)
    print(res)
    return APIResponse(msg='删除成功')
