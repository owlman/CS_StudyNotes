import Vue from 'vue';
import box from './box.vue'
import counter from './counter.vue';
    
new Vue({
    el: '#app', 
    components: {
        'my-box' : box,
        'my-counter': counter
    },
    data: {
        num: 0
    },
    methods: {}
});