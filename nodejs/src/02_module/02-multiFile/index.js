// 模拟Node.js的多文件模块
// 作者：owlman
// 时间：2019年07月09日

const func = require('./file1')
const str = require('./file2')

class multiFile_module {
    constructor(){
        this.func = func.add
        this.name = str.name
    }

    sayhello(){
        console.log('Hello', this.name)
        console.log('x + y = ', this.func(10,5))
    }
}

module.exports = multiFile_module
