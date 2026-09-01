<script setup>
import { ref, watch } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
import DynamicBackground from './components/DynamicBackground.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
import ThemeToggle from './components/ThemeToggle.vue'
import { useLocaleStore } from './stores/locale'
import { applyDocumentTitle } from './utils/documentTitle'

const route = useRoute()
const localeStore = useLocaleStore()

// 语言切换后立即用新语言重算浏览器标题（路由级切换由 router.beforeEach 负责）
watch(
  () => localeStore.locale,
  () => {
    applyDocumentTitle(route)
  }
)

// ===== 导航配置（桌面横向导航 + 移动端抽屉共用） =====
const navItems = [
  { key: 'home', path: '/', disabled: false },
  { key: 'resume', path: '/resume', disabled: false },
  { key: 'agent', path: '/agent-workflow', disabled: false },
  { key: 'music', path: '/music', disabled: false },
  { key: 'board', path: '/message-board', disabled: true },
  { key: 'tools', path: '/tools', disabled: true },
  { key: 'talents', path: '/talents', disabled: false }
]

// ===== 移动端抽屉菜单 =====
const menuOpen = ref(false)

const closeMenu = () => {
  menuOpen.value = false
}

// 路由变化时自动收起抽屉
watch(
  () => route.fullPath,
  () => {
    closeMenu()
  }
)

// 抽屉打开时锁定背景滚动
watch(menuOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})

// ===== 页脚社交链接（占位，部署前替换为真实链接） =====
const socialLinks = [
  {
    key: 'github',
    label: 'GitHub',
    href: 'https://github.com/XiaoguaiXiaowai/',
    path: 'M12 2C6.48 2 2 6.48 2 12c0 4.42 2.87 8.17 6.84 9.5.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.89 1.52 2.34 1.08 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02.8-.22 1.65-.33 2.5-.33s1.7.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85V21c0 .27.18.58.69.48C19.14 20.16 22 16.42 22 12c0-5.52-4.48-10-10-10Z'
  },
  {
    key: 'email',
    label: 'Email',
    href: 'mailto:jimmy_0406@sina.com',
    path: 'M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm0 2 9 6 9-6'
  },
  {
    key: 'rss',
    label: 'RSS',
    href: '#',
    path: 'M4 11a9 9 0 0 1 9 9M4 4a16 16 0 0 1 16 16M5 19a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z'
  }
]
</script>

<template>
  <div class="app-container">
    <DynamicBackground />
    <div class="content-overlay">
      <header>
        <div class="wrapper">
          <div class="site-branding">
            <span class="logo-main">{{ $t('common.brandName') }}</span>
            <span class="logo-sub">{{ $t('common.brandSub') }}</span>
          </div>
          <div class="header-right">
            <nav class="desktop-nav" aria-label="主导航">
              <template v-for="item in navItems" :key="item.key">
                <RouterLink v-if="!item.disabled" :to="item.path">
                  {{ $t(`nav.${item.key}`) }}
                </RouterLink>
                <div v-else class="nav-item-wrapper disabled-nav">
                  <span class="nav-text">{{ $t(`nav.${item.key}`) }}</span>
                  <span class="wip-badge">WIP</span>
                </div>
              </template>
            </nav>
            <div class="header-actions">
              <LanguageSwitcher />
              <ThemeToggle />
              <button
                class="menu-toggle"
                :class="{ 'is-open': menuOpen }"
                :aria-expanded="menuOpen"
                aria-label="打开菜单"
                @click="menuOpen = !menuOpen"
              >
                <span></span>
                <span></span>
                <span></span>
              </button>
            </div>
          </div>
        </div>

        <!-- 移动端抽屉菜单 -->
        <transition name="drawer-fade">
          <div v-if="menuOpen" class="drawer-backdrop" @click="closeMenu"></div>
        </transition>
        <transition name="drawer-slide">
          <nav v-if="menuOpen" class="mobile-nav" aria-label="移动端导航">
            <template v-for="item in navItems" :key="item.key">
              <RouterLink v-if="!item.disabled" :to="item.path" @click="closeMenu">
                {{ $t(`nav.${item.key}`) }}
              </RouterLink>
              <div v-else class="mobile-nav-item disabled-nav">
                <span>{{ $t(`nav.${item.key}`) }}</span>
                <span class="wip-badge">WIP</span>
              </div>
            </template>
          </nav>
        </transition>
      </header>

      <main>
        <RouterView />
      </main>

      <footer>
        <div class="footer-inner">
          <div class="footer-social">
            <a
              v-for="link in socialLinks"
              :key="link.key"
              :href="link.href"
              :aria-label="link.label"
              :title="link.label"
              target="_blank"
              rel="noopener noreferrer"
            >
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path :d="link.path" />
              </svg>
            </a>
          </div>
          <p>{{ $t('common.footerCopyright') }}</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-overlay {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  flex: 1;
}

header {
  background-color: var(--header-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid var(--header-border);
}

.wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.2rem 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 18px;
  justify-content: flex-end;
  min-width: 0;
}

