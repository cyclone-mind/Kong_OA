<template>
  <!-- 使用 Element UI 的 el-menu 组件来构建侧边栏菜单 -->
  <el-menu default-active="1" <!-- 默认激活的菜单项 -->
    class="el-menu-vertical-demo"
    <!-- 侧边栏菜单的自定义类 -->
    background-color="#333744"
    <!-- 菜单背景色 -->
    text-color="#fff"
    <!-- 菜单文字颜色 -->
    active-text-color="#ffd04b"
    <!-- 激活菜单项文字颜色 -->
    >
    <!-- 首页的菜单项 -->
    <router-link to="/index">
      <el-menu-item index="Index">
        <el-icon :size="20">
          <HomeFilled />
          <!-- 首页图标组件 -->
        </el-icon>
        <span slot="title">首页</span>
        <!-- 菜单标题 -->
      </el-menu-item>
    </router-link>

    <!-- 动态生成子菜单，每个 sub-menu 展示后端返回的菜单数据 -->
    <el-sub-menu :index="menu.name" v-for="menu in menuList">
      <!-- 子菜单标题区域 -->
      <template #title>
        <el-icon :size="20">
          <!-- 动态渲染菜单图标，通过后端返回的数据确定图标 -->
          <component :is="menu.icon"></component>
        </el-icon>
        <span>{{ menu.title }}</span>
        <!-- 子菜单的标题 -->
      </template>

      <!-- 子菜单中的菜单项组 -->
      <el-menu-item-group>
        <!-- 遍历子菜单项 children，每个菜单项对应一个路由 -->
        <router-link :to="item.path" v-for="item in menu.children">
          <el-menu-item :index="item.name" @click="selectMenu(item)">
            <el-icon>
              <component :is="item.icon"></component>
              <!-- 子菜单项图标 -->
            </el-icon>
            {{ item.title }}
            <!-- 子菜单项标题 -->
          </el-menu-item>
        </router-link>
      </el-menu-item-group>
    </el-sub-menu>
  </el-menu>
</template>

<script setup>
import { computed } from "vue"; // 引入 Vue 的 computed 方法，用于创建响应式数据
import { definedMenus } from "../store/menus.js"; // 引入 Pinia 的菜单 store

// 初始化并获取菜单数据的 store
let $store = definedMenus();

// 使用 computed 创建响应式的 menuList，数据来源于 store，当 store 中 menuList 变化时，侧边栏菜单也会随之更新
const menuList = computed({
  get() {
    // 返回 store 中的 menuList
    return $store.menuList;
  },
});

// 当菜单项被点击时调用该方法，用于添加选中的菜单项选项卡
function selectMenu(item) {
  $store.addTab(item);
}
</script>

<style scoped>
/* 设置侧边栏菜单高度为视口高度 */
.el-menu-vertical-demo {
  height: 100vh;
}

/* 移除 router-link 默认下划线 */
a {
  text-decoration: none;
}

/* 确保 router-link 内部元素无下划线 */
router-link {
  text-decoration: none;
}
</style>
