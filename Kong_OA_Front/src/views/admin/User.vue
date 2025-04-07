<template>
  <div class="area-search">
    <el-form :inline="true" class="demo-form-inline">
      <el-form-item label="用户名">
        <el-input v-model="searchForm.username" placeholder="输入用户名" clearable/>
      </el-form-item>
      <el-form-item label="用户昵称">
        <el-input v-model="searchForm.nick_name" placeholder="输入昵称" clearable/>
      </el-form-item>
      <el-form-item label="用户状态">
        <el-select
            v-model="searchForm.is_active"
        >
          <el-option label="活跃" :value="true"/>
          <el-option label="锁定" :value="false"/>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">查询</el-button>
      </el-form-item>
    </el-form>


  </div>
  <el-divider border-style="dashed"/>
  <div class="area-btn">
    <span>用户列表</span>
    <div>
      <el-button type="primary" @click="dialogVisible=true" v-if="hasAuth('user:add')">新增</el-button>
      <el-button type="success" @click="deleteHandle()" v-if="hasAuth('user:delete')">批量删除</el-button>
      <el-button type="warning" @click="lockUsersHandle()" v-if="hasAuth('user:lock')">批量停用</el-button>

    </div>
  </div>
  <el-divider border-style="dashed"/>
  <div class="area-table">
    <el-table
        ref="multipleTableRef"
        :data="usersData"
        style="width: 100%"
        @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55"/>
      <el-table-column label="头像" width="100">
        <template #default="scope">
          <el-avatar :size="40" :src="scope.row.avatar"></el-avatar>
        </template>
      </el-table-column>
      <el-table-column property="username" label="用户名" width="120"/>
      <el-table-column property="nick_name" label="用户昵称"/>
      <el-table-column property="gender" label="性别" width="100">
        <template #default="scope">
          <el-tag v-if="scope.row.gender==1">男</el-tag>
          <el-tag v-else-if="scope.row.gender==2">女</el-tag>
          <el-tag v-else>未知</el-tag>
        </template>
      </el-table-column>
      <el-table-column property="roles" label="角色名称">
        <template #default="scope">
          <el-tag size="small" type="danger" v-for="item in scope.row.roles_detail">{{ item.name }}</el-tag>
        </template>

      </el-table-column>
      <el-table-column property="email" label="邮箱"></el-table-column>
      <el-table-column property="phone" label="手机号"></el-table-column>
      <el-table-column property="is_active" label="状态">
        <template #default="scope">
          <el-tag size="small" v-if="scope.row.is_active" type="success">正常</el-tag>
          <el-tag size="small" v-else type="danger">禁用</el-tag>
        </template>

      </el-table-column>

      <el-table-column width="300px" label="操作">
        <template #default="scope">
          <el-button link type="primary" @click="setRoles(scope.row.id)" v-if="hasAuth('user:role')">分配角色
          </el-button>
          <el-divider direction="vertical"></el-divider>
          <el-popconfirm title="你确定重置密码为123456吗?" @confirm="resetPassword(scope.row.id)"
                         >
            <template #reference>
              <el-button link type="primary" v-if="hasAuth('user:resetpassword')">重置密码</el-button>
            </template>
          </el-popconfirm>
          <el-divider direction="vertical"></el-divider>
          <el-button link type="primary" @click="handleEdit(scope.row.id)" v-if="hasAuth('user:update')">编辑
          </el-button>
          <el-divider direction="vertical"></el-divider>
          <el-popconfirm title="你确定删除吗?" @confirm="deleteHandle(scope.row.id)">
            <template #reference>
              <el-button link type="danger">删除</el-button>
            </template>
          </el-popconfirm>


        </template>
      </el-table-column>

    </el-table>

  </div>
  <div class="area-page">
    <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        layout="total, sizes, prev, pager, next, jumper"
        :page-sizes="[2,5,8]"
        :current-page="searchForm.page"
        :page-size="searchForm.page_size"
        :total="total">
    </el-pagination>
  </div>


  <!--  新增对话框-->
  <el-dialog :before-close="handleClose" v-model="dialogVisible" title="用户操作" width="600px" center>

    <el-form ref="editFormRef" :model="userEditForm" :rules="editFormRules">
      <el-form-item label="用户名:" prop="username" label-width="70px">
        <el-input v-model="userEditForm.username"/>
        <el-alert
            title="初始密码为:123456"
            :closable="false"
            type="info"
        ></el-alert>
      </el-form-item>
      <el-form-item label="性 别:" prop="gender" label-width="70px">
        <el-radio-group v-model="userEditForm.gender">
          <el-radio :value="1" border style="width: 230px">男</el-radio>
          <el-radio :value="2" border style="width: 230px">女</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="电 话:" prop="phone" label-width="70px">
        <el-input v-model.number="userEditForm.phone"/>
      </el-form-item>
      <el-form-item label="昵 称:" prop="nick_name" label-width="70px">
        <el-input v-model="userEditForm.nick_name"/>
      </el-form-item>
      <el-form-item label="邮 箱:" prop="email" label-width="70px">
        <el-input v-model="userEditForm.email"/>
      </el-form-item>


      <el-form-item label="岗 位:" prop="jobs" label-width="70px">
        <el-select
            v-model="userEditForm.job"
            multiple
            placeholder="请选择"
        >
          <el-option
              v-for="item in jobData"
              :key="item.name"
              :label="item.name"
              :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="部 门:" label-width="70px">
        <el-tree-select
            placeholder="选择部门"
            v-model="userEditForm.dept_id"
            :data="deptData"

        />
      </el-form-item>


      <el-form-item label="角 色:" prop="roles" label-width="70px">
        <el-select
            v-model="userEditForm.roles"
            multiple
            placeholder="请选择"
        >
          <el-option
              v-for="item in roleTreeData"
              :key="item.name"
              :label="item.name"
              :value="item.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="状 态:" prop="is_active" label-width="70px">
        <el-radio-group v-model="userEditForm.is_active">
          <el-radio :label="false" border style="width: 230px">禁用</el-radio>
          <el-radio :label="true" border style="width: 230px">启用</el-radio>
        </el-radio-group>

      </el-form-item>

    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="text" @click="handleClose()">取消</el-button>
        <el-button type="primary" @click="submitForm()">确认</el-button>
      </div>
    </template>
  </el-dialog>
  <!--  分配角色对话框-->
  <el-dialog title="分配角色" v-model="roleDialogFormVisible" width="600px">
    <el-tree
        :data="roleTreeData"
        show-checkbox
        ref="roleTreeRef"
        :check-strictly=true
        node-key="id"
        :default-expand-all=true
        :props="{children: 'children',label: 'name'}"
    >
    </el-tree>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="roleDialogFormVisible=false">取 消</el-button>
        <el-button type="primary" @click="submitRoleHandle()">确 定</el-button>
      </div>
    </template>

  </el-dialog>

