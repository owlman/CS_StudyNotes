// 程序名称： toDoList
// 实现目标：
//   1. 学习 v-model、v-for 等指令
//   2. 掌握如何处理用户输入

// 加载开发环境版本，该版本包含了有帮助的命令行警告
import Vue from '../node_modules/vue/dist/vue.esm.browser.js';
// 或者
// 加载生产环境版本，该版本优化了文件大小和载入速度
// import Vue from '../node_modules/vue/dist/vue.esm.browser.min.js';

const app = new Vue({
    el: '#app',
    data:{
        newTask: '',
        taskList: [],
        doneList: []
    },
    methods:{
        addNew: function() {
                  if(this.newTask !== '') {
                      this.taskList.push(this.newTask);
                      this.newTask = '';
                  }
                },
        remove: function(index) {
                  if(index >=  0) {
                      this.taskList.splice(index,1);
                  }
                }
    }
});
