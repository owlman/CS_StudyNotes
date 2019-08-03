// 在Express框架中实现学生管理系统
// 作者：owlman
// 时间：2019年07月27日

const fs = require('fs')
const path = require('path')
const SqliteDB = require(path.join(__dirname,'./Sqlite'))
const dbPath = path.join(__dirname, '../public/DB/studentsDB.db')


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
