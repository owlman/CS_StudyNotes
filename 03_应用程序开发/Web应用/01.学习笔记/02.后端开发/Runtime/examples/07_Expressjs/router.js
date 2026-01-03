// 在Node.js中使用Express框架
// 作者：owlman
// 时间：2019年07月25日

const path = require('path')
var express = require('express')
var sayHello = require(path.join(__dirname, 'sayHello'))
var student = require(path.join(__dirname, 'student'))
var board = require(path.join(__dirname, 'board'))

var router = express.Router()

// Hello，Express！
sayHello(router)
// 学生管理
student(router)
// 留言板
board(router)

module.exports = router