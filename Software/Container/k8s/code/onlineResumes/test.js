// 引入 mongodb 扩展包
const { MongoClient } = require('mongodb');
// 设置数据库所在的服务器连接地址和端口号
const serverUrl = 'mongodb://localhost:27017';
// 设置要使用的数据库名称
const databaseName = 'online_resumes';
// 创建数据库的连接对象
const client = new MongoClient(serverUrl);

// 测试数据库是否可用
// async function test() {
//     try {
//         await client.connect();
//         const db = client.db(databaseName);
//         const collect = db .collection('users');
//         console.log('数据库连接成功！');
//     } catch(error) {
//         console.log('数据库连接错误：' + error);  
//     } finally {
//         await client.close();  
//     }
// }
// test()

// 创建当前模块要导出的 API 对象
const MongodbApi = {};

// 创建用于向指定数据集中插入数据的 API
MongodbApi.insert = async function(collectName, jsonData) {
    try {
        await client.connect();
        const db = client.db(databaseName);
        const collect = db .collection('users');
        await collect.insertOne(jsonData);
        console.log('数据库连接成功！' );  
        return true;
    } catch(error) {
        console.log('数据库连接错误：' + error);  
        return false;
    } finally {
        // 关闭数据库连接
        await client.close();  
    }
}

// 创建用于查看指定数据集中所有数据的 API
MongodbApi.getAll = async function(collectName) {
    try {
        await client.connect();
        const db = client.db(databaseName);
        const collect = db .collection('users');
        const result = await collect.find({});
        // console.log(await result.toArray());
        console.log('数据库连接成功！' );  
        return await result.toArray();
    } catch(error) {
        console.log('数据库连接错误：' + error);  
        return false;
    } finally {
        // 关闭数据库连接
        await client.close();  
    }
};

// 创建用于向指定数据集中查询指定编号的数据的 API
MongodbApi.getDataById = async function(collectName, id) {
    try {
        await client.connect();
        const db = client.db(databaseName);
        const collect = db .collection('users');
        const result = await collect.find({'cv_id' : Number(id)}).toArray();
        console.log('数据库连接成功！' );  
        return result;
    } catch(error) {
        console.log('数据库连接错误：' + error);  
        return false;
    } finally {
        // 关闭数据库连接
        await client.close();  
    }
};

// 创建用于根据姓名获取个人简历主数据的 API
MongodbApi.getResumeByName = async function(name) {
    try {
        await client.connect();
        const db = client.db(databaseName);
        const collect = db .collection('users');
        const result = await collect.find({'name' : name}).toArray();
        console.log('数据库连接成功！' );  
        return result;
    } catch(error) {
        console.log('数据库连接错误：' + error);  
        return false;
    } finally {
        // 关闭数据库连接
        await client.close();  
    }
};

// 创建用于在指定数据集中修改指定数据的 API
MongodbApi.update = async function(collectName, id, jsonData) {
    try {
        await client.connect();
        const db = client.db(databaseName);
        const collect = db .collection('users');
        await collect.updateOne({'cv_id' : Number(id)}, {$set : jsonData});
        console.log('数据库连接成功！' );  
        return true;
    } catch(error) {
        console.log('数据库连接错误：' + error);  
        return false;
    } finally {
        // 关闭数据库连接
        await client.close();  
    }
};

// 创建用于在指定数据集中删除指定数据的 API
MongodbApi.delete = async function(collectName, id) {
    try {
        await client.connect();
        const db = client.db(databaseName);
        const collect = db .collection('users');
        await collect.deleteOne({'cv_id' : Number(id)});
        console.log('数据库连接成功！' );  
        return true;
    } catch(error) {
        console.log('数据库连接错误：'+error);  
        return false;
    } finally {
        // 关闭数据库连接
        await client.close();  
    }
};

module.exports = MongodbApi;

async function testAPI(dbApi) {
    try { 
        // 测试插入数据
        await dbApi.insert('resumes',{
            "cv_id": 202202042,
            "name":"张三",
            "gender":"男",
            "age":"25",
            "email":"zhangsan@zhangshanmail.com",
            "phone":"72444441111",
            "Education": [
                {
                    "school":"浙江大学",
                    "major":"计算机科学与技术",
                    "degree":"硕士",
                    "graduation":"2014"
                }
            ],
            "professional": [
                {
                    "company":"微软公司",
                    "title":"软件测试工程师",
                    "startingDate":"2015",
                    "endingDate":"2017"
                }
            ]
        });

        // 测试查询数据
        await dbApi.getAll('resumes')
        .then(function(re) {
            console.log(re);
        });

        await dbApi.delete('resumes' , '202202042');
    } finally {
        await client.close();
    }
}

testAPI(MongodbApi)
