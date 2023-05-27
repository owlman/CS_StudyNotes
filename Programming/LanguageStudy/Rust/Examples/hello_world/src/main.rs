use std::io;

fn main() {
    let mut name = String::new();
    println!("Please enter a name...");
    io::stdin().read_line(&mut name).expect("输入错误");
    println!("Hello, world! \nMy name is {}.", name.trim());
} 
