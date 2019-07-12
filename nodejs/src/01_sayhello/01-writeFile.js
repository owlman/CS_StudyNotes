// 用Node.js脚本写文本文件
// 作者：owlman
// 时间：2019年07月03日

var fs = require('fs')
var str = '你好，Nodejs！'

fs.writeFile('../data/output.txt', str, function(err){
    if(err) {
        console.error(err)
    } else {
        console.log("文件写入成功!")
    }
})
