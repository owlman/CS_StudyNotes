// 测试Node.js的模块语法
// 作者：owlman
// 时间：2019年07月09日

const singleFile_module = require(`./02-singleFile`)
const testobj = new singleFile_module()
testobj.sayhello()

const multiFile_module = require(`./02-multiFile`)
const testobj2 = new multiFile_module()
testobj2.sayhello()
