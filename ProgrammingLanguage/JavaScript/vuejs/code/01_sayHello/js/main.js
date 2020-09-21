// 程序名称： sayHello
// 实现目标：
//   1. 验证 Vue.js 执行环境
//   2. 体验构建 Vue.js 程序的基本步骤

const app = new Vue({
    el: '#app',
    data:{
        sayHello: '你好，Vue.js！',
        vueLogo: 'img/logo.png'
    }
});
