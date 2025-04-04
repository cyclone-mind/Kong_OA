import { defineStore } from "pinia";

/* 定义一个菜单的store，用于管理菜单的添加、删除、切换等操作，之所以使用store，是因为菜单是全局共享的，不仅在Tabs中使用，
Sidebar中也要使用，需要频繁操作 */
export const definedMenus = defineStore(
  "definedMenus", //必须唯一
  {
    state: () => {
      // state中用于定义数据
      return {
        editableTabs: [
          {
            // 标签页列表， 组件名字，默认首页，且所有人都能看到，不能删除
            title: "首页",
            name: "Index",
          },
        ],
        editableTabsValue: "Index", // 当前选中的标签页
        hasRoute:false, // 是否已经获取过动态路由
        menuList:[], // 菜单列表，字典套列表，后端返回的 nav 对应的数据
        permList:[], // 权限列表，后端返回的 authoritys 对应的数据
      };
    },
    getters: {},
    actions: {
      addTab(tab) {
        // 添加标签页的操作
        let index = this.editableTabs.findIndex((e) => e.name === tab.name); // 查找点击的Tab是否已经存在
        if (index === -1) { // 如果Tab不存在，则添加
          this.editableTabs.push({
            title: tab.title,
            name: tab.name,
          });
        }
        this.editableTabsValue = tab.name; // 切换到点击的 Tab 页
        // 删除标签页的操作不用写在这里，写在 Tab 组件中
      },

      // 我们正常使用 pinia ， 不直接操作 state ， 而是通过 actions 来操作
      setMenuList(menus){
        this.menuList = menus;
      },
      setPermList(perms){
        this.permList = perms;
      },
      changeRouteStatus(hasRoutes){
        this.hasRoute = hasRoutes;
      }
    },
  }
);
