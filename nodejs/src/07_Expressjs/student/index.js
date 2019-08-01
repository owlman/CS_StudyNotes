
module.exports = function(app) {
    app.get('/student', (req, res) => res.send('Hello student!'))
}