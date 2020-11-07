const path = require('path');
const knex = require('knex');

function users(app) {
    const appDB = knex({
        client: 'sqlite3', // 设置要连接的数据类型
        connection: {      // 设置数据库的链接参数
            filename: path.join(__dirname, '../data/database.sqlite')
        },
        debug: true,       // 设置是否开启 debug 模式，true 表示开启
        pool: {            // 设置数据库连接池的大小，默认为{min: 2, max: 10}
            min: 2,
            max: 7
        },
        useNullAsDefault: true
    });

    appDB.schema.hasTable('users')  // 查看数据库中是否已经存在 users 表
    .then(function(exists) {
        if(exists == false) {       // 如果 users 表不存在就创建它
            appDB.schema.createTable('users', function(table) {
                // 创建 users 表：
                table.increments('uid').primary();// 将 uid 设置为自动增长的字段，并将其设为主键。
                table.string('userName');         // 将 userName 设置为字符串类型的字段。
                table.string('password');         // 将 password 设置为字符串类型的字段。
                appDB('users').insert(
                    {
                        userName : 'owlman',
                        password: '0000'
                    }
                )
                .catch(function(err) {
                   console.log('添加初始数据失败，错误信息为：', err);
                });
            })
            .catch(function(err) {
                console.log('users表创建失败，错误信息为：', err);
            });
        }
    })
    .then(function() {
        app.post('/user/login', function(req, res) {
            appDB('users').select('*')
            .where('userName','=', req.body['userName'])
            .andWhere('password', '=', req.body['password'])
            .then(function(data) {
                res.status(200).send(data);                
            })
        });
    })
    .catch(function() {
        // 断开数据库连接，并销毁 appDB 对象
        appDB.destroy();
    });    
};

module.exports = users;