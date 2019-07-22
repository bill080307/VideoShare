import Vue from 'vue'
import Router from 'vue-router'
import Videolist from './views/Videolist.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Videolist
    },
    {
      path: '/*',
      name: 'type',
      component: Videolist
    }
  ]
})
