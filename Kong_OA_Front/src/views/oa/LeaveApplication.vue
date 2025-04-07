<template>
    <!--  按钮部分-->
    <div class="btn-area">
      <span>我的请假记录</span>
      <div>
        <!--v-if="hasAuth('leave:add')"-->
        <el-button type="primary" @click="dialogVisible=true" >申请请假</el-button>
      </div>
    </div>
    <el-divider border-style="dashed"/>
    <!--  展示-->
    <div class="data-area">
      <el-table
          :data="tableData"
          tooltip-effect="dark"
          style="width: 100%"
          border
          stripe>
  
        <el-table-column
            prop="owner.nick_name"
            label="请假人"
            width="120">
        </el-table-column>
        <el-table-column
            prop="reason"
            label="请假事由">
        </el-table-column>
        <el-table-column
            prop="time"
            label="请假时间">
        </el-table-column>
        <el-table-column
            prop="days"
            label="请假天数">
        </el-table-column>
        <el-table-column
            prop="type"
            label="请假类型">
          <template #default="scope">
            <el-tag size="small" v-if="scope.row.type==1" type="success">病假</el-tag>
            <el-tag size="small" v-if="scope.row.type==2" type="success">事假</el-tag>
            <el-tag size="small" v-if="scope.row.type==3" type="success">年假</el-tag>
          </template>
  
        </el-table-column>
        <el-table-column
            prop="status"
            label="请假状态">
          <template #default="scope">
            <el-tag size="small" v-if="scope.row.status==0" type="danger">待审批</el-tag>
            <el-tag size="small" v-if="scope.row.status==1" type="success">通过</el-tag>
            <el-tag size="small" v-if="scope.row.status==2" type="warning">驳回</el-tag>
          </template>
  
        </el-table-column>
        <el-table-column
            prop="icon"
            label="操作">
          <template #default="scope">
  
            <el-button link @click="editHandle(scope.row.id)">编辑</el-button>
            <el-divider direction="vertical"></el-divider>
            <el-popconfirm title="你确定删除吗?" @confirm="delHandle(scope.row.id)" >
              <template #reference>
                <el-button link type="danger">删除</el-button>
              </template>
            </el-popconfirm>
  
          </template>
        </el-table-column>
  
      </el-table>
    </div>
  
    <!--  新增修改对话框-->
    <el-dialog
        title="提示"
        v-model:="dialogVisible"
        width="600px"
        :before-close="handleClose">
  
      <el-form :model="editForm" label-width="100px" :rules="editFormRules" ref="editFormRef">
  
        <el-form-item label="请假事由" prop="reason" label-width="100px">
          <el-input v-model="editForm.reason" autocomplete="off"></el-input>
        </el-form-item>
  
        <el-form-item label="请假开始" prop="time" label-width="100px">
          <el-input v-model="editForm.time" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="请假天数" prop="days" label-width="100px">
          <el-input v-model="editForm.days" autocomplete="off"></el-input>
        </el-form-item>
  
        <el-form-item label="请假类型" prop="enabled" label-width="100px">
          <el-radio-group v-model="editForm.type">
            <el-radio :value='1'>病假</el-radio>
            <el-radio :value='2'>事假</el-radio>
            <el-radio :value='3'>年假</el-radio>
          </el-radio-group>
        </el-form-item>
  
        <el-form-item>
          <el-button type="primary" @click="submitForm()">立即创建</el-button>
          <el-button @click="handleClose()">重置</el-button>
        </el-form-item>
      </el-form>
  
    </el-dialog>
  
  
  </template>
  <script setup>
  import {ref} from "vue";
  
  import {ElMessage} from "element-plus";
  import {reqDeleteLeave, reqLeaveList,reqCreateLeave,reqLeave,reqUpdateLeave} from "../../api/leave.js";
  
  // Table的数据源
  const tableData = ref([])
  // 新增对话框功能
  const dialogVisible = ref(false)
  // 新增岗位数据的字典
  const editForm = ref({
    reason: '',
    time: '',
    leave_type: 1,
  })
  
  const editFormRef = ref(null)
  // 校验表单
  const editFormRules = ref({
    reason: [
      {required: true, message: '请假原因必填', trigger: 'blur'},
      {min: 1, max: 30, message: '请假原因最短1，最长30', trigger: 'blur'},
    ],
    time: [
      {required: true, message: '请假时间必填', trigger: 'blur'},
    ],
    days: [
      {required: true, message: '请假天数必填', trigger: 'blur'},
    ],
  
  
  })
  
  // 加载本人所有请假
  async function getOwnLeaveList() {
    let res = await reqLeaveList(1)
    tableData.value = res.results
  }
  
  
  // 单删和多删
  async function delHandle(id) {
    let ids = []
    ids.push(id)
    let res = await reqDeleteLeave(ids)
    ElMessage({
      message: res.msg,
      type: 'success',
      plain: true,
      onClose: () => {
        getOwnLeaveList()
      }
    })
  
  }
  
  // 修改新增框弹出后，关闭
  function handleClose() {
    dialogVisible.value = false
    editForm.value = {}
  }
  
  // 修改或新增
  async function submitForm() {
    // 数据校验过后，才能提交
    await editFormRef.value.validate(async (valid, fields) => {
      if (valid) {
        console.log('数据合法!')
        //发送网络请求，提交数据
        let res
        if (editForm.value.id) {
          res = await reqUpdateLeave(editForm.value.id, editForm.value)
        } else {
          res = await reqCreateLeave(editForm.value)
        }
        ElMessage({
          message: res.msg,
          type: 'success',
          plain: true,
          onClose: () => {
            handleClose()
            getOwnLeaveList()
          }
        })
      } else {
        console.log('数据有误', fields)
      }
    })
  }
  
  // 加载单个
  async function editHandle(id) {
    let res = await reqLeave(id)
    editForm.value = res.result
    dialogVisible.value = true
  }
  
  
  getOwnLeaveList()
  
  </script>
  
  
  <style scoped>
  .btn-area {
    display: flex;
    justify-content: space-between;
  }
  
  .btn-area > span {
    font-size: 20px;
    font-weight: bold;
  }
  </style>