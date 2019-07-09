// 模拟Node.js的单文件模块
// 作者：owlman
// 时间：2019年07月09日

class ES6_syntax {
    constructor() {
        this.name = "ES6_syntax";    
    }
    sayhello() {
        console.log("Hello", this.name);
    }
};

module.exports = ES6_syntax;
