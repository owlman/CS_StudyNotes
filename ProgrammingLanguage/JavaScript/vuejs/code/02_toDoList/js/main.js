// 程序名称： toDoList
// 实现目标：
//   1. 学习 v-if、v-for 等指令
//   2. 体验如何处理用户输入

const app = new Vue({
    el: '#app',
    data:{
        newTask: '',
        taskList: [],
        doneList: []
    },
    methods:{
        todo: function() {
                if(this.newTask !== '')
                  this.taskList.push(this.newTask);
              }
    }
});
