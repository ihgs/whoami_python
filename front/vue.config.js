module.exports = {
  runtimeCompiler: true,
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:5042/',
        changeOrigin: true
      }
    }
  }
}