// 在Node.js中使用mongodb
// 作者：owlman
// 时间：2019年07月21日

var MongoClient = require('mongodb').MongoClient
var async = require('async')
const server = 'mongodb://localhost:27017'
const dbName = 'hrdb'
const collect = 'hr_table'
const dbPath = server + '/' + dbName

MongoClient.connect(dbPath, { useNewUrlParser: true },
                                    function(err, db) {
    if ( err !== null ) { 
        console.log('错误信息：' + err.message)
        return false
    }
    var dbo = db.db(dbName)
    console.log(dbName + '数据库创建成功')
            
    async.waterfall([
        // 控制程序串行执行

        // callback => {
        //     // 创建集合
        //     dbo.createCollection(collect, function(err, coll) {
        //         if (err !== null ) {
        //             console.log('错误信息：' + err.message)
        //             return false            
        //         }
        //         console.log(collect + '集合创建成功')            
        //     })
        //     callback()
        // },

        callback => {
            // 插入单条数据
            var data = {
                name  : '杨过',
                age   : '42',
                sex   : '男',
                items : '看书, 喝酒, 习武'
            }

            dbo.collection(collect).insertOne(data, function(err, res) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                console.log("单条数据插入成功")
                db.close()
            })
            callback()
        },

        callback => {
            // 查询所有数据
            dbo.collection(collect). find({}).toArray(function(err, result) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                console.log('查看当前集合中的所有数据：')
                console.log(result)
            })
            callback()
        },

        callback => {
            // 插入多条数据
            var dataArray = [
                {
                    name  : '小龙女',
                    age   : '24',
                    sex   : '男',
                    items : '看书, 唱歌, 习武'
                },
                {
                    name  : '郭靖',
                    age   : '52',
                    sex   : '男',
                    items : '看书, 喝酒, 习武'
                },
                {
                    name  : '黄蓉',
                    age   : '45',
                    sex   : '女',
                    items : '看书, 绘画, 习武'
                }
            ]
            dbo.collection(collect).insertMany(dataArray, function(err, res) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                console.log("数组插入成功")
                db.close()
            })
            callback()
        },

        callback => {
            // 查询所有数据
            dbo.collection(collect). find({}).toArray(function(err, result) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                console.log('查看当前集合中的所有数据：')
                console.log(result)
            })
            callback()
        },

        callback => {
            // 更新单一数据
            var whereData = {'name' : '小龙女'}
            var updataValue = { $set: { 'sex' : '女' } }
            dbo.collection(collect).updateOne(whereData, updataValue,
                                                function(err, res) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                console.log(whereData['name'] + "的数据更新成功")
            })
            callback()
        },

        callback => {
            // 查询指定数据
            var querystr = { 'name' : '小龙女' }
            dbo.collection(collect). find(querystr).toArray(function(err, result) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                console.log('查看更新后的' + querystr['name'] + '的数据：')
                console.log(result)
            })
            callback()
        },

        callback => {
            // 删除指定单一数据
            var whereData = { 'name' : '黄蓉' }
            dbo.collection(collect).deleteOne(whereData,function(err, result) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                console.log(whereData['name'] + '的数据已被删除')
            })
            callback()
        },

        callback => {
            // 查询所有数据
            dbo.collection(collect). find({}).toArray(function(err, result) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                console.log('查看当前集合中的所有数据：')
                console.log(result)
            })
            callback()
        },

        callback => {
            // 删除指定多条数据
            var whereData = { 'age' : '24' }
            dbo.collection(collect).deleteMany(whereData,function(err, result) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                console.log('年龄为' + whereData['age'] + '的数据已被删除')
            })
            callback()
        },

        callback => {
            // 查询所有数据
            dbo.collection(collect). find({}).toArray(function(err, result) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                console.log('查看当前集合中的所有数据：')
                console.log(result)
            })
            callback()
        },

        callback => {
            // 删除指定集合
            dbo.dropCollection(collect, function(err, delOK) {
                if ( err !== null ) { 
                    console.log('错误信息：' + err.message)
                    return false
                }
                if ( delOK !== null ) {
                    console.log(collect + "集合已删除！")  
                } 
            })
            callback()
        }
    ])
    db.close()
})