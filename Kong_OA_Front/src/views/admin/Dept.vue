<template>
  <!--  按钮部分-->
  <div class="btn-area">
    <span>部门列表</span>
    <div>
      <el-button type="primary" @click="addDeptHandle()" v-if="hasAuth('depts:add')">新增部门</el-button>
      <el-button type="danger" @click="delHandle()" v-if="hasAuth('depts:delete')">批量删除</el-button>
    </div>
  </div>
  <el-divider border-style="dashed" />
  <!--  部门展示-->
  <div class="data-area">
    <el-table
      :data="tableData"
      ref="multipleTableRef"
      row-key="id"
      stripe
      style="width: 100%"
      default-expand-all
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="name" label="名称" sortable width="180">
      </el-table-column>

      <el-table-column prop="dept_sort" label="排序号"> </el-table-column>
      <el-table-column prop="enabled" label="状态">
        <template #default="scope">
          <el-tag size="small" v-if="scope.row.enabled" type="success"
            >正常</el-tag
          >
          <el-tag size="small" v-else="scope.row.enabled" type="danger"
            >禁用</el-tag
          >
        </template>
      </el-table-column>

      <el-table-column prop="create_time" label="创建时间"> </el-table-column>
      <el-table-column prop="icon" label="操作">
        <template #default="scope">
          <el-button link @click="editHandle(scope.row.id)" v-if="hasAuth('depts:update')"
            >编辑</el-button
          >
          <el-divider direction="vertical"></el-divider>
          <el-popconfirm
            title="你确定删除吗?"
            @confirm="delHandle(scope.row.id)" v-if="hasAuth('depts:delete')"
          >
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
    title="部门操作"
    v-model="dialogVisible"
    width="600px"
    :before-close="handleClose"
  >
    <el-form
      :model="editForm"
      :rules="editFormRules"
      ref="editFormRef"
      label-width="100px"
      class="demo-editForm"
    >
      <el-form-item label="部门名称" prop="name" label-width="100px">
        <el-input v-model="editForm.name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="部门序号" prop="dept_sort" label-width="100px">
        <el-input v-model="editForm.dept_sort" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="状态" prop="enabled" label-width="100px">
        <el-radio-group v-model="editForm.enabled">
          <el-radio :label="false">禁用</el-radio>
          <el-radio :label="true">正常</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="顶级部门" prop="pid_id" label-width="100px">
        <el-radio-group
          v-model="editForm.type"
          @change="
            editForm.type == 0
              ? (chooseParentDept = true)
              : (chooseParentDept = false)
          "
        >
          <el-radio :label="1">是</el-radio>
          <el-radio :label="0">否</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="上级部门" prop="pid_id" v-show="chooseParentDept">
        <el-select v-model="editForm.pid_id" placeholder="请选择上级部门">
          <template v-for="item in tableData">
            <el-option :label="item.name" :value="item.id"></el-option>
            <template v-for="child in item.children">
              <el-option :label="child.name" :value="child.id">
                <span>{{ "- " + child.name }}</span>
              </el-option>
            </template>
          </template>
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="submitForm()">提交</el-button>
        <el-button @click="handleClose()">取消</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive } from "vue";
import {
  reqDeptList,
  reqDept,
  reqDeleteDept,
  reqUpdateDept,
  reqCreateDept,
} from "../../api/system.js";
import { ElMessage } from "element-plus";
import { hasAuth } from "../../routers/utils.js";


// ======== 状态变量定义 ========
// 部门列表数据
const tableData = ref([]);
// 选中的部门列表，用于批量删除
const multipleSelection = ref([]);
// 表单引用
const editFormRef = ref(null);
// 对话框显示状态
const dialogVisible = ref(false);
// 是否显示上级部门选择框
const chooseParentDept = ref(false);

// 部门表单数据
const editForm = ref({
  name: "",
  dept_sort: "",
  enabled: 1,
  pid_id: "",
  type: 1, // 默认为顶级部门
});

// 表单验证规则
const editFormRules = ref({
  name: [
    { required: true, message: "岗位名必填", trigger: "blur" },
    { min: 3, max: 8, message: "岗位名最短3，最长8", trigger: "blur" },
  ],
  dept_sort: [{ required: true, message: "请输入部门序号", trigger: "blur" }],
});

// ======== 生命周期方法 ========
// 初始化加载部门列表
getDeptList();

// ======== 方法定义 ========
/**
 * 加载所有部门数据
 */
async function getDeptList() {
  let res = await reqDeptList();
  tableData.value = res.results;
}

/**
 * 新增部门按钮点击事件
 */
function addDeptHandle() {
  dialogVisible.value = true;
  // 默认顶级部门时，不显示上级部门选择框
  chooseParentDept.value = false;
}

/**
 * 关闭对话框，重置表单
 */
function handleClose() {
  dialogVisible.value = false;
  editForm.value = {
    name: "",
    dept_sort: "",
    enabled: 1,
    pid_id: "",
    type: 1, // 重置为顶级部门
  };
}

/**
 * 提交表单数据（新增或修改）
 */
async function submitForm() {
  // 数据校验过后，才能提交
  await editFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      //发送网络请求，提交数据
      let res;
      // editForm如果没有pid_id，是最顶级--》就把pid_id删除
      if (!editForm.value.pid_id) {
        delete editForm.value.pid_id;
      }
      if (editForm.value.id) {
        // 修改
        res = await reqUpdateDept(editForm.value.id, editForm.value);
      } else {
        // 新增
        res = await reqCreateDept(editForm.value);
      }
      handleClose();
      getDeptList();

      ElMessage({
        message: res.msg,
        type: "success",
        plain: true,
      });
    } else {
      console.log("数据有误", fields);
    }
  });
}

/**
 * 编辑部门信息
 * @param {number} id 部门ID
 */
async function editHandle(id) {
  let res = await reqDept(id);
  editForm.value = res.result;

  // 判断是否为顶级部门：如果pid_id为空则为顶级部门
  editForm.value.type = editForm.value.pid_id ? 0 : 1;
  // 根据type控制是否显示上级部门选择
  chooseParentDept.value = editForm.value.type === 0;

  dialogVisible.value = true;
}

/**
 * 表格选择变化事件处理
 * @param {Array} val 选中的行
 */
function handleSelectionChange(val) {
  multipleSelection.value = val;
  console.log("选中了", multipleSelection);
}

/**
 * 删除部门（单个或批量）
 * @param {number} id 部门ID，不传则为批量删除
 */
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
  console.log("要删除的部门是：", ids);
  let res = await reqDeleteDept(ids);
  ElMessage({
    message: "删除部门成功",
    type: "success",
    plain: true,
    onClose: () => {
      getDeptList();
    },
  });
}
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
