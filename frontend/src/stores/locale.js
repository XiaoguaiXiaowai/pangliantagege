import { defineStore } from 'pinia'
import i18n, {
  SUPPORTED_LOCALES,
  STORAGE_KEY,
  COOKIE_KEY,
  detectInitialLocale
} from '../i18n'

/**
 * 语言偏好 store。
 * 切换语言时同步：vue-i18n locale、<html lang>、localStorage 与 cookie，
 * 保持 URL 不变（SPA 无刷新切换）。
 * 浏览器标题（document.title）由 App.vue 监听 locale 变化统一处理。
 */
export const useLocaleStore = defineStore('locale', {
  state: () => ({
    locale: detectInitialLocale()
  }),
  getters: {
    /** 当前语言展示名（中文 / English / 日本語），用于切换器按钮 */
    currentLabel: (state) => {
      const found = SUPPORTED_LOCALES.find((l) => l.code === state.locale)
      return found ? found.label : '中文'
    },
    /** 当前语言对应的后端 ?lang= 参数值（zh-CN -> zh） */
    apiCode: (state) => {
      const found = SUPPORTED_LOCALES.find((l) => l.code === state.locale)
      return found ? found.apiCode : 'zh'
    }
  },
  actions: {
    setLocale(code) {
      if (!SUPPORTED_LOCALES.some((l) => l.code === code)) return
      this.locale = code
      i18n.global.locale.value = code
      try {
        window.localStorage.setItem(STORAGE_KEY, code)
      } catch (_) {
        /* localStorage 不可用时忽略 */
      }
      document.cookie = `${COOKIE_KEY}=${code}; path=/; max-age=${60 * 60 * 24 * 365}`
      document.documentElement.setAttribute('lang', code)
    }
  }
})