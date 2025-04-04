<template>
  <el-menu
    default-active="1"
    class="el-menu-vertical-demo"
    background-color="#333744"
    text-color="#fff"
    active-text-color="#ffd04b"
  >
    <router-link to="/index">
      <el-menu-item index="Index">
        <el-icon :size="20">
          <HomeFilled />
        </el-icon>
        <span slot="title">首页</span>
      </el-menu-item>
    </router-link>

    <el-sub-menu :index="menu.name" v-for="menu in menuList">
      <template #title>
        <el-icon :size="20">
          <!-- 小图标动态变化,通过后端返回，动态路由-->
          <component :is="menu.icon"></component>
        </el-icon>
        <span>{{ menu.title }}</span>
      </template>
      <el-menu-item-group>
        <router-link :to="item.path" v-for="item in menu.children">
          <el-menu-item :index="item.name" @click="selectMenu(item)">
            <el-icon>
              <component :is="item.icon"></component>
            </el-icon>
            {{ item.title }}
          </el-menu-item>
        </router-link>
      </el-menu-item-group>
    </el-sub-menu>
  </el-menu>
</template>
<script setup>
import { computed } from "vue";
import { definedMenus } from "../store/menus.js";
let $store = definedMenus();

// 拿到去后端请求回来的 menu列表，pinia中的：menuList
const menuList = computed({
  get() {
    // 这个值变---》外层的menuList 就会跟着变
    return $store.menuList;
  },
});
function selectMenu(item) {
  $store.addTab(item);
}
</script>
<style scoped>
.el-menu-vertical-demo {
  height: 100vh;
}
</style>
