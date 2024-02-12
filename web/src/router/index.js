import { createRouter, createWebHistory } from 'vue-router'
import Songs from '../views/Songs.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Songs,  
    },

    {
      path: '/music',
      name: 'Songs',
      component: Songs,
    },

    {
      path: '/album',
      name: 'Albums',
      component: () => import('../views/Albums.vue'),
    },
  ]
})

export default router