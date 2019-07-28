const async = require('async')
const MongoDB = require('./Mongodb')
const url = 'mongodb://localhost:27017'
var arr = [
    ['凌杰', '24', '男', '看书, 看电影, 旅游'],
    ['蔓儿', '25', '女', '看书, 看电影, 写作'],
    ['张语', '32', '女', '看书, 旅游, 绘画']
]   
var dbObj = null

async.waterfall([
    op => {
        dbObj = new MongoDB(url, 'hrdb')
        op()
    },

    op => {
        async.each(arr, function(item, callback) {
            dbObj.insertData('hr_table', {
                name  : item[0],
                age   : item[1],
                sex   : item[2],
                items : item[3]
            })
            callback()
        }) 
        op()
    },

    op => {
        dbObj.queryAllData('hr_table')
        op()
    },

    op => {
        dbObj.queryDataFor('hr_table', { 'name' : '蔓儿'})
        op()
    },

    op => {
        dbObj.dropCollection('hr_table')
        op()
    }
])