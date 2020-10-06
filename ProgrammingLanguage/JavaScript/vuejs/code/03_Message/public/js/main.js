// 程序名称： Message
// 实现目标：
//   1. 学习 axios 库的使用
//   2. 掌握如何与服务器进行数据交互

const app = new Vue({
    el: '#app',
    data:{
        userName: '',
        Message: '',
        notes: []
    },
    created: function() {
        that = this;
        axios.get('/data/get')
        .then(function(res) {
            that.notes = res.data;
        })
        .catch(function(err) {
            console.error(err);
        });
    },
    methods:{        
        addNew: function() {
            if(this.userName !== '' && this.Message !== '') {
                that = this;
                axios.post('/data/add', {
                    userName: that.userName,
                    noteMessage: that.Message
                }).catch(function(err) {
                    console.error(err);
                });
                this.Message = '';
                this.userName = '';
                axios.get('/data/get')
                .then(function(res) {
                    that.notes = res.data;
                })
                .catch(function(err) {
                    console.error(err);
                });
            }
        },
        remove: function(uid) {
            if(uid > 0) {
                that = this;
                axios.post('/data/delete', {
                    'uid' : uid
                }).catch(function(err) {
                    console.error(err);
                });
                axios.get('/data/get')
                .then(function(res) {
                    that.notes = res.data;
                })
                .catch(function(err) {
                    console.error(err);
                });
            }
        }
    }
});
