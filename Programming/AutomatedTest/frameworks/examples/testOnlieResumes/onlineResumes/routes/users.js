const express = require('express');
const router = express.Router();
// const dbApi = require('./useMysql');
const dbApi = require('./useMongodb');

// 用户注册
router.post('/newuser', async function(req, res, next) {
    // 确认表单数据不为空
    if(JSON.stringify(req.body) == '{}') {
        res.status(400).json({
            'message' : '服务端没有收到有效数据'
         });
    }
    // 执行数据插入操作
    const  isAdded
        = await dbApi.insert('users', req.body);
    // 返回服务端响应信息
    if(isAdded) {
        res.status(200).json({
            'message' : '用户注册成功'
        });
    } else {
        res.status(500).json({
            'message' : '用户注册失败'
        });
    }
});

// 用户登录
router.post('/session', async function(req, res, next) {
    // 确认表单数据不为空
    if(JSON.stringify(req.body) == '{}') {
        res.status(400).json({
            'message' : '服务端没有收到有效数据'
        });
    }
    // 查看指定用户是否有登录资格
    const  user
        = await dbApi.checkUser(req.body);
    // 根据查看结果返回服务端响应信息
    if(user.length != 1) {
        res.status(302).json({
            'message' : '用户名或密码错误'
        });
    } else {
        res.status(200).json({
            'uid' : user[0].uid,
            'message' : '用户登录成功'
        });
    }
});

 // 查看用户信息
router.get('/:id', async function(req, res, next) {
    // 确认用户ID有效并且有查看权限
    if(JSON.stringify(req.params) == '{}') {
        res.status(400).json({
            'message' : '服务端没有收到有效数据'
        });
    } else if(JSON.stringify(req.cookies) == '{}') {
        res.status(302).json({
            'message' : '用户尚未登录'
        });
    } else if(req.cookies['uid'] != req.params.id) {
        res.status(403).json({
            'message' : '你无权限查看该用户数据'
        });
    }
    const user 
        = await dbApi.getDataById('users', req.params.id);
        // 根据查看结果返回服务端响应信息
    if(user.length != 1) {
        res.status(404).json({
            'message' : '指定用户信息不存在'
        });
    } else {
        res.status(200).json(user);
    }
});

 // 修改用户信息
 router.put('/:id', async function(req, res, next) {
    // 确认用户ID有效并且有查看权限
    if(JSON.stringify(req.params) == '{}' || 
        JSON.stringify(req.body) == '{}') {
        res.status(400).json({
            'message' : '服务端没有收到有效数据'
        });
    } else if(JSON.stringify(req.cookies) == '{}') {
        res.status(302).json({
            'message' : '用户尚未登录'
        });
    } else if(req.cookies['uid'] != req.params.id) {
        res.status(403).json({
            'message' : '你无权限修改该用户数据'
        });
    }
    const  isUpdated
        = await dbApi.update('users', req.params.id, req.body);
    // 返回服务端响应信息
    if(isUpdated) {
        res.status(200).json({
            'message' : '用户数据修改成功'
        });
    } else {
        res.status(500).json({
            'message' : '用户数据修改失败'
        });
    }
});

 // 删除用户信息
 router.delete('/:id', async function(req, res, next) {
    // 确认用户ID有效并且有查看权限
    if(JSON.stringify(req.params) == '{}') {
        res.status(400).json({
            'message' : '服务端没有收到有效数据'
        });
    } else if(JSON.stringify(req.cookies) == '{}') {
        res.status(302).json({
            'message' : '用户尚未登录'
        });
    } else if(req.cookies['uid'] != req.params.id) {
        res.status(403).json({
            'message' : '你无权限删除该用户数据'
        });
    }
    const isDelUser
        = await dbApi.delete('users', req.params.id);
    // 根据查看结果返回服务端响应信息
    if(isDelUser) {
        res.status(200).json({
            'message' : '用户数据删除成功'
        });
    } else {
        res.status(500).json({
            'message' : '用户数据删除失败'
        });
    }
});
  
module.exports = router;
