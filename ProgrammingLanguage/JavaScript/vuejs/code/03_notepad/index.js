const path = require('path');
const express = require('express')
const bodyParser = require('body-parser');
const port = 8080;

// 创建服务器实例
const app = express();

// 配置 public 目录
app.use('/', express.static(path.join(__dirname, 'public')));

//配置 body-parser 中间件，以便获取 POST 请求数据。
app.use(bodyParser.urlencoded({ extended : false}));
app.use(bodyParser.json());

// 创建数据库实例
const knex = require('knex');

// 创建数据库连接对象：
const appDB = knex({
    client: 'sqlite3', // 设置要连接的数据类型
    connection: {      // 设置数据库的链接参数
        filename: path.join(__dirname, 'data/database.sqlite')
    },
    debug: true,       // 设置是否开启 debug 模式，true 表示开启
    pool: {            // 设置数据库连接池的大小，默认为{min: 2, max: 10}
        min: 2,
        max: 7
    },
    useNullAsDefault: true
});

appDB.schema.hasTable('notes')  // 查看数据库中是否已经存在 notes 表
.then(function(exists) {
    if(exists == false) { // 如果 notes 表不存在就创建它
        return appDB.schema.createTable('notes', function(table) {
            // 创建 notes 表：
            table.increments('uid').primary();// 将 uid 设置为自动增长的字段，并将其设为主键。
            table.string('userName');         // 将 userName 设置为字符串类型的字段。
            table.string('noteMessage');      // 将 notes 设置为字符串类型的字段。
    });
  }
})
.then()


// 请求路由
// 设置网站首页
app.get('/', function(req, res) {
    res.redirect('/index.htm');
});

// 响应前端获取数据的 GET 请求
app.get('/data/get', function(req, res) {
    appDB('notes').select('*')
    .then(function(data) {
        console.log(data);
  });
});

// 响应前端获取数据的 GET 请求
app.get('/data/get', function(req, res) {
    appDB('notes').delete()
    .where('uid', '=', req.body['uid']);
});

// 响应前端提交数据的 POST 请求
app.post('/data/add', function(req, res) {
    console.log('post data');
    appDB('notes').insert([
        {
          userName : req.body['userName'],
          noteMessage : req.body['noteMessage']
        }
      ]);
});

// 响应前端修改数据的 POST 请求
app.post('/data/edit', function(req, res) {
    appDB('notes').update({notes : '2222'})
    .where('uid', '=' ,req.body['uid']);
});

// 监听 8080 端口
app.listen(port, function(){
    console.log(`访问 http://localhost:${port}/，按 Ctrl+C 终止服务！`);
});
