// 用Node.js处理get表单
// 作者：owlman
// 时间：2019年07月15日

const http = require('http')
const fs = require('fs')
const url = require('url')
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

const server = http.createServer(function(req, res){
    const query = url.parse(req.url, true)
    let obj = null
    let query_error = false
    if ( query.pathname === '/' ) {
        query_error = false
    }
    else if (query.pathname === '/query') {
        for(let i = 0; i < db.length; ++i) {
            if (db[i].name == query.query["qname"]) {
                obj = db[i]
            }
        }
        if ( obj === null ) {
            query_error = true
        }
    } else  {
        return res.end('<h1>404 页面没找到！</h1>')
    }

    fs.readFile('./index.htm', function(err, data){
        if ( err !== null ) {
            return res.end('<h1>404 没找到模版文件！</h1>')
        }
        
        let strHtml = null
        if ( obj !== null ) {
            strHtml = template.render(data.toString(), {
                name : obj.name,
                age  : obj.age,
                sex  : obj.sex,
                items: obj.items,
                query_error: query_error
            })
        } else {
            strHtml = template.render(data.toString(), {
                name : false,
                query_error: query_error
            })
        }
        res.end(strHtml)
    })
})

server.listen(8080, function(){
    console.log('请访问http://localhost:8080/，按Ctrl+C终止服务！')
})
