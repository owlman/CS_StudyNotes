// 在Node.js中使用Express框架
// 作者：owlman
// 时间：2019年07月25日

const path = require('path')
const express = require('express')
const bodyParser =require('body-parser')
const router = require(path.join(__dirname, 'router'))
const app = express()

// 配置public目录
app.use('/public/', express.static(path.join(__dirname, 'public')))

//配置body-parser中间件，以便获取post请求数据。
app.use(bodyParser.urlencoded({ extended : false}));
app.use(bodyParser.json());

// 配置模板引擎为art-template
app.engine('htm', require('express-art-template'))
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'art')

// 调用路由表函数
app.use(router)

// 监听8080端口
app.listen(8080, function(){
    console.log('请访问http://localhost:8080/，按Ctrl+C终止服务！')
})
