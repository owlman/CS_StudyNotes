// 在Node.js中使用sqlite
// 作者：owlman
// 时间：2019年07月20日

const async = require('async')
const SqliteDB = require('./Sqlite')
const file = "HRDB.db"
const sqliteDB = new SqliteDB(file)

function dataDeal(objects, message) {
    console.log(message)
    for ( let i = 0; i < objects.length; ++i )  {
        console.log(objects[i])
   }
}

async.waterfall([
    function (callback) {
        // 创建表格
        const createTableSql = `
            create table if not exists HR_TABLE (
                name  TEXT,
                age   TEXT,
                sex   TEXT,
                items TEXT
            );`
        sqliteDB.createTable(createTableSql)
        callback()
    },

    function (callback) {
        // 插入数据
        const insertTileSql = `
            insert into HR_TABLE
                (name, age, sex, items)
                values(?, ?, ?, ?)`
        
        const arr = [
            ['凌杰', '24', '男', '看书, 看电影, 旅游'],
            ['蔓儿', '25', '女', '看书, 看电影, 写作'],
            ['张语', '32', '女', '看书, 旅游, 绘画']
        ]
        sqliteDB.insertData(insertTileSql, arr)
        callback()
    },

    function (callback) {
        // 查询数据
        const querySql = 'select * from HR_TABLE'
        sqliteDB.queryData(querySql, dataDeal, '初始数据')
        callback()
    },
    
    function (callback) {
        // 更新数据
        const updateSql = `update HR_TABLE set age = 37 where name = "凌杰"`
        sqliteDB.executeSql(updateSql)
        callback()
    },
     
    function (callback) {
        // 查询更新后的数据
        querySql = `select * from HR_TABLE`
        sqliteDB.queryData(querySql, dataDeal, '更新后数据')
        callback()
    },

    function (callback) { 
        sqliteDB.close()
        callback()
    }
])
