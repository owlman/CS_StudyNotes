// import Vue from './node_modules/vue/dist/vue.js';
import sayhello from './sayhello.js';

const app = new Vue({
    el: '#app',
    components: {
        'say-hello': sayhello
    },
    data: {
        who:'vue'
    }
});