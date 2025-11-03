// 测试 JavaScript 的语法
// 作者：owlman

// {
//     var CNY, exRate, USD;
//     CNY = 100;
//     exRate = 0.1404;
//     USD = CNY * exRate;
// }

// console.log(USD);

// {
//     let CNY, exRate, USD;
//     CNY = 200;
//     exRate = 0.1404;
//     USD = CNY * exRate;
// }

// console.log(USD);


// let CNY, USD;
// const exRate = -0.1404; // 现在汇率为负值。
// CNY = 100;
// if (CNY < 0) {
//     console.log('人民币的币值不能为负数！');
// } else if (exRate < 0) {
//     console.log('人民币对美元的汇率不能为负数！');
// } else {
//     USD = CNY * exRate;
//     console.log('换算的美元币值为：', USD);
// }

// let number = 1002;

// switch (number) {
// case 1001:
//     console.log('张三');
//     break;
// case 1002:
//     console.log('李四');
//     break;
// case 1003:
//     console.log('王五');
//     break;
// case 1004:
//     console.log('赵六');
//     break;
// default:
//     console.log('你拨打的是空号！');
//     break;
// }

function printArguments() {
    for (let i = 0; i < arguments.length; ++i) {
        console.log(arguments[i]);
    }
  }
  
printArguments('one','two','three');
printArguments('batman','owlman');
printArguments(1,'123','three');
  