import Vue from 'vue';
import sayHello from './sayHello.vue';
    
new Vue({
    el: '#app', 
    components: {
        'say-hello': sayHello
    },
    data: {
        who:'vue'
    },
    methods: {
        showMessage : function() {
            window.alert('Hello, ' + this.who);
        }
    }
});