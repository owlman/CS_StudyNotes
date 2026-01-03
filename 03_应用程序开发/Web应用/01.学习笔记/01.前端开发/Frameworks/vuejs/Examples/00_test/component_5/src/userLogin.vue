<template>
    <div id="tab-login">
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
                    if(this.userName === 'owlman' && this.password === '0000') {
                        this.$emit('input', true);
                    } else {
                        window.alert('用户名或密码错误！');
                        
                    }
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
