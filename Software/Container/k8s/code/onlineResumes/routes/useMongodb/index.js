// 引入 mongodb 扩展包
const { MongoClient } = require('mongodb');
// 设置数据库所在的服务器连接地址和端口号
const serverUrl = 'mongodb://localhost:27017';
// 设置要使用的数据库名称
const databaseName = 'online_resumes';
// 创建数据库的连接对象
const client = new MongoClient(serverUrl);

// 创建当前模块要导出的 API 对象
const MongodbApi = {
    openCollect : async function(collectName) {
        try {
            if(typeof this.conn == 'undefined') {
                this.conn = await client.connect();
                console.log('数据库连接成功！' );  
            }
            if(typeof this.collect == 'undefined' || 
                this.collect.collectName !== collectName) {
                    const db = this.conn.db(databaseName);
                    this.collect = await db.collection(collectName);
                }
        } catch(error) {
            console.log('数据库连接错误：' + error);  
        }
    },

    // 创建用于向指定数据集中插入数据的 API
    insert : async function(collectName, jsonData) {
        try {
            await this.openCollect(collectName);
            const index = await this.collect.count({}) -1;
            const end = await this.collect.find({}).toArray();
            if(index < 0) {
                jsonData['uid'] = 1;
            } else if(collectName == 'users') {
                jsonData['uid'] = end[index] .uid+ 1;
            } else {
                jsonData['cv_id'] = end[index].cv_id+ 1;
            }
            await this.collect.insertOne(jsonData);
            return true;
        } catch(error) {
            console.log('数据插入错误：' + error);  
            return false;
        };
    },
    
    // 创建用于查看指定数据集中所有数据的 API
    getAll : async function(collectName) {
        try {
            await this.openCollect(collectName);
            const result = await this.collect.find({}).toArray();
            return result;
        } catch(error) {
            console.log('数据查询错误：' + error);  
            return false;
        }
    },

    // 创建用于向指定数据集中查询指定编号的数据的 API
    getDataById : async function(collectName, id) {
        try {
            await this.openCollect(collectName);
            const key = collectName == 'users' ? 'uid' : 'cv_id';
            const result =
                await this.collect.find({[key] : Number(id)}).toArray();
            return result;
        } catch(error) {
            console.log('数据查询错误：' + error);  
            return false;
        }
    },

    // 该 API 用于验证用户的登录权限
    // 登录成功时返回该用户的数据
    checkUser : async function(userData) {
        try {
            await this.openCollect('users');
            const result = await this.collect.find(userData).toArray();
            return result;
        } catch(error) {
            console.log('数据查询错误：' + error);  
            return false;
        }
    },

    // 创建用于根据获取同用户简历数据的 API
    getResumeByUID : async function(uid) {
        try {
            await this.openCollect('resumes');
            const result = await this.collect.find({
                'uid' : Number(uid)
            }).toArray();
        return result;
        } catch(error) {
            console.log('数据查询错误：' + error);  
            return false;
        }
    },

    // 创建用于在指定数据集中修改指定数据的 API
    update : async function(collectName, id, jsonData) {
        try {
            await this.openCollect(collectName);
            const key = collectName == 'users' ? 'uid' : 'cv_id';
            await this.collect.updateOne({[key] : Number(id)}, 
                                                            {$set : jsonData});
            return true;
        } catch(error) {
            console.log('数据修改错误：' + error);  
            return false;
        }
    },

    // 创建用于在指定数据集中删除指定数据的 API
    delete : async function(collectName, id) {
        try {
            await this.openCollect(collectName);
            const key = collectName == 'users' ? 'uid' : 'cv_id';
            await this.collect.deleteOne({[key] : Number(id)});
            return true;
        } catch(error) {
            console.log('数据删除错误：'+error);  
            return false;
        }
    },

    // 创建用于清理数据库连接的 API
    clean : async function() {
        try {
            await client.close();
        } catch (error) {
            console.log('数据库关闭错误：'+error);  
        }
    }
}

module.exports = MongodbApi;

// 以下为测试代码
// async function testAPI(dbApi) {
//     try { 
//         // 测试插入数据
//         await dbApi.insert('resumes',{
//             "cv_id": 202202042,
//             "name":"张三",
//             "gender":"男",
//             "age":"25",
//             "email":"zhangsan@zhangshanmail.com",
//             "phone":"72444441111",
//             "Education": [
//                 {
//                     "school":"浙江大学",
//                     "major":"计算机科学与技术",
//                     "degree":"硕士",
//                     "graduation":"2014"
//                 }
//             ],
//             "professional": [
//                 {
//                     "company":"微软公司",
//                     "title":"软件测试工程师",
//                     "startingDate":"2015",
//                     "endingDate":"2017"
//                 }
//             ]
//         });

//         // 测试查询数据
//         await dbApi.getAll('resumes')
//         .then(function(re) {
//             console.log(re);
//         });

//         await dbApi.delete('resumes' , '202202042');
//     } finally {
//         await dbApi.clean();
//     }
// }
// testAPI(MongodbApi)
