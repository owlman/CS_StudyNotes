use std::io;

fn main() {
    let mut input = String::new();
    println!("Please give me a name...");
    match io::stdin().read_line(&mut input) {
        Ok(n) => {
            println!("{n} bytes read");
            let name = input.trim();
            println!("Hello, world! \nMy name is {name}.");
        }
        Err(e) => {
            println!("Error Message: {e}");
        }
    }
} 
