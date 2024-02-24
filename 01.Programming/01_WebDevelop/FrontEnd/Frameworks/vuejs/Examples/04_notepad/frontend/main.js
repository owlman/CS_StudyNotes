import Vue from 'vue';

// 引入自定义模块文件。
import userLogin from './components/userLogin.vue';
import userSignUp from './components/userSignUp.vue';
import noteList from './components/noteList.vue';

// 引入主样式文件
import "./style/main.css";

new Vue({
    el: '#app',
    data: {
        user: {
            isLogin: false,
            data:[]
        },
        checked: 'login'
    },
    components: {
        'user-login': userLogin,
        'user-sign-up': userSignUp,
        'note-list': noteList
    },
    methods: {}
});