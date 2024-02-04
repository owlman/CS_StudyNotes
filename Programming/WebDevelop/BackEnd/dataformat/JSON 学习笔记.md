# JSON 学习笔记

JSON 是 JavaScript Object Notation 这个专有名词的缩写形式，从字面上理解，这就是一种 JavaScript 对象的表示方法。由于这种表示方法在描述结构化数据时使用的是 JavaScript 中的一些语法格式，这使得它看起来比 XML 这种传统的结构化数据格式更为简洁明了，也更易于解析，所以 JSON 更多时候被当做一种描述结构化数据的格式，常用于执行一些轻量级的数据交换任务。需要特别说明的是，JSON 数据并不是只可以在 JavaScript 中被使用，Java、Python、C# 等多种编程语言也都支持该数据格式的序列化与解析，它如今与 XML 一样，已经成为了一种描述结构化数据的通用格式。

但从语法上来说，JSON 数据的格式仍然可被认为是 JavaScript 语法中字面量表示法的一个子集，它可以描述的数据只有简单值、对象和数组三种类型，下面我们就逐一来做个说明：

- **简单值**：这种类型的 JSON 数据通常只有一个单值，该值可以是数字、字符串、布尔值或 null，但不能是 JavaScript 中的 undefined 值。当然，在实际应用中，我们很少会需要动用 JSON 格式来描述一个单值，它更多时候是作为后两种复杂类型的基础而存在的。

- **对象**：这种类型的 JSON 数据的描述语法与一般 JavaScript 对象的字面直接量是非常相似的，都是被一个大括号括住的一系列键/值对，例如：

    ```JSON
    {
        "name" : "owlman",
        "age"  : 40
    }
    ```

  但如果仔细观察，还是会发现 JSON 格式描述的对象与用字面直接量描述的 JavaScript 对象之间还是有两点重要区别的。第一，JSON 对象的属性名必须要用双引号括起来，第二，JSON 对象的属性值同样只能是 JSON 格式可描述的简单值、对象或数组，不能是 JavaScript 中的函数、原型对象或 undefined 值。

- **数组**：这种类型的 JSON 数据的描述语法与一般 JavaScript 数组的字面直接量也非常相似，都是被一个中括号括住的一组值，这组值可以是一组 JSON 格式的简单值，例如：

    ```JSON
    ["owlman", 40, false, null]
    ```

  也可以是 JSON 格式的对象，例如：

    ```JSON
    [
        {
            "name" : "owlman",
            "age"  : 40
        },
        {
            "name" : "batman",
            "age"  : 45
        },
        {
            "name" : "superman",
            "age"  : 42
        }
    ]
    ```

  甚至可以是另一个 JSON 格式的数组，但同样不能是 JavaScript 中的函数、原型对象或 undefined 值。

当然，这些语法只是用于描述结构化数据，但数据本身在程序的输入/输出是以字符串的形式存在的。对此，我们可以写一个脚本验证一下，首先，我们需要在之前用于存放示例代码的`code`目录下创建一个名为`data`的目录，并在其中创建一个名为`hero.json`的文件，该文件的内容如下：

```JSON
[
    {
        "name" : "owlman",
        "age"  : 40
    },
    {
        "name" : "batman",
        "age"  : 45
    },
    {
        "name" : "superman",
        "age"  : 42
    }
]
```

然后在之前用于测试代码的`code/03_web/03-test.js`脚本文件中这样调用我们之前封装的`ajax_get()`函数：

```JavaScript
ajax_get('../data/hero.json', function(data) {
    console.log(typeof data); // 输出：string
    console.log(data);        // 输出内容与 hero.json 文件的内容一致
});
```

在通过`03-test.htm`文件执行上述代码之后。我们就可以看到`data`的数据类型是字符串，且其内容是一段与`hero.json`文件内容相同的 JSON 格式的数据，具体如下图所示：

![查看响应数据的类型及其内容](./img/10-1.png)

所以，要想在浏览器端用 JavaScript 脚本对 JSON 数据进行处理，首先要将从服务器输入的包含数据内容的字符串**解析**成 JavaScript 中相应类型的对象，以便进一步处理，然后在处理数据之后，又要将相应的 JavaScript 对象重新**序列化**成用于描述 JSON 数据的字符串，以便输出给服务器。为了方便解决这些问题，ECMAScript 规范为我们定义了一个名为 JSON 的全局对象，专用于解析和序列化 JSON 字符串，它主要提供了以下两个方法：

