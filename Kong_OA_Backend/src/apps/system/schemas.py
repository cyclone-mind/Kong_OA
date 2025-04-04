from typing import List, Any

from pydantic import BaseModel

from src.settings import setting


class RoleSchema(BaseModel):
    id: int
    name: str

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
    is_active: bool
    roles: List[RoleSchema]

    # 使用pydantic 把对象转成字典，要带它
    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # 使用super()调用父类的方法从_orm来创建数据表示
        data = super().from_orm(obj)
        data.avatar = f"http://{setting.APP_HOST}:{setting.APP_PORT}/media/{data.avatar}"  # 在某个字段前后加固定的
        return data


class DeptOutSchema(BaseModel):
    id: int
    pid_id: int | None = None
    name: str
    enabled: bool
    dept_sort: int
    # 后期还需要动----》有子关系--》递归序列化
    # children:List['DeptOutSchema']|None=[]
    children: Any | None = []

    # 使用pydantic 把对象转成字典，要带它
    class Config:
        from_attributes = True

    # 自定义一个方法来调用-->递归序列化
    @classmethod
    async def from_orm_recursive(cls, obj):
        if obj is None:
            return None
        # 1 这个obj是一个 部门对象--->使用序列化类[DeptOutSchema]--->转成字典
        # 坑：dept_dict.children-->不能直接转
        dept_dict = cls.from_orm(obj).dict()
        # 2 查出当前部门所有的子部门对象，把children查出来
        children = await obj.children.filter(is_delete=False).all()
        # 3 自己转，然后替换,是字典
        dept_dict['children'] = [await cls.from_orm_recursive(child) for child in children]
        # 4 把转完之后的返回
        return dept_dict


class DeptInSchema(BaseModel):
    # 前端给我们的
    pid_id: int | None = None
    name: str
    enabled: bool
    sub_count: int | None = None
    dept_sort: int

    class Config:
        from_attributes = True


# 岗位相关
# 序列化的类--》给前端用的
class JobOutSchema(BaseModel):
    id: int
    name: str
    enabled: bool
    job_sort: int

    # 后期还需要动----》有子关系--》递归序列化
    # 使用pydantic 把对象转成字典，要带它
    class Config:
        from_attributes = True


# 反序列化的，前端给我们的
class JobInSchema(BaseModel):
    # id: int
    name: str
    enabled: bool
    job_sort: int | None = None

    class Config:
        from_attributes = True


class RoleOutSchema(BaseModel):
    id: int
    name: str
    level: int
    description: str
    data_scope: str
    status: bool

    # 关联关系：db_table 指定中间表的名字
    # depts : list[DeptOutSchema]
    # menus : list[MenuOutSchema]

    class Config:
        from_attributes = True


class RoleInSchema(BaseModel):
    name: str
    level: int
    description: str
    data_scope: str
    status: bool

    # 关联关系：db_table 指定中间表的名字
    # depts : list[DeptOutSchema]
    # menus : list[MenuOutSchema]

    class Config:
        from_attributes = True


# 菜单相关
class MenuInSchema(BaseModel):
    pid_id: int | None = None
    sub_count: int | None = None
    # 0 菜单，1 子菜单，2 按钮
    type: int
    title: str
    name: str
    component: str
    menu_sort: int
    icon: str
    path: str
    i_frame: bool
    cache: bool
    hidden: bool
    permission: str
    is_menu: bool

    class Config:
        from_attributes = True


class MenuOutSchema(BaseModel):
    id: int
    sub_count: int | None = None
    # 0 菜单，1 子菜单，2 按钮
    type: int
    title: str
    name: str
    component: str | None = None
    menu_sort: int
    icon: str
    path: str
    i_frame: bool
    cache: bool
    hidden: bool
    permission: str | None = None
    is_menu: bool

    class Config:
        from_attributes = True
