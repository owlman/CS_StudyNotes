import Vue from 'vue';
import userLogin from './userLogin.vue';
import userSignUp from './userSignUp.vue';

new Vue({
    el: '#app',
    data: {
        componentId: 'login',
        isLogin: false
    },
    components: {
        login: userLogin,
        signup : userSignUp
    }
})