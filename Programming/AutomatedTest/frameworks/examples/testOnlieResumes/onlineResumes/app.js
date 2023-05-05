// 引入 Express.js 框架文件
const express = require('express');
// 引入 Node.js 平台内置的 path 模块
// 用于处理文件路径相关的任务
const path = require('path');
// 引入 cookie-parser 功能模块的中间件
// 用于解析 HTTP 请求中附带的cookie消息
const cookieParser = require('cookie-parser');
// 引入 morgan 日志功能模块的中间件
// 用于记录服务器端接收到的 HTTP 请求
const logger = require('morgan');
// 引入 connect-history-api-fallback 中间件
const history = require('connect-history-api-fallback');

// 引入存储在 routes 目录中的自定义模块
const indexRouter = require('./routes/index');
const usersRouter = require('./routes/users');
const resumesRouter = require('./routes/resumes');

// 创建一个 Express 应用实例
const app = express();

// 加载 morgan 中间件
// 将日志设置为开发者模式
app.use(logger('dev'));
// express.json() 会加载 Express 中的内置中间件 json
// 该中间件可用于解析 HTTP 请求中的 JSON 格式数据
app.use(express.json());
// express.urlencoded() 会加载 Express 中的内置中间件 urlencoded
// 该中间件可用于解析 HTTP 请求中的 url-encoded 格式数据
// 当 extended=false 时采用querystring模块，无法解析嵌套数据
app.use(express.urlencoded({ extended: false }));
// 加载 cookie-parser 中间件
app.use(cookieParser());
// 将静态资源目录改为 webClient/dist' 目录
// app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'webClient/dist')));
// 加载 connect-history-api-fallback 中间件
//app.use(history());

// 将客户端请求路径映射到自定义模块创建的路由器上。
app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/resumes', resumesRouter);

// 将 Express 实例设置为导出模块
module.exports = app;
