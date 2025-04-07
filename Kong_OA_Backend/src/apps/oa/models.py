from tortoise import Model, fields

from src.utils.common_model import BaseModel

class Leave(BaseModel):
    owner = fields.ForeignKeyField(model_name='models.UserInfo', on_delete=fields.SET_NULL, description='请假人',null=True)
    reason = fields.CharField(max_length=150,  description='请假原因')
    time = fields.CharField(max_length=128, description='请假开始时间')
    days = fields.CharField(max_length=128, description='请假天数')
    type = fields.IntField(default=1, description='请假类型:1病假，2事假，3年假')
    approver = fields.CharField(max_length=128, description='审批人',null=True)
    status=fields.IntField(default=0, description='请假状态:0已提交待审批，1审批通过，2审批驳回',null=True)

    class Meta:
        table = 'oa_leave'
