// 在Node.js中使用Express框架
// 作者：owlman
// 时间：2019年07月25日

var sayHello = require('./sayHello')
var student = require('./student')
var board = require('./board')

module.exports = function(app) {
    // Hello，Express！
    sayHello(app)
    // 学生管理
    student(app)
    // 留言板
    board(app)
}