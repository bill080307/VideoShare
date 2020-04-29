import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import BootstrapVue from 'bootstrap-vue'
import VueIpfs from './plugins/vue-ipfs';
Vue.config.productionTip = false
Vue.use(BootstrapVue);

VueIpfs.install(Vue,{
    repo: '/ipfs-' + Math.random(),
    config: {
        Addresses: {
            Swarm: ['/dns4/ws-star.discovery.libp2p.io/tcp/443/wss/p2p-websocket-star/']
        }
    },
    EXPERIMENTAL: {pubsub: true}
})
Vue.use(VueIpfs);
new Vue({
  router,
  render: function (h) { return h(App) }
}).$mount('#app')