- **`parse()`方法**：该方法的作用是将包含 JSON 数据的字符串解析成 JavaScript 中相应类型的对象。在大多数情况下，我们在调用该方法时只需要提供那个要解析的目标字符串作为实参即可。例如，我们可以像下面这样修改之前对`ajax_get()`函数的调用：

    ```JavaScript
    ajax_get('../data/hero.json', function(data) {
        console.log(typeof data); // 输出：string
        console.log(data);        // 输出内容与 hero.json 文件的内容一致
        const hero = JSON.parse(data);
        console.log(typeof hero); // 输出：object
        for(const item of hero) {
            console.log(item.name + ':' + item.age);
        }
        // 以上循环输出：
        // owlman:40
        // batman:45
        // superman:42
    });
    ```

  在通过`03-test.htm`文件执行上述代码之后。我们就可以看到`data`字符串被解析成了一个可在 JavaScript 中被遍历的数组对象，具体如下图所示：

  ![解析响应数据](./img/10-2.png)

  另外，在特定需求下，我们有时候还会在提供要解析的目标字符串外，还会额外提供一个回调函数作为实参，用于排除一些数据或修改一些数据被解析的方式。在专业术语上，我们通常将这个回调函数称之为“还原函数”，他设置有两个形参，分别用于接收键和值。例如在下面的代码中，如果我们不希望解析 JSON 数据中的`age`属性，就可以这样做：

    ```JavaScript
    const jsonData = `
        {
            "name" : "owlman",
            "age"  : 40
        }`;

    const jsObj = JSON.parse(jsonData, function(key, value) {
        if(key == 'age') {
            return undefined;
        } else {
            return value;
        }
    });

    console.log(jsObj.name); // 输出：owlman
    console.log(jsObj.age);  // 输出：undefined
    ```

  如果执行了上述代码，我们就会看到`jsonData`字符串中 JSON 数据在被解析成`jsObj`对象后，`age`属性的值变成了 undefined。

- **`stringify()`方法**：该方法的作用是将 JavaScript 中的对象数据序列化成字符串类型的 JSON 数据。同样地，在大多数情况下，我们在调用该方法时只需要提供要序列化的 JavaScript 对象作为实参即可，例如像这样：

    ```JavaScript
    const TCPL_Book = {
        title   : 'The C Programmming Language',
        authors : [
            'Brian W.Kernighan',
            'Dennis M.Ritchie'
        ]
    };

    const jsonData = JSON.stringify(TCPL_Book);
    console.log(jsonData);
    ```

  如果执行了上述代码，我们就会看到`TCPL_Book`对象被序列化成了如下内容的字符串：

    ```JSON
    {"title":"The C Programmming Language","authors":["Brian W.Kernighan","Dennis M.Ritchie"]}
    ```

  需要注意的是，在 JavaScript 对象被序列化的过程中，值为函数、原型对象或 undefined 的属性将会被忽略。并且，在特定情况下，我们也可以在提供被序列化的目标对象之外，再提供一个用于排除一些数据或修改一些数据被序列化的方式的实参。在专业术语上，我们称这个实参为“过滤器”，它可以有两种形式，如果是一个数组，那么就只有在该数组中列出的属性会被序列化。例如，如果我们将上面的代码修改成这样：

    ```JavaScript
    const TCPL_Book = {
        title   : 'The C Programmming Language',
        authors : [
            'Brian W.Kernighan',
            'Dennis M.Ritchie'
        ]
    };

    const jsonData = JSON.stringify(TCPL_Book,['title']);
    console.log(jsonData);
    ```

  就会看到其序列化结果中已经没有“authors”属性的数据了。而如果“过滤器”实参是个回调函数，那么该回调函数的用法与`parse()`方法的“还原函数”相似，可以改变一些数据被序列化的方式。例如，如果我们希望“authors”属性的数据被序列化之后的结果是个字符串，而不再是个数组，就可以将上述代码修改成这样：

    ```JavaScript
    const TCPL_Book = {
        title   : 'The C Programmming Language',
        authors : [
            'Brian W.Kernighan',
            'Dennis M.Ritchie'
        ]
    };

    const jsonData = JSON.stringify(TCPL_Book, function(key, value) {
        if(key == 'authors') {
            return value.join(', ');
        } else {
            return value;
        }
    });
    console.log(jsonData);
    ```

  在重新执行脚本之后，就会看到`jsonData`字符串的内容变成了这样：

    ```JSON
    {"title":"The C Programmming Language","authors":"Brian W.Kernighan, Dennis M.Ritchie"}
    ```

  另外，为了便于数据的网络传输，默认情况下的序列化结果是不带任何用于缩进或换行的空白符的。如果出于某种考虑，希望序列化的结果能带有缩进或换行的话，我们还可以在调用`stringify()`方法时提供第三个实参。用它来指定缩进的方式，如果该实参传递的是数字，代表的就是缩进所用的空格数，如果该实参传递的是一个字符串，那么序列化的结果就会用该字符串来进行缩进，并且，序列化过程也会在缩进的同时按照属性进行自动换行。例如，如果我们将上面对`stringify()`方法的调用改成这样：

    ```JavaScript
    const jsonData = JSON.stringify(TCPL_Book, function(key, value) {
        if(key == 'authors') {
            return value.join(', ');
        } else {
            return value;
        }
    }, 4);
    ```

  在重新执行脚本之后，就会看到`jsonData`字符串的内容变成了这样：

    ```JSON
    {
        "title": "The C Programmming Language",
        "authors": "Brian W.Kernighan, Dennis M.Ritchie"
    }
    ```
