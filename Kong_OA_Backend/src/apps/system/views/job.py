from fastapi import APIRouter
from src.apps.system.models import Job
from src.apps.system.schemas import JobOutSchema, JobInSchema
from src.utils.common_response import APIResponse
from typing import List
router = APIRouter()


# 1 查询所有岗位，不分页，不需要带page和page_size--》登录才能使用
@router.get('/jobs', description='查询所有岗位')
async def get_job_list(
        # user: UserInfo = Depends(get_current_user)
):
    # 岗位，分父级和子级---》到时候要加过滤条件--》只查出没有父级的岗位--》最顶级岗位
    jobs = await Job.filter(is_delete=False).all()
    job_dicts = [JobOutSchema.from_orm(job).dict() for job in jobs]
    return APIResponse(results=job_dicts)


# 3 岗位新增---{pid_id:1,sub_count；5，name:山东分公司，enabled:True,Job_sort:1}
@router.post('/jobs', description='新增岗位')
async def add_job(
        job: JobInSchema,
        # user: UserInfo = Depends(get_current_user)
):
    await Job.create(**job.dict())
    return APIResponse('岗位新增成功')


# 4 删除岗位---》单条和多条
@router.delete('/jobs', description='删除岗位')
async def delete_Job(
        ids: List[int],  # [1,2,3]
        # user: UserInfo = Depends(get_current_user)
):
    await Job.filter(id__in=ids).update(is_delete=True)  # 软删除
    # res=await Job.filter(id__in=ids).delete() # 硬删除
    return APIResponse(msg='删除岗位成功')


# 5 查询一个岗位
@router.get('/jobs/{job_id}', description='查询一个岗位')
async def get_job(
        job_id: int  # /Jobs/1-->查询id为1的岗位详情
        # user: UserInfo = Depends(get_current_user)
):
    job = await Job.filter(id=job_id).first()
    job_dict = JobOutSchema.from_orm(job).dict()
    return APIResponse(msg='岗位查询成功', result=job_dict)


# 6 修改一个岗位
@router.put('/jobs/{job_id}', description='修改一个岗位')
async def get_job(
        job_id: int,  # /Jobs/1-->修改id为1的岗位详情
        job: JobInSchema,
        # user: UserInfo = Depends(get_current_user)
):
    await Job.filter(id=job_id).update(**job.dict())
    return APIResponse(msg='修改岗位成功')