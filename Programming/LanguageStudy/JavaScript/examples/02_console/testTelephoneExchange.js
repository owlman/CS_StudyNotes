// 电话交换机测试
// 作者：owlman

// for (let number = 1001; number < 1006; ++number) {
//     switch (number) {
//         case 1001:
//             console.log('张三');
//             break;
//         case 1002:
//             console.log('李四');
//             break;
//         case 1003:
//             console.log('王五');
//             break;
//         case 1004:
//             console.log('赵六');
//             break;
//         default:
//             console.log('你拨打的是空号！');
//             break;
//     }
// }

function telephoneExchange(number) {
    switch (number) {
        case 1001:
            console.log('张三');
            break;
        case 1002:
            console.log('李四');
            break;
        case 1003:
            console.log('王五');
            break;
        case 1004:
            console.log('赵六');
            break;
        default:
            console.log('你拨打的是空号！');
            break;
    }
}

function testTelephoneExchange (callback) {
    for (let number = 1001; number < 1006; ++number) {
        callback(number);
    }
}

testTelephoneExchange(telephoneExchange);

testTelephoneExchange( number => {
    if (number == 1001) {
        console.log('batman');
    } else if (number == 1002) {
        console.log('owlman');
    } else {
        console.log('你拨打的是空号！')
    }
});
