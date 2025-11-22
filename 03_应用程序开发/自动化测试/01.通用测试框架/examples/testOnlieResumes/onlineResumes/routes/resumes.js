const express = require('express');
const router = express.Router();
// const dbApi = require('./useMysql');
const dbApi = require('./useMongodb');

// 添加新的简历
router.post('/newresume', async function(req, res, next) {
    // 确认表单数据不为空
    if(JSON.stringify(req.body) == '{}') {
        res.status(400).json({
            'message':'表单数据丢失'
        });
    }
    // 执行数据插入操作
    const  isAdded
        = await dbApi.insert('resumes', req.body);
    // 返回服务端响应信息
    if(isAdded) {
        res.status(200).json({
            'message':'数据添加成功'
        });
    } else {
        res.status(500).json({
            'message':'数据添加失败'
        });
    }
});

 // 查看指定用户的所有简历
router.get('/user/:id', async function(req, res, next) {
    if(JSON.stringify(req.params.id) == '{}') {
        res.status(400).json({
            'message' : '服务端没有收到有效数据'
        });
    } else if(JSON.stringify(req.cookies) == '{}') {
        res.status(302).json({
            'message' : '用户尚未登录'
        });
    } else if(req.cookies['uid'] != req.params.id) {
        res.status(403).json({
            'message' : '你无权查看该用户的简历'
        });
    }
    const rs = await dbApi.getResumeByUID(req.params.id);
    // 根据查看结果返回服务端响应信息
    if(rs.length < 1) {
        res.status(404).json({
            'message' : '指定用户还没有简历'
        });
    } else {
        res.status(200).json(rs);
    }
});

 // 查看指定id的简历
router.get('/:id', async function(req, res, next) {
    if(JSON.stringify(req.params.id) == '{}') {
        res.status(400).json({
            'message' : '服务端没有收到有效数据'
        });
    } else if(JSON.stringify(req.cookies) == '{}') {
        res.status(302).json({
            'message' : '用户尚未登录'
        });
    } 
    const rs = await dbApi.getDataById('resumes', req.params.id);
    // 根据查看结果返回服务端响应信息
    if(rs.length != 1) {
        res.status(404).json({
            'message' : '指定用户还没有简历'
        });
    } else if(req.cookies['uid'] != rs[0].uid) {
        res.status(403).json({
            'message' : '你无权查看该用户的简历'
        });
    } else {
        res.status(200).json(rs);
    }
});

 // 查看用户简历的pdf版本
 router.get('/pdf/:id', function(req, res, next) {
});


 // 修改用户简历
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
    }
    const isUpdated
        = await dbApi.update('resumes', req.params.id, req.body);
    // 根据查看结果返回服务端响应信息
    if(isUpdated) {
        res.status(200).json({
            'message' : '简历修改成功'
        });
    } else {
        res.status(500).json({
            'message' : '简历修改失败'
        });
    }
});

 // 删除用户简历
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
    }
    const isDel
        = await dbApi.delete('resumes', req.params.id);
    // 根据查看结果返回服务端响应信息
    if(isDel) {
        res.status(200).json({
            'message' : '简历删除成功'
        });
    } else {
        res.status(500).json({
            'message' : '简历删除失败'
        });
    }

});

 // 删除指定用户的所有简历
router.delete('/user/:id', async function(req, res, next) {
    if(JSON.stringify(req.params.id) == '{}') {
        res.status(400).json({
            'message' : '服务端没有收到有效数据'
        });
    } else if(JSON.stringify(req.cookies) == '{}') {
        res.status(302).json({
            'message' : '用户尚未登录'
        });
    } else if(req.cookies['uid'] != req.params.id) {
        res.status(403).json({
            'message' : '你无权删除该用户的简历'
        });
    }
    const rs = await dbApi.getResumeByUID(req.params.id);
    for(let i=0; i < rs.length; ++i) {
        const isdel = await dbApi.delete('resumes', rs[i].cv_id);
        if(isdel == false) {
            res.status(500).json({
                'message' : '简历删除失败'
            });    
        }
    }
    res.status(200).json({
        'message' : '简历删除成功'
    })
});

module.exports = router;
