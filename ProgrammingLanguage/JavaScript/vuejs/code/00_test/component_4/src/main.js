import Vue from 'vue';
import counter from './counter.vue';
    
new Vue({
    el: '#app', 
    components: {
        'my-counter': counter
    },
    data: {
        num: 0
    },
    methods: {}
});