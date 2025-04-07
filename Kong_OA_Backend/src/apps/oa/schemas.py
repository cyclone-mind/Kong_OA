from pydantic import BaseModel,Field
class LeaveInSchema(BaseModel):
    reason:str
    time:str
    days:str
    type:int

class UserInfoSchema(BaseModel):
    id:int
    nick_name:str
    class Config:
        from_attributes = True

class LeaveOutSchema(BaseModel):
    id:int
    reason: str
    time: str
    days: str
    type: int
    status:int
    owner:UserInfoSchema|None
    class Config:
        from_attributes = True