const path = require('path');
const express = require('express');
const users = require(path.join(__dirname, 'users'));
const notes = require(path.join(__dirname, 'notes'));

const router = express.Router();
// 用户管理
users(router);
// 文章列表
notes(router);

module.exports = router