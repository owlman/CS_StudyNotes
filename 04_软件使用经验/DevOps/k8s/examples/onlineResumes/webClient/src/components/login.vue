<script setup>
import md5 from 'blueimp-md5';
import axios from 'axios';
import Qs from 'qs' ;
import { ref, defineEmits } from 'vue';

axios.defaults.withCredentials = true;

const emit = defineEmits(['logined']);
const userName = ref('');
const password = ref('');

async function login() {
    if(userName.value !== '' &&
        password.value !== '') {
        const userData =  {
            user: userName.value,
            passwd: md5(password.value)
        };
        try {
            const res = await axios.post(`/users/session`,
                                            Qs.stringify(userData));
            if(res.status == 200) {
                window.alert(res.data.message);
                emit('logined', res.data.uid);
            }
        } catch (error) {
            if(error.response) {
                window.alert(error.response.data.message);
            }
        }
    } else {
        window.alert('用户名与密码都不能为空！');
    }
}

function reset() {
    userName.value = '';
    password.value = '';
}
</script>

<template>
    <div id="tabLogin">
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

