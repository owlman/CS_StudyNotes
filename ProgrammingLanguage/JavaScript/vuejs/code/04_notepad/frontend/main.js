import Vue from 'vue';
import userLogin from './components/userLogin.vue';
import userSignUp from './components/userSignUp.vue';

new Vue({
    el: '#app',
    data: {
        isLogin: false,
        checked: 'login'
    },
    components: {
        'user-login': userLogin,
        'user-sign-up': userSignUp
    },
    methods: {}
});