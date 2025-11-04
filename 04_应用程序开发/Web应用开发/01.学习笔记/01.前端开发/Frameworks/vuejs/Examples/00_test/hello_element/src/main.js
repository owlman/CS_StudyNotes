import Vue from 'vue';
import ElementUI from 'element-ui';

Vue.use(ElementUI);

new Vue({
  el: '#app',
  data : {
      title: 'Element 组件库',
      message : '一套为开发者、设计师和产品经理准备的基于 Vue 2.0 的桌面端组件库。'
  },
  methods : {
      goDocument : function() {
        window.open('https://element.faas.ele.me/#/zh-CN', '_blank');
      }
  }
});