import { createI18n } from 'vue-i18n'
import zhCN from './locales/zh-CN.json'
import en from './locales/en.json'
import ja from './locales/ja.json'

export const STORAGE_KEY = 'site-locale'
export const COOKIE_KEY = 'site_locale'

/**
 * 站点支持的语言列表。
 * code 同时用于 URL 参数 lang 与 localStorage / cookie 持久化。
 * apiCode 用于后端 ?lang= 参数（zh-CN -> zh）。
 */
export const SUPPORTED_LOCALES = [
  { code: 'zh-CN', apiCode: 'zh', label: '中文', short: '中' },
  { code: 'en', apiCode: 'en', label: 'English', short: 'EN' },
  { code: 'ja', apiCode: 'ja', label: '日本語', short: '日本語' }
]

/** 初始语言判定：已存偏好 > 浏览器语言映射 > 默认 zh-CN */
export function detectInitialLocale() {
  if (typeof window === 'undefined') return 'zh-CN'
  try {
    const saved = window.localStorage.getItem(STORAGE_KEY)
    if (saved && SUPPORTED_LOCALES.some((l) => l.code === saved)) return saved
  } catch (_) {
    /* localStorage 不可用时忽略 */
  }
  const nav = (typeof navigator !== 'undefined' && (navigator.language || 'zh-CN')) || 'zh-CN'
  const lang = nav.toLowerCase()
  if (lang.startsWith('ja')) return 'ja'
  if (lang.startsWith('en')) return 'en'
  return 'zh-CN'
}

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: 'zh-CN',
  fallbackLocale: 'zh-CN',
  messages: {
    'zh-CN': zhCN,
    en: en,
    ja: ja
  }
})

export default i18n