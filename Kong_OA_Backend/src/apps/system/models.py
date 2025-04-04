from tortoise import Model, fields
from passlib.context import CryptContext
from src.utils.common_model import BaseModel
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 1 用户表

class UserInfo(BaseModel):
    """
    用户信息类，继承自Model基类。

    该类用于定义用户信息的数据结构，通常包括用户相关的各种属性。
    通过继承Model基类，UserInfo类可以使用Django提供的ORM功能，进行数据库操作。

    属性:
    - username: 用户名，唯一标识一个用户
    - password: 用户密码，用于用户身份验证
    - email: 用户邮箱，用于账户激活、找回密码等功能
    - is_active: 布尔值，表示用户账户是否处于激活状态
    """


    username = fields.CharField(max_length=150, unique=True, description='用户名')
    password = fields.CharField(max_length=128, description='用户密码')
    is_active = fields.BooleanField(default=True, description='是否是活跃用户')
    email = fields.CharField(max_length=32, description='邮箱', null=True)
    nick_name = fields.CharField(max_length=32, description='用户昵称', null=True, unique=True)
    gender = fields.CharField(max_length=16, description='性别', null=True)
    phone = fields.CharField(max_length=11, description='电话号码', null=True, unique=True)
    avatar = fields.CharField(max_length=64, default='avatar/default.png', description='头像')
    enabled = fields.BooleanField(default=True, description='是否启用?状态：1启用、0禁用')
    is_superuser = fields.BooleanField(default=False, description='是否是超级用户')

    # 用户和角色：多对多
    roles = fields.ManyToManyField(model_name="models.Roles",description = '用户和角色的关联表',through="oa_user_roles")
    # 用户和部门：一对多关系
    dept = fields.ForeignKeyField(model_name='models.Dept', description='用户和部门的关联表', on_delete=fields.SET_NULL, null=True)
    # 用户和岗位：多为多
    jobs = fields.ManyToManyField(model_name="models.Job", description='用户和岗位的关联表', through="oa_user_jobs")
    class Meta:
        table = 'OA_users'


    @classmethod
    def make_password(cls,password:str):
        return pwd_context.hash(password)

    def check_password(self,password:str):
        return pwd_context.verify(password,self.password)

class OnlineUser(BaseModel):

    browser = fields.CharField(max_length=128, description='浏览器',null=True)
    ip = fields.CharField(max_length=64, description='ip地址',null=True)
    key = fields.CharField(max_length=64, description='Token',null=True)
    user = fields.ForeignKeyField('models.UserInfo', description='用户名',null=True)


    class Meta:
        table = 'OA_online_user'

# 菜单表：Menu    部门表：Dept   角色表：Roles  岗位表：Job

class Menu(BaseModel): # 权限
    """
    上级菜单id, 子菜单数目， 菜单类型， 菜单标题， 组件名称， 组件， 排序， 图标， 连接地址， 是否外链， 缓存， 隐藏
    权限
    """
    pid = fields.ForeignKeyField(model_name='models.Menu', description='父菜单id', on_delete=fields.SET_NULL, null=True,related_name='children')
    sub_count = fields.IntField(description='子菜单数目', null=True, blank=True)
    # 0 菜单，1 子菜单，2 按钮
    type = fields.IntField(description='菜单类型',  null=True)
    title = fields.CharField(max_length=32, description='菜单标题',  null=True, unique=True)
    name = fields.CharField(max_length=255, description='前端组件名称',  null=True, unique=True)
    component = fields.CharField(max_length=255, description='前端组件',  null=True)
    menu_sort = fields.IntField(description='菜单排序',  null=True)
    icon = fields.CharField(max_length=255,  null=True, description='菜单图标')
    path = fields.CharField(max_length=255,  null=True, description='菜单链接地址')
    i_frame = fields.BooleanField(default=False, description='是否外链')
    cache = fields.BooleanField(default=False, description='缓存')
    hidden = fields.BooleanField(default=False, description='是否隐藏')
    permission = fields.CharField(max_length=255, description='权限',  null=True)
    is_menu = fields.BooleanField(default=False, description='是否是菜单')

    class Meta:
        table = 'oa_menu'


    def __str__(self):
        return self.title

class Dept(BaseModel):
    """
    id, 父部门id, 子部门数目, name,
    """
    # 对于查询到的一个异步查询集，也就是一个对象，我们
    # 可以dept.pid--》去查询父级部门
    # 可以 dept.pid_id--》去查询父级部门的id
    # 可以 dept.children--》去查询子部门，也就是反向查询
    pid = fields.ForeignKeyField(model_name='models.Dept', description='父部门id', null=True,  on_delete=fields.SET_NULL,related_name="children")
    sub_count = fields.IntField(null=True, description='子部门数量')
    name = fields.CharField(max_length=64, description='部门名', unique=True)
    enabled = fields.BooleanField(default=True, description='状态')
    dept_sort = fields.IntField(description='排序',  null=True)

    class Meta:
        table = 'oa_dept'

    def __str__(self):
        return self.name


class Roles(BaseModel):
    """
    name, 级别， 描述， 数据权限，
    """
    name = fields.CharField(max_length=32, description='角色名',  null=True, unique=True)
    level = fields.IntField(description='角色级别',  null=True)
    description = fields.CharField(max_length=255, description='描述信息',  null=True)
    data_scope = fields.CharField(max_length=32, description='权限描述,唯一编码',  null=True)
    status = fields.BooleanField(default=True, description='是否启用?状态：1启用、0禁用')
    # 关联关系：table 指定中间表的名字
    depts = fields.ManyToManyField(model_name='models.Dept', through='oa_roles_depts', description='角色和部门的关联表')
    menus = fields.ManyToManyField(model_name='models.Menu', through='oa_roles_menus', description='角色和菜单的关联表')

    class Meta:
        table = 'oa_role'

    def __str__(self):
        return self.name


class Job(BaseModel):
    """
    岗位名称， 岗位状态， 排序，
    """
    name = fields.CharField(max_length=32, description='岗位名称',  null=True)
    enabled = fields.BooleanField(description='岗位状态', default=False)
    job_sort = fields.IntField(description='排序',  unique=True)

    class Meta:
        table = 'oa_job'

    def __str__(self):
        return self.name
    
    
if __name__ == '__main__':
    print(UserInfo.make_password('123456'))
