<script setup>
import { watch } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
import DynamicBackground from './components/DynamicBackground.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
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
            <nav>
              <RouterLink to="/">{{ $t('nav.home') }}</RouterLink>
              <RouterLink to="/resume">{{ $t('nav.resume') }}</RouterLink>
              <RouterLink to="/agent-workflow">{{ $t('nav.agent') }}</RouterLink>
              <RouterLink to="/music">{{ $t('nav.music') }}</RouterLink>
              <div class="nav-item-wrapper disabled-nav">
                <span class="nav-text">{{ $t('nav.board') }}</span>
                <span class="wip-badge">WIP</span>
              </div>

              <div class="nav-item-wrapper disabled-nav">
                <span class="nav-text">{{ $t('nav.tools') }}</span>
                <span class="wip-badge">WIP</span>
              </div>

              <RouterLink to="/talents">{{ $t('nav.talents') }}</RouterLink>
            </nav>
            <LanguageSwitcher />
          </div>
        </div>
      </header>

      <main>
        <RouterView />
      </main>

      <footer>
        <p>{{ $t('common.footerCopyright') }}</p>
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
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(167, 235, 242, 0.3);
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
  font-size: 2.0rem;
  font-weight: 800;
  line-height: 1.2;
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

nav {
  display: flex;
  gap: 10px;
  align-items: center;
  min-width: 0;
  /* 导航区允许横向滚动，保证页头始终单行、高度不因语言变化 */
  overflow-x: auto;
  scrollbar-width: none;
}

nav::-webkit-scrollbar {
  display: none;
}

nav a, .nav-item-wrapper {
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

nav a:hover {
  color: var(--luna-darkest);
  background-color: rgba(167, 235, 242, 0.2); /* Luna Lightest tint */
}

nav a.router-link-active {
  color: #fff;
  background-color: var(--luna-medium);
  box-shadow: 0 4px 12px rgba(38, 101, 140, 0.3);
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
  background: linear-gradient(135deg, #f0f4f8, #e2e8f0);
  color: var(--luna-medium);
  padding: 2px 6px;
  border-radius: 10px;
  border: 1px solid rgba(167, 235, 242, 0.5);
  box-shadow: 0 2px 4px rgba(1, 28, 64, 0.05);
  letter-spacing: 0.05em;
  transform: translateY(-1px);
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
  padding: 40px 20px;
  background-color: #fff;
  color: var(--text-secondary);
  font-size: 0.85rem;
  border-top: 1px solid rgba(167, 235, 242, 0.3);
}

@media (max-width: 900px) {
  .wrapper {
    gap: 20px;
    padding: 1rem 20px;
  }

  .logo-sub {
    display: none;
  }
}
</style>