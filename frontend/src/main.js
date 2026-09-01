import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import i18n, { STORAGE_KEY, SUPPORTED_LOCALES } from './i18n'
import { useLocaleStore } from './stores/locale'
import { useThemeStore } from './stores/theme'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(i18n)
app.use(router)

// 应用持久化/浏览器检测出的初始语言
const localeStore = useLocaleStore()
i18n.global.locale.value = localeStore.locale
document.documentElement.setAttribute('lang', localeStore.locale)

// 应用主题（跟随系统 + 手动覆盖），mount 前执行避免闪烁
const themeStore = useThemeStore()
themeStore.init()

// 所有 axios 请求自动携带当前语言参数（用于后端内容本地化）
axios.interceptors.request.use((config) => {
  let saved = null
  try {
    saved = window.localStorage.getItem(STORAGE_KEY)
  } catch (_) {
    /* ignore */
  }
  const locale =
    saved && SUPPORTED_LOCALES.some((l) => l.code === saved)
      ? saved
      : localeStore.locale
  const lang = SUPPORTED_LOCALES.find((l) => l.code === locale)?.apiCode || 'zh'
  config.params = { ...(config.params || {}), lang }
  return config
})

app.mount('#app')