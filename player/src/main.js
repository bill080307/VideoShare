import Vue from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'video.js/dist/video-js.css'
import BootstrapVue from 'bootstrap-vue'
import JsonViewer from 'vue-json-viewer'
Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(JsonViewer);
new Vue({
  render: function (h) { return h(App) },
}).$mount('#app');
