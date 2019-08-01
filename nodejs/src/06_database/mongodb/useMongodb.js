// 在Node.js中使用mongodb
// 作者：owlman
// 时间：2019年07月21日

var MongoClient = require('mongodb').MongoClient
var async = require('async')
const server = 'mongodb://localhost:27017'
const dbName = 'hrdb'
const collName = 'hr_table'
const dbPath = server + '/' + dbName

MongoClient.connect(dbPath, { useNewUrlParser: true },
                                    function(err, db) {
    if ( err !== null ) { 
        return console.error('错误信息：' + err.message)
    }

    var dbo = db.db(dbName)
    console.log(dbName + '数据库创建成功')

    var collect = dbo.collection(collName)
    console.log(collName + '集合创建成功')

    async.series([
        // 控制程序串行执行
        
        function (callback) {
            // 插入单条数据
            var data = {
                name  : '杨过',
                age   : '42',
                sex   : '男',
                items : '看书, 喝酒, 习武'
            }

            collect.insertOne(data, function(err, res) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                console.log('单条数据插入成功')
            })
            callback()
        },
        
        function (callback) {
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
                },
                {
                    name  : '雅典娜',
                    age   : '24',
                    sex   : '女',
                    items : '看书, 音乐, 被救'
                }
            ]
            
            collect.insertMany(dataArray, function(err, res) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                console.log('数组插入成功')
            })
            callback()
        },

        function (callback) {
            // 列出所有数据
            collect. find({}).toArray(function(err, result) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                console.log('列出当前集合中的所有数据：')
                console.log(result)
            })
            callback()
        },

        function (callback){
            // 更新单一数据
            var whereData = {'name' : '小龙女'}
            var updataValue = { $set: { 'sex' : '女' } }
            collect.updateOne(whereData, updataValue,
                                                function(err, res) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                console.log(whereData['name'] + "的数据更新成功")
            })
            callback()
        },

        function (callback) {
            // 查询指定数据
            var querystr = { 'name' : '小龙女' }
            collect. find(querystr).toArray(function(err, result) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                console.log('查看更新后的' + querystr['name'] + '的数据：')
                console.log(result)
            })
            callback()
        },

        function (callback){
            // 删除指定单一数据
            var whereData = { 'name' : '黄蓉' }
            collect.deleteOne(whereData,function(err, result) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                console.log(whereData['name'] + '的数据已被删除')
            })
            callback()
        },

        function (callback) {
            // 查询所有数据，并按name降序排列
            var isort = { name : -1 }
            collect. find({}).sort(isort).toArray(function(err, result) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                console.log('降序排列当前集合中的所有数据：')
                console.log(result)
            })
            callback()
        },

        function (callback) {
            // 删除指定多条数据
            var whereData = { 'age' : '24' }
            collect.deleteMany(whereData,function(err, result) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                console.log('年龄为' + whereData['age'] + '的数据已被删除')
            })
            callback()
        },

        function (callback) {
            // 查询所有数据，并按name升序排列
            var isort = { name : 1 }
            collect. find({}).sort(isort).toArray(function(err, result) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                console.log('升序排列当前集合中的所有数据：')
                console.log(result)
            })
            callback()
        },

        function (callback) {
            // 删除指定集合
            dbo.dropCollection(collName, function(err, delOK) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                if ( delOK !== null ) {
                    console.log(collName + "集合已删除！")  
                } 
            })
            callback()
        }
    ])

    db.close()
})
