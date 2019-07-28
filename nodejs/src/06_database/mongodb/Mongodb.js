// 在Node.js中使用mongodb
// 作者：owlman
// 时间：2019年07月21日

var MongoClient = require('mongodb').MongoClient

class MongoDB {
    constructor(url, dbName) {
        this.dbpath = url+'/'+dbName
        this.dbName = dbName

        MongoClient.connect(this.dbpath, 
                            { useNewUrlParser: true }, 
                            function(err, db) {
            if ( err !== null ) { 
                console.log('错误信息1：' + err.message)
                return false
            }
            console.log(dbName + "数据库已创建!")
            db.db(dbName)
            db.close()
        })
    }

    createCollection(collect) {
        var dbName = this.dbName
    
        MongoClient.connect(this.dbpath,
                            { useNewUrlParser: true },
                            function (err, db) {
            if ( err !== null ) { 
                console.log('错误信息2：' + err.message)
                return false
            }
            var dbo = db.db(dbName)
            dbo.createCollection(collect, function (err, coll) {
                if ( err !== null ) { 
                    console.log('错误信息3：' + err.message)
                    return false
                }
                console.log(collect + "集合已创建!")
                db.close()
            })
        })
    }

    insertData(collect, doc) {
        var dbName = this.dbName

        MongoClient.connect(this.dbpath,
                            { useNewUrlParser: true },
                            function(err, db) {
            if ( err !== null ) { 
                console.log('错误信息4：' + err.message)
                return false
            }
            var dbo = db.db(dbName)
            dbo.collection(collect).insertOne(doc, function(err, res) {
                if ( err !== null ) { 
                    console.log('错误信息5：' + err.message)
                    return false
                }
                console.log(doc + "文档插入成功")
                db.close()
            })
        })
    }
    
    queryAllData(collect) {
        var dbName = this.dbName

        MongoClient.connect(this.dbpath,
                           { useNewUrlParser: true }, 
                           function(err, db) {
            if ( err !== null ) { 
                console.log('错误信息6：' + err.message)
                return false
            }
            var dbo = db.db(dbName)
            dbo.collection(collect). find({}).toArray(function(err, result) {
                if ( err !== null ) { 
                    console.log('错误信息7：' + err.message)
                    return false
                }
                console.log(result)
                db.close()
            })
        })
    }

    queryDataFor(collect, querystr) {
        var dbName = this.dbName

        MongoClient.connect(this.dbpath,
                           { useNewUrlParser: true }, 
                           function(err, db) {
            if ( err !== null ) { 
                console.log('错误信息8：' + err.message)
                return false
            }
            var dbo = db.db(dbName)
            dbo.collection(collect). find(querystr).toArray(function(err, result) {
                if ( err !== null ) { 
                    console.log('错误信息9：' + err.message)
                    return false
                }
                console.log(result)
                db.close()
            })
        })
    }

    dropCollection(collect) {
        var dbName = this.dbName
    
        MongoClient.connect(this.dbpath,
                            { useNewUrlParser: true },
                            function (err, db) {
            if ( err !== null ) { 
                console.log('错误信息10：' + err.message)
                return false
            }
            var dbo = db.db(dbName)
            dbo.dropCollection(collect, function(err, delOK) {  // 执行成功 delOK 返回 true，否则返回 false
                if ( err !== null ) { 
                    console.log('错误信息11：' + err.message)
                    return false
                }
                if ( delOK !== null ) {
                    console.log(collect + "集合已删除！")  
                } 
                db.close()
            })
        })
    }

}

module.exports = MongoDB