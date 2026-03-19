<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const avatarUrl = ref('')

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

const fetchAvatar = async () => {
  try {
    const isProd = import.meta.env.PROD
    const isDevPort = window.location.port === '5173'
    const hostname = window.location.hostname
    const isPublicIP = hostname.startsWith('8.') || (hostname !== '127.0.0.1' && hostname !== 'localhost' && !hostname.startsWith('192.168.'))

    let finalUrl = '/api/resume/'
    if (!isProd || isDevPort) {
        finalUrl = `http://${hostname}:8000/api/resume/`
    }
    if (isPublicIP && isDevPort) {
       finalUrl = `http://${hostname}:8000/api/resume/`
    }

    const response = await axios.get(finalUrl)
    if (response.data && response.data.basic_info && response.data.basic_info.avatar) {
      let url = response.data.basic_info.avatar
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        if (!isProd || isDevPort) {
          url = `http://${hostname}:8000${url}`
        }
      }
      avatarUrl.value = url
    }
  } catch (err) {
    console.error('Failed to fetch avatar:', err)
  }
}

onMounted(() => {
  fetchAvatar()
})
</script>

<template>
  <div class="home-container">
    <section class="hero-section">
      <div class="dynamic-intro-wrapper">
        <!-- Concentric Orbits Background -->
        <div class="orbit-container">
          <div class="orbit orbit-1">
            <div class="orbit-item" style="--angle: 0deg;">
              <div class="orbit-content icon-box">
                <img src="https://upload.wikimedia.org/wikipedia/commons/9/95/Vue.js_Logo_2.svg" alt="Vue" />
              </div>
            </div>
            <div class="orbit-item" style="--angle: 180deg;">
              <div class="orbit-content dot-orange"></div>
            </div>
          </div>
          
          <div class="orbit orbit-2">
            <div class="orbit-item" style="--angle: 90deg;">
              <div class="orbit-content icon-box">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" />
              </div>
            </div>
            <div class="orbit-item" style="--angle: 270deg;">
              <div class="orbit-content dot-blue"></div>
            </div>
          </div>
          
          <div class="orbit orbit-3">
            <div class="orbit-item" style="--angle: 45deg;">
              <div class="orbit-content icon-box">
                <img src="https://upload.wikimedia.org/wikipedia/commons/3/35/Tux.svg" alt="Linux" />
              </div>
            </div>
            <div class="orbit-item" style="--angle: 225deg;">
              <div class="orbit-content dot-orange-large"></div>
            </div>
          </div>
        </div>

        <!-- Avatar Layer -->
        <div class="avatar-layer">
          <div class="avatar-container">
            <img v-if="avatarUrl" :src="avatarUrl" alt="李佳" class="avatar-img" />
            <div v-else class="avatar-placeholder">
              <span>LJ</span>
            </div>
          </div>
        </div>

        <!-- Central Intro Card -->
        <div class="intro-card">
          <div class="card-header">
            <span class="label-text">My name is:</span>
            <h1 class="name-text">李 佳</h1>
          </div>
          <div class="divider"></div>
          <div class="card-body">
            <span class="label-text">I'm a:</span>
            <ul class="role-list">
              <li>资深云运维工程师 (SRE)</li>
              <li>独立全栈开发者</li>
              <li>系统架构设计者</li>
              <li>十年+IT行业老兵</li>
              <li>技术探索者</li>
            </ul>
          </div>
        </div>
      </div>
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
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  position: relative;
  overflow: visible;
}

.dynamic-intro-wrapper {
  position: relative;
  width: 100%;
  max-width: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 450px;
}

/* Orbit Animations & Layout */
.orbit-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 500px;
  height: 500px;
  pointer-events: none;
  z-index: 0;
}

.orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 1px dashed rgba(167, 235, 242, 0.6);
  border-radius: 50%;
  animation: spin linear infinite;
}

.orbit-1 {
  width: 280px;
  height: 280px;
  animation-duration: 25s;
}

.orbit-2 {
  width: 380px;
  height: 380px;
  animation-duration: 35s;
  animation-direction: reverse;
}

.orbit-3 {
  width: 480px;
  height: 480px;
  animation-duration: 45s;
}

@keyframes spin {
  100% {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

.orbit-item {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  transform: translate(-50%, -50%) rotate(var(--angle));
}

.orbit-content {
  position: absolute;
  top: -15px; /* Adjust based on icon size */
  left: 50%;
  transform: translateX(-50%);
  /* Counter spin */
  animation: counter-spin linear infinite;
}

.orbit-1 .orbit-content { animation-duration: 25s; }
.orbit-2 .orbit-content { animation-duration: 35s; animation-direction: reverse; }
.orbit-3 .orbit-content { animation-duration: 45s; }

@keyframes counter-spin {
  100% {
    transform: translateX(-50%) rotate(-360deg);
  }
}

.icon-box {
  width: 40px;
  height: 40px;
  background: #fff;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  top: -20px;
}

.icon-box img {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.dot-orange {
  width: 12px;
  height: 12px;
  background-color: #ff9800;
  border-radius: 50%;
  top: -6px;
}

.dot-blue {
  width: 10px;
  height: 10px;
  background-color: #03a9f4;
  border-radius: 50%;
  top: -5px;
}

.dot-orange-large {
  width: 24px;
  height: 24px;
  background-color: #ff9800;
  border-radius: 50%;
  top: -12px;
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.4);
}

/* Avatar Layer */
.avatar-layer {
  position: absolute;
  left: -20px;
  bottom: 0px;
  z-index: 2;
}

.avatar-container {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  border: 4px solid #fff;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  background: var(--luna-light);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 2rem;
  font-weight: bold;
  color: #fff;
}

/* Central Card */
.intro-card {
  position: relative;
  z-index: 1;
  background: #fff;
  border-radius: 16px;
  padding: 40px;
  width: 380px;
  box-shadow: 0 20px 40px rgba(1, 28, 64, 0.08);
  border: 1px solid rgba(167, 235, 242, 0.3);
}

.card-header {
  margin-bottom: 20px;
}

.label-text {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--luna-dark);
  display: block;
  margin-bottom: 8px;
}

.name-text {
  font-size: 3rem;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(135deg, #ff9800, #ff5722);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  line-height: 1.2;
}

.divider {
  height: 2px;
  background: var(--luna-darkest);
  width: 100%;
  margin: 20px 0;
}

.card-body {
  text-align: right;
}

.card-body .label-text {
  text-align: left;
}

.role-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.role-list li {
  font-size: 1.05rem;
  color: var(--luna-darkest);
  font-weight: 500;
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
