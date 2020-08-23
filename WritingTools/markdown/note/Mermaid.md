# Mermaid生成图形示例

## 流程图

```Mermaid
graph TD
    id1((用户)) --访问--> id2((导航栏))
    subgraph 书籍销售系统
        id2 --分类或搜索--> id3{查看图书信息}
        id2 --如果没有登录--> id4{用户登录}
        id2 --如果已经登录--> id5{查看交易记录}
        id2 --如果已经登录--> id6{查看购物车}
        id3 --加入采购清单--> id6
        id4 --登录成功--> id3
        id4 --登录成功--> id6
        id5 --支付未完成的交易-->id7((支付平台))
        id6 --立即购买--> id7
        id6 --延后付款--> id5
    end
```

## 序列图

```Mermaid
sequenceDiagram
    participant 张三
    participant 李四
    participant 王五
    张三 -> 王五: 老王，你论文写好了吗？
    loop 检查论文
        王五 -> 王五: 确认完成度
    end
    Note right of 王五: 再三确认 <br/>再回答……
    王五 --> 张三: 写好了，但还需修改。
    王五 -> 李四: 你怎么样？
    李四 --> 王五: 我已经发给老师了！
```
