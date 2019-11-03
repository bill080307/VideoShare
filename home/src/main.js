import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import BootstrapVue from 'bootstrap-vue'
Vue.config.productionTip = false
Vue.use(BootstrapVue)
new Vue({
  router,
  render: function (h) { return h(App) }
}).$mount('#app')
