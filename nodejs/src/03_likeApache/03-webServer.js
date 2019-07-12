// 用Node.js仿真Apache
// 作者：owlman
// 时间：2019年07月12日

var http = require('http')
var fs = require('fs')
var server = http.createServer()

server.on('request', function(req, res){
    var webRoot = './www'
    var url = req.url
    if (url === '/') {
        url = '/index.htm'
    }
       
    fs.readFile(webRoot+url, function(err, data){
        if (err) {
            console.error(err)
            return res.end('<h1>404 页面没找到！</h1>')
        }
        res.end(data)
    })
})

server.listen(8080, function(){
    console.log('请访问http://localhost:8080/，按Ctrl+C终止服务！')
})
