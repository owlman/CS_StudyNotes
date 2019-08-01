// 在Node.js中使用Express框架
// 作者：owlman
// 时间：2019年07月25日

const path = require('path')
const express = require('express')
const router = require('./router')
const app = express()

// 配置模板引擎为art-template
app.engine('art', require('express-art-template'))
app.set('view', {
    debug: process.env.NODE_ENV !== 'production'
})
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'art')

// 配置public目录
app.engine('/node_modules/', express.static(path.join(__dirname, 'node_modules')))
app.engine('/public/', express.static(path.join(__dirname, 'public')))

// routes
router(app)

app.listen(8080, function(){
    console.log('请访问http://localhost:8080/，按Ctrl+C终止服务！')
})