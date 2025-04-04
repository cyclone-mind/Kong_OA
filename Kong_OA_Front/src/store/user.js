import {defineStore} from 'pinia'
import $cookie from 'vue-cookies'
export const definedUser = defineStore(
    'definedUser', //必须唯一
    {
        state: () => { // state中用于定义数据
            return {
                login_user:{
                    username:'',
                    avatar:'',
                    token:''
                }
            }
        },
        getters: {
        },
        actions: {
            set_user(user){
                // 设置登录用户信息 到state中
                this.login_user = user
                // 设置cookie
                $cookie.set('username',user.username, "37d")
                $cookie.set('avatar',user.avatar, "7d")
                $cookie.set('token',user.token, "7d")
                console.log(user)
            },
            log_out(){
                // 清空登录用户信息
                this.login_user = {
                    username:'',
                    avatar:'',
                    token:''
                }
                // 删除cookie
                $cookie.remove('username')
                $cookie.remove('avatar')
                $cookie.remove('token')
            }
        }
    }
)
