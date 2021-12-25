<template>
    <div id="tab-login" class="tab-content">
        <table>
            <tr>
                <td>用户名：</td>
                <td><input type="text" v-model="userName"></td>
            </tr>
            <tr>
                <td>密  码：</td>
                <td><input type="password" v-model="password"></td>
            </tr>
            <tr>
                <td><input type="button" value="登录" @click="login"></td>
                <td><input type="button" value="重置" @click="reset"></td>
            </tr>
        </table>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "tab-login",
        props : ['value'],
        data: function() {
            return {
                userName: '',
                password: ''
            };
        },
        methods: {
            login: function() {
                if(this.userName !== '' && this.password !== '') {
                    const that = this;
                    axios.get('/user/login', {
                        params: {
                            'userName': that.userName,
                            'password': that.password
                        }
                    })
                    .then(function(res) {
                        if(res.statusText === 'OK' && 
                           res.data.length == 1) {
                            const user = {
                                isLogin: true,
                                data: res.data[0]
                            };
                            that.$emit('input', user);
                        } else {
                            window.alert('用户名或密码错误！');
                        }
                    })
                    .catch(function() {
                        window.alert('登录请求失败！');
                    });
                } else {
                    window.alert('用户名与密码都不能为空！');

                }
            },
            reset: function() {
                this.userName = '';
                this.password = '';
            }
        }
};
</script>

<style scoped>
</style>
