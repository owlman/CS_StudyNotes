// 程序名称： sayHello
// 实现目标：
//   1. 验证 Vue.js 执行环境
//   2. 体验构建 Vue.js 程序的基本步骤

// 加载开发环境版本，该版本包含了有帮助的命令行警告
import Vue from '../node_modules/vue/dist/vue.esm.browser.js';
// 或者
// 加载生产环境版本，该版本优化了文件大小和载入速度
// import Vue from '../node_modules/vue/dist/vue.esm.browser.min.js';

const app = new Vue({
    el: '#app',
    data:{
        sayHello: '你好，Vue.js！',
        vueLogo: 'img/logo.png',
        isShow: true
    },
    methods:{
        toggleShow: function() {
            this.isShow = !this.isShow;
        }
    }
});
``