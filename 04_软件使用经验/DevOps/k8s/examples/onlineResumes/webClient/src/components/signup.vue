<script setup>
    import md5 from 'blueimp-md5';
    import axios from 'axios';
    import Qs from 'qs' ;
    import { ref, defineEmits } from 'vue';

    const emit = defineEmits(['goLogin']);
    const userName = ref('');
    const password = ref('');
    const rePassword = ref('');

    async function signUp() {
        if(userName.value !== '' &&
            password.value !== '' &&
            rePassword.value !== '') {
            if(password.value === rePassword.value) {
                const newUser = {
                    user: userName.value,
                    passwd: md5(password.value)
                }
                try {
                    const res = await axios.post('/users/newuser',
                                                    Qs.stringify(newUser));
                    if(res.status == 200) {
                        window.alert(res.data.message);
                        emit('goLogin');
                    }
                } catch (error) {
                    if(error.response) {
                        window.alert(error.response.data.message);
                    }
                }
            } else {
                window.alert('你两次输入的密码不一致！');
            }
        } else {
            window.alert('请正确填写注册信息！');
        }
    }

    function reset() {
        userName.value = '';
        password.value = '';
        rePassword.value = '';
    }
</script>

<template>
    <div id="tab-sign">
        <table>
            <tr>
                <td>请输入用户名：</td>
                <td><input type="text" v-model="userName"></td>
            </tr>
            <tr>
                <td>请设置密码：</td>
                <td><input type="password" v-model="password"></td>
            </tr>
            <tr>
                <td>请重复密码：</td>
                <td><input type="password" v-model="rePassword"></td>
            </tr>
            <tr>
                <td><input type="button" value="注册" @click="signUp"></td>
                <td><input type="button" value="重置" @click="reset"></td>
            </tr>
        </table>
    </div>
</template>

<style>
</style>
