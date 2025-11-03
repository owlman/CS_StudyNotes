// 在Express框架中实现留言板应用
// 作者：owlman
// 时间：2019年07月27日

var MongoClient = require('mongodb').MongoClient
var async = require('async')
const server = 'mongodb://localhost:27017'
const dbName = 'boardDB'
const collName = 'message_table'
const dbPath = server + '/' + dbName

module.exports = function(app) {
    app.get('/board', function (req, res) {
        MongoClient.connect(dbPath, { useNewUrlParser: true },
                                            function(err, db) {
            if ( err !== null ) { 
                return console.error('错误信息：' + err.message)
            }
            var dbo = db.db(dbName)
            var collect = dbo.collection(collName)
            collect. find({}).toArray(function(err, result) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
                var num =result.length
                res.render('board.htm', {
                    num : num,
                    db  : result
                })
            })
        })
    })

    app.post('/board', function (req, res) {
        MongoClient.connect(dbPath, { useNewUrlParser: true },
                                            function(err, db) {
            if ( err !== null ) { 
                return console.error('错误信息：' + err.message)
            }
            var dbo = db.db(dbName)
            var collect = dbo.collection(collName)
            var data = {
               name    : req.body['name'],
               message : req.body['message'],
               time    : Date()
            }
            collect.insertOne(data, function(err, res) {
                if ( err !== null ) { 
                    return console.error('错误信息：' + err.message)
                }
            })
            res.redirect('/board')
        })
    })
}