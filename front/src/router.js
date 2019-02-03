import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import System from './components/System.vue'

Vue.use(Router)

 let router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {isPublic: true}
    },
    {
      path: '/systems',
      name: 'system',
      component: System,
      meta: {isPublic: true}
    },
    {
      path: '/signin',
      name: 'Signin',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue'),
      meta: {isPublic: true}
    }
  ]
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => !record.meta.isPublic)
  if (requiresAuth) {
    const currentUser = false
    if (!currentUser) {
      next({
        path: 'signin',
        query: {
          redirect: to.fullPath
        }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})
export default router