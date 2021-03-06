
"use strict";

const path = require('path');
const paths = require('./paths.js');
const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const WebpackNotifierPlugin = require('webpack-notifier');

module.exports = {
    target: 'web',
    externals: {},
    context: paths.baseInputDir,
    entry: {
        app: './app.js',
        news_preview: './scripts/news_preview',
    },
    module: {
        rules: [
            {
                test: /\.(scss|css)$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: "css-loader",
                        options: {}
                    },
                    {
                        loader: "sass-loader",
                        options: {}
                    }
                ]
            },
            {
                test: /\.(png|jpe?g|gif|ico)$/,
                loader: 'file-loader?name=assets/images/[name].[hash].[ext]'
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2)$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]',
                    outputPath: 'assets/fonts',
                    publicPath: 'assets/fonts/'
                }
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "[name].[hash].css",
            chunkFilename: "[id].css"
        }),
        // Provide basic 3d-party plugins.
        // Comment unneeded.
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            jquery: 'jquery',
            'window.jQuery': 'jquery'
        }),
        // Clean build directory.
        // To provide what files or directories should not be cleared use
        // cleanOnceBeforeBuildPatterns property. To exclude files use '!filename.extension'
        // or for directories '!*name/**'.
        new CleanWebpackPlugin({
            verbose: true,
            protectWebpackAssets: true,
            cleanOnceBeforeBuildPatterns: ['**/*', '!.gitkeep']
        }),
        // Notify whether build finished or failed
        new WebpackNotifierPlugin({
            title: 'website',
            skipFirstNotification: true
        }),
    ],
    optimization: {
        // Extract shared runtime code.
        runtimeChunk: 'single',
        namedModules: true,
        noEmitOnErrors: true
    },
    // If multiple files share the same name but have different extensions, webpack
    // will resolve the one with the extension listed first in the array and skip the rest.
    resolve: {
        extensions: ['.js'],
    },
    // Set a path for dynamic imports e.g.: import(`./some/${file}`) to work properly
    output: {
        publicPath: '/static/'
    }
}
