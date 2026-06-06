import { createApp } from 'vue'
import App from './App.vue'
import vueCookies from 'vue-cookies';
import vueRouter from './router';
import store from './store';

const app = createApp(App);
app.config.globalProperties.$cookies = vueCookies;
app.use(vueRouter);
app.use(store);
app.mount('#app')