import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { applyDocumentTitle } from '../utils/documentTitle'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { titleKey: 'home' }
    },
    {
      path: '/resume',
      name: 'resume',
      component: () => import('../views/ResumeView.vue'),
      meta: { titleKey: 'resume' }
    },
    {
      path: '/message-board',
      name: 'message-board',
      component: () => import('../views/MessageBoardView.vue'),
      meta: { titleKey: 'messageBoard' }
    },
    {
      path: '/agent-workflow',
      name: 'agent-workflow',
      component: () => import('../views/AgentWorkflowView.vue'),
      meta: { titleKey: 'agentWorkflow' }
    },
    {
      path: '/ai-assistant',
      redirect: '/agent-workflow'
    },
    {
      path: '/tools',
      name: 'tools',
      component: () => import('../views/ToolsView.vue'),
      meta: { titleKey: 'tools' }
    },
    {
      path: '/music',
      name: 'music-space',
      component: () => import('../views/MusicSpaceView.vue'),
      meta: { titleKey: 'musicSpace' }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { titleKey: 'login' }
    },
    {
      path: '/talents',
      name: 'talents',
      component: () => import('../views/TalentsView.vue'),
      meta: { titleKey: 'talents' }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: { titleKey: 'notFound' }
    }
  ]
})

router.beforeEach((to, from, next) => {
  applyDocumentTitle(to)
  next()
})

export default router