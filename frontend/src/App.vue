<script setup>
import { RouterLink, RouterView } from 'vue-router'
import DynamicBackground from './components/DynamicBackground.vue'
</script>

<template>
  <div class="app-container">
    <DynamicBackground />
    <div class="content-overlay">
      <header>
        <div class="wrapper">
          <div class="site-branding">
            <span class="logo-main">胖脸她哥哥</span>
            <span class="logo-sub"> - 李佳的个人网站</span>
          </div>
          <nav>
            <RouterLink to="/">首页</RouterLink>
            <RouterLink to="/resume">工作简历</RouterLink>
            <RouterLink to="/music">音乐作品</RouterLink>
            
            <div class="nav-item-wrapper disabled-nav">
              <span class="nav-text">留言板</span>
              <span class="wip-badge">WIP</span>
            </div>
            
            <div class="nav-item-wrapper disabled-nav">
              <span class="nav-text">AI 助理</span>
              <span class="wip-badge">WIP</span>
            </div>
            
            <div class="nav-item-wrapper disabled-nav">
              <span class="nav-text">小工具</span>
              <span class="wip-badge">WIP</span>
            </div>
            
            <RouterLink to="/talents">其他</RouterLink>
          </nav>
        </div>
      </header>

      <main>
        <RouterView />
      </main>

      <footer>
        <p>&copy; 2026 胖脸她哥哥 - 李佳的个人网站. All rights reserved.</p>
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

.site-branding {
  display: flex;
  align-items: baseline;
  letter-spacing: -0.01em;
  flex-shrink: 0;
}

.logo-main {
  font-size: 2.0rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--luna-darkest), var(--luna-medium));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.logo-sub {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-left: 8px;
}

nav {
  display: flex;
  gap: 10px;
  align-items: center;
}

nav a, .nav-item-wrapper {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  padding: 8px 18px;
  border-radius: 20px;
  transition: all 0.3s ease;
  position: relative;
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
</style>
