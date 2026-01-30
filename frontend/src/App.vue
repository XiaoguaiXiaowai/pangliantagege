<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <header>
      <div class="wrapper">
        <div class="site-branding">
          <span class="logo-main">胖脸她哥哥</span>
          <span class="logo-sub"> - 李佳的个人网站</span>
        </div>
        <nav>
          <RouterLink to="/">个人简历</RouterLink>
          <RouterLink to="/message-board">留言板</RouterLink>
          <RouterLink to="/ai-assistant">AI 助理</RouterLink>
          <RouterLink to="/tools">小工具</RouterLink>
          <RouterLink to="/talents">才艺</RouterLink>
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
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(0,0,0,0.03);
}

.wrapper {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1rem 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.site-branding {
  display: flex;
  align-items: baseline;
  letter-spacing: -0.01em;
}

.logo-main {
  font-size: 1.5rem;
  font-weight: 500;
  background: linear-gradient(135deg, var(--color-purple), var(--color-blue));
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
}

nav a {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

nav a:hover {
  color: var(--text-primary);
  background-color: rgba(0,0,0,0.03);
}

nav a.router-link-active {
  color: #fff;
  background-color: var(--color-blue);
  box-shadow: 0 4px 12px rgba(139, 174, 182, 0.3);
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
  border-top: 1px solid rgba(0,0,0,0.03);
}
</style>
