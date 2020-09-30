// 程序名称： toDoList
// 实现目标：
//   1. 学习 v-model、v-for 等指令
//   2. 掌握如何处理用户输入

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
