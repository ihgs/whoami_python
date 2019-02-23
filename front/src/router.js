import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Admin from './views/Admin.vue'
import System from './components/System.vue'
import AdminRoute from './components/admin'
import store from './store'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/systems',
      name: 'system',
      component: System
    },
    {
      path: '/admin',
      component: Admin,
      children: [
        AdminRoute
      ]
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
  //const requiresAuth = false
  if (requiresAuth) {
    if (!store.getters.logined) {
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