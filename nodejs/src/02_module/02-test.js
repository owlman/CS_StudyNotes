// 测试Node.js的模块语法
// 作者：owlman
// 时间：2019年07月09日

const es5_syntax = require("./02-singleFile");
const testobj = new es5_syntax();
testobj.sayhello();

const multi_file_module = require("./02-multiFile");
const testobj2 = new multi_file_module();
testobj2.sayhello();
