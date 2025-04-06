<template>
  <!--  按钮部分-->
  <div class="btn-area">
    <span>角色列表</span>
    <div>
      <el-button type="primary" @click="dialogVisible = true"
        >新建角色</el-button
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

      <el-table-column prop="name" label="名称" width="120"> </el-table-column>
      <el-table-column prop="data_scope" label="数据权限" show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip>
      </el-table-column>

      <el-table-column prop="status" label="状态">
        <template #default="scope">
          <el-tag size="small" v-if="scope.row.status" type="success"
            >正常</el-tag
          >
          <el-tag size="small" v-else type="danger">禁用</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="icon" label="操作">
        <template #default="scope">
          <el-button type="text" @click="permHandle(scope.row.id)"
            >分配权限</el-button
          >
          <el-divider direction="vertical"></el-divider>

          <el-button type="text" @click="editHandle(scope.row.id)"
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

  <!--  新增和修改权限话框-->
  <el-dialog
    title="提示"
    v-model="dialogVisible"
    width="600px"
    :before-close="handleClose"
  >
    <el-form
      :model="editForm"
      :rules="editFormRules"
      ref="editFormRef"
      label-width="100px"
    >
      <el-form-item label="角色名称" prop="name" label-width="100px">
        <el-input v-model="editForm.name"></el-input>
      </el-form-item>

      <el-form-item label="角色级别" prop="level">
        <el-input v-model="editForm.level" />
      </el-form-item>

      <el-form-item label="描述" prop="description" label-width="100px">
        <el-input v-model="editForm.description" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="数据范围" prop="data_scope">
        <el-select
          v-model="editForm.data_scope"
          placeholder="请选择"
          label-width="100px"
        >
          <el-option label="全部" value="全部" />
          <el-option label="本级" value="本级" />
          <el-option label="自定义" value="自定义" />
        </el-select>
      </el-form-item>
      <el-form-item
        label="数据权限"
        prop="description"
        label-width="100px"
        v-if="data_scope_show"
      >
        <el-tree-select
          placeholder="选择部门"
          v-model="editForm.depts"
          multiple
          :data="deptData"
          :check-strictly="true"
        />
      </el-form-item>

      <el-form-item label="状态" prop="status" label-width="100px">
        <el-radio-group v-model="editForm.status">
          <el-radio :label="false">禁用</el-radio>
          <el-radio :label="true">正常</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm()">立即创建</el-button>
        <el-button @click="handleClose()">重置</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
  <!-- 分配权限对话框-->
  <el-dialog title="分配权限" v-model="permDialogVisible" width="600px">
    <el-form :model="permForm">
      <el-tree
        :data="permTreeData"
        show-checkbox
        node-key="value"
        :default-expand-all="true"
        :check-strictly="true"
        :default-expanded-keys="[2, 3]"
        ref="permTreeRef"
      >
      </el-tree>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="permDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitPermFormHandle()"
          >确 定</el-button
        >
      </div>
    </template>
  </el-dialog>
</template>
<script setup>
import { ref, watch } from "vue";
import {
  reqRole,
  reqRoleList,
  reqUpdateRole,
  reqDeleteRole,
  reqCreateRole,
  reqDeptTreeList,
  reqMenuTreeList,
} from "../../api/system.js";
import { ElMessage } from "element-plus";
// #######定义变量#############
// 1.1 角色页面多选checkbox
const multipleSelection = ref([]);
// 1.2 角色列表展示数据--后端加载
const tableData = ref([]);
// 1.3 新增角色对话框功能：是否显示
const dialogVisible = ref(false);
// 1.4 分配权限对话框：是否显示
const permDialogVisible = ref(false);
// 1.5 新增角色数据的字典
const editForm = ref({
  name: "",
  job_sort: "",
  enabled: 1,
});
// 1.6 校验新增表单
const editFormRef = ref(null);
// 1.7 校验表单数据源
const editFormRules = ref({
  name: [{ required: true, message: "请输入角色名称", trigger: "blur" }],
  code: [{ required: true, message: "请输入唯一编码", trigger: "blur" }],
  statu: [{ required: true, message: "请选择状态", trigger: "blur" }],
});
//1.8 数据权限：全部，本级和自定义-自定义时此变量为true，可以选择部门
const data_scope_show = ref(false);
// 1.9 部门数据，创建角色时，分配数据权限，需要使用部门
const deptData = ref([]);
// 1.10 分配权限功能--》展示所有菜单
const permTreeData = ref([]);
// 1.11 分配权限功能--》被选中的菜单数组
const permTreeRef = ref(null);

// ###########方法############
// 2.1 获取所有部门树方法
async function getDeptList() {
  let res = await reqDeptTreeList();
  deptData.value = res.results;
}

// 2.2 加载所有角色
async function getRoleList() {
  let res = await reqRoleList();
  tableData.value = res.results;
}

// 2.3 删除角色方法-->checkbox选中与否控制
function handleSelectionChange(val) {
  multipleSelection.value = val;
  console.log("选中了", multipleSelection);
}
// 2.3 删除角色方法-->单删-多删
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
  let res = await reqDeleteRole(ids);
  ElMessage({
    message: "删除角色成功",
    type: "success",
    plain: true,
    onClose: () => {
      getRoleList();
    },
  });
}
// 2.4 关闭新增角色对话框
function handleClose() {
  dialogVisible.value = false;
  editForm.value = {};
}
// 2.5 提交角色数据：新增和修改共享
async function submitForm() {
  // 数据校验过后，才能提交
  await editFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      console.log("数据合法!");
      //发送网络请求，提交数据
      let res;
      if (editForm.value.id) {
        res = await reqUpdateRole(editForm.value.id, editForm.value);
      } else {
        res = await reqCreateRole(editForm.value);
      }
      ElMessage({
        message: res.msg,
        type: "success",
        plain: true,
        onClose: () => {
          handleClose();
          getRoleList();
        },
      });
    } else {
      console.log("数据有误", fields);
    }
  });
}

// 2.4 点击修改单个角色时触发
async function editHandle(id) {
  let res = await reqRole(id);
  editForm.value = res.result;
  console.log(editForm.value, "----------");
  dialogVisible.value = true;
}
// 2.5 获取菜单树--》分配权限用
async function getMenuTreeList() {
  let res = await reqMenuTreeList();
  permTreeData.value = res.results;
}

// 2.5 点击分配权限时触发--》先加载角色详情，查询角色下菜单权限--》使checkbox设为选中
async function permHandle(id) {
  permDialogVisible.value = true;
  let res_01 = await reqRole(id);
  editForm.value = res_01.result;
  // 查询当前角色目前的权限【菜单】
  let res_02 = await reqRole(id);
  permTreeRef.value.setCheckedKeys(res_02.result.menus);
}

// 2.6 分配权限提交时触发
async function submitPermFormHandle() {
  let menus = permTreeRef.value.getCheckedKeys();
  editForm.value.menus = menus;
  let res = await reqUpdateRole(editForm.value.id, editForm.value);
  ElMessage({
    message: res.msg,
    type: "success",
    plain: true,
    onClose: () => {
      permDialogVisible.value = false;
      permTreeRef.value.setCheckedKeys([]);
      getRoleList();
    },
  });
}

// 2.7 监听data_scope属性--自定义数据权限时，可以选择部门
watch(
  () => editForm.value.data_scope,
  (newValue, oldValue) => {
    if (newValue == "自定义") {
      data_scope_show.value = true;
    } else {
      delete editForm.value.depts;
      data_scope_show.value = false;
    }
  }
);

getMenuTreeList();
getDeptList();
getRoleList();
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
