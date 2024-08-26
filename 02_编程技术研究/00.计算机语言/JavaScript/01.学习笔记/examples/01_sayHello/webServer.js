const http = require('http');
const server = http.createServer();

server.on('request', function(req, res){
    res.end('<h1>Hello Nodejs! </h1>');
});

server.listen(8081, function(){
    console.log('请访问http://localhost:8081/，按Ctrl+C终止服务！');
});
