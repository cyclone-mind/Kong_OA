// 导入 Vue 的 createApp 函数，用于创建 Vue 应用实例
import { createApp } from 'vue'
import "./style.css"
// 导入根组件 App.vue
import App from './App.vue'
// 导入路由配置文件 routers.js
import router from './routers'

import "bootstrap/dist/css/bootstrap.min.css"

// 导入 Pinia 库的 createPinia 函数，用于创建 Pinia 实例
import { createPinia } from 'pinia'
// 创建 Pinia 实例
let pinia = createPinia()

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import * as ElementPlusIconsVue from '@element-plus/icons-vue'
const app =createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }

// 创建 Vue 应用实例，使用根组件 App，并挂载到 #app 元素上
app.use(router).use(pinia).use(ElementPlus).mount('#app')