.site-branding {
  display: flex;
  align-items: center;
  /* 固定品牌区高度：避免日文/英文下 CJK 字形行盒溢出导致页头变高 */
  height: 51px;
  flex-shrink: 0;
}

.logo-main {
  font-family: var(--font-display);
  font-size: 2.0rem;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, var(--luna-darkest), var(--luna-medium));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.logo-sub {
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.2;
  color: var(--text-secondary);
  margin-left: 8px;
  white-space: nowrap;
}

/* ===== 桌面导航 ===== */
.desktop-nav {
  display: flex;
  gap: 10px;
  align-items: center;
  min-width: 0;
  /* 导航区允许横向滚动，保证页头始终单行、高度不因语言变化 */
  overflow-x: auto;
  scrollbar-width: none;
}

.desktop-nav::-webkit-scrollbar {
  display: none;
}

.desktop-nav a,
.nav-item-wrapper {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  /* 固定高度 + 居中：导航项高度不随语言字形度量变化，页头高度恒一致 */
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 18px;
  border-radius: 20px;
  transition: all 0.3s ease;
  position: relative;
  white-space: nowrap;
  flex-shrink: 0;
}

.desktop-nav a:hover {
  color: var(--text-primary);
  background-color: var(--nav-hover-bg);
}

.desktop-nav a.router-link-active {
  color: var(--nav-active-color);
  background: var(--nav-active-bg);
  box-shadow: 0 4px 12px var(--nav-active-shadow);
}

.nav-item-wrapper.disabled-nav {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: not-allowed;
  opacity: 0.7;
}

.nav-item-wrapper.disabled-nav:hover {
  background-color: transparent;
}

.wip-badge {
  font-size: 0.65rem;
  font-weight: 800;
  font-family: var(--font-display);
  background: var(--badge-bg);
  color: var(--luna-medium);
  padding: 2px 6px;
  border-radius: 10px;
  border: 1px solid var(--badge-border);
  box-shadow: 0 2px 4px rgba(1, 28, 64, 0.05);
  letter-spacing: 0.05em;
  transform: translateY(-1px);
}

/* ===== 右侧操作区 ===== */
.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

/* 汉堡按钮（仅移动端显示） */
.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--card-bg-soft);
  border: 1px solid var(--card-border);
  padding: 0;
  flex-shrink: 0;
}

.menu-toggle span {
  display: block;
  width: 18px;
  height: 2px;
  border-radius: 2px;
  background: var(--text-secondary);
  transition: transform 0.3s ease, opacity 0.3s ease, background-color 0.3s ease;
}

.menu-toggle.is-open span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.menu-toggle.is-open span:nth-child(2) {
  opacity: 0;
}

.menu-toggle.is-open span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* ===== 移动端抽屉 ===== */
.drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(2, 18, 34, 0.45);
  backdrop-filter: blur(2px);
  z-index: 110;
}

.mobile-nav {
  position: fixed;
  top: 0;
  right: 0;
  height: 100dvh;
  width: min(78vw, 320px);
  background: var(--header-bg);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-left: 1px solid var(--header-border);
  box-shadow: -16px 0 48px rgba(0, 0, 0, 0.18);
  z-index: 120;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 88px 18px 28px;
  overflow-y: auto;
}

.mobile-nav a,
.mobile-nav .mobile-nav-item {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 600;
  font-size: 1.08rem;
  height: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-radius: 14px;
  transition: all 0.25s ease;
}

.mobile-nav a:hover {
  background-color: var(--nav-hover-bg);
}

.mobile-nav a.router-link-active {
  color: var(--nav-active-color);
  background: var(--nav-active-bg);
  box-shadow: 0 4px 12px var(--nav-active-shadow);
}

.mobile-nav .mobile-nav-item.disabled-nav {
  opacity: 0.6;
  cursor: not-allowed;
}

.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 0.25s ease;
}

.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}

.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.drawer-slide-enter-from,
.drawer-slide-leave-to {
  transform: translateX(100%);
}

main {
  flex: 1;
  padding: 40px 20px;
  max-width: 1100px;
  margin: 0 auto;
  width: 100%;
}

footer {
  text-align: center;
  padding: 32px 20px 40px;
  background-color: var(--footer-bg);
  color: var(--text-secondary);
  font-size: 0.85rem;
  border-top: 1px solid var(--header-border);
}

.footer-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}

.footer-social {
  display: flex;
  gap: 14px;
}

.footer-social a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: var(--text-secondary);
  border: 1px solid var(--card-border);
  background: var(--card-bg-soft);
  transition: all 0.3s ease;
}

.footer-social a:hover {
  color: var(--nav-active-color);
  background: var(--nav-active-bg);
  box-shadow: 0 4px 12px var(--nav-active-shadow);
  opacity: 1;
  transform: translateY(-2px);
}

footer p {
  margin: 0;
}

@media (max-width: 900px) {
  .wrapper {
    gap: 20px;
    padding: 1rem 20px;
  }

  .logo-sub {
    display: none;
  }

  .desktop-nav {
    display: none;
  }

  .menu-toggle {
    display: inline-flex;
  }
}
</style>
