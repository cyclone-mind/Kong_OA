from .models import UserInfo
from jose import JWTError, jwt
from src.settings import setting
from datetime import timedelta, datetime
from fastapi.requests import Request
from src.utils.common_exception import AuthException
from fastapi import Depends
# 去数据库验证用户名和密码，
async def authenticate_user(username:str,password:str):
    # 传入的 password 是明文密码
    # 先根据用户名查询到用户，
    user = await UserInfo.get_or_none(username=username)
    # 校验密码
    if not user:
        return False
    if not user.check_password(password):
        return False
    # 用户是活跃的
    if user.is_active:
        return user
    else:
        return False

# 签发token函数
def create_access_token(data: dict,expires_delta:timedelta=None):
    to_encode = data.copy()
    # data 是一个字典，里面是token要包含的信息，比如用户名，用户id，用户角色等
    # expires_delta 是token的过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # 1. 生成token
    encoded_jwt = jwt.encode(to_encode,setting.SECRET_KEY,algorithm=setting.ALGORITHM)
    # 2. 返回给前端
    return encoded_jwt

# 3 认证 ：依赖注入---》所有需要登录才才能访问的接口，必须先执行这个--》drf--》认证类
from fastapi.security import OAuth2PasswordBearer # 要求前端请求头中带:Authorization :Bearer token三段式
oauth2 = OAuth2PasswordBearer(tokenUrl="token")
async def oauth2_scheme(request: Request):
    # 1. 验证token是否合法
    # 2. 解析token
    # 3. 返回token中的信息
    try:
        token = await oauth2(request)
        print("token:::",token)
        return token
    except Exception as e:
        raise AuthException(msg="token验证失败")

# 4 获取当前登录用户，使用用户携带的 token 来拿到

async def get_current_user(token:str = Depends(oauth2_scheme)):

    e = AuthException(msg="token验证失败")
    try:
        # 使用jwt库解码用户提供的token，验证其合法性
        # 参数token是前端请求中提取的JWT令牌
        # setting.SECRET_KEY是项目中定义的密钥，用于验证token的签名
        # setting.ALGORITHM是项目中定义的加密算法，指定了解码token时应使用的算法
        payload = jwt.decode(token,setting.SECRET_KEY,algorithms=[setting.ALGORITHM])
        print("payload:::",payload) 
        username: str = payload.get("username")
        print("username:::",username)
        # 通过用户名查询用户信息
        if username is None:
            raise e
        user = await UserInfo.get_or_none(username=username)
    except JWTError:
        raise e
    return user