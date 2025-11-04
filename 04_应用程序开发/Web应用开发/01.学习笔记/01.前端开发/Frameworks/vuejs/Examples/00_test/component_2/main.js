// import Vue from './node_modules/vue/dist/vue.js';
import sayHello from './sayHello.js';

const app = new Vue({
    el: '#app',
    components: {
        'say-hello': sayHello
    },
    data: {
        who:'vue'
    }
});