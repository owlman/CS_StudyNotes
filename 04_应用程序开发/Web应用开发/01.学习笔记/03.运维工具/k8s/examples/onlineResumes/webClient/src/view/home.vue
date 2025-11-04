<script setup>
    // This starter template is using Vue 3 <script setup> SFCs
    // Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
    import { ref } from 'vue';
    import { useStore } from 'vuex';
    import login from '../components/login.vue';
    import signup from '../components/signup.vue';
    import userMessage from '../components/userMessage.vue';
    import resumeList from '../components/resumeList.vue';

    const store = useStore();
    const goSignup = ref(false);

    function logined(uid) {
        store.commit('login', {
            'isLogin' : true,
            'uid' : uid
        });
        $cookies.set('uid', uid);
    }

    function logout() {
        store.commit('logout');
        $cookies.remove('uid');
    }
</script>

<template>
    <div class="home">
        <div class="users" v-if="!$store.getters.isLogin">
            <input type="button" value="用户登录" 
                :class="['tab-button', { active: goSignup == false }]"
                @click="goSignup= false">
            
            <input type="button" value="注册新用户" 
                :class="['tab-button', { active: goSignup == true }]"
                @click="goSignup = true">
            <keep-alive>
                <component 
                    class="tab" 
                    :is="goSignup ? signup : login" 
                    @goLogin="goSignup = false"
                    @logined="logined" />
            </keep-alive>
        </div>
        <div class="users" v-if="$store.getters.isLogin">
            <userMessage @logout="logout"></userMessage>
            <resumeList></resumeList>
        </div>
    </div>
</template>

<style scoped>
    @import '../assets/styles/Home.css';
</style>
