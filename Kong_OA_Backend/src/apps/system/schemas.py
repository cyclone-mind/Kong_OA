from pydantic import BaseModel
from typing import List
from src.settings import setting
class RoleSchema(BaseModel):
    id:int
    name:str
    # 使用pydantic 把对象转成字典，要带它
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str
    
class UserSchema(BaseModel):
    id: int
    username: str
    nick_name: str
    gender: int
    avatar: str  # 都带一个固定前缀
    email: str
    phone: str
    is_active:bool
    roles:List[RoleSchema]
    # 使用pydantic 把对象转成字典，要带它
    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # 使用super()调用父类的方法从_orm来创建数据表示
        data = super().from_orm(obj)
        data.avatar = f"http://{setting.APP_HOST}:{setting.APP_PORT}/media/{data.avatar}" # 在某个字段前后加固定的
        return data