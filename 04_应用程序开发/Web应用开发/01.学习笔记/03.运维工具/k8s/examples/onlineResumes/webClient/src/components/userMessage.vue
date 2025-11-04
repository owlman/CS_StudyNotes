<script setup>
    import md5 from 'blueimp-md5';
    import axios from 'axios';
    import Qs from 'qs' ;
    import { ref, defineEmits } from 'vue';
    import { useStore } from 'vuex';

    axios.defaults.withCredentials = true;

    const store = useStore();
    const emit = defineEmits(['logout']);
    const isUpdate = ref(false);
    const userName = ref('');
    const password = ref('');
    const rePassword = ref('');

    const vMyDirective = {
        beforeMount: async function() {
            try {
                const res = await axios.get('/users/'+store.getters.UID);
                if(res.status == 200 && 
                    res.data.length == 1) {
                    userName.value = res.data[0].user;
                }        
            } catch (error) {
                if(error.response) {
                    window.alert(error.response.data.message);
                }
            }
        }
    }

    async  function update() {
        if(userName.value !== '' &&
            password.value !== '' &&
            rePassword.value !== '') {
            if(password.value === rePassword.value) {
                const newMessage = {
                    uid: store.getters.UID,
                    user: userName.value,
                    passwd: md5(password.value)
                }
                const res = await axios.put('/users/'+newMessage.uid,
                                                    Qs.stringify(newMessage));
                try {
                    if(res.status == 200) {
                        window.alert(res.data.message);
                        isUpdate.value = false;
                    }
                } catch(error) {
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

    function logout() {
        emit('logout');
    }

    async function deleteUser() {
        try {
            await axios.delete('/resumes/user/'+store.getters.UID);
            const res = await axios.delete('/users/'+store.getters.UID);
            if(res.status == 200) {
                window.alert(res.data.message);
                emit('logout');
            }
        } catch (error) {
            if(error.response) {
                window.alert(error.response.data.message);
            }
        }
    }

    function reset() {
        userName.value = '';
        password.value = '';
        rePassword.value = '';
    }
</script>

<template>
    <div v-my-directive id="userMessage" class="box">
        <h3> 欢迎回来，{{ userName }} </h3>
        <div class="operation">
            <h4> 可执行的操作： </h4>
            <div class="edit" v-show="isUpdate">
                <table>
                    <tr>
                        <td>用户名：</td>
                        <td><input type="text" v-model="userName"></td>
                    </tr>
                    <tr>
                        <td>设置密码：</td>
                        <td><input type="password" v-model="password"></td>
                    </tr>
                    <tr>
                        <td>重复密码：</td>
                        <td><input type="password" v-model="rePassword"></td>
                    </tr>
                    <tr>
                        <td><input type="button" value="提交" @click="update"></td>
                        <td><input type="button" value="重置" @click="reset"></td>
                    </tr>
                </table>
            </div>
            <ul>
                <li><a href="javascript:void(0)" @click="isUpdate=!isUpdate">
                    {{ isUpdate? '取消设置': '设置用户' }}
                </a></li>
                <li><a href="javascript:void(0)" @click="deleteUser">
                    注销用户
                </a></li>
                <li><a href="javascript:void(0)" @click="logout">退出登录</a></li>
            </ul>
        </div>
    </div>
</template>

<style>
    .box {
        width: 95%;
    }
    .box h3 {
        padding: 6px 10px;
        border-top-left-radius: 3px;
        border-top-right-radius: 14px;
        border: 1px solid #42b983;
        background: #f0f0f0;
        margin: 0px;
    }
    .box .operation {
        border: 1px solid #42b983;
        padding: 5px;        
    }
    .box ul {
        list-style: none;
    }
</style>