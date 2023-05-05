import { createStore } from 'vuex'

const store = createStore({
    state: {
        user: { 
            isLogin: false,
            uid: ''
        }
    },
    mutations: {
        login (state, userData) {
            state.user.isLogin = userData.isLogin;
            state.user.uid = userData.uid;
            localStorage.isLogin = userData.isLogin;
            localStorage.uid = userData.uid;
        },
        logout (state) {
            localStorage.removeItem('uid');
            localStorage.removeItem('isLogin');
            state.user.isLogin = false;
            state.user.uid = '';
        }
    },
    getters: {
        isLogin: function(state) {
            if(localStorage.isLogin === 'true') {
                state.user.isLogin = localStorage.isLogin;
            }
            return state.user.isLogin;
        },
        UID: function(state) {
            if(localStorage.isLogin === 'true') {
                state.user.uid = localStorage.uid;
            }
            return state.user.uid;
        }
    }
})

export default store;

