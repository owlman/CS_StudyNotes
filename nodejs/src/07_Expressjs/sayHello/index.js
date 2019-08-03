
// 在Express框架中说Hello
// 作者：owlman
// 时间：2019年07月25日

module.exports = function(app) {
    app.get('/', function (req, res) {
        res.render('hello.htm', {name : 'Express'})
    })
}
