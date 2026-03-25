import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: '首页' }
    },
    {
      path: '/resume',
      name: 'resume',
      component: () => import('../views/ResumeView.vue'),
      meta: { title: '工作简历' }
    },
    {
      path: '/message-board',
      name: 'message-board',
      component: () => import('../views/MessageBoardView.vue'),
      meta: { title: '留言板' }
    },
    {
      path: '/ai-assistant',
      name: 'ai-assistant',
      component: () => import('../views/AIAssistantView.vue'),
      meta: { title: 'AI 助理' }
    },
    {
      path: '/tools',
      name: 'tools',
      component: () => import('../views/ToolsView.vue'),
      meta: { title: '小工具' }
    },
    {
      path: '/music',
      name: 'music-space',
      component: () => import('../views/MusicSpaceView.vue'),
      meta: { title: '音乐作品' }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { title: '登录' }
    },
    {
      path: '/talents',
      name: 'talents',
      component: () => import('../views/TalentsView.vue'),
      meta: { title: '才艺' }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: { title: '页面不存在' }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const siteTitle = '李佳的个人网站'
  if (to.meta.title) {
    document.title = `${siteTitle} - ${to.meta.title}`
  } else {
    document.title = siteTitle
  }
  next()
})

export default router
