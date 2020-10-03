// 用Node.js处理post表单
// 作者：owlman
// 时间：2019年07月15日

const http = require('http')
const fs = require('fs')
const url = require('url')
const querystring = require('querystring')
const template = require('art-template')

class human {
    constructor(name, age, sex, items=[])
    {
        this.name  = name
        this.age   = age
        this.sex   = sex
        this.items = items
    }
}

const db = [
    new human('凌杰', '37', '男', ['看书', '看电影','旅游']),
    new human('蔓儿', '25', '女', ['看书', '看电影','写作']),
    new human('张语', '32', '女', ['看书', '旅游','绘画'])
]

const server = http.createServer(function(req, res) {
    const query = url.parse(req.url, true)
    if ( query.pathname === '/' ) {
        fs.readFile('./index.htm', function(err, data) {
            if ( err !== null ) {
                return res.end('<h1>404 没找到模版文件！</h1>')
            }
            
            const strHtml = template.render(data.toString(),{
                "db": db
            })
            
            res.end(strHtml)
        })
    }
    else if ( query.pathname === '/add' ) {
        req.on('data', function(chunk) {
            const obj = querystring.parse(chunk.toString())
            db.push(new human(
                obj['uname'],
                obj['age'],
                obj['sex'],
                obj['items'].split('，'),
            ))
        })

        res.writeHead(302, {
            'location': `/`
        })

        res.end()
    } else  {
        return res.end('<h1>404 页面没找到！</h1>')
    }    
})

server.listen(8080, function(){
    console.log('请访问http://localhost:8080/，按Ctrl+C终止服务！')
})
