const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const config = {
    entry: {
        main: path.join(__dirname,'src/main.js')
    },
    output: {
        path: path.resolve(__dirname,'./public/'),
        filename:'js/[name]-bundle.js'
    },
    plugins:[
        new VueLoaderPlugin(),
        new HtmlWebpackPlugin({
            template: path.join(__dirname, 'src/index.htm')
        })
    ],
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader' // 处理以.vue结尾的文件
            },
            {
                test: /\.js$/,
                loader: 'babel-loader'
            },
            {
                test: /\.css/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js' //内部为正则表达式  vue结尾的
        }
    }
};

module.exports = config;
