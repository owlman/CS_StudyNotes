// 引入 Knex.js 框架文件
const knex = require('knex');
// 创建数据库连接对象
const MyDB = knex({
    client: 'mysql',         // 指定knex要操作的数据库为MySQL
    connection: {
        host : '127.0.0.1',    // 设置数据库所在的服务器地址
        user : 'your_username', // 设置你登录数据库的用户名
        password : 'your_password',// 设置你登录数据库的密码
        database : 'online_resumes' // 设置要操作的数据库名称
    },
    pool: 6 // 设置数据库连接池的大小
});

// 如果 users 表不存在就创建它
MyDB.schema.createTableIfNotExists('users', function(table) {
    table.increments('uid').primary();  // 将 uid 设置为自动增加的整数类型的主键字段
    table.string('userName');               // 将 userName 设置为字符串类型的字段
    table.string('password');                // 将 password 设置为字符串类型的字段
    table.string('resumes');                  // 将 resumes 设置为字符串类型的字段
});

// 如果 resumes 表不存在就创建它
MyDB.schema.createTableIfNotExists('resumes', function(table) {
    table.increments('cv_id').primary();// 将 cv_id 设置为类型为 bigInt 的主键字段
    table.bigInteger('uid');                   // 将 uid 设置为 bigInt 类型的字段
    table.string('name');                      // 将 name 设置为字符串类型的字段
    table.string('gender');                   // 将 gender 设置为字符串类型的字段
    table.string('age');                         // 将 age 设置为字符串类型的字段
    table.string('phone');                    // 将 phone 设置为字符串类型的字段
    table.string('email');                      // 将 email 设置为字符串类型的字段
    table.string('education');               // 将 education 设置为字符串类型的字段
    table.string('professional');            // 将 professional 设置为字符串类型的字段
});

// 如果 education 表不存在就创建它
MyDB.schema.createTableIfNotExists('education', function(table) {
    table.bigInteger('edu_id').primary(); // 将 edu_id 设置为类型为字符串的主键字段
    table.string('school');                      // 将 school 设置为字符串类型的字段
    table.string('major');                       // 将 major 设置为字符串类型的字段
    table.string('degree');                     // 将 degree 设置为字符串类型的字段
    table.date('graduation');                 // 将 graduation 设置为 date 类型的字段
});

// 如果 professional 表不存在就创建它
MyDB.schema.createTableIfNotExists('professional', function(table) {
    table.bigInteger('pro_id').primary(); // 将 pro_id 设置为类型为字符串的主键字段
    table.string('company');              // 将 company 设置为字符串类型的字段
    table.string('title');                       // 将 title 设置为字符串类型的字段
    table.date('startingDate');           // 将 startingDate 设置为 date 类型的字段
    table.date('endingDate');            // 将 endingDate 设置为 date 类型的字段
});

// 创建当前模块要导出的 API 对象
const MysqlApi = {
    // 创建用于向指定数据表中插入数据的 API
    insert :  function(table, jsonData) {
        return MyDB(table).insert(jsonData);
    },

    // 创建用于查看指定数据表中所有数据的 API
    getAll : async function(table) {
        const data = await MyDB(table).select('*');
        return data; 
    },

    // 创建用于向指定数据表中查询指定编号的数据的 API
    getDataById : async function(table, id) {
        const key = 'cv_id'
        if(table == 'education') {
            key = 'edu_id';
        } else if(table == 'professional') {
            key = 'pro_id';
        } else if(table == 'users') {
            key = 'uid';
        }
        const data = await MyDB(table).select('*')
        .where(key, '=', Number(id));
        return data;
    },

    // 该 API 用于验证用户是否存在，如果存在就返回该用户数据
    checkUser : async function(userData) {
        const data = await MyDB('users').select('*')
        .where('user', '=', userData.user)
        .andWhere('passwd', '=', userData.passwd);
        return data;
    },

    // 创建用于获取同用户id的所有简历的 API
    getResumeByUID : async function(uid) {
        const data = await MyDB('resumes').select('*')
        .where('uid', '=', Number(uid));
        return data;
    },

    // 创建用于在指定数据表中修改指定数据的 API
    update : function(table, id, data) {
        const key = 'cv_id'
        if(table == 'education') {
            key = 'edu_id';
        } else if(table == 'professional') {
            key = 'pro_id';
        }  else if(table == 'users') {
            key = 'uid';
        }
        return MyDB(table).update(data)
        .where(key, '=', Number(id));
    },

    // 创建用于在指定数据表中删除指定数据的 API
    delete : function(table, id) {
        const key = 'cv_id'
        if(table == 'education') {
            key = 'edu_id';
        } else if(table == 'professional') {
            key = 'pro_id';
        }  else if(table == 'users') {
            key = 'uid';
        }
        return MyDB(table).delete()
        .where(key, '=', Number(id));
    },
};

module.exports = MysqlApi;
