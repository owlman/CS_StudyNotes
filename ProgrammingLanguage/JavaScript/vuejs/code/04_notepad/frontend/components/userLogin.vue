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
                    axios.post('/user/login', {
                        'userName': that.userName,
                        'password': that.password
                    })
                    .then(function(res){
                        if(res.data.length = 1) {
                            const user = {
                                isLogin: true,
                                data: res.data
                            };
                            that.$emit('input', user);
                        }
                    })
                    .catch(function(err) {
                        // 错误处理
                    });
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
