const path = require('path');
const express = require('express');
const bodyParser =require('body-parser');
const router = require(path.join(__dirname, 'router'));
const port = 8080;

// 创建服务器实例
const app = express();

// 配置 public 目录，将其开放给浏览器端
app.use('/', express.static(path.join(__dirname, '../public')));

//配置 body-parser 中间件，以便获取 post 请求数据。
app.use(bodyParser.urlencoded({ extended : false}));
app.use(bodyParser.json());

// 调用路由表函数
app.use(router);

// 监听 8080 端口
app.listen(port, function(){
    console.log(`访问 http://localhost:${port}/，按 Ctrl+C 终止服务！`);
});
