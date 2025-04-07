import {definedMenus} from "../store/menus.js";
const $store=definedMenus()
export const hasAuth = (perm) => {
    // 1 拿到pinia中存储的按钮权限 --》是个列表---》['role:add',''role:delete']
    let authority = $store.permList
    // 2 判断传入的字符串，是否在列表中，如果在就是true，不在就false
    return authority.indexOf(perm) > -1
}


// ##################### 后续  ##########
// 在每个页面中导入 hasAuth
// 在按钮上加如下代码即可
// v-if="hasAuth('role:role')"