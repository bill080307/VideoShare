import Vue from 'vue'
import Router from 'vue-router'
import videos from './views/videos.vue'
import home from './views/home.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'videos',
      component: videos
    },
    {
      path: '/home',
      name: 'home',
      component: home
    }
  ]
})
