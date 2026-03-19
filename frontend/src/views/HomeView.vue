<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (path) => {
  router.push(path)
}

const features = [
  {
    title: '工作简历',
    description: '查看我的详细个人信息、工作经历、项目经验以及技能栈。',
    path: '/resume',
    icon: '📄'
  },
  {
    title: '留言板',
    description: '欢迎在这里留下您的足迹，与我交流或分享您的想法。',
    path: '/message-board',
    icon: '💬'
  },
  {
    title: 'AI 助理',
    description: '与集成先进大语言模型的智能助理对话，获取信息与帮助。',
    path: '/ai-assistant',
    icon: '🤖'
  },
  {
    title: '小工具',
    description: '我开发的一些实用在线小工具，旨在提高日常工作效率。',
    path: '/tools',
    icon: '🛠️'
  },
  {
    title: '其他',
    description: '分享我的业余爱好、才艺展示以及其他有趣的内容。',
    path: '/talents',
    icon: '✨'
  }
]
</script>

<template>
  <div class="home-container">
    <section class="hero-section">
      <h1>欢迎来到我的个人网站</h1>
      <p class="intro-text">
        你好！我是李佳，一名资深云运维工程师(SRE)与独立全栈开发者。
        <br />
        拥有十多年的IT行业经验，热衷于技术探索与系统架构设计。在这里，你可以了解我的职业经历，体验我开发的小工具，或者与我的AI助理聊聊天。
      </p>
    </section>

    <section class="navigation-grid">
      <div 
        v-for="feature in features" 
        :key="feature.title" 
        class="nav-card"
        @click="navigateTo(feature.path)"
      >
        <div class="card-icon">{{ feature.icon }}</div>
        <div class="card-content">
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
        <div class="card-arrow">→</div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
  max-width: 900px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: #fff;
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  background-image: radial-gradient(circle at top right, rgba(167, 235, 242, 0.3), transparent 60%);
}

.hero-section h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 20px;
  background: linear-gradient(135deg, var(--luna-darkest), var(--luna-medium));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.intro-text {
  font-size: 1.15rem;
  line-height: 1.8;
  color: var(--text-primary);
  max-width: 700px;
  margin: 0 auto;
}

.navigation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.nav-card {
  background: #fff;
  border-radius: 20px;
  padding: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
  cursor: pointer;
  border: 1px solid rgba(167, 235, 242, 0.4);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(1, 28, 64, 0.1);
  border-color: var(--luna-medium);
}

.nav-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, var(--luna-light), var(--luna-medium));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-card:hover::before {
  opacity: 1;
}

.card-icon {
  font-size: 2.5rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(167, 235, 242, 0.2);
  border-radius: 16px;
  flex-shrink: 0;
}

.card-content {
  flex: 1;
}

.card-content h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--luna-darkest);
  margin: 0 0 8px 0;
}

.card-content p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
}

.card-arrow {
  font-size: 1.5rem;
  color: var(--luna-light);
  font-weight: bold;
  transition: transform 0.3s ease;
}

.nav-card:hover .card-arrow {
  transform: translateX(5px);
  color: var(--luna-medium);
}

@media (max-width: 768px) {
  .navigation-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-section {
    padding: 40px 20px;
  }
  
  .hero-section h1 {
    font-size: 2rem;
  }
}
</style>
