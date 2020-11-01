const path = require('path');
const express = require('express')
const port = 8080;

// 创建服务器实例
const app = express();

// 配置 public 目录，将其开放给浏览器端
app.use('/', express.static(path.join(__dirname, 'public')));

// 监听 8080 端口
app.listen(port, function(){
    console.log(`访问 http://localhost:${port}/，按 Ctrl+C 终止服务！`);
});
