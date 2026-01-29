<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <header>
      <div class="wrapper">
        <div class="site-branding">
          胖脸他哥哥 - 李佳的个人网站
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
      <p>&copy; 2026 胖脸他哥哥 - 李佳的个人网站. All rights reserved.</p>
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
  background-color: #333;
  color: white;
}

.wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.site-branding {
  font-size: 1.2rem;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.site-branding .highlight {
  font-size: 5rem;
  color: #42b983;
  margin-right: 5px;
}

nav {
  display: flex;
  gap: 20px;
}

nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

nav a.router-link-active {
  color: #42b983;
}

main {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

footer {
  text-align: center;
  padding: 20px;
  background-color: #f0f0f0;
  color: #666;
}
</style>
