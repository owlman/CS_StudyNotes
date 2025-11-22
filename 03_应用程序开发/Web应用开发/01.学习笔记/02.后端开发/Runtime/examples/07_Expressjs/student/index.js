// 在Express框架中实现学生管理系统
// 作者：owlman
// 时间：2019年07月27日

const fs = require('fs')
const path = require('path')
const async = require('async')
const SqliteDB = require(path.join(__dirname,'Sqlite'))
const dbPath = path.join(__dirname, '../public/DB/studentsDB.db')

// 配置数据库
if ( !fs.existsSync(dbPath) ) {
    const studentsDB = new SqliteDB(dbPath)
  
    async.series([
        function(callback) {
            var createTableSql = `
            create table if not exists STUDENT_TABLE (
                name  TEXT,
                age   TEXT,
                sex   TEXT,
                items TEXT
            )`
            studentsDB.createTable(createTableSql)
            callback()
        },

        function(callback) {
            var insertTileSql = `
                insert into STUDENT_TABLE
                    (name, age, sex, items)
                    values(?, ?, ?, ?)`
            var arr = [
                ['凌杰', '24', '男', '看书、看电影、旅游'],
                ['蔓儿', '25', '女', '看书、看电影、写作'],
                ['张语', '32', '女', '看书、旅游、绘画']
            ]
            studentsDB.insertData(insertTileSql, arr)  
            callback()
        }
    ])
    studentsDB.close()
}

module.exports = function(app) {
    app.get('/student', function (req, res) {
        const studentsDB = new SqliteDB(dbPath)

        var querySql = 'select * from STUDENT_TABLE'
        studentsDB.queryData(querySql, function(data) {
            if ( data === null ) { 
                return console.log('数据查询错误！')
            }
            res.render('student.htm', { db : data })
        })
        
        studentsDB.close()
    })

    app.get('/student/add', function  (req, res) {
        res.render('add.htm', { })
    })

    app.post('/student/add', function (req, res) {
        const studentsDB = new SqliteDB(dbPath)

        var arr =[
            [req.body['name'],req.body['age'],req.body['sex'],req.body['items']]
        ]

        var insertTileSql = `
            insert into STUDENT_TABLE
                (name, age, sex, items)
                values(?, ?, ?, ?)`
        studentsDB.insertData(insertTileSql, arr)

        studentsDB.close()
        res.redirect('/student')
    })

    app.get('/student/delete', function (req, res) {
        const studentsDB = new SqliteDB(dbPath)

        var deleteSql = `
            delete from STUDENT_TABLE where name = '`
            + req.query['name']
            + `'`
        studentsDB.executeSql(deleteSql)
        
        studentsDB.close()
        res.redirect('/student')
    })

    app.get('/student/edit', function (req, res) {
        const studentsDB = new SqliteDB(dbPath)

        var querySql = `
            select * from STUDENT_TABLE where name = '`
            + req.query['name']
            + `'`
        studentsDB.queryData(querySql, function(data) {
            if ( data === null ) { 
                return console.log('数据查询错误！')
            }
            res.render('edit.htm', { 
                name  : data[0]['name'],
                age   : data[0]['age'],
                sex   : data[0]['sex'],
                items : data[0]['items']
            })
        })
        
        studentsDB.close()
    })

    app.post('/student/edit', function (req, res) {
        const studentsDB = new SqliteDB(dbPath)

        var updateSql = 
            `update STUDENT_TABLE set name = '`
            + req.body['name']
            + `', `
            + `age = '`
            + req.body['age']
            + `', `
            + `sex = '`
            + req.body['sex']
            + `', `
            + `items = '`
            + req.body['items']
            + `' `
            + ` where name = '`
            + req.body['name']
            + `'`

        studentsDB.executeSql(updateSql)

        studentsDB.close()
        res.redirect('/student')
    })
}
