from typing import Any, Tuple, List, Optional
from fastapi.responses import ORJSONResponse as JSONResponse
from fastapi import status
import math

class APIResponse(JSONResponse):
    """
    成功响应
    """
    def __init__(
            self,
            msg: Optional[str] = "成功",
            code: int = 100,
            status_code: int = status.HTTP_200_OK,
            **kwargs
    ) -> None:
        self.data = {
            "code": code,
            "msg": msg
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status_code)
        
        
# 分页的
class PaginationResponse(JSONResponse):
    def __init__(
            self,
            data: List[Any] = [], # 要返回给前端的数据
            msg: Optional[str] = "查询成功",
            code: int = 100,  # 状态码
            page: int = 1,
            page_size: int = 10,
            status_code: int = status.HTTP_200_OK # http响应状态码
    ):
        if page < 1 or page_size < 1:
            raise

        total, results = self.get_paginated_response(data, page, page_size)
        has_next = True if math.ceil(total / page_size) > page else False
        self.data = {
            "code": code,
            "msg": msg,
            "total": total,
            "page": page,
            "page_size": page_size,
            "has_next": has_next,
            "results": results,
        }
        super().__init__(content=self.data, status_code=status_code)


    @staticmethod
    def get_paginated_response(data, page, page_size):
        """
        生成分页响应数据

        根据指定的页码和页大小，从数据列表中提取相应部分的数据返回

        参数:
        data (list): 待分页的数据列表
        page (int): 当前页码
        page_size (int): 每页数据大小

        返回:
        tuple: 包含数据总数和当前页的数据列表的元组
        """
        # 计算起始索引和结束索引
        start = (page - 1) * page_size
        end = page * page_size

        # 根据计算出的索引提取分页数据
        paginated_data = data[start:end]
        # 返回数据总数和分页数据
        return len(data), paginated_data