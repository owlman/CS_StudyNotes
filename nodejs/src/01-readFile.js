// 用Node.js脚本读取文本文件
// 作者：owlman
// 时间：2019年07月03日

var fs = require("fs");
fs.readFile("data/text-data.txt", function(err, data) {
    if(err) {
        return console.error(err);
    }
    console.log(data.toString());
});
