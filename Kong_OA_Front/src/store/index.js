import {defineStore} from 'pinia'
export const definedMain = defineStore(
    'definedMain', //必须唯一
    {
        state: () => { // state中用于定义数据
            return {
                title:'Kong-OA'
            }
        },
        getters: {
        },
        actions: {
        },
    }
)
