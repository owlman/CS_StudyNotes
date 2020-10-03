// 用Node.js脚本构建Web服务器
// 作者：owlman
// 时间：2019年07月05日

const http = require('http')
const server = http.createServer()

server.on('request', function(req, res){
    res.end('<h1>你好，Nodejs！</h1>')
})

server.listen(8080, function(){
    console.log('请访问http://localhost:8080/，按Ctrl+C终止服务！')
})
