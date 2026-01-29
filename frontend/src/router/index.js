import { createRouter, createWebHistory } from 'vue-router'
import ResumeView from '../views/ResumeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'resume',
      component: ResumeView,
      meta: { title: '个人简历' }
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
      path: '/talents',
      name: 'talents',
      component: () => import('../views/TalentsView.vue'),
      meta: { title: '才艺' }
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
