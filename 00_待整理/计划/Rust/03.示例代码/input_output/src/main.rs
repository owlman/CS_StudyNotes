// 引入标准库中的 I/O 模块
use std::io::{self, Write};

// 将相关操作封装成函数
fn say_hello () {
    // 定义一个可变量，用于接受用户的输入
    let mut input = String::new();
    // 使用 print! 这个宏输出不带换行符的字符串信息
    print!("Please give me a name: ");
    // 刷新标准输出的缓存，以确保上面的字符串已经被输出到终端中
    io::stdout().flush().expect("output error!");
    // 使用 match 关键字匹配用户执行输入之后的状态
    //  io::stdin().read_line() 方法会从标准输入中获取到用户的输入
    match io::stdin().read_line(&mut input) {
        Ok(n) => { // 如果输入成功，执行如下代码
            println!("{} bytes read", n);
            // 定义一个不可变量，用于存储被处理后的信息
            // input.trim() 方法用于去除掉输入信息中的换行符
            let name = input.trim();
            println!("Hello, world! \nMy name is {}.", name);
        }
        Err(_) => { // 如果输入失败，执行如下代码
            println!("Input Error!");
        }
    }
}

fn main() {
    // 调用自定义函数
    say_hello();   
}
