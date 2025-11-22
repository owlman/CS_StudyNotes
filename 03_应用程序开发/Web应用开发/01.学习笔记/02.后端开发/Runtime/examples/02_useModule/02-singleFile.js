// 模拟Node.js的单文件模块
// 作者：owlman
// 时间：2019年07月09日

class singleFile_module {
    constructor() {
        this.name = 'singleFile_module'    
    }

    sayhello() {
        console.log('Hello', this.name)
    }
}

module.exports = singleFile_module
