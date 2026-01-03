// 在Node.js中使用mongoose包
// 作者：owlman
// 时间：2019年07月31日

const server = 'mongodb://localhost:27017'
const dbName = 'hrdb'
const collName = 'hr_table'
const dbPath = server + '/' + dbName
const mongoose = require('mongoose');
var async = require('async')
var Schema = mongoose.Schema
var hrSchema = new Schema({
    name : {
        type : String,
        required: true 
    },
    age : {
        type : String,
        required: true
    },
    sex : {
        type : String,
        required: true
    },
    items : {
        type : String,
        required: true
    }
})
var hrModel = new mongoose.model('Hrobj', hrSchema)
mongoose.connect(dbPath, {useNewUrlParser: true});
var conn = mongoose.connection
conn.on('error', console.error.bind(console, '连接错误:'))
conn.on('open', console.log.bind(console, '数据库连接成功'))
conn.on('disconnected', console.log.bind(console, '断开数据库连接'))

conn.once('open', function(){
    async.series([
        function(callback) {
            // 插入单条数据
            var someone = new hrModel ({
                name  : '杨过',
                age   : '42',
                sex   : '男',
                items : '看书, 喝酒, 习武'
            })
            someone.save(function(err, one){
                callback(err, one.name+'的数据插入成功')
            })
            
        },

        function(callback) {
            hrModel.find(function(err, hrTable){
                callback(err, '插入一条数据后的结果：' + hrTable)
            })
        },

        function(callback) {
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
                },
                {
                    name  : '阿波罗',
                    age   : '24',
                    sex   : '女',
                    items : '看书, 音乐, 被救'
                }
            ]

            hrModel.insertMany(dataArray, function(err) {
                callback(err, '数组中的数据插入成功')
            })
        },

        function(callback) {
            hrModel.find(function(err, hrTable){
                callback(err, '插入多条数据后的结果：' + hrTable)
            })
        },

        function(callback) {
            hrModel.updateMany({sex:'男'}, {sex:'女'}, function(err, one){
                callback(err, '将所有男人改为女人')
            })
        },

        function(callback) {
            hrModel.updateOne({name:'阿波罗'}, {sex:'男'}, function(err, one){
                callback(err, '将阿波罗的性别改为：男')
            })
        },        

        function(callback) {
            hrModel.find({age:'24'}, function(err, hrTable){
                callback(err, '所有年龄为24的数据：' + hrTable)
            })
        },

        function(callback) {
            hrModel.findOne({age:'24'}, function(err, hrTable){
                callback(err, '第一个年龄为24的结果：' + hrTable)
            })
        },

        function(callback) {
            hrModel.deleteMany({age:'24'}, function(err, hrTable){
                callback(err, '所有年龄为24数据已被删除')
            })
        },

        function(callback) {
            hrModel.find({age:'24'}, function(err, hrTable){
                callback(err, '所有年龄为24的数据：' + hrTable)
            })
        },

        function(callback) {
            hrModel.deleteMany({}, function(err, hrTable){
                callback(err, '所有数据已被删除')
            })
        },

        function(callback) {
            hrModel.find(function(err, hrTable){
                callback(err, '删除所有数据后的结果：' + hrTable)
            })
        },

        function(callback) {
            mongoose.disconnect(function(err){
                callback(err, '正在断开连接……')
            })
        }
    ], function(err, message) {
        if ( err !== null ) {
            return console.error('错误信息：' + err.message)
        }
        console.log(message)
    })
})