</template>

<script setup>
import {reactive, ref} from 'vue'
import {
  reqUserList,
  reqDeleteUser,
  reqUser,
  reqResetPassword,
  reqLockUsers,
  reqUpdateUser,
  reqCreateUser
} from "../../api/user.js";
import {ElMessage} from "element-plus";
import {reqDeptTreeList, reqJobList, reqRoleList} from "../../api/system.js";
import {hasAuth} from "../../routers/utils.js";

// ###变量定义###
// 1.1 搜索条件
const searchForm = reactive({
  username: '',
  nick_name: '',
  is_active: true,
  page: 1,
  page_size: 5
})
// 1.2 总条数---分页用
const total = ref(0)
// 1.3 表格展示需要的数据
const usersData = ref([])
// 1.4 定义列表，存放选中的用户---》批量操作时的checkbox
const multipleSelection = ref([])
// 1.5 新增或修改用户，弹出框是否显示
const dialogVisible = ref(false)
// 1.6 用户分配角色时，弹出框是否展示
const roleDialogFormVisible = ref(false)
// 1.7 新增或修改用户数据校验
const editFormRules = reactive({
  username: [
    {required: true, message: '请输入用户名称', trigger: 'blur'}
  ],
  nick_name: [
    {required: true, message: '请输入昵称', trigger: 'blur'}
  ],
  phone: [
    {required: true, message: '手机号', trigger: 'blur'}
  ],
  email: [
    {required: true, message: '请输入邮箱', trigger: 'blur'}
  ],
  gender: [
    {required: true, message: '请选择性别', trigger: 'blur'}
  ],

})
// 1.8 新增或修改用户的数据对象
const userEditForm = ref({})
// 1.9 新增或修改用户时--》校验通过--》才能提交表单--》使用这个变量来判断是否校验通过
const editFormRef = ref(null)
// 1.10 所有部门列表
const deptData = ref([])
// 1.11 所有岗位列表
const jobData = ref([])
// 1.12 所有角色
const roleTreeData = ref([])
// 1.13 分配角色--多选--checkbox--》被选中的数组
const roleTreeRef = ref(null)

