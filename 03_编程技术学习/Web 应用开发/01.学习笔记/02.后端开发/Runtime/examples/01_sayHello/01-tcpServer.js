// 用Node.js脚本构建TCP服务器
// 作者：owlman
// 时间：2019年07月05日

const net = require('net')
const server = net.createServer(function (socket) {
    console.log('连接来自' + socket.remoteAddress)
    socket.end('你好，Nodejs！\n')
})

server.listen(7000, 'localhost', function(){
    console.log('TCP服务器监听 localhost 的 7000 端口，按 Ctrl+C 终止服务！')
})
