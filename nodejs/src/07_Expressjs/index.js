// 在Node.js中使用Express框架
// 作者：owlman
// 时间：2019年07月25日

const path = require('path')
const express = require('express')
const router = require('./router')
const bodyParser =require('body-parser')
const app = express()

// 配置public目录
app.use('/public/', express.static(path.join(__dirname, 'public')))

//配置body-parser中间件
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());

// 配置模板引擎为art-template
app.engine('htm', require('express-art-template'))
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'art')

// 调用路由表函数
router(app)

// 监听8080端口
app.listen(8080, function(){
    console.log('请访问http://localhost:8080/，按Ctrl+C终止服务！')
})
