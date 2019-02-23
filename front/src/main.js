import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import VueFormGenerator from 'vue-form-generator'
import axios from 'axios'

axios.defaults.withCredentials = true

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(VueFormGenerator)


import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

new Vue({
  router,
  render: h => h(App),
  store
}).$mount('#app')
