import { createRouter, createWebHistory } from "vue-router";
import $cookie from "vue-cookies";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
// 创建路由对象,声明路由规则
import Index from "../views/admin/Index.vue";
// import Info from '../views/admin/Info.vue'
// import Job from '../views/admin/Job.vue'
// import User from '../views/admin/User.vue'
// import Role from '../views/admin/Role.vue'
// import Menu from '../views/admin/Menu.vue'
// import Dept from '../views/admin/Dept.vue'
import { definedMenus } from "../store/menus";
import { reqAuth } from "../api/system";

const router = createRouter({
  // 使用 createWebHistory 创建 HTML5 历史模式的路由
  history: createWebHistory(),
  // 定义路由规则数组
  routes: [
    // 定义根路径的路由规则
    {
      // 路径为根路径
      path: "/",
      // 对应的组件为 HomeView
      component: HomeView,
      children: [
        {
          // 首页一直在，不动态生成
          path: "/index",
          name: "Index",
          component: Index,
        },
      ],
    },
    {
      path: "/login",
      component: LoginView,
    },
    {
      path: "/",
      redirect: "/index",
    },
  ],
});

function menuToRoute(menu) {
  if (!menu.component) {
    // 没有 component ，说明是根，最顶层
    return null;
  }
  let route = {
    name: menu.name,
    path: menu.path,
    meta: {
      title: menu.title,
      icon: menu.icon,
    },
  };
  const componentPath = "../views/" + menu.component + ".vue";
  console.log("Loading component from:", componentPath);
  route.component = () => import(/* @vite-ignore */ componentPath);
  return route;
}

async function reqMenusFunc() {
  let menusStore = definedMenus();
  // 发送请求获取动态菜单路由
  let res = await reqAuth();
  // 菜单列表套字典
  menusStore.setMenuList(res.nav);
  menusStore.setPermList(res.authoritys);
  let newRoutes = router.options.routes; // vue-router 给出的路由规则数组
  // console.log("newRoutes:::",newRoutes);

  /* 
    动态绑定路由---重点

    */
  res.nav.forEach((menu) => {
    // 判断有没有 children ，如果有，则继续循环 children ，如果没有，则直接添加路由
    if (menu.children) {
      menu.children.forEach((item) => {
        // 生成一个 route 对象
        let route = menuToRoute(item);
        if (route) {
          newRoutes[0].children.push(route);
        }
      });
    }
  });

  // 把所有的生成的路由对象，放到 router 这里那个
  newRoutes.forEach((route) => {
    router.addRoute(route);
  });
  // hasRoute 为 true ，说明已经加载过动态路由，不需要再加载
  menusStore.changeRouteStatus(true);
}

/* 
用户登陆以后，点击任何一个菜单，都会触发路由守卫，判断用户是否有权限。
我们把 发送请求获取动态路径的代码，放在 路由守卫 中，因为路由守卫在每次进入页面时都会执行。
- 什么情况获取：没有加载过
- 什么情况不获取：加载过，一旦加载过，不用每次都去获取，节省效率

路由守卫--》在进入到某个地址之前，先执行这个代码，判断用户是否有权限
在这里面我们可以通过判断：cookie中，如果有token，说明是登录了，要访问那个页面，就能进哪个页面
如果token为空，访问任何页面，都重定向到login
to:去哪个路由对象，from是从哪个路由对象过来，next是个函数，如果允许它跳转，直接执行next() 
*/
router.beforeEach(async (to, from, next) => {
  let token = $cookie.get("token");
  // 拿到 pinia 对象, 这个初始化不能放在外面，因为如果放在外面，在main.js中导入import router from './router'时，会重复初始化
  let menusStore = definedMenus();
  let hasRoute = menusStore.hasRoute;
  if (to.path == "/login") {
    // 访问登录页面，直接去
    next();
  } else if (!token) {
    // 重定向到login
    next({ path: "/login" });
  } else if (token && !hasRoute) {
    //token 有值：登录了，但是 hasRoute 为false，说明没有获取过动态菜单路由
    // 发送请求获取动态菜单路由
    try {
      // 发送请求获取动态菜单路由，并等待它完成
      await reqMenusFunc();
      // 动态路由已添加，现在重试原始导航请求
      // 使用 {...to, replace: true} 来确保导航到原始目标路径
      // replace: true 可避免在历史记录中留下重复记录
      next({ ...to, replace: true });
    } catch (error) {
      console.error("加载动态路由失败:", error);
      // 可选：处理错误，例如清除 token 并重定向到登录页
      // $store.log_out(); // 假设 user store 有 log_out action
      next({ path: "/login" });
    }
  }
  next();
});
// 导出路由对象
export default router;
