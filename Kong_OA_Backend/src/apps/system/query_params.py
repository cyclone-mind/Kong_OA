from fastapi import Query
from typing import Optional
class PaginationQueryParams():
    def __init__(self,
                 page:int=Query(default=1,description='页码'),
                 page_size:int=Query(default=5,description='每页数量',ge = 1, le = 10))->None:
        self.page = page
        self.page_size = page_size

class UserQueryParams():
    def __init__(
            self,
            username: Optional[str] = Query(None, description="用户名"),
            nick_name: Optional[str] = Query(None, description="用户昵称"),
            is_active: Optional[bool] = Query(True, description="状态")
    ) -> None:
        self.username = username
        self.nick_name = nick_name
        self.is_active = is_active

    def to_query_params(self):
        query_params = {}
        for item, value in self.__dict__.items():  # slef.__dict={username:None,nick_name:None,is_active:false}
            if value:
                if item == 'is_active':
                    query_params.update({'is_active': value})
                else:
                    query_params.update({item + '__icontains': value})
        return query_params  # {nick_name__icontains:刘}