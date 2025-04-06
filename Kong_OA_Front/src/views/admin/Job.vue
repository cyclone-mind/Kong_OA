<template>
  <!--  按钮部分-->
  <div class="btn-area">
    <span>岗位列表</span>
    <div>
      <el-button type="primary" @click="dialogVisible = true"
        >新增岗位</el-button
      >
      <el-button type="danger" @click="delHandle()">批量删除</el-button>
    </div>
  </div>
  <el-divider border-style="dashed" />
  <!--  展示-->
  <div class="data-area">
    <el-table
      ref="multipleTable"
      :data="tableData"
      tooltip-effect="dark"
      style="width: 100%"
      border
      stripe
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55"> </el-table-column>

      <el-table-column prop="name" label="岗位名称" width="120">
      </el-table-column>
      <el-table-column prop="job_sort" label="排序号"> </el-table-column>
      <el-table-column prop="enabled" label="状态">
        <template #default="scope">
          <el-tag size="small" v-if="scope.row.enabled" type="success"
            >正常</el-tag
          >
          <el-tag size="small" v-else type="danger">禁用</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="icon" label="操作">
        <template #default="scope">
          <el-button link @click="editHandle(scope.row.id)"
            >编辑</el-button
          >
          <el-divider direction="vertical"></el-divider>
          <el-popconfirm
            title="你确定删除吗?"
            @confirm="delHandle(scope.row.id)"
          >
            <template #reference>
              <el-button link type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </div>

  <!--  新增和修改部门对话框-->
  <!--  新增修改对话框-->
  <el-dialog
    title="提示"
    v-model:="dialogVisible"
    width="600px"
    :before-close="handleClose"
  >
    <el-form
      :model="editForm"
      label-width="100px"
      :rules="editFormRules"
      ref="editFormRef"
    >
      <el-form-item label="岗位名称" prop="name" label-width="100px">
        <el-input v-model="editForm.name" autocomplete="off"></el-input>
      </el-form-item>

      <el-form-item label="排序" prop="job_sort" label-width="100px">
        <el-input v-model="editForm.job_sort" autocomplete="off"></el-input>
      </el-form-item>

      <el-form-item label="状态" prop="enabled" label-width="100px">
        <el-radio-group v-model="editForm.enabled">
          <el-radio :value="false">禁用</el-radio>
          <el-radio :value="true">正常</el-radio>
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
import { ref } from "vue";
import {
  reqJobList,
  reqJob,
  reqDeleteJob,
  reqUpdateJob,
  reqCreateJob,
} from "../../api/system.js";
import { ElMessage } from "element-plus";

// 左侧checkbox--》多选
const multipleSelection = ref([]);
// 岗位Table的数据源
const tableData = ref([]);
// 新增岗位对话框功能
const dialogVisible = ref(false);
// 新增岗位数据的字典
const editForm = ref({
  name: "",
  job_sort: "",
  enabled: 1,
});

const editFormRef = ref(null);
// 校验表单
const editFormRules = ref({
  name: [
    { required: true, message: "岗位名必填", trigger: "blur" },
    { min: 1, max: 8, message: "岗位名最短1，最长8", trigger: "blur" },
  ],
});
// 加载所有部门
async function getJobList() {
  let res = await reqJobList();
  tableData.value = res.results;
}
// 删除方法-->单删和多删
function handleSelectionChange(val) {
  multipleSelection.value = val;
  console.log("选中了", multipleSelection);
}

// 单删和多删
async function delHandle(id) {
  let ids = [];
  if (id) {
    ids.push(id); // 单删
  } else {
    multipleSelection.value.forEach((row) => {
      ids.push(row.id);
    });
  }
  // 如果不传id就以multipleSelection为准，多删
  console.log("要删除的岗位是：", ids);
  let res = await reqDeleteJob(ids);
  ElMessage({
    message: "删除岗位成功",
    type: "success",
    plain: true,
    onClose: () => {
      getJobList();
    },
  });
}
// 修改新增框弹出后，关闭
function handleClose() {
  dialogVisible.value = false;
  editForm.value = {};
}

// 修改或新增
async function submitForm() {
  // 数据校验过后，才能提交
  await editFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      console.log("数据合法!");
      //发送网络请求，提交数据
      let res;
      if (editForm.value.id) {
        res = await reqUpdateJob(editForm.value.id, editForm.value);
      } else {
        res = await reqCreateJob(editForm.value);
      }
      ElMessage({
        message: res.msg,
        type: "success",
        plain: true,
        onClose: () => {
          handleClose();
          getJobList();
        },
      });
    } else {
      console.log("数据有误", fields);
    }
  });
}

// 加载单个
async function editHandle(id) {
  let res = await reqJob(id);
  editForm.value = res.result;
  dialogVisible.value = true;
}

getJobList();
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
