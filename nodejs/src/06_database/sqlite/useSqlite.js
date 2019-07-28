// 在Node.js中使用sqlite
// 作者：owlman
// 时间：2019年07月20日

var async = require('async')
var SqliteDB = require('./Sqlite')
var file = "HRDB.db"
var sqliteDB = new SqliteDB(file)

var arr = [
    ['凌杰', '24', '男', '看书, 看电影, 旅游'],
    ['蔓儿', '25', '女', '看书, 看电影, 写作'],
    ['张语', '32', '女', '看书, 旅游, 绘画']
]

function dataDeal(objects, message) {
    console.log(message)
    for ( var i = 0; i < objects.length; ++i )  {
        console.log(objects[i])
   }
}

async.waterfall([
    op => {
        // 创建表格
        var createTableSql = `
            create table if not exists HR_TABLE (
                name  TEXT,
                age   TEXT,
                sex   TEXT,
                items TEXT
            );`
        sqliteDB.createTable(createTableSql)
        op()
    },

    op => {
        // 插入数据
        var insertTileSql = `
            insert into HR_TABLE
                (name, age, sex, items)
                values(?, ?, ?, ?)`
        sqliteDB.insertData(insertTileSql, arr)
        op()
    },

    op => {
        // 查询数据
        var querySql = 'select * from HR_TABLE'
        sqliteDB.queryData(querySql, dataDeal, '初始数据')
        op()
    },
    
    op => {
        // 更新数据
        var updateSql = `update HR_TABLE set age = 37 where name = "凌杰"`
        sqliteDB.executeSql(updateSql)
        op()
    },
     
    op => {
        // 查询更新后的数据
        querySql = `select * from HR_TABLE`
        sqliteDB.queryData(querySql, dataDeal, '更新后数据')
        op()
    },

    op => { 
        sqliteDB.close()
        op()
    }
])