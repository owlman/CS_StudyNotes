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

// function telephoneExchange(number) {
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

// function testTelephoneExchange (callback) {
//     for (let number = 1001; number < 1006; ++number) {
//         callback(number);
//     }
// }

// testTelephoneExchange(telephoneExchange);

// testTelephoneExchange( number => {
//     if (number == 1001) {
//         console.log('batman');
//     } else if (number == 1002) {
//         console.log('owlman');
//     } else {
//         console.log('你拨打的是空号！')
//     }
// });

// // 电话交换机测试 2.0 版
// // 作者：owlman

// class TelephoneExchange {
//     constructor(names) {        // names 形参允许指定加入该电话交换机的初始名单
//         this.mp = new Map();
//         this.firstNum = 1001;     // 该电话交换机的第一个未占用的号码

//         for(let name of names) {
//             this.firstNum++;
//             this.mp.set(this.firstNum, name); // 为初始名单分配电话号码
//         }
//     }

//     add(name) {                          // 为新客户添加线路
//         this.firstNum++;
//         this.mp.set(this.firstNum, name);
//     }

//     delete(number) {                     // 删除线路
//         this.mp.delete(number);
//     }

//     update (number, name) {               // 修改已有线路的所属人
//         if (this.mp.has(number)) {
//             this.mp.set(number, name);
//         } else {
//             console.log(number + '是空号！');
//         }
//     }

//     call(number) {                       // 拨打指定线路
//         if (this.mp.has(number)) {
//             let name = this.mp.get(number);
//             console.log('你拨打的用户是： ' + name);
//         } else {
//             console.log(number + '是空号！');
//         }
//     }

//     callAll() {                          // 拨打所有线路
//         for (let number of this.mp.keys()) {
//             this.call(number);
//         }
//     }
// };

// let phoneExch = new TelephoneExchange(['张三', '李四', '王五', '赵六']);
// phoneExch.callAll();
// console.log('-----------');
// phoneExch.add('owlman');
// phoneExch.callAll();
// console.log('-----------');
// phoneExch.delete(1002);
// phoneExch.callAll();
// console.log('-----------');
// phoneExch.update(1003,'batman');
// phoneExch.callAll();
// console.log('-----------');

// 电话交换机测试 4.0 版
// 作者：owlman

class TelephoneExchange {
    constructor(names) {        // names 形参允许指定加入该电话交换机的初始名单
        this.map = new Map();
        this.firstNum = 1001;     // 该电话交换机的第一个未占用的号码

        for(let name of names) {
            this.firstNum++;
            this.map.set(this.firstNum, name); // 为初始名单分配电话号码
        }
    }

    add(name) {                           // 为新客户添加线路
        this.firstNum++;
        this.map.set(this.firstNum, name);
    }

    delete(number) {                      // 删除线路
        this.map.delete(number);
    }

    update(number, name) {                // 修改已有线路的所属人
        if (this.map.has(number)) {
            this.map.set(number, name);
        } else {
            console.log(number + '是空号！');
        }
    }

    call(number) {                        // 拨打指定线路
        const me = this;
        return new Promise(function(resolve, reject) {
            const time = Math.random()*5000;
            setTimeout(function() {
                if (me.map.has(number)) {
                    let name = me.map.get(number);
                    if(time > 3000) {
                        resolve('呼叫超时');
                    } else {
                        resolve('你拨打的用户是： ' + name);
                    }
                } else {
                    resolve(number + '是空号！');
                }
            }, time);
        }).then(function(msg) {
            console.log(msg);
        });
    }

    async callAll() {
        console.log('-----开始测试系统所有线路------');
        const promises = new Array();                         // 拨打所有线路
        for(let number of this.map.keys()) {
            promises.push(this.call(number));
        }
        return await Promise.all(promises).then(function() {
            console.log('-----系统全部线路测试结束------');
        });
    }
};

async function testTelephoneExchange(phoneExch) {
    await phoneExch.callAll();  
    phoneExch.add('owlman');
    await phoneExch.callAll();
    phoneExch.delete(1002);
    await phoneExch.callAll();
    phoneExch.update(1003,'batman');
    await phoneExch.callAll();
}

testTelephoneExchange(new TelephoneExchange(['张三', '李四', '王五', '赵六']));  
