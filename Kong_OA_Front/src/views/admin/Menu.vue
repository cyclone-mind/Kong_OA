<template>
    <!--  按钮部分-->
    <div class="btn-area">
      <span>菜单列表</span>
      <div>
        <el-button type="primary" @click="dialogVisible=true">新增菜单</el-button>
      </div>
    </div>
    <el-divider border-style="dashed"/>
    <!--  展示-->
    <div class="data-area">
      <el-table
          :data="tableData"
          style="width: 100%;margin-bottom: 20px;"
          row-key="id"
          border
          stripe
          :tree-props="{children: 'children', hasChildren: 'hasChildren'}">
  
        <el-table-column
            prop="title"
            label="名称"
            sortable
            width="180">
        </el-table-column>
        <el-table-column
            prop="permission"
            label="权限编码"
            sortable
            width="180">
        </el-table-column>
  
        <el-table-column
            prop="icon"
            label="图标">
        </el-table-column>
  
        <el-table-column
            prop="type"
            label="类型">
          <template #default="scope">
            <el-tag size="small" v-if="scope.row.type === 0">目录</el-tag>
            <el-tag size="small" v-else-if="scope.row.type === 1" type="success">菜单</el-tag>
            <el-tag size="small" v-else-if="scope.row.type === 2" type="info">按钮</el-tag>
          </template>
  
        </el-table-column>
  
        <el-table-column
            prop="path"
            label="菜单URL">
        </el-table-column>
        <el-table-column
            prop="component"
            label="菜单组件">
        </el-table-column>
        <el-table-column
            prop="menu_sort"
            label="排序号">
        </el-table-column>
        <el-table-column
            prop="hidden"
            label="状态">
          <template #default="scope">
            <el-tag size="small" v-if="!scope.row.hidden" type="success">正常</el-tag>
            <el-tag size="small" v-else type="danger">隐藏</el-tag>
          </template>
  
        </el-table-column>
        <el-table-column
            prop="icon"
            label="操作">
  
          <template #default="scope">
            <el-button type="text" @click="editHandle(scope.row.id)">编辑</el-button>
            <el-divider direction="vertical"></el-divider>
  
            <el-popconfirm title="你确定删除吗?" @confirm="delHandle(scope.row.id)">
              <template #reference>
                <el-button link type="danger">删除</el-button>
              </template>
            </el-popconfirm>
  
          </template>
        </el-table-column>
  
      </el-table>
  
    </div>
  
    <!--  新增和修改菜单对话框-->
    <el-dialog
        title="提示"
        v-model:="dialogVisible"
        width="600px"
        :before-close="handleClose">
  
      <el-form :model="editForm" :rules="editFormRules" ref="editFormRef" label-width="100px">
  
        <el-form-item label="类型" label-width="100px">
          <el-radio-group v-model="editForm.type">
            <el-radio :value=0>目录</el-radio>
            <el-radio :value=1>菜单</el-radio>
            <el-radio :value=2>按钮</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="上级菜单">
          <el-tree-select
              placeholder="选择上级菜单"
              check-strictly=true
              v-model="editForm.pid_id"
              :render-after-expand="false"
              :data="editTableData"
          />
        </el-form-item>
  
        <el-form-item label="标题" prop="title" label-width="100px">
          <el-input v-model="editForm.title" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="名字" prop="name" label-width="100px">
          <el-input v-model="editForm.name" autocomplete="off"></el-input>
        </el-form-item>
  
        <el-form-item label="图标" prop="icon" v-show="editShow.icon" label-width="100px">
          <el-input v-model="editForm.icon" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="地址" prop="path" v-show="editShow.path" label-width="100px">
          <el-input v-model="editForm.path" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="权限编码" prop="permission" v-show="editShow.permission" label-width="100px">
          <el-input v-model="editForm.permission" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="菜单组件" prop="component" v-show="editShow.component" label-width="100px">
          <el-input v-model="editForm.component" autocomplete="off"></el-input>
        </el-form-item>
  
        <el-form-item label="状态" prop="statu" label-width="100px">
          <el-radio-group v-model="editForm.hidden">
            <el-radio :value='true'>禁用</el-radio>
            <el-radio :value='false'>正常</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="排序号" prop="menu_sort" label-width="100px">
          <el-input-number v-model="editForm.menu_sort" :min="1" label="排序号">1</el-input-number>
        </el-form-item>
  
  
        <el-form-item>
          <el-button type="primary" @click="submitForm()">立即创建</el-button>
          <el-button @click="handleClose()">重置</el-button>
        </el-form-item>
      </el-form>
  
    </el-dialog>
  
  
  </template>
  <script setup>
  import {ref, watch} from "vue";
  import {
    reqMenu,
    reqMenuList,
    reqUpdateMenu,
    reqCreateMenu,
    reqDeleteMenu,
    reqMenuTreeList
  } from "../../api/system.js";
  import {ElMessage} from "element-plus";
  
  
  const tableData = ref([])
  // 对话框功能
  const dialogVisible = ref(false)
  // 新增数据的字典
  const editForm = ref({
    type:2
  })
  const editFormRef = ref(null)
  // 校验表单
  const editFormRules = ref({
    type: [
      {required: true, message: '请选择类型', trigger: 'blur'}
    ],
    title: [
      {required: true, message: '请输入名称', trigger: 'blur'}
    ],
    hidden: [
      {required: true, message: '请选择状态', trigger: 'blur'}
    ],
    menu_sort: [
      {required: true, message: '请填入排序号', trigger: 'blur'}
    ]
  
  })
  // 新增菜单下拉选择用
  const editTableData = ref([])
  // 目录显示 ：图片，地址--》名字，状态，序号 都有
  // 菜单显示 ：图片，地址，权限编码，组件---》名字，状态，序号 都有
  // 按钮显示：权限编码 ---》名字，状态，序号 都有
  const editShow = ref({
    icon: true,
    path: true,
    permission: false,
    component: false,
  })
  
  // 加载所有菜单
  async function getMenuList() {
    let res = await reqMenuList()
    tableData.value = res.results
  }
  
  getMenuList()
  
  async function getMenuTreeList() {
    let res = await reqMenuTreeList()
    editTableData.value = res.results
  }
  
  getMenuTreeList()
  
  // 删除方法-->单删
  
  async function delHandle(id) {
    let ids = []
    ids.push(id) // 单删
    let res = await reqDeleteMenu(ids)
    ElMessage({
      message: '删除菜单成功',
      type: 'success',
      plain: true,
      onClose: () => {
        getMenuList()
      }
    })
  
  }
  
  
  function handleClose() {
    dialogVisible.value = false
    editForm.value = {}
  }
  
  
  // 监听属性
  watch(() => editForm.value.type, (newValue, oldValue) => {
    if (newValue == 0) { // 目录
      editShow.value.icon = true
      editShow.value.path = true
      editShow.value.permission = false
      editShow.value.component = false
      editForm.value.is_menu = true
  
    } else if (newValue == 1) {// 菜单
      editShow.value.icon = true
      editShow.value.path = true
      editShow.value.permission = true
      editShow.value.component = true
  
      editForm.value.is_menu = false
      editForm.value.component = 'Layout'
    } else {// 按钮
      editShow.value.icon = false
      editShow.value.path = false
      editShow.value.permission = true
      editShow.value.component = false
  
      editForm.value.is_menu = false
      editForm.value.component = null
    }
  })
  
  async function submitForm() {
    // 数据校验过后，才能提交
    await editFormRef.value.validate(async (valid, fields) => {
      if (valid) {
        console.log('数据合法!')
        //发送网络请求，提交数据
        let res
        if (editForm.value.id) {
          res = await reqUpdateMenu(editForm.value.id, editForm.value)
        } else {
          res = await reqCreateMenu(editForm.value)
        }
        ElMessage({
          message: res.msg,
          type: 'success',
          plain: true,
          onClose: () => {
            handleClose()
            getMenuList()
          }
        })
      } else {
        console.log('数据有误', fields)
      }
    })
  }
  
  // 加载单个
  async function editHandle(id) {
    let res = await reqMenu(id)
    editForm.value = res.result
    console.log(editForm.value, '----------')
    dialogVisible.value = true
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