//##### 方法#########
// 2.1 新增或修改用户关闭方法
function handleClose() {
  dialogVisible.value = false
  userEditForm.value = {
    job: [],
    dept: '',
    roles: []
  }
}

// 2.2 搜索按钮被点击
const onSubmit = () => {
  searchForm.page = 1
  searchForm.page_size = 5
  getUserList()
}

// 2.3  分页2个函数
function handleSizeChange(val) {
  searchForm.page_size = val
  getUserList()

}
function handleCurrentChange(val) {
  searchForm.page = val
  getUserList()
}

// 2.4 查询用户列表
async function getUserList() {
  let res = await reqUserList(searchForm)
  usersData.value = res.results
  total.value = res.total
}


// 2.5  选中某个用户--checkbox，会触发
function handleSelectionChange(val) {
  multipleSelection.value = val
  console.log('选中了', multipleSelection)
}

// 2.6 删除功能
async function deleteHandle(id) {
  let ids = []
  // 如果传了id，就是单删
  if (id) {
    ids.push(id)
  } else {
    multipleSelection.value.forEach(row => {
      ids.push(row.id)
    })
  }
  // 如果不传id就以multipleSelection为准，多删
  console.log('要删除的用户是：', ids)
  let res = await reqDeleteUser(ids)
  ElMessage({
    message: '删除成功',
    type: 'success',
    plain: true,
    onClose: () => {
      getUserList()
    }
  })
}

// 2.7 获取部门列表---新增用户用
async function getDeptList() {
  let res = await reqDeptTreeList()
  deptData.value = res.results
}

// 2.8 获取所有岗位
async function getJobList() {
  let res = await reqJobList()
  jobData.value = res.results
}

// 2.9 获取所有角色
async function getRoleList() {
  let res = await reqRoleList()
  roleTreeData.value = res.results
}

// 2.10 分配角色
async function setRoles(id) {
  roleDialogFormVisible.value = true
  let res = await reqUser(id)
  roleTreeRef.value.setCheckedKeys(res.result.roles);
  userEditForm.value = res.result
}

// 2.11 重置密码
async function resetPassword(id) {
  let res = await reqResetPassword(id)
  ElMessage({
    message: res.msg,
    type: 'success',
    plain: true,
  })
}

// 2.12锁定用户
async function lockUsersHandle() {
  let ids = []
  multipleSelection.value.forEach(row => {
    ids.push(row.id)
  })
  let res = await reqLockUsers(ids)
  ElMessage({
    message: res.msg,
    type: 'success',
    plain: true,
    onClose: () => {
      getUserList()
    }
  })

}

// 2.13 分配角色的提交
async function submitRoleHandle() {
  let roles = roleTreeRef.value.getCheckedKeys()
  userEditForm.value.roles = roles
  let res = await reqUpdateUser(userEditForm.value.id, userEditForm.value)
  ElMessage({
    message: res.msg,
    type: 'success',
    plain: true,
    onClose: () => {
      roleDialogFormVisible.value = false
      getUserList()
    }
  })

}

// 2.14 点击修改按钮--》查询当前用户详情，渲染到弹出框中
async function handleEdit(id) {
  dialogVisible.value = true
  let res = await reqUser(id)
  userEditForm.value = res.result
}

// 2.15 新增或修改的提交
async function submitForm() {
  // 数据校验过后，才能提交
  await editFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      console.log('数据合法!')
      //发送网络请求，提交数据
      let res
      if (userEditForm.value.id) {
        res = await reqUpdateUser(userEditForm.value.id, userEditForm.value)
      } else {
        res = await reqCreateUser(userEditForm.value)
      }
      ElMessage({
        message: res.msg,
        type: 'success',
        plain: true,
        onClose: () => {
          handleClose()
          getUserList()
        }
      })
    } else {
      console.log('数据有误', fields)
    }
  })
}

getUserList()
getJobList()
getDeptList()
getRoleList()


</script>
<style scoped>
.demo-form-inline .el-input {
  --el-input-width: 220px;
}

.demo-form-inline .el-select {
  --el-select-width: 220px;
}

.area-btn {
  display: flex;
  justify-content: space-between;
}

.area-btn > span {
  font-size: 20px;
  font-weight: bold;
}

.area-page {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

</style>