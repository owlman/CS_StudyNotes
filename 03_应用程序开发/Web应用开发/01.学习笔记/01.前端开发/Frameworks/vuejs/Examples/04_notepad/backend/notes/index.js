const path = require('path');
const knex = require('knex');

function notes(app) {
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

    appDB.schema.hasTable('notes')  // 查看数据库中是否已经存在 notes 表
    .then(function(exists) {
        if(exists == false) {       // 如果 notes 表不存在就创建它
            appDB.schema.createTable('notes', function(table) {
                // 创建 notes 表：
                table.increments('nid').primary();  // 将 uid 设置为自动增长的字段，并将其设为主键。
                table.integer('uid');               // 将 uid 设置为整数类型的字段。
                table.string('title');              // 将 title 设置为字符串类型的字段。
                table.string('text');               // 将 text 设置为字符串类型的字段。
            })
            .catch(function(err) {
                console.log('notes表创建失败，错误信息为：', err);
            });
        }
    })
    .then(function() {
        app.post('/notes/add', function(req, res) {
            appDB('notes').insert(
                {
                    uid: req.body['uid'],
                    title: req.body['title'],
                    text: req.body['text']
                }
            )
            .then(function() {
                appDB('notes').select('*')
                .where('uid', '=', req.body['uid'])
                .then(function(data) {
                    res.status(200).send(data);
                })
                .catch(function(err) {
                    res.status(404);
                    console.error('获取笔记列表错误：', err);
                });
            })
            .catch(function() {
                res.status(404);
             });            
        });
        
        app.get('/notes/get', function(req, res) {
            appDB('notes').select('*')
            .where('uid', '=', req.query.uid)
            .then(function(data) {
                res.status(200).send(data);
            })
            .catch(function(err) {
                res.status(404);
                console.error('获取笔记列表错误：', err);
             });
        });

        app.delete('/notes/delete', function(req, res) {
            appDB('notes').delete()
            .where('nid', '=', req.query.nid)
            .then(function() {
                appDB('notes').select('*')
                .where('uid', '=', req.query.uid)
                .then(function(data) {
                    res.status(200).send(data);
                })
                .catch(function(err) {
                    res.status(404);
                    console.error('获取笔记列表错误：', err);
                });
            })
            .catch(function() {
                res.status(404);
             });
        });
    })
    .catch(function() {
        // 断开数据库连接，并销毁 appDB 对象
        appDB.destroy();
    });    
};

module.exports = notes;