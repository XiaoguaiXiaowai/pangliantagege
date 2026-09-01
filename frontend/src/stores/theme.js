import { defineStore } from 'pinia'

/**
 * 主题偏好 store（Luna 2.0）。
 * 策略：跟随系统（auto）+ 手动覆盖（light/dark），选择持久化到 localStorage。
 * 通过 <html data-theme> + colorScheme 应用主题；
 * index.html 中有一份内联脚本在首帧前做同样的初始化，避免深色用户看到闪烁。
 */
export const useThemeStore = defineStore('theme', {
  state: () => ({
    /** 'auto' | 'light' | 'dark'；初始为 auto（跟随系统） */
    theme: 'auto'
  }),
  getters: {
    /** 系统当前是否为深色偏好 */
    systemDark: () => {
      if (typeof window === 'undefined') return false
      return window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? false
    },
    /** 最终生效的主题（auto 时解析为系统偏好） */
    resolved() {
      return this.theme === 'auto' ? (this.systemDark ? 'dark' : 'light') : this.theme
    },
    /** 当前是否处于深色 */
    isDark() {
      return this.theme === 'dark' || (this.theme === 'auto' && this.systemDark)
    }
  },
  actions: {
    /** 应用主题到 <html>（store 内读取 getter 用 this） */
    apply() {
      const dark = this.isDark
      document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
      document.documentElement.style.colorScheme = dark ? 'dark' : 'light'
    },
    /** 初始化：读取持久化偏好 + 监听系统主题变化。在 app mount 前调用。 */
    init() {
      let saved = null
      try {
        saved = window.localStorage.getItem('luna-theme')
      } catch (_) {
        /* localStorage 不可用时忽略 */
      }
      if (saved === 'light' || saved === 'dark') this.theme = saved
      this.apply()

      const mq = window.matchMedia?.('(prefers-color-scheme: dark)')
      if (mq && typeof mq.addEventListener === 'function') {
        mq.addEventListener('change', () => {
          // 仅在 auto 模式下跟随系统变化
          if (this.theme === 'auto') this.apply()
        })
      }
    },
    /** 设置主题（light / dark / auto）并持久化 */
    setTheme(theme) {
      if (theme !== 'light' && theme !== 'dark' && theme !== 'auto') return
      if (this.theme === theme) return
      this.theme = theme
      try {
        window.localStorage.setItem('luna-theme', theme)
      } catch (_) {
        /* 忽略 */
      }
      // 短暂开启全局过渡，让主题切换平滑
      const root = document.documentElement
      root.classList.add('theme-switching')
      this.apply()
      window.setTimeout(() => root.classList.remove('theme-switching'), 420)
    },
    /** 在浅色/深色之间切换（离开 auto 即视为手动覆盖） */
    toggle() {
      this.setTheme(this.isDark ? 'light' : 'dark')
    }
  }
})
