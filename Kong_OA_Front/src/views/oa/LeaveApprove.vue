<template>
    <!--  按钮部分-->
    <div class="btn-area">
      <span>我的请假记录</span>
      <div>
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
  
            <el-button link @click="changeLeaveStatus(scope.row.id,1)">通过</el-button>
            <el-divider direction="vertical"></el-divider>
            <el-popconfirm title="你确定驳回吗?" @confirm="changeLeaveStatus(scope.row.id,2)" >
              <template #reference>
                <el-button link type="danger">驳回</el-button>
              </template>
            </el-popconfirm>
  
          </template>
        </el-table-column>
  
      </el-table>
    </div>
  
  
  
  </template>
  <script setup>
  import {ref} from "vue";
  
  import {ElMessage} from "element-plus";
  import {hasAuth} from "../../routers/utils.js";
  import {
    reqLeaveList, reqChangeLeaveStatus,
  } from "../../api/leave.js";
  
  // Table的数据源
  const tableData = ref([])
  
  
  // 加载所有请假
  async function getLeaveList() {
    let res = await reqLeaveList(2)
    tableData.value = res.results
  }
  
  
  async function changeLeaveStatus(id,status){
      let res = await reqChangeLeaveStatus(id,status)
          ElMessage({
          message: res.msg,
          type: 'success',
          plain: true,
          onClose: () => {
            getLeaveList()
          }
        })
  
  }
  
  
  
  
  getLeaveList()
  
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