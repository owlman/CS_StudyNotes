use std::io::{self, Write};

fn main() {
    let mut input = String::new();
    print!("Please give me a name: ");
    io::stdout().flush().expect("output error!");
    match io::stdin().read_line(&mut input) {
        Ok(n) => {
            println!("{} bytes read", n);
            let name = input.trim();
            println!("Hello, world! \nMy name is {}.", name);
        }
        Err(e) => {
            println!("Error Message: {}", e);
        }
    }
} 
