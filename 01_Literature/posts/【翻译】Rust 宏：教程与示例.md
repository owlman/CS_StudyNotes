# 【翻译】Rust 语言中的宏：示例教程

> **文献说明：**  
> 英文文献：[Macros in Rust: A tutorial with examples](https://link.zhihu.com/?target=https%3A//blog.logrocket.com/macros-in-rust-a-tutorial-with-examples/) ；  
> 参考翻译：[Rust宏：教程与示例](https://zhuanlan.zhihu.com/p/353421021#Rust%20%E5%AE%8F%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F)；  
> 二次加工：调整文章结构、改善翻译质量、标注文章要点；  

----

在这篇文献中，我们将会涵盖你需要了解的关于 Rust 宏（macro）的一切，包括对 Rust 宏的介绍和如何使用 Rust 宏的示例。  

我们会涵盖以下内容：

- Rust 宏是什么？
- Rust 宏的类型
- Rust 宏的声明  
    
-   创建声明式宏  
    
-   Rust 中声明式宏的高级解析
-   从结构体中解析元数据
-   声明式宏的限制  
    
-   Rust 中的过程宏  
    
-   属性式风格宏  
    
-   自定义继承宏
-   函数式风格宏

Rust 对宏（macro）有着非常好的支持。宏能够使得你能够通过写代码的方式来生成代码，这通常被称为元编程（metaprogramming）。  

宏提供了类似函数的功能，但是没有运行时开销。但是，因为宏会在编译期进行展开（expand），所以它会有一些编译期的开销。  

Rust 宏非常不同于 C 里面的宏。Rust 宏会被应用于词法树（token tree），而 C 语言里的宏则是文本替换。

## Rust 宏的类型

Rust 有两种类型的宏：

-  声明式宏（Declarative macros）使得你能够写出类似 match 表达式的东西，来操作你所提供的 Rust 代码。它使用你提供的代码来生成用于替换宏调用的代码。  
    
-   过程宏（Procedural macros）允许你操作给定 Rust 代码的抽象语法树（abstract syntax tree, AST）。过程宏是从一个（或者两个）`TokenStream`到另一个`TokenStream`的函数，用输出的结果来替换宏调用。  
    

让我们来看一下声明式宏和过程宏的更多细节，并讨论一些关于如何在 Rust 中使用宏的例子。

## Rust 中的声明式宏

宏通过使用`macro_rules!`来声明。声明式宏虽然功能上相对较弱，但提供了易于使用的接口来创建宏来移除重复性代码。最为常见的一个声明式宏就是`println！`。声明式宏提供了一个类似`match`的接口，在匹配时，宏会被匹配分支的代码替换。

## 创建声明式宏

```
macro_rules! add{
 // macth like arm for macro
    ($a:expr,$b:expr)=>{
 // macro expand to this code
        {
// $a and $b will be templated using the value/variable provided to macro
            $a+$b
        }
    }
}

fn main(){
 // call to macro, $a=1 and $b=2
    add!(1,2);
}
```

这段代码创建了一个宏来对两个数进行相加。[\[macro\_rules!\]](https://link.zhihu.com/?target=https%3A//doc.rust-lang.org/rust-by-example/macros.html)与宏的名称，`add`，以及宏的主体一同使用。  

这个宏没有对两个数执行相加操作，它只是把自己替换为把两个数相加的代码。宏的每个分支接收一个函数的参数，并且参数可以被指定多个类型。如果想要`add`函数也能仅接收一个参数，我们可以添加另一个分支：

```
macro_rules! add{
 // first arm match add!(1,2), add!(2,3) etc
    ($a:expr,$b:expr)=>{
        {
            $a+$b
        }
    };
// Second arm macth add!(1), add!(2) etc
    ($a:expr)=>{
        {
            $a
        }
    }
}

fn main(){
// call the macro
    let x=0;
    add!(1,2);
    add!(x);
}
```

在一个宏中，可以有多个分支，宏根据不同的参数展开到不同的代码。每个分支可以接收多个参数，这些参数使用`$`符号开头，然后跟着一个 token 类型：

-   `item` ——一个项（item），像一个函数，结构体，模块等。
-   `block` ——一个块 （block）（即一个语句块或一个表达式，由花括号所包围）
-   `stmt` —— 一个语句（statement）
-   `pat` ——一个模式（pattern）
-   `expr` —— 一个表达式（expression）
-   `ty` ——一个类型（type）
-   `ident`—— 一个标识符（indentfier）
-   `path` —— 一个路径（path）（例如，`foo`，`::std::mem::replace`，`transmute::<_, int>`，...）
-   `meta` —— 一个元数据项；位于`#[...]`和`#![...]`属性  
    
-   `tt`——一个词法树  
    
-   `vis`——一个可能为空的`Visibility`限定词

在上面的例子中，我们使用`$typ`参数，它的 token 类型为`ty`，类似于`u8`，`u16`。这个宏在对数字进行相加之前转换为一个特定的类型。

```
macro_rules! add_as{
// using a ty token type for macthing datatypes passed to maccro
    ($a:expr,$b:expr,$typ:ty)=>{
        $a as $typ + $b as $typ
    }
}

fn main(){
    println!("{}",add_as!(0,2,u8));
}
```

Rust 宏还支持接收可变数量的参数。这个操作非常类似于正则表达式。`*`被用于零个或更多的 token 类型，`+`被用于零个或者一个参数。

```
macro_rules! add_as{
    (
  // repeated block
  $($a:expr)
 // seperator
   ,
// zero or more
   *
   )=>{
       {
   // to handle the case without any arguments
   0
   // block to be repeated
   $(+$a)*
     }
    }
}

fn main(){
    println!("{}",add_as!(1,2,3,4)); // => println!("{}",{0+1+2+3+4})
}
```

重复的 token 类型被`$()`包裹，后面跟着一个分隔符和一个`*`或一个`+`，表示这个 token 将会重复的次数。分隔符用于多个 token 之间互相区分。`$()`后面跟着`*`和`+`用于表示重复的代码块。在上面的例子中，`+$a`是一段重复的代码。  

如果你更仔细地观察，你会发现这段代码有一个额外的 0 使得语法有效。为了移除这个 0，让`add`表达式像参数一样，我们需要创建一个新的宏，被称为[TT muncher](https://link.zhihu.com/?target=https%3A//danielkeep.github.io/tlborm/book/pat-incremental-tt-munchers.html)。

```
macro_rules! add{
 // first arm in case of single argument and last remaining variable/number
    ($a:expr)=>{
        $a
    };
// second arm in case of two arument are passed and stop recursion in case of odd number ofarguments
    ($a:expr,$b:expr)=>{
        {
            $a+$b
        }
    };
// add the number and the result of remaining arguments
    ($a:expr,$($b:tt)*)=>{
       {
           $a+add!($($b)*)
       }
    }
}

fn main(){
    println!("{}",add!(1,2,3,4));
}
```

TT muncher 以递归方式分别处理每个 token，每次处理单个 token 也更为简单。这个宏有三个分支：

-   第一个分支处理是否单个参数通过的情况  
    
-   第二个分支处理是否两个参数通过的情况  
    
-   第三个分支使用剩下的参数再次调用`add`宏  
    

宏参数不需要用逗号分隔。多个 token 可以被用于不同的 token 类型。例如，圆括号可以结合`ident`token 类型使用。Rust 编译器能够匹配对应的分支并且从参数字符串中导出变量。

```
macro_rules! ok_or_return{
// match something(q,r,t,6,7,8) etc
// compiler extracts function name and arguments. It injects the values in respective varibles.
    ($a:ident($($b:tt)*))=>{
       {
        match $a($($b)*) {
            Ok(value)=>value,
            Err(err)=>{
                return Err(err);
            }
        }
        }
    };
}

fn some_work(i:i64,j:i64)->Result<(i64,i64),String>{
    if i+j>2 {
        Ok((i,j))
    } else {
        Err("error".to_owned())
    }
}

fn main()->Result<(),String>{
    ok_or_return!(some_work(1,4));
    ok_or_return!(some_work(1,0));
    Ok(())
}
```

`ok_or_return`这个宏实现了这样一个功能，如果它接收的函数操作返回`Err`，它也返回`Err`，或者如果操作返回`Ok`，就返回`Ok`里的值。它接收一个函数作为参数，并在一个 match 语句中执行该函数。对于传递给参数的函数，它会重复使用。  

通常来讲，很少有宏会被组合到一个宏中。在这些少数情况中，内部的宏规则会被使用。它有助于操作这些宏输入并且写出整洁的 TT munchers。  

要创建一个内部规则，需要添加以`@`开头的规则名作为参数。这个宏将不会匹配到一个内部的规则除非显式地被指定作为一个参数。

```
macro_rules! ok_or_return{
 // internal rule.
    (@error $a:ident,$($b:tt)* )=>{
        {
        match $a($($b)*) {
            Ok(value)=>value,
            Err(err)=>{
                return Err(err);
            }
        }
        }
    };

// public rule can be called by the user.
    ($a:ident($($b:tt)*))=>{
        ok_or_return!(@error $a,$($b)*)
    };
}

fn some_work(i:i64,j:i64)->Result<(i64,i64),String>{
    if i+j>2 {
        Ok((i,j))
    } else {
        Err("error".to_owned())
    }
}

fn main()->Result<(),String>{
   // instead of round bracket curly brackets can also be used
    ok_or_return!{some_work(1,4)};
    ok_or_return!(some_work(1,0));
    Ok(())
}
```

## 在 Rust 中使用声明式宏进行高级解析

宏有时候会执行需要解析 Rust 语言本身的任务。  

让我们创建一个宏把我们到目前为止讲过的所有概念融合起来，通过`pub`关键字使其成为公开的。  

首先，我们需要解析 Rust 结构体来获取结构体的名字，结构体的字段以及字段类型。

### 解析结构体的名字及其字段

一个`struct`（即结构体）声明在其开头有一个可见性关键字（比如`pub` ） ，后面跟着`struct`关键字，然后是`struct`的名字和`struct`的主体。

![](https://pic2.zhimg.com/v2-2df8d58a6366dfdbcf53f08f91346305_b.jpg)

```
macro_rules! make_public{
    (
  // use vis type for visibility keyword and ident for struct name
     $vis:vis struct $struct_name:ident { }
    ) => {
        {
            pub struct $struct_name{ }
        }
    }
}
```

`$vis`将会拥有可见性，`$struct_name`将会拥有一个结构体名。为了让一个结构体是公开的，我们只需要添加`pub`关键字并忽略`$vis`变量。

![](https://pic2.zhimg.com/v2-60bfd6426d4c7ec107670534bf8f4021_b.jpg)

一个`struct`可能包含多个字段，这些字段具有相同或不同的数据类型和可见性。`ty` token 类型用于数据类型，`vis`用于可见性，`ident`用于字段名。我们将会使用`*`用于零个或更多字段。

```
macro_rules! make_public{
    (
     $vis:vis struct $struct_name:ident {
        $(
 // vis for field visibility, ident for field name and ty for field data type
        $field_vis:vis $field_name:ident : $field_type:ty
        ),*
    }
    ) => {
        {
            pub struct $struct_name{
                $(
                pub $field_name : $field_type,
                )*
            }
        }
    }
}
```

### 从`struct`中解析元数据

通常，`struct`有一些附加的元数据或者过程宏，比如`#[derive(Debug)]`。这个元数据需要保持完整。解析这类元数据是通过使用`meta`类型来完成的。

```
macro_rules! make_public{
    (
     // meta data about struct
     $(#[$meta:meta])*
     $vis:vis struct $struct_name:ident {
        $(
        // meta data about field
        $(#[$field_meta:meta])*
        $field_vis:vis $field_name:ident : $field_type:ty
        ),*$(,)+
    }
    ) => {
        {
            $(#[$meta])*
            pub struct $struct_name{
                $(
                $(#[$field_meta:meta])*
                pub $field_name : $field_type,
                )*
            }
        }
    }
}
```

我们的`make_public` 宏现在准备就绪了。为了看一下`make_public`是如何工作的，让我们使用[Rust Playground](https://link.zhihu.com/?target=https%3A//play.rust-lang.org/)来把宏展开为真实编译的代码。

```
macro_rules! make_public{
    (
     $(#[$meta:meta])*
     $vis:vis struct $struct_name:ident {
        $(
        $(#[$field_meta:meta])*
        $field_vis:vis $field_name:ident : $field_type:ty
        ),*$(,)+
    }
    ) => {

            $(#[$meta])*
            pub struct $struct_name{
                $(
                $(#[$field_meta:meta])*
                pub $field_name : $field_type,
                )*
            }
    }
}

fn main(){
    make_public!{
        #[derive(Debug)]
        struct Name{
            n:i64,
            t:i64,
            g:i64,
        }
    }
}
```

展开后的代码看起来像下面这样：

```
// some imports


macro_rules! make_public {
    ($ (#[$ meta : meta]) * $ vis : vis struct $ struct_name : ident
     {
         $
         ($ (#[$ field_meta : meta]) * $ field_vis : vis $ field_name : ident
          : $ field_type : ty), * $ (,) +
     }) =>
    {

            $ (#[$ meta]) * pub struct $ struct_name
            {
                $
                ($ (#[$ field_meta : meta]) * pub $ field_name : $
                 field_type,) *
            }
    }
}

fn main() {
        pub struct name {
            pub n: i64,
            pub t: i64,
            pub g: i64,
    }
}
```

## 声明式宏的限制

声明式宏有一些限制。有些是与 Rust 宏本身有关，有些则是声明式宏所特有的：

-   缺少对宏的自动完成和展开的支持  
    
-   声明式宏调式困难  
    
-   修改能力有限  
    
-   更大的二进制  
    
-   更长的编译时间（这一条对于声明式宏和过程宏都存在）  
    

![动图封面](https://pic1.zhimg.com/v2-d09750201555784c9d28f5aef49c0d80_b.jpg)

> 原文标题：Macros in Rust: A tutorial with examples  
> 原文链接：[https://blog.logrocket.com/macros-in-rust-a-tutorial-with-examples/](https://link.zhihu.com/?target=https%3A//blog.logrocket.com/macros-in-rust-a-tutorial-with-examples/)  
> 公众号： Rust 碎碎念  
> 翻译 by： Praying  

[过程宏（Procedural macros）](https://link.zhihu.com/?target=https%3A//blog.logrocket.com/procedural-macros-in-rust/)是一种更为高级的宏。过程宏能够扩展 Rust 的现有语法。它接收任意输入并产生有效的 Rust 代码。  

过程宏接收一个`TokenStream`作为参数并返回另一个`TokenStream`。过程宏对输入的`TokenStream`进行操作并产生一个输出。有三种类型的过程宏：

1.  属性式宏（Attribute-like macros）
2.  派生宏（Derive macros）
3.  函数式宏（Function-like macros）

接下来我们将会对它们进行详细讨论。

### 属性式宏

属性式宏能够让你创建一个自定义的属性，该属性将其自身关联一个项（item），并允许对该项进行操作。它也可以接收参数。

```
#[some_attribute_macro(some_argument)]
fn perform_task(){
// some code
}
```

在上面的代码中，`some_attribute_macros`是一个属性宏，它对函数`perform_task`进行操作。  

为了编写一个属性式宏，我们先用`cargo new macro-demo --lib`来创建一个项目。创建完成后，修改`Cargo.toml`来通知 cargo，该项目将会创建过程宏。

```
# Cargo.toml
[lib]
proc-macro = true
```

现在，我们可以开始过程宏学习之旅了。

过程宏是公开的函数，接收`TokenStream`作为参数并返回另一个`TokenStream`。要想写一个过程宏，我们需要先实现能够解析`TokenStream`的解析器。Rust 社区已经有了很好的 crate——[syn](https://link.zhihu.com/?target=https%3A//crates.io/crates/syn)，用于解析`TokenStream`。  

`syn`提供了一个现成的 Rust 语法解析器能够用于解析`TokenStream`。你可以通过组合`syn`提供的底层解析器来解析你自己的语法、  

把`syn`和[quote](https://link.zhihu.com/?target=https%3A//crates.io/crates/quote)添加到`Cargo.toml`。

```
# Cargo.toml
[dependencies]
syn = {version="1.0.57",features=["full","fold"]}
quote = "1.0.8"
```

现在我们可以使用`proc_macro`在`lib.rs`中写一个属性式宏，`proc_macro`是编译器提供的用于写过程宏的一个 crate。对于一个过程宏 crate，除了过程宏外，不能导出其他任何东西，crate 中定义的过程宏不能在 crate 自身中使用。

```
// lib.rs
extern crate proc_macro;
use proc_macro::{TokenStream};
use quote::{quote};

// using proc_macro_attribute to declare an attribute like procedural macro
#[proc_macro_attribute]
// _metadata is argument provided to macro call and _input is code to which attribute like macro attaches
pub fn my_custom_attribute(_metadata: TokenStream, _input: TokenStream) -> TokenStream {
    // returing a simple TokenStream for Struct
    TokenStream::from(quote!{struct H{}})
}
```

为了测试我们添加的宏，我们需要创建一个测试。创建一个名为`tests`的文件夹然后在该文件夹添加文件`attribute_macro.rs`。在这个文件中，我们可以测试我们的属性式宏。

```
// tests/attribute_macro.rs

use macro_demo::*;

// macro converts struct S to struct H
#[my_custom_attribute]
struct S{}

#[test]
fn test_macro(){
// due to macro we have struct H in scope
    let demo=H{};
}
```

使用命令`cargo test`来运行上面的测试。  

现在，我们理解了过程宏的基本使用，让我们用`syn`来对`TokenStream`进行一些高级操作和解析。

为了理解`syn`是如何用来解析和操作的，让我们来看[syn Github 仓库](https://link.zhihu.com/?target=https%3A//github.com/dtolnay/syn/blob/master/examples/trace-var/trace-var/src/lib.rs)上的一个示例。这个示例创建了一个 Rust 宏，这个宏可以追踪变量值的变化。  

首先，我们需要去验证，我们的宏是如何操作与其所关联的代码的

```
#[trace_vars(a)]
fn do_something(){
  let a=9;
  a=6;
  a=0;
}
```

`trace_vars`宏获取它所要追踪的变量名，然后每当输入变量（也就是`a`）的值发生变化时注入一条打印语句。这样它就可以追踪输入变量的值了。  

首先，解析属性式宏所关联的代码。`syn`提供了一个适用于 Rust 函数语法的内置解析器。`ItemFn`将会解析函数，并且如果语法无效，它会抛出一个错误。

```
#[proc_macro_attribute]
pub fn trace_vars(_metadata: TokenStream, input: TokenStream) -> TokenStream {
// parsing rust function to easy to use struct
    let input_fn = parse_macro_input!(input as ItemFn);
    TokenStream::from(quote!{fn dummy(){}})
}
```

现在我们已经解析了`input`，让我们开始转移到`metadata`。对于`metadata`，没有适用的内置解析器，所以我们必须自己使用`syn`的`parse`模块写一个解析器。

```
#[trace_vars(a,c,b)] // we need to parse a "," seperated list of tokens
// code
```

要想`syn`能够工作，我们需要实现`syn`提供的`Parse` trait。`Punctuated`用于创建一个由`,`分割`Indent`的`vector`。

```
struct Args{
    vars:HashSet<Ident>
}

impl Parse for Args{
    fn parse(input: ParseStream) -> Result<Self> {
        // parses a,b,c, or a,b,c where a,b and c are Indent
        let vars = Punctuated::<Ident, Token![,]>::parse_terminated(input)?;
        Ok(Args {
            vars: vars.into_iter().collect(),
        })
    }
}
```

一旦我们实现`Parse` trait，我们就可以使用`parse_macro_input`宏来解析`metadata`。

```
#[proc_macro_attribute]
pub fn trace_vars(metadata: TokenStream, input: TokenStream) -> TokenStream {
    let input_fn = parse_macro_input!(input as ItemFn);
    // using newly created struct Args
    let args= parse_macro_input!(metadata as Args);
    TokenStream::from(quote!{fn dummy(){}})
}
```

现在，我们准备修改`input_fn`以便于在当变量值变化时添加`println!`。为了完成这项修改，我们需要过滤出有复制语句的代码，并在那行代码之后插入一个 print 语句。

```
impl Args {
    fn should_print_expr(&self, e: &Expr) -> bool {
        match *e {
            Expr::Path(ref e) => {
 // variable shouldn't start wiht ::
                if e.path.leading_colon.is_some() {
                    false
// should be a single variable like `x=8` not n::x=0
                } else if e.path.segments.len() != 1 {
                    false
                } else {
// get the first part
                    let first = e.path.segments.first().unwrap();
// check if the variable name is in the Args.vars hashset
                    self.vars.contains(&first.ident) && first.arguments.is_empty()
                }
            }
            _ => false,
        }
    }

// used for checking if to print let i=0 etc or not
    fn should_print_pat(&self, p: &Pat) -> bool {
        match p {
// check if variable name is present in set
            Pat::Ident(ref p) => self.vars.contains(&p.ident),
            _ => false,
        }
    }

// manipulate tree to insert print statement
    fn assign_and_print(&mut self, left: Expr, op: &dyn ToTokens, right: Expr) -> Expr {
 // recurive call on right of the assigment statement
        let right = fold::fold_expr(self, right);
// returning manipulated sub-tree
        parse_quote!({
            #left #op #right;
            println!(concat!(stringify!(#left), " = {:?}"), #left);
        })
    }

// manipulating let statement
    fn let_and_print(&mut self, local: Local) -> Stmt {
        let Local { pat, init, .. } = local;
        let init = self.fold_expr(*init.unwrap().1);
// get the variable name of assigned variable
        let ident = match pat {
            Pat::Ident(ref p) => &p.ident,
            _ => unreachable!(),
        };
// new sub tree
        parse_quote! {
            let #pat = {
                #[allow(unused_mut)]
                let #pat = #init;
                println!(concat!(stringify!(#ident), " = {:?}"), #ident);
                #ident
            };
        }
    }
}
```

在上面的示例中，`quote`宏用于模板化和生成 Rust 代码。`#`用于注入变量的值。  

现在，我们将会在`input_fn`上进行 DFS，并插入 print 语句。`syn`提供了一个`Fold`trait 可以用来对任意`Item`实现 DFS。我们只需要修改与我们想要操作的 token 类型所对应的 trait 方法。

```
impl Fold for Args {
    fn fold_expr(&mut self, e: Expr) -> Expr {
        match e {
// for changing assignment like a=5
            Expr::Assign(e) => {
// check should print
                if self.should_print_expr(&e.left) {
                    self.assign_and_print(*e.left, &e.eq_token, *e.right)
                } else {
// continue with default travesal using default methods
                    Expr::Assign(fold::fold_expr_assign(self, e))
                }
            }
// for changing assigment and operation like a+=1
            Expr::AssignOp(e) => {
// check should print
                if self.should_print_expr(&e.left) {
                    self.assign_and_print(*e.left, &e.op, *e.right)
                } else {
// continue with default behaviour
                    Expr::AssignOp(fold::fold_expr_assign_op(self, e))
                }
            }
// continue with default behaviour for rest of expressions
            _ => fold::fold_expr(self, e),
        }
    }

// for let statements like let d=9
    fn fold_stmt(&mut self, s: Stmt) -> Stmt {
        match s {
            Stmt::Local(s) => {
                if s.init.is_some() && self.should_print_pat(&s.pat) {
                    self.let_and_print(s)
                } else {
                    Stmt::Local(fold::fold_local(self, s))
                }
            }
            _ => fold::fold_stmt(self, s),
        }
    }
}
```

`Fold` trait 用于对一个`Item`进行 DFS。它使得你能够针对不同的 token 类型采取不同的行为。  

现在我们可以使用`fold_item_fn`在我们解析的代码中注入 print 语句。

```
#[proc_macro_attribute]
pub fn trace_var(args: TokenStream, input: TokenStream) -> TokenStream {
// parse the input
    let input = parse_macro_input!(input as ItemFn);
// parse the arguments
    let mut args = parse_macro_input!(args as Args);
// create the ouput
    let output = args.fold_item_fn(input);
// return the TokenStream
    TokenStream::from(quote!(#output))
}
```

这个代码示例来自于[syn 示例仓库](https://link.zhihu.com/?target=https%3A//github.com/dtolnay/syn/blob/master/examples/trace-var/trace-var/src/lib.rs)，该仓库也是关于过程宏的一个非常好的学习资源。

### 自定义派生宏

Rust 中的自定义派生宏能够对 trait 进行自动实现。这些宏通过使用`#[derive(Trait)]`自动实现 trait。  

`syn`对`derive`宏有很好的支持。

```
#[derive(Trait)]
struct MyStruct{}
```

要想在 Rust 中写一个自定义派生宏，我们可以使用`DeriveInput`来解析派生宏的输入。我们还将使用`proc_macro_derive`宏来定义一个自定义派生宏。

```
#[proc_macro_derive(Trait)]
pub fn derive_trait(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
    let input = parse_macro_input!(input as DeriveInput);

    let name = input.ident;

    let expanded = quote! {
        impl Trait for #name {
            fn print(&self) -> usize {
                println!("{}","hello from #name")
           }
        }
    };

    proc_macro::TokenStream::from(expanded)
}
```

使用`syn`可以编写更为高级的过程宏，请查阅`syn`仓库中的[这个示例](https://link.zhihu.com/?target=https%3A//github.com/dtolnay/syn/blob/master/examples/heapsize/heapsize_derive/src/lib.rs)。

### 函数式宏

函数式宏类似于声明式宏，因为他们都通过宏调用操作符`!`来执行，并且看起来都像是函数调用。它们都作用于圆括号里的代码。  

下面是如何在 Rust 中写一个函数式宏：

```
#[proc_macro]
pub fn a_proc_macro(_input: TokenStream) -> TokenStream {
    TokenStream::from(quote!(
            fn anwser()->i32{
                5
            }
))
}
```

函数式宏在编译期而非在运行时执行。它们可以在 Rust 代码的任何地方被使用。函数式宏同样也接收一个`TokenStream`并返回一个`TokenStream`。

使用过程宏的优势包括：

-   使用`span`获得更好的错误处理
-   更好的控制输出
-   社区已有`syn`和`quote`两个 crate
-   比声明式宏更为强大

## 总结

在这篇 Rust 教程中，我们涵盖了 Rust 中关于宏的基本内容，声明式宏和过程宏的定义，以及如果使用各种语法和社区的 crate 来编写这两种类型的宏。我们还总结了每种类型的 Rust 宏所具有优势。

Update 2021-3-12：

感谢

老师纠正，将Derive macros译为派生宏更为合适。

![动图封面](https://pic1.zhimg.com/v2-d09750201555784c9d28f5aef49c0d80_b.jpg)
