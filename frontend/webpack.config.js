const webpack = require('webpack');

const config = {
    entry:  __dirname + '/index.jsx',
    output: {
        path: '/home/abhishek/code/Mporter/static/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    module: {
        rules: [
            { test: /\.jsx?/, exclude: /node_modules/, use: 'babel-loader' }
        ]
    },
    devtool: 'source-map'
};

module.exports = config;
