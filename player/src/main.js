import Vue from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'video.js/dist/video-js.css'
import BootstrapVue from 'bootstrap-vue'
import JsonViewer from 'vue-json-viewer'
import hls from 'videojs-contrib-hls'
Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(JsonViewer);
Vue.use(hls);
new Vue({
    render: function (h) {
        return h(App)
    },
}).$mount('#app');
