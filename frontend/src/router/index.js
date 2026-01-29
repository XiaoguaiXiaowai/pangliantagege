import { createRouter, createWebHistory } from 'vue-router'
import ResumeView from '../views/ResumeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'resume',
      component: ResumeView
    },
    {
      path: '/message-board',
      name: 'message-board',
      component: () => import('../views/MessageBoardView.vue')
    },
    {
      path: '/ai-assistant',
      name: 'ai-assistant',
      component: () => import('../views/AIAssistantView.vue')
    },
    {
      path: '/tools',
      name: 'tools',
      component: () => import('../views/ToolsView.vue')
    },
    {
      path: '/talents',
      name: 'talents',
      component: () => import('../views/TalentsView.vue')
    }
  ]
})

export default router
