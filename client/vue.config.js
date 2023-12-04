const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
        proxy: 'http://127.0.0.1:5000'
    },
    pages: {
        'index': {
            entry: './src/pages/both/main.js',
            template: 'public/index.html',
            title: 'Home',
            chunks: ['chunk-vendors', 'chunk-common', 'index']
        },
        'audio': {
            entry: './src/pages/audio/main.js',
            template: 'public/index.html',
            title: 'Audio Detection',
            chunks: ['chunk-vendors', 'chunk-common', 'audio']
        },
        'image': {
            entry: './src/pages/image/main.js',
            template: 'public/index.html',
            title: 'Image Detection',
            chunks: ['chunk-vendors', 'chunk-common', 'image']
        }
    }
})
