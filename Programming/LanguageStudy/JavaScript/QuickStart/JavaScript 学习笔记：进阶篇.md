# JavaScript 学习笔记：进阶篇

> 本文节选自笔者于 2021 年出版的[《JavaScript 全栈开发》](https://book.douban.com/subject/35493728/)一书。

在[[JavaScript 学习笔记：基础篇]]的最后部分中，笔者对“电话交换机测试”这个程序做了一系列的改进。首先，我们将程序中不同的任务操作分离出来封装成了函数，然后又将任务中使用的数据分离出来组织成了数据结构，最后再将数据结构与其相关的函数组合起来封装成了对象。细心的读者应该已经发现了，这一系列分离、组合、封装动作都来自同一个需求驱动力，那就是降低代码中的耦合度。为什么降低耦合度这件事在编程方法上占有如此重要的位置？其根本原因在于计算机程序的规模日益膨胀，以至于如今大多数程序都不是靠单打独斗就可以完成的了。既然在编程上的多人协作已经不可避免，如何进行团队分工就自然而然地成为了编程工作中首先要解决的问题。

对于分工协作，人类所有成功的经验基本上都来自于工业革命以来逐步完善的制造业工厂。为了使生产效率实现最大化，工厂生产线上所有的对象，包括工人，各个级别的管理员也都像生产零件一样是可替换的。要想实现这一点，生产线上各个对象之间的耦合度就必须降到最低，理论上它们都只需要做好自己的事情，彼此甚至都不需要知道对方的存在。而致力于将硬件生产线上的成功经验复制到编程工作中来，形成软件生产线的努力就被我们称之为“软件工程”，正是这种将软件生产工程化的努力催化出了致力于从各个角度降低耦合度的编程方法。在这篇笔记中，我将为读者介绍面向对象编程与异步编程这两种编程方法在 JavaScript 中的使用和具体实现方式。在阅读完本章内容之后，我们希望读者能：

## 面向对象编程

在程序被分割成一个个对象，并且将对象之间的耦合度降低到一定程度之后，程序员们就会面临随之而来的一个新问题，那就是这些对象之间要如何互动呢？例如，当我们将电话交换机的实现封装成一个对象之后，回过头来却发现之前的测试函数不能用了，当然，我们为该对象编写了相应的测试代码：

```javascript
let phoneExch = new TelephoneExchange(['张三', '李四', '王五', '赵六']);
phoneExch.callAll();
console.log('-----------');
phoneExch.add('owlman');
phoneExch.callAll();
console.log('-----------');
phoneExch.delete(1002);
phoneExch.callAll();
console.log('-----------');
phoneExch.update(1003,'batman');
phoneExch.callAll();
console.log('-----------');
```

如你所见，这段代码测试了电话交换机的初始化，电话线路的添加、删除与修改，并且在每次线路变化时都会呼叫一遍所有线路，以便确认其是否工作正常。但是，这些测试都只是针对`TelephoneExchange`这个类的对象来编写的。我们现在要思考的是：如果电话交换机有了新的实现方式，其测试代码是否也要随之重写呢？更重要的问题是，如果我们是要对新的电话交换机实现进行完全不一样的测试，重写当然是很自然的事，但对于电话交换机来说，除了线路网络的初始化，增加、删除、修改与呼叫之外，还有多少新的测试可写呢？既然所有的电话交换机测试都大同小异，上面的测试代码为什么就不能被重用呢？

要想找到这个问题的解决思路，我们就需要先回到软件工程的思想源头，看看人们在工厂的生产线上是怎么解决类似问题的。在关于流水线生产的描述上，很多人应该都听说过“流水线上每个人都是一颗可被替换的螺丝钉”的说法。是的，这就是流水线生产的最理想状态。对于一颗螺丝钉，你想成本低廉，它可以是铁的，你不想它生锈，它可以是不锈钢的，你想减轻重量，它可以是铝合金的。但无论这些螺丝钉是用什么做的，它们最终都必须要能被拧进一个螺丝孔里。换句话说，在工厂流水线上，判断螺丝钉是否可相互替换的测试方法只有一个，那就是看它们能不能被拧进被指定的螺丝孔里，这与它的材质并没有多大的关系。对应到编程术语中，用不锈钢、铝合金这些材质制作螺丝钉的过程被称作对象的“实现”，而这些螺丝钉最终要被拧进去的这个螺丝孔则被称作对象的“接口”。所以从此可以看出，让上述测试代码可被重用的关键就在于我们能否实现接口一致的电话交换机。对于这种将对象接口一致化的编程方式，我们通常称之为**面向对象编程**。

在面向对象编程的方法论中，我们通常会先为将要执行某一类操作的对象设计一个抽象的“基类”，然后以该类的接口为基准来实现其他用于具现化这些对象的“具体类”。在编程术语中，我们称这些后来的具体类是“继承”了基类的接口，它们是这个基类的“子类”，因而基类有时也被称作“父类”。接下来，就让我们来看看具体到了 JavaScript 中，父类、子类以及它们之间的接口继承是如何实现的。

### 接口设计与实现

在具体设计并实现对象的接口之前，我们首先要了解如何用编程语言来实现“接口”这个概念。相信学习过 C++、Java 的读者应该都还记得，我们在使用这些传统面向对象编程语言定义类的时候，通常都会被要求为其属性和方法设置`private`、`public`等不同层次的访问权限。通常情况下，被设置为`private`的属性和方法主要供其所在对象内部来使用，对象外面的代码是无法直接使用它们的。而被设置为`public`的属性和方法则是直接提供给该对象的调用方来使用的。在编程术语上，被设置为public的这部分属性和方法通常就被称之为**接口**。

所以，设计对象接口的工作本质上就是在决定对象的哪一部分应该提供给调用方，成为接口，而哪一部分应该被视为对象的实现细节而隐藏在对象内部。但这样一来，我们就会立即面临到一个现实问题：JavaScript 在语法层面上并没有提供`private`、`public`这种限制权限的机制。为此，我们得使用一些变通手段来完成接口的设计工作，下面就来为介绍两种目前较为常用的解决方案：

- **编码规范约束**：众所周知，编码规范是程序员之间靠自觉遵守的一种君子协议。它虽然不具有强制性，但为了使团队协作顺畅，降低代码维护成本，大部分程序员都会选择自觉遵守。所以，对象的设计者可以通过某种约定的命名方式告诉对象的调用方，哪一些属性和方法是不希望被对象外部的代码使用的。例如对于一个`Point`类的对象来说，如果我们不希望外界直接访问它的`x`、`y`属性，就可以在这些属性名前面加上一个下划线：

    ```javascript
    class Point {
        constructor(x,y) {
            this._x = x;
            this._y = y;
        }

        printCoords() {
            console.log('坐标：（'+ this._x + ', ' + this._y + '）');
        }
    };
    ```

    这样一来，我们就等于告诉了`Point`类的调用方一个信息：“`_`x和`_y`是私有属性，为了相关代码的日后维护，请不要直接使用它们”。当然，必须再强调一次，这种约束没有强制性，如果有人没有团队协作概念，硬要直接使用甚至修改这两个属性，JavaScript 解释器是不会报错的：

    ```javascript
    const p = new Point(5,5);
    p.printCoords();  // 输出： 坐标：（5,5）
    p._y = -10;
    p.printCoords();  // 输出： 坐标：（5,-10）
    ```

- **局部变量方案**：在 JavaScript 中，由于变量的作用域被分为了函数作用域和全局作用域（ES6 标准新增了块级作用域），函数内部的局部变量在函数之外是不可见的，所以我们可以利用这一特性将需要设置为`private`的属性隐藏在构造函数的作用域内。例如，对于上面的`Point`类，我们也可以这样定义：

    ```javascript
    class Point {
        constructor(x,y) {
            let _x = x;
            let _y = y;

            this.printCoords = function() {
                console.log('坐标：（'+ _x + ', ' + _y + '）');
            };
        }
    };

    const p = new Point(5,5);
    p.printCoords();   // 输出： 坐标：（5,5）
    p._y = 10;         // 操作无效，只是给 p 对象额外增加了一个 _y 属性
    p.printCoords();   // 输出： 坐标：（5,5）
    ```

    如你所见，`Point`类的调用方现在无法修改直接访问类定义的坐标属性了，它只能为`p`这个单一对象添加一个无用的_y属性，影响不了对象方法的行为。但这样做的坏处也是显而易见的：首先，为了让Point类自己的方法能使用构造函数的局部变量，我们得用属性的形式将这些方法定义在构造函数内部，这不仅会造成上一章中所说的代码冗余，而且也破坏了 ES6 标准新增的类定义语法，使我们在很大程度上用回了 ES5 时代以及更早之前的、那种不够优雅且隐晦难懂的语法。但无论如何，这种解决方案是真正实现了将相关对象属性设置为`private`的效果，不再需要调用方自觉遵守某种约定了。

总而言之，虽然 JavaScript 本身没有提供私有化对象属性和方法的机制，但我们可以利用这门语言强大的自由度来实现类似的功能。但我们同时也必须谨记“自由即责任”的原则，在享受自由度带来的强大功能之时，也要承担自由所带来的风险，这实际上也是对程序员自身能力的严峻考验。

在隐藏了对象的“实现”部分之后，我们接下来就该来考虑对象的“接口”问题了。这个问题的另一个问法是：我们希望调用方如何使用对象？例如，对于上面的`Point`类，调用方只能在初始化对象时为其指定一个二维标，然后就只能通过`printCoords`方法来在终端输出该“点”对象的坐标了，所以我们可以理所当然地认为，`Point`类的设计者希望提供的是一个固定的“点”对象，它在坐标系中的位置是不变的。接下来，如果我们将`Point`类的设计意图修改成一个可移动的“点”对象，就必须为其调用方提供一个修改坐标的接口：

```javascript
class Point {
    constructor(x,y) {
        let _x = x;
        let _y = y;

        this.printCoords = function() {
            console.log('坐标：（'+ _x + ', ' + _y + '）');
        };

        this.updateCoords = function(x,y) {
            _x = x;
            _y = y;
        };
    }  
};


const p = new Point(5,5);
p.printCoords();         // 输出： 坐标：（5,5）
p.updateCoords(10,10);
p.printCoords();         // 输出： 坐标：（10,10）
```

如你所见，现在`Point`类的调用方可以通过`updateCoords`方法来修改“点”对象的坐标了。而且，从这里读者也可以看出允许直接修改`_x`、`_y`属性，与让人通过接口来修改坐标的区别，那就是我们可以通过后者来限制调用方的动作，以防止一些破坏性的修改。例如，如果我们的“点”对象只能在坐标系第一象限内活动，那就必须确保`_x`和`_y`不能为负值，为此我们需要修改一下`updateCoords`方法的实现：

```javascript
this.updateCoords = function(x,y) {
    if ((x<0) || (y<0)) {
        console.log('坐标不能为负值！');
        return false;
    }
    _x = x;
    _y = y;
};
```

这样一来，当该类的调用方执行`p.updateCoords(10,-10)`这样的操作时，修改动作就会被制止。同样地，如果我们还希望允许调用方以只读方式获取`_x`或`_y`坐标值，还可以再提供`getX`和`getY`这两个方法：

```javascript
class Point {
    constructor(x,y) {
        let _x = x;
        let _y = y;

        this.printCoords = function() {
            console.log('坐标：（'+ _x + ', ' + _y + '）');
        };

        this.updateCoords = function(x,y) {
            if ((x<0) || (y<0)) {
                console.log('坐标不能为负值！');
                return false;
                }
            _x = x;
            _y = y;
        };

        this.getX = function() {
            return _x;
        };

        this.getY = function() {
            return _y;
        };
    }  
};

const p = new Point(5,5);
p.updateCoords(10,10);
console.log(p.getX()+','+p.getY()); // 输出: 10,10
```

现在，相信读者已经对接口的设计思路有了一个初步的认识，要想更深一步理解接口的作用，就必须要了解如何让未来的类共享现有类的接口，以实现真正的面向对象编程了。

### 使用类继承语法

希望上一节中那些自由放纵的，新旧标准混搭的类定义语法没有给读者带来太大的困惑。毕竟，在笔者个人看来，JavaScript 这门语言最大的魅力就在于“自由”，当然享受自由这件事需要量力而行，不要忘记“自由即责任”的原则。接下来，为了让读者对类型继承能有一个较为直观的理解，我们会先暂且用回 ES6 标准制定的类定义语法，以便引出对类继承的介绍。待掌握类型继承机制在 JavaScript 语言中的具体实现之后，我们再来讨论如何将上述隐藏实现的技巧也应用到类型继承机制中。

书归正传，想必大家都已经知道了，ES6 标准为 JavaScript 语言新增了与传统面向对象语言相类似的类型继承语法，具体如下：

```javascript
class [子类名] extends [父类名] {
    constructor([构造形参]) {
        super([父类的构造实参]);
        [创建子类属性并将其初始化]
    }

    [子类方法定义]
};
```

下面，我们来对类继承语法中的各个单元做个说明：首先，该语法依然是一个类定义语句，所以它沿用了之前类定义语句中所有的元素。只不过，这次我们是基于一个现有类来构造新的类型，它必须用`extends`关键字为自己指定一个基础类型，所以这里的`[父类名]`必须是一个已经被定义的类名。然后，在子类的`constructor`函数中，我们必须先用`super`关键字调用父类构造函数，然后才能用`this`引用添加子类的属性，因为在类继承语法中，子类的`this`是在父类构造函数中创建的。例如，如果我们想基于之前的`Point`类创造一个可以标记颜色的“点”类型`colorPoint`，就可以这样做：

```javascript
class Point {
    constructor(x,y) {
        this._x = x;
        this._y = y;
    }

    printCoords() {
        console.log('坐标：（'+ this._x + ', ' + this._y + '）');
    }

    updateCoords(x,y) {
        if ((x<0) || (y<0)) {
            console.log('坐标不能为负值！');
            return false;
            }
        this._x = x;
        this._y = y;
    };

    getX() {
        return this._x;
    };

    getY() {
        return this._y;
    };
};

class colorPoint extends Point {
    constructor(x,y,color) {
        super(x,y);
        this._color = color;
    }

    updateColor(color) {
        this._color = color;
    }

    printCoords() {
        super.printCoords();
        console.log('颜色：', this._color);
    }
}

const p = new colorPoint(5,5,'红');
p.printCoords();         // 输出： 坐标：（5,5）
                                   //             颜色：红
p.updateCoords(10,10);
p.updateColor('绿')
p.printCoords();         // 输出： 坐标：（10,10）
                                   //            颜色：绿
```

从上述代码中，我们可以看到三点：

- 第一：子类可以原封不动地共享父类的接口及其实现，譬如`updateCoords`方法就完全使用了父类原有的实现。
- 第二：子类可以共享父类的接口并修改其实现，譬如`printCoords`方法的实现就在子类中被重新修改了。
- 第三：子类可以在父类实现的基础上为自己添加新的属性和方法，譬如`_color`属性和`updateColor`方法就是子类中新增的部分。

在编程术语上，上述这种子类共享父类接口与实现的方式就被称作“继承”，而对于继承自父类的接口进行重新实现的行为，我们通常称之为“重写”或“覆写”。请注意，从上面我们对`printCoords`方法的覆写可以看出，即使该方法被覆写了，父类的`printCoords`方法在子类的内部依然是可用的，我们可以通过`super`关键字来调用它。

需要注意的是，`super`关键字在子类中实际上有两种用法：第一种是使用函数调用操作符，例如`super()`，这种用法只能用于调用父类的构造函数，并且只能在子类的构造函数中调用。第二种是使用成员操作符，例如`super.printCoords()`，这种用法只能用于在子类方法中调用父类的方法。是的，很令人意外，我们“只能”用`super`调用父类的方法，而不能用它来获取父类的属性。也就是说，如果我们在子类方法中调用`console.log(super._x)`，得到的会是`undefined`。这是为什么呢？这就涉及到 JavaScript 中对象的具体实现问题了。

### 深度探索对象

众所周知，在 ES6 标准发布之前，在 JavaScript 中是用构造函数来充当“类”的角色的。那么，构造函数与它所创建的对象之间究竟是什么关系呢？事实上，这个问题也可以回到工厂生产过程中去寻找答案。大家都知道“类”的作用就相当于是对象的模版，现在请试想一下，如果要在没有模版的情况下生产一个新产品，工人们会怎么做呢？答案是，他们通常会先试着找到一个现有产品，然后再以该产品为基础设计出一个原型产品，最后再以原型产品为基准来生产目标产品。对应在编程术语上，这种用作基准的对象被称作目标对象的“原型对象”，而构造函数的作用就是为将要创建的对象设计原型对象。

#### 使用原型对象

换而言之，在 JavaScript 中，每个对象都会有一个原型对象，而其原型对象则来自于它们各自的构造函数。那么，这个说法可以用代码来证明吗？答案是肯定的，我们可以通过 JavaScript 的内置对象方法`Object.getPrototypeOf()`来查看指定对象的原型对象，下面来做个实验：先定义一个构造函数，然后再用它创建两个对象，看看这两个对象的原型是什么：

```javascript
function Hero(name) {
    this.name = name;
}
  
let hero_1 = new Hero('owlman');
let hero_2 = new Hero('batman');

console.log(hero_1.name)                     // 输出： owlman
console.log(Object.getPrototypeOf(hero_1));  // 输出： Hero ()
console.log(hero_2.name)                     // 输出： batman
console.log(Object.getPrototypeOf(hero_2));  // 输出： Hero ()
```

从上述实验的结果，我们可以看到：`hero_1`和`hero_2`的`name`属性值分别为`"owlman"`和`"batman"`，但它们的原型对象都指向了构造函数`Hero()`。这也就是说，这两个对象虽然有各自独立的属性，但却是基于同一个原型对象的产物，而这个原型对象正是它们的构造函数。另外，这个实验也间接证明了我们之前所说的：如果在构造函数中将对象的方法也定义在`this`引用上，就会让每个实体对象都拥有一份独立但相同的方法实现，这意味着，如果我们用构造函数创建一万个对象，同一个对象方法就会被重复实现一万次，这显然会造成代码冗余。所以，一个对象的方法实现应该被定义在其原型对象上，这样只要对象来自同一个原型对象，它们调用的就是同一份方法实现。

但我们都知道，其实构造函数本身在没有被`new`操作符调用之前只是一个普通函数，而在 JavaScript 中，函数本身也是一个对象，它又是如何在被`new`操作符调用时成为了其所创建对象的原型对象的呢？答案就是函数的`prototype`属性。在 JavaScript 中，为了让用户定义的函数都可以被当作构造函数来使用，每个由用户定义的函数都会有一个`prototype`属性。当这些函数被当作普通函数调用时，该属性是被忽略的，然而一旦它们被new操作符调用，该属性就会被初始化，并成为了其所创建对象的原型对象。例如，如果我们想为上面创建的`hero_1`和`hero_2`对象添加一个`sayHello`方法，又不想有代码冗余的问题，就可以接着上面的实验代码这样写：

```javascript
Hero.prototype.sayHello = function() {
    console.log('Hello,', this.name);
};                         // 在原型对象上添加方法

hero_1.sayHello();         // 输出： Hello, owlman
hero_2.sayHello();         // 输出： Hello, batman

Hero.prototype.sayHello = function() {
    console.log('你好,', this.name);
};                         // 修改原型对象上的方法
  
hero_1.sayHello();         // 输出： 你好, owlman
hero_2.sayHello();         // 输出： 你好, batman

hero_1.sayHello = function() {
    console.log(this.name, '不是英雄！');
};                         // 在 hero_1 对象上添加同名方法

hero_1.sayHello();         // 输出： owlman不是英雄！
hero_2.sayHello();         // 输出： 你好, batman

delete hero_1.sayHello;    // 删除 hero_1 上的同名方法

hero_1.sayHello();         // 输出： 你好, owlman
hero_2.sayHello();         // 输出： 你好, batman
```

如你所见，如果在构造函数的`prototype`属性上添加或修改方法的实现，会影响其创建的所有对象，而如果我们在某个实体对象上添加或修改方法的实现，不会影响到其他对象。另外，上面的代码也说明了一件事，即当一个对象实体的`this`引用上的方法与其原型对象上的方法同名时，JavaScript 解释器会优先调用`this`引用上的方法。这也是我们不赞成在构造函数中用`this`引用来定义对象方法的另一个原因，它会隐藏掉我们在原型对象上定义的方法。

#### 再探对象属性

<!-- 整理标记 -->
除了方法之外，属性也是可以被定义在原型对象上的。在 JavaScript 中，对象的属性按其拥有者可分为被定义在this引用上的自有属性和被定义在原型对象上的原型属性两种。对此，我们可以使用每个对象都拥有的hasOwnPrototype方法来判断一个属性是否为当前对象的自有属性。下面，让我们接着上面的实验继续往下写：
Hero.prototype.counter = 2;                     // 添加一个原型属性
console.log(hero_1.hasOwnProperty('name'));     // 输出： true
console.log(hero_1.hasOwnProperty('counter'));  // 输出： false
console.log(hero_1.name === hero_2.name);       // 输出： false
console.log(hero_1.counter === hero_2.counter)  // 输出： true
从上述实验的结果，我们可以看到：由于name属性是被构造函数定义在this引用上的，所以hero_1.hasOwnProperty('name')返回的是 true，而新增的counter属性则是被定义在Hero.prototype上的，所以hero_1.hasOwnProperty('counter')返回了 false。另外，对象的自有属性是彼此独立的，而原型属性则是该原型所创建的所有对象共同拥有的。所以在原型对象上添加属性需要格外小心，该属性会影响到该原型对象所创建的所有对象，包括在它被添加到原型对象之前所创建的对象。接下来，我们可以搭配用于枚举对象属性的for-in循环来看看hero_1对象中到底有哪些自有属性和原型属性：
for(property in hero_1) {
  if (hero_1.hasOwnProperty(property)) {
    console.log('自有属性：', property);
  } else {
    console.log('原型属性：', property);
  }
}
// 以上代码输出：
// 自有属性： name
// 原型属性： sayHello
// 原型属性： counter
如你所见，for-in循环的作用是遍历指定对象中所有可枚举的属性，程序会依次将hero_1对象中的元素读取到循环变量（即这里的property变量）中，然后交由hasOwnProperty方法来判断是否为自有属性。当然，在这里我们会发现一件有趣的事，那就是sayHello方法也会被当作属性被枚举了出来，这本身倒不难理解，毕竟它可以被看作是值为函数的属性。比较让人难以理解的是：既然对象方法也会被当作属性被列举出来，我们明明眼见hero_1对象调用了hasOwnProperty方法，为什么该方法却没有被列出来呢？事实上，这个问题涉及到了 JavaScript 中的最终原型对象Object，我们将会在下一节中详细介绍该对象。现在，读者先暂且只需要知道for-in循环遍历的是可枚举的属性，而来自Object中的原型属性都是不可枚举的。在 JavaScript 中，每个对象的属性都有属性值、可写性、可枚举性以及可配置性四个特性，它们分别对应着以下四个“属性描述符”：
- value：即属性的值，这个特性我们已经一直在使用了，它决定的是属性中存储的数据，默认值为 undefine 。
- writable：即属性是否可写，默认值为 true、如果将其设置为 false，该属性在初始化之后就不可再被修改了，请注意，这里的“不可修改”针对的是所有地方，包括该属性所在对象的方法，这与我们之前讨论的“让对象外部不能直接修改属性"不是一回事。
- enumerable：即属性是否可枚举，默认值为 true。如果将其设置为 false，该属性就不会被for-in循环遍历到。
- configurable：即属性是否可配置，默认值为 true。如果将其设置为 false，该属性在初始化之后其所有的特性，包括congfigurable特性本身，就都不可修改了。
如果我们想查看现有属性的特性配置，我们可以使用Object.getOwnPropertyDescriptor()方法来查看。例如，如果想查看上述实验中hero_1对象的name属性，我们就可以接着上面的代码这样写：
let msg = Object.getOwnPropertyDescriptor(hero_1, 'name');
console.log(msg);
// 以上代码输出：
// { value: 'owlman',
//   writable: true,
//   enumerable: true,
//   configurable: true }
在这里，我们需要传递给Object.getOwnPropertyDescriptor()方法两个实参：第一个实参是我们要查看属性所属的对象，第二个实参是该属性的名称，请注意，该名称必须用一个字符串来表示。需要说明的是，在通常情况下，我们在定义对象属性时只需要指定它的value即可，其它三个特性会被自动被赋予默认值。当然了，如果实在有特定的需求，我们也可以使用Object.defineProperty()方法来详细定义属性。换句话说，下面两种定义属性的方式在效果上是完全一致的：
hero_1.test = 'test';
console.log(hero_1.test);          // 输出： test
Object.defineProperty(hero_1,'test', { value: 'test',
                                       writable: true,
                                       enumerable: true,
                                       configurable: true });
console.log(hero_1.test);          // 输出： test
在这里，我们需要传递给Object.defineProperty()方法三个实参：第一个实参是我们要定义属性所属的对象；第二个实参是该属性的名称，该名称必须用一个字符串来表示；第三个实参是一个用于逐条指定该属性特性的对象直接量。从这里我们也可以看出，事实上每个对象的属性本身也是一个对象。除此之外，在configuration没有被设置为 false 的前提下，我们也可以用Object.defineProperty()方法来修改现有属性的特性。例如，如果我们不想让for-in循环遍历到test属性，就可以接着上面的代码这样写：
Object.defineProperty(hero_1,'test', { value: 'test',
                                       enumerable: true });
到目前为止，我们一直在对Hero()构造函数所创建的对象执行各种扩展、修改和缩减操作，充分展现了 JavaScript 对象的灵活性和自由度，但正如我们一直所强调的，享受自由的同时必须注意随之而来的风险。在某些情况下，如果我们觉得不能放任自己设计的对象像上面这样被调用方随意增加、修复甚至删除属性，就可以对这些行为进行禁止。在 JavaScript 中，禁止修改对象的方法有三个，下面我们就逐一来介绍一下它们。
首先，我们可以用Object.preventExtensions()方法将它们设置为不可扩展的对象。这时候，如果我们用Object.isExtensible()方法来查看它们的可扩展性，就会看到其返回 false 了。下面，我们就继续拿已经饱受折磨的hero_1对象来试一下：
console.log(Object.isExtensible(hero_1));  // 输出： true
Object.preventExtensions(hero_1);
console.log(Object.isExtensible(hero_1));  // 输出： false
hero_1.isbaby = true;
console.log(`isbaby` in hero_1); // 输出 false，证明操作失败
如你所见，isbaby属性已经不能被添加到hero_1中，如果声明为严格模式，上述代码还会直接报错，并被 JavaScript 解释器终止执行。需要提醒的是，Object.preventExtensions()方法执行的操作是不可逆的，hero_1一旦被设定为不可扩展，就不可能再被改回来了，所以对于这个操作，程序员在执行之前可要想好了。那么，hero_1现在是不是终于可以松口气，庆祝一下它被我们反复折腾的恶梦结束了呢？如果它真的这么想，那就太天真了。Object.preventExtensions()方法只能保证对象的自有属性不会再被扩展了，但我们仍然可以删除它的自有属性。例如，如果我们想删除之前添加的test属性，就可以这样做：
console.log(`test` in hero_1); // 输出 true，证明该属性目前存在
delete hero_1.test;
console.log(`test` in hero_1); // 输出 false，证明删除操作成功
然后，如果不想允许调用方删除对象的属性，我们还可以使用Object.seal()方法封印对象。同样地，在执行封印操作之后，我们可以用Object.isSealed()方法来验证封印是否成功。在一个对象被封印之后，它不但无法再扩展新的自有属性，现有的自有属性也会被设置为不可配置。这样一来，如果我们再想删除hero_1对象的name属性，操作就会失败：
console.log(Object.isSealed(hero_1)); // 输出： false
Object.seal(hero_1);
console.log(Object.isSealed(hero_1)); // 输出： true
console.log(`name` in hero_1); // 输出 true，证明该属性目前存在
delete hero_1.name;
console.log(`name` in hero_1); // 输出 true，证明删除操作失败
请注意，封印对象的操作也是不可逆的，对象一旦被封印就无法再解封了。现在，hero_1对象的自有属性不能被添加或删除，也无法再配置可写性和可枚举性了，但我们仍然可以修改它的name值。例如，我们可以接着上面的代码这样写：
hero_1.name = 'owlbaby';
hero_1.sayHello();         // 输出： 你好, owlbaby
这时候，hero_1对象的状态就基本类似于我们在 C++、Java 这些语言中使用的对象了，由此也可以看出 JavaScript 相对于这些传统的面向对象编程语言给予了程序员多大的自由度。当然，如果我们想彻底将hero_1设置成一个不可修改的对象，我们还可以使用Object.freeze(）方法冻结对象，同样地，在冻结了对象之后，我们可以使用Object.isFrozen()来验证操作是否成功。在hero_1对象被冻结之后，如果我们再想修改其name属性，操作就会无效，在严格模式下，JavaScript 解释器还会报错并终止执行：
console.log(Object.isFrozen(hero_1));  // 输出： false
Object.freeze(hero_1);
console.log(Object.isFrozen(hero_1));  // 输出： true
hero_1.name = 'owlman';
hero_1.sayHello();         // 输出 “你好, owlbaby”， 证明操作失败。
同样地，冻结对象也是不可逆的，一旦对象被冻结了，他就无法再被解冻。现在，hero_1可以稍微安心一点了，它被我们反复折腾的日子总算基本结束了。当然了，我们还是可以通过Hero.prototype来为其添加新的方法，但这个操作同时也会影响到hero_2和其他用Hero()构造函数创建的对象，甚至还包括继承了Hero.prototype原型的后续原型对象，以及它们所创建的对象，程序员们至少会更谨慎一些。为了让读者能对这一部分的操作做出合理的决策，我们接下来就要来详细介绍对象之间，原型之间的继承关系。
4.2.3 理解 Object 对象
细心的读者可能已经发现了，我们之前在介绍原型对象时，似乎遗漏了一个关键问题：既然 JavaScript 中的每个对象都有自己的原型对象，而用构造函数创建的对象的原型对象来自于其构造函数，那么充当构造函数的这些函数的原型对象是什么呢？这些原型对象的原型对象又是什么呢？以此类推的话，这个问题似乎可以一直问下去，但这显然是不现实的，所以我们可以推断出 JavaScript 所定义的世界中必定有一个最初的原型对象，所有对象的原型都来自于它，这个对象就是我们之前一直在使用，但还尚未做说明的Object对象，它的Object.prototype属性是 JavaScript 中所有对象的原型。如果我们用直接量创建一个对象，它的原型就是Object.prototype。对此，我们可以用以下方法来查看一下：
let machine = { name:'robot'}; // 用直接量创建对象
let prototype = Object.getPrototypeOf(machine);
console.log(prototype === Object.prototype); // 输出： true
这也就是说，当我们用直接量创建对象的时候，实际上就是调用了Object构造函数，即：
// 当我们这样写：
let machine = { name:'robot'};
// 就等同于：
let machine = new Object();
machine.name = 'robot';
在 JavaScript 中，Object是一个极为特殊的构造函数，它不但提供了可由 JavaScript 中所有对象调用的实例方法，还提供了一组只能由Object本身调用的静态方法。虽然我们之前或多或少都已经使用过这些方法了，但始终没有系统地介绍过它们。下面，就让我们来补上这一课。
实例方法：
Object构造函数提供的实例方法主要有六个，鉴于Object.prototype是 JavaScript 中所有对象的原型，这些方法应该可以被所有对象调用，下面是这些方法的具体介绍：
- hasOwnProperty(propertyName)方法： 用于判断其调用对象中是否有名为propertyName的自由属性，是就返回 true，不是则返回 false。例如，对于上面的machine对象，我们可以这样：
 	console.log(machine.hasOwnProperty('name'));
// 输出： true
- propertyIsEnumerable(propertyName)方法： 用于判断其调用对象的propertyName属性是否属于可枚举属性，是就返回 true，不是则返回 false。例如，对于上面的machine对象，我们可以这样：
 	console.log(machine.propertyIsEnumerable('name'));
// 输出： true
- isPrototypeOf(object)方法： 用于判断其调用对象是否为object对象的原型对象，是就返回 true，不是则返回 false。例如，对于上面的machine对象，我们可以这样：
 	console.log(Object.prototype.isPrototypeOf(machine));
// 输出： true
- toString()方法： 用于返回其调用对象的、被本地化了的字符串描述。例如：
 	let arr = [1, 2, 3];
console.log(arr.toString()); // 输出： 1,2,3
- toLocaleString()方法： 用于以用户所在系统设置的语言返回其调用对象的字符串描述。例如：
 	let date = new Date();
console.log(date.toLocaleString());
// 输出： 2019/10/6 下午3:26:21
- valueOf()方法： 用于返回其调用对象的原始值。例如：
 	let arr = [1, 2, 3];
console.log(arr.valueOf());  // 输出：  [ 1,2,3 ]
静态方法：
Object的静态方法指的是只能由Object自身作为一个实体来调用的方法，这些方法主要用于更细致、更精确地创建、使用和修改 JavaScript 中的对象。下面是这些方法的具体介绍：
- Object.assign(target, ...sources)方法： 用于将sources指定的一个或多个对象复制到target对象中，并将其作为一个新创建的对象返回。在复制过程中，如果target对象与sources对象有同名属性，后者的属性会覆盖前者。如果sources中的多个对象有同名属性，则靠后出现的属性会覆盖前面的属性。
 	需要提醒的是，Object.assign()方法执行的是浅拷贝而非深拷贝，所以如果sources对象中的某个属性值是对象类型的，那么target对象得到的是该属性值的引用，例如：
 	let obj_1 = { x: { num: 1 } };
let obj_2 = Object.assign({}, obj_1);
console.log(obj_2.x.num); // 输出： 1
obj_1.x.num = 2;
console.log(obj_2.x.num); // 输出： 2
- Object.create(prototype，propertyDescriptor)方法： 用于以prototype指定的对象为原型创建一个对象，并赋予其用propertyDescriptor描述的属性。该方法有利于我们更精确地创建一个对象，例如：
 	// 对于下面这个对象：
let machine = { name:'robot'};
// 我们也可以这样定义：
let machine = Object.create(Object.prototype,{
  name: {
      value: 'robot',
      writable: true,
      enumerable: true,
      configurable: true
  }
});
- Object.defineProperty(target, propertyDescriptor)方法： 用于将propertyDescriptor描述的属性添加到target对象中，如果该属性已经存在，就覆盖它。由于我们之前已经演示过该方法的使用，这里就不再举例了。
- Object.defineProperties(target, propertyDescriptor)方法： 用于将propertyDescriptor描述的多个属性添加到target对象中，如果这些属性已经存在，就覆盖它们。例如：
 	Object.defineProperties(machine,{
  name: {
      value: 'robot',
      writable: true,
      enumerable: true,
      configurable: true
  },
  cpu: {
      value: 'i5',
      writable: true,
      enumerable: true,
      configurable: true
  }
});

console.log(machine.name, machine.cpu); // 输出 robot i5
- Object.entries(target)方法： 用于以键/值对数组的形式返回target对象的可枚举属性。例如，对于上面的machine对象，我们可以这样查看它的可枚举属性：
 	console.log(Object.entries(machine));
// 输出： [ [ 'name', 'robot' ], [ 'cpu', 'i5' ] ]
- Object.keys(target)方法： 用于以数组的形式返回target对象中可枚举属性的名称。例如，对于上面的machine对象，我们可以这样：
 	console.log(Object.keys(machine));
// 输出： [ 'name', 'cpu' ]
- Object.values(target)方法： 用于以数组的形式返回target对象中可枚举属性的值。例如，对于上面的machine对象，我们可以这样：
 	console.log(Object.values(machine));
// 输出 [ 'robot', 'i5' ]
- Object.getOwnPropertyDescriptor(target， propertyName)方法： 用于获取target对象的propertyName属性的具体描述。例如，对于上面的machine对象，我们可以这样：
 	console.log(Object.getOwnPropertyDescriptor(machine,'name'));
// 以上代码输出：
// { value: 'robot',
//   writable: true,
//   enumerable: true,
//   configurable: true }
- Object.getOwnPropertyNames(target)方法： 用于以一个字符串数组的形式返回target对象中所有自有属性的名称。例如，对于上面的machine对象，我们可以这样：
 	console.log(Object.getOwnPropertyNames(machine));
// 以上代码输出： [ 'name', 'cpu' ]
- Object.getOwnPropertySymbols(target)方法： 用于以一个数组的形式返回target对象自身所有的符号属性。由于我们目前还没有介绍 ES6 新增的Symbols对象，暂时就先不举例了。
- Object.getPrototypeOf(target)方法： 用于返target对象的原型对象。由于我们之前已经演示过该方法的使用，这里就不再举例了。
- Object.setPrototypeOf(target, prototype)方法： 用于将target对象的原型设置为prototype。例如，对于上面的machine对象，我们可以这样：
 	Object.setPrototypeOf(machine, Hero.prototype);
 	关于修改现有对象的原型，我们稍后还会做详细讨论。
- Object.preventExtensions(target)方法： 用于关闭target对象的可扩展性，该操作是不可逆的。由于我们之前已经演示过该方法的使用，这里就不再举例了。
- Object.isExtensible(target)方法： 用于判断target对象的可扩展性，其返回 false 就代表target对象不可扩展了。由于我们之前已经演示过该方法的使用，这里就不再举例了。
- Object.seal(target)方法： 用于封印target对，防止其他代码删除对象的属性，这也是个不可逆的操作。由于我们之前已经演示过该方法的使用，这里就不再举例了。
- Object.isSealed(target)方法： 用于判断target对象是否已经封印，其返回 true 就代表target对象已被封印。由于我们之前已经演示过该方法的使用，这里就不再举例了。
- Object.freeze(target)方法： 用于冻结target对象，使得其他代码不能添加、删除或更改该任何对象属性，这也是个不可逆的操作。由于我们之前已经演示过该方法的使用，这里就不再举例了。
- Object.isFrozen(target)方法： 用于判断target对象是否已经冻结，其返回 true 就代表target对象已被冻结。由于我们之前已经演示过该方法的使用，这里就不再举例了。
4.3 原型继承机制
正如我们在 4.1 节中所介绍的，我们之所以要用继承现有类的方式来创建一个新的类，主要是因为想让新建的类共享现有类的接口及其部分实现。而在没有引入类定义语法之前，JavaScript 中的继承关系是以原型链的形式来呈现的。
4.3.1 理解原型链
以我们之前使用的hero_1对象为例，它的原型是Hero.prototype，而Hero.prototype的原型则是Object.prototype，这是 JavaScript 中的最终原型。在 JavaScript 中，这一连串的原型就被称作hero_1对象的“原型链”。换而言之，hero_1对象从一开始就已经位于一组继承关系中了，它既可以调用Hero.prototype中定义的接口与实现，也共享了Object.prototype中定义的接口与实现。例如，下面用hero_1对象来调用Object对象的实例方法：
console.log(hero_1.toString());       // 输出： [object Object]
console.log(hero_1.valueOf());        // 输出： Hero { name: 'owlman' }
console.log(hero_1.toLocaleString()); // 输出： [object Object]
如你所见，hero_1对象也可以调用Object对象的实例方法，所以可以认为是Hero()构造函数在定义其原型的同时，"继承"了Object()构造函数定义的原型。为了便于理解，我们在某些情况下可以将Object()构造函数“看作”是Hero()构造函数的“父类”。但与此同时，读者心里必须要清楚，这种类比并不完全符合事实，构造函数至始至终都是一个有实体存在的“对象”，而不是一个代表了对象模版的“类”，这些概念在技术上这是不能混淆的。也就是说，在 JavaScript 中，继承关系是直接发生在对象与对象之间的，这与我们所熟悉的 C++、Java 这些传统的面向对象语言有很大的不同。
当然，在这里Hero对象继承Object对象的动作是由 JavaScript 语言机制自动完成的，下面我们以手动调整继承关系的方式来展示一下原型链机制的灵活性。想必大家还记得之前使用的machine对象吧？它是一个用Object()构造函数定义的对象。现在，我们来改变一下它在原型链中的位置，使其变成一个由Hero()构造函数定义的对象，该怎么办呢？答案很简单，只需要将machine对象的原型设置成Hero.prototype即可，我们可以接着上面的代码这样写：
// 之前的定义：let machine = { name:'robot'};
Object.setPrototypeOf(machine, Hero.prototype);
// 调用 Hero.prototype 上的方法：
machine.sayHello();                    // 输出： 你好 robot
// 调用 Object.prototype 上的方法：
console.log(machine.toString());       // 输出： [object Object]
console.log(machine.valueOf());        // 输出： Hero { name: 'robot' }
console.log(machine.toLocaleString()); // 输出： [object Object]
是的，这里看起来会有些奇怪，我们没有创建新的对象，只是调整了一下现有对象的原型，就改变了它的数据类型。也就是说，从类型的概念上来说，machine对象现在由Object对象变成了一个Hero对象，而后者是前者的“子类”。这就是 JavaScript 的灵活性，这种自由度在 C++、Java 这些语言中是很难想象的。
下面，让我们稍微回归一下传统，既然构造函数在 JavaScript 中充当了“类”的角色，那么下面就来看看如何模拟传统的面向对象编程，基于现有的“类”来创建新的“类”。毕竟我们刚才直接让一个machine实体变成了一个Hero“类”的对象，怎么看都有些粗鲁。下面，我们来设计一个能创建机器英雄的“类”，它想必应该是个AI_Hero“类”，其定义代码如下：
function AI_Hero(name) {
  this.name = name;
}
AI_Hero.prototype = new Hero();
如你所见，如果我们想让AI_Hero继承自Hero，只需要正常定义一个名为AI_Hero的构造函数，然后将该构造函数的prototype属性设置为一个Hero实体即可。请注意，在这里构建Hero对象是不必传递实参的，因为在AI_Hero所在作用域中，this是引用不到Hero对象的实体属性的。换句话说，在用原型链实现的继承机制中，只有被定义在prototype中的东西。下面，让我们用AI_Hero构造函数重新构建一个machine对象，看看效果是否符合我们对继承的预期：
let machine = new AI_Hero('Machine');
// 调用 Hero.prototype 上的方法：
machine.sayHello();                    // 输出： 你好， Machine
// 调用 Object.prototype 上的方法：
console.log(machine.toString());       // 输出： [object Object]
console.log(machine.valueOf());        // 输出： Hero { name: 'Machine' }
console.log(machine.toLocaleString()); // 输出： [object Object]
4.3.2 剥开语法糖
那么，现在的问题是 ES6 所带来的类定义与继承语法是否改变了 JavaScript 对于继承机制的实现呢？为了说明这个问题，下面我们将找回在 4.1 节中所使用的Point类与colorPoint类，并对它们进行一些分析：
// 类设计
class Point {
  constructor(x,y) {
    this._x = x;
    this._y = y;
  }

  printCoords() {
    console.log('坐标：（'+ this._x + ', ' + this._y + '）');
  }

  updateCoords(x,y) {
    if ((x<0) || (y<0)) {
      console.log('坐标不能为负值！');
      return false;
    }
    this._x = x;
    this._y = y;
  }
};

class colorPoint extends Point {
  constructor(x,y,color) {
    super(x,y);
    this._color = color;
  }

  updateColor(color) {
    this._color = color;
  }

  printCoords() {
    super.printCoords();
    console.log('颜色：', this._color);
  }

  testSuper() { // 临时新增方法：验证super是否为父类的prototype
    Point.prototype.temp = 10;
    console.log(super.temp);
  }
}

// 先来看看“类”在 JavaScript 中的实际数据类型：
console.log(typeof(Point));          // 输出： function
console.log(typeof(colorPoint));     // 输出： function

// 再来看看两者之间是否属于原型继承：：
let proto = Object.getPrototypeOf(colorPoint);
console.log(proto === Point);        // 输出： true

// 最后再来看看子类的super引用的是不是父类的prototype：
const p = new colorPoint(5,5,'红');
p.testSuper();                       // 输出： 10
如你所见，我们首先用typeof查看了Point和colorPoint的实际数据类型，得知了它们都是函数。然后，我们用Object.getPrototypeOf()方法证实了这两个类之间依然是原型继承的关系。最后，我们为colorPoint类临时新增了一个testSuper()方法。在其中，我们先在Point.prototype上添加了一个临时变量temp，然后用super读取到了该变量的值。这证明了子类的super引用的正是父类的prototype，这就解释了为什么super不能引用父类对象的自有属性（如super._x）。
从上述分析结果，我们可以得出一个结论：ES6 新增的语法并没有改变该语言用原型链实现继承机制的事实。换句话说，ES6 提供类定义与继承语法的目的仅仅是为程序员们提供一种类似于使用传统面向对象编程语言的体验，我们通常将这些在语法上提供便利，但并不改变内部实现的语言特性称之为“语法糖”。在理解语法糖的作用之后，我们就可以更灵活地使用 ES6 提供的语法了。例如，之前为了私有化部分数据，将自有属性定义成了构造函数的局部变量。相应地，为了让对象方法能访问这些私有数据，它们也必须在构造函数内定义。但想必大家都还记得，我们当时遇到了一个麻烦：这些对象方法都被定义在了this上，这不仅带来了代码冗余，而且让它的子类无法继承父类的方法。现在，我们知道了 JavaScript 的继承机制依然是用原型链实现的，所以只需要将这些方法定义在Point.prototype上即可：
class Point {
  constructor(x,y) {
    let _x = x;
    let _y = y;
  
    Point.prototype.printCoords = function() {
      console.log('坐标：（'+ _x + ', ' + _y + '）');
    };
  
    Point.prototype.updateCoords = function(x,y) {
      if ((x<0) || (y<0)) {
        console.log('坐标不能为负值！');
        return false;
      }
      _x = x;
      _y = y;
    };
  }  
};

class colorPoint extends Point {
  constructor(x,y,color) {
    super(x,y);
    this._color = color;
  }

  updateColor(color) {
    this._color = color;
  }

  printCoords() {
    super.printCoords();
    console.log('颜色：', this._color);
  }
}

// 接下来逐个测试方法的调用
const p = new colorPoint(5,5,'红');
p.printCoords();         // 输出： 坐标：（5,5）
                         //       颜色：红
p.updateCoords(10,10);
p.updateColor('绿');
p.printCoords();         // 输出： 坐标：（10,10）
                         //       颜色：绿

现在，colorPoint类对象的方法就可以通过super调用Point类定义的方法了。当然，需要提醒读者的是，在享受 JavaScript 赋予我们的自由度之前，需要先对自己所做的事有所把握。毕竟，类定义与继承语法在 JavaScript 中的出现是经历了很多年的呼吁的，所以我们虽然在原则上鼓励读者去了解这种语法背后的实现机制，但并不鼓励轻易破坏或绕过它。

## 异步编程
