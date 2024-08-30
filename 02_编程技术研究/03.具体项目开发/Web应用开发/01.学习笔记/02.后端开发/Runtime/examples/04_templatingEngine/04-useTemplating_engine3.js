// 用Node.js生成动态页面
// 作者：owlman
// 时间：2019年07月12日

const http = require('http')
const fs = require('fs')
const template = require('art-template')

template.defaults.root = __dirname

class human {
    constructor(name, age, sex, items=[])
    {
        this.name  = name
        this.age   = age
        this.sex   = sex
        this.items = items
    }
}

const server = http.createServer()

server.on('request', function(req, res) {
    const url = req.url
    let boy = null
    if (url === '/') {
        boy = new human('凌杰', '37', '男', ['看书', '看电影','旅游'])
    } else if (url === '/wang') {
        boy = new human('蔓儿', '25', '女', ['看书', '看电影','写作'])
    }

    if (boy === null) {
        return res.end('<h1>404 页面没找到！</h1>')
    }

    fs.readFile('./extendTpl.htm', function(err, data) {
        if ( err !== null ) {
            return res.end('<h1>404 没找到模版文件！</h1>')
        }

        const strHtml = template.render(data.toString(), {
            name : boy.name,
            age  : boy.age,
            sex  : boy.sex,
            items: boy.items
        })

        res.end(strHtml)
    })
})

server.listen(8080, function(){
    console.log('请访问http://localhost:8080/，按Ctrl+C终止服务！')
})
