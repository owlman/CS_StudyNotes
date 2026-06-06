// 用Node.js脚本写文本文件
// 作者：owlman
// 时间：2019年07月03日

const fs = require('fs')
const str = '你好，Nodejs！'

fs.writeFile('./data/output.txt', str, function(err){
    if ( err !== null ) {
        return console.error('错误信息：' + err.message)
     }
     console.log("文件写入成功!")
})
