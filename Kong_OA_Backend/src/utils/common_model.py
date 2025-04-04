from tortoise import Model, fields
#  基表，以后所有表都继承这个表，这些字段就不用写了
class BaseModel(Model):
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间',  null=True)
    update_time = fields.DatetimeField(auto_now=True, description='更新时间', null=True)
    create_by = fields.CharField(max_length=32, description='创建者', null=True)
    update_by = fields.CharField(max_length=32, description='更新者',  null=True)
    is_delete = fields.BooleanField(default=False, description='是否删除')

    class Meta:
        abstract = True # 不在数据库中生成，只用来继承