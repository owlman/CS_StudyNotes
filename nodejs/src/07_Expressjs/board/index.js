
module.exports = function(app) {
    app.get('/board', (req, res) => res.send('Hello Board!'))
}