const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const CopyWebpackPlugin = require('copy-webpack-plugin');


var filename = "[name].[ext]";

var PATHS = {
    JS: "/js/",
    CSS: "/css/",
    FONTS: "/fonts/",
    IMAGES: "/img/",
};
var fontsPath = PATHS.FONTS + filename;
var imagesPath = PATHS.IMAGES + filename;
var env = process.env.ENVIRONMENT;
var static_path;

if (env == 'production') {
    static_path = path.resolve("/static");
}
else {
    static_path = path.resolve("../apimocker/static/");
}

module.exports = {
    devtool: "source-map",
    entry: {
        "styles": "./src/scss/main.scss",
        "application": "./src/app/app.js",
    },
    output: {
        path: static_path,
        publicPath: "/static/",
        filename: "[name].js",
    },
    module: {
        rules: [{
                test: /\.html$/,
                use: [{
                    loader: 'raw-loader',
                }]
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['env']
                    }
                }
            },
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: 'css-loader'
                })
            },
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: "css-loader!sass-loader"
                })
            },
            {
                test: /\.(png|jpg|gif)$/,
                use: [{
                    loader: 'url-loader',
                    options: {
                        limit: 8192
                    }
                }]
            },
            // fonts
            {
                test: /\.woff(\?v=\d+\.\d+\.\d+|\?.*)?$/,
                use: "url-loader?limit=10000&mimetype=application/font-woff&name=" + fontsPath,
            },
            {
                test: /\.woff2(\?v=\d+\.\d+\.\d+|\?.*)?$/,
                use: "url-loader?limit=10000&mimetype=application/font-woff&name=" + fontsPath,
            },
            {
                test: /\.ttf(\?v=\d+\.\d+\.\d+|\?.*)?$/,
                use: "url-loader?limit=10000&mimetype=application/octet-stream&name=" + fontsPath,
            },
            {
                test: /\.eot(\?v=\d+\.\d+\.\d+|\?.*)?$/,
                use: "file-loader?name=" + fontsPath,
            },
            {
                test: /\.svg(\?v=\d+\.\d+\.\d+|\?.*)?$/,
                use: "url-loader?limit=10000&mimetype=image/svg+xml&name=" + imagesPath,
            },
            {
                test: /\.(png|gif|jpg|svg)$/,
                use: "url-loader?limit=100&name=" + imagesPath,
            },
            // Temporary solution, load script to use them in <script/>
            {
                test: require.resolve("jquery"),
                use: [{
                    loader: "expose-loader",
                    options: "$"
                }]
            },
        ]
    },
    resolve: {
        extensions: [".js"],
    },
    plugins: [
        new webpack.LoaderOptionsPlugin({
            options: {
                context: __dirname
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            beautify: true,
            comments: false
        }),
        new webpack.optimize.CommonsChunkPlugin({
            name: "common",
            minChunks: function (module, count) {
                return module.resource && module.resource.indexOf(path.resolve(__dirname, "src")) === -1;
            }
        }),
        new ExtractTextPlugin({
            filename: "[name].css",
            disable: false,
            allChunks: true
        }),
        // new CopyWebpackPlugin([{
        //     from: './src/',
        //     to: 'img',
        // }]),
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            "window.jQuery": "jquery",
        }),
    ]
};