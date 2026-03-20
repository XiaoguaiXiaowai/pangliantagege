<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
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
    description: '查看我的详细工作经历、项目经验以及技能栈。',
    path: '/resume',
    icon: '💼'
  },
  {
    title: '音乐小空间',
    description: '记录我的音乐作品和一些演出视频，音乐是我生活中的重要部分。',
    path: '/music',
    icon: '🎸'
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
    icon: '🛸'
  },
  {
    title: '小工具',
    description: '我开发的一些实用小工具，旨在提高日常工作效率。',
    path: '/tools',
    icon: '🛠️'
  },
  {
    title: '其他',
    description: '可以看着背景的两个小球发呆。',
    path: '/talents',
    icon: '🎱'
  }
]

const names = ['李 佳', '胖脸她哥哥', 'Jimmy Li']
const currentNameIndex = ref(0)
let nameInterval = null

// Card 3D Tilt Effect
const cardRef = ref(null)
const cardRotation = ref({ x: 0, y: 0 })
const isHovering = ref(false)

const handleMouseMove = (e) => {
  if (!cardRef.value) return
  const card = cardRef.value
  const rect = card.getBoundingClientRect()
  
  // Calculate mouse position relative to the center of the card
  const x = e.clientX - rect.left - rect.width / 2
  const y = e.clientY - rect.top - rect.height / 2
  
  // Adjust sensitivity (divisor). Larger divisor = less tilt
  const sensitivityX = 20
  const sensitivityY = 20
  
  cardRotation.value = {
    x: -(y / sensitivityY),
    y: (x / sensitivityX)
  }
}

const handleMouseEnter = () => {
  isHovering.value = true
}

const handleMouseLeave = () => {
  isHovering.value = false
  // Reset rotation when mouse leaves
  cardRotation.value = { x: 0, y: 0 }
}

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
  nameInterval = setInterval(() => {
    currentNameIndex.value = (currentNameIndex.value + 1) % names.length
  }, 3000) // Change name every 3 seconds
})

onUnmounted(() => {
  if (nameInterval) {
    clearInterval(nameInterval)
  }
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
              <div class="orbit-content">
                <div class="orbit-counter" style="--angle: 0deg;">
                  <div class="icon-box icon-cloud"><span class="emoji-icon">⛅️</span></div>
                </div>
              </div>
            </div>
            <div class="orbit-item" style="--angle: 180deg;">
              <div class="orbit-content">
                <div class="orbit-counter" style="--angle: 180deg;">
                  <div class="dot-luna"></div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="orbit orbit-2">
            <div class="orbit-item" style="--angle: 90deg;">
              <div class="orbit-content">
                <div class="orbit-counter" style="--angle: 90deg;">
                  <div class="icon-box icon-ai"><span class="emoji-icon">🛸</span></div>
                </div>
              </div>
            </div>
            <div class="orbit-item" style="--angle: 210deg;">
              <div class="orbit-content">
                <div class="orbit-counter" style="--angle: 210deg;">
                  <div class="icon-box icon-music"><span class="emoji-icon">🎸</span></div>
                </div>
              </div>
            </div>
            <div class="orbit-item" style="--angle: 330deg;">
              <div class="orbit-content">
                <div class="orbit-counter" style="--angle: 330deg;">
                  <div class="dot-luna-small"></div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="orbit orbit-3">
            <div class="orbit-item" style="--angle: 45deg;">
              <div class="orbit-content">
                <div class="orbit-counter" style="--angle: 45deg;">
                  <div class="icon-box icon-tech"><span class="emoji-icon">💼</span></div>
                </div>
              </div>
            </div>
            <div class="orbit-item" style="--angle: 165deg;">
              <div class="orbit-content">
                <div class="orbit-counter" style="--angle: 165deg;">
                  <div class="icon-box icon-ops"><span class="emoji-icon">🛠️</span></div>
                </div>
              </div>
            </div>
            <div class="orbit-item" style="--angle: 285deg;">
              <div class="orbit-content">
                <div class="orbit-counter" style="--angle: 285deg;">
                  <div class="dot-luna-large"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Central Intro Card -->
        <div 
          class="intro-card"
          ref="cardRef"
          @mousemove="handleMouseMove"
          @mouseenter="handleMouseEnter"
          @mouseleave="handleMouseLeave"
          :style="{
            transform: `perspective(1000px) scale(${isHovering ? 1.05 : 1}) rotateX(${cardRotation.x}deg) rotateY(${cardRotation.y}deg)`,
            transition: isHovering ? 'transform 0.1s ease-out' : 'transform 0.5s ease-out'
          }"
        >
          <div class="card-header">
            <span class="label-text">My name is:</span>
            <div class="name-text-wrapper">
              <transition name="fade-slide" mode="out-in">
                <h1 :key="names[currentNameIndex]" class="name-text">{{ names[currentNameIndex] }}</h1>
              </transition>
            </div>
          </div>
          <div class="divider"></div>
          <div class="card-body">
            <span class="label-text">I'm a:</span>
            <ul class="role-list">
              <li>资深云架构运维工程师 (偏SRE)</li>
              <li>日语口语流利的项目经理</li>
              <li>AI增强型全栈开发者</li>
              <li>各种小工具的开发爱好者</li>
              <li>一脸好奇的AI技术探索者</li>
              <li>自娱自乐的独立音乐人</li>
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
  transform: translate(-50%, -50%) rotateX(65deg);
  width: 1350px;
  height: 1350px;
  pointer-events: none;
  z-index: 0;
  transform-style: preserve-3d;
}

.orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  border: 1.5px dashed rgba(167, 235, 242, 0.6);
  border-radius: 50%;
  transform-style: preserve-3d;
}

.orbit-1 {
  width: 780px;
  height: 780px;
  animation: spin-orbit 25s linear infinite;
}

.orbit-2 {
  width: 1020px;
  height: 1020px;
  animation: spin-orbit-reverse 35s linear infinite;
}

.orbit-3 {
  width: 1275px;
  height: 1275px;
  animation: spin-orbit 45s linear infinite;
}

@keyframes spin-orbit {
  0% { transform: translate(-50%, -50%) rotateZ(0deg); }
  100% { transform: translate(-50%, -50%) rotateZ(360deg); }
}

@keyframes spin-orbit-reverse {
  0% { transform: translate(-50%, -50%) rotateZ(0deg); }
  100% { transform: translate(-50%, -50%) rotateZ(-360deg); }
}

.orbit-item {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  transform: translate(-50%, -50%) rotateZ(var(--angle));
  transform-style: preserve-3d;
}

.orbit-content {
  position: absolute;
  top: 0;
  left: 50%;
  width: 0;
  height: 0;
  transform-style: preserve-3d;
}

.orbit-1 .orbit-content { animation: counter-spin-orbit 25s linear infinite; }
.orbit-2 .orbit-content { animation: counter-spin-orbit-reverse 35s linear infinite; }
.orbit-3 .orbit-content { animation: counter-spin-orbit 45s linear infinite; }

@keyframes counter-spin-orbit {
  0% { transform: rotateZ(0deg); }
  100% { transform: rotateZ(-360deg); }
}

@keyframes counter-spin-orbit-reverse {
  0% { transform: rotateZ(0deg); }
  100% { transform: rotateZ(360deg); }
}

.orbit-counter {
  position: absolute;
  top: 0;
  left: 0;
  transform-style: preserve-3d;
  transform: rotateZ(calc(var(--angle) * -1)) rotateX(-65deg);
}

.icon-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fff;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 6px 22px rgba(167, 235, 242, 0.4);
  border: 1.5px solid var(--luna-light);
}

.icon-cloud { width: 67.5px; height: 67.5px; font-size: 1.8rem; }
.icon-ai { width: 82.5px; height: 82.5px; font-size: 2.25rem; }
.icon-music { width: 52.5px; height: 52.5px; font-size: 1.5rem; }
.icon-tech { width: 97.5px; height: 97.5px; font-size: 2.7rem; }
.icon-ops { width: 60px; height: 60px; font-size: 1.65rem; }

.emoji-icon {
  line-height: 1;
}

.dot-luna {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  width: 21px; height: 21px; background-color: var(--luna-medium);
  border-radius: 50%; box-shadow: 0 0 15px var(--luna-medium);
}

.dot-luna-small {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  width: 15px; height: 15px; background-color: var(--luna-dark);
  border-radius: 50%; box-shadow: 0 0 12px var(--luna-dark);
}

.dot-luna-large {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  width: 30px; height: 30px; background-color: var(--luna-light);
  border-radius: 50%; box-shadow: 0 0 22px var(--luna-light);
}

/* Central Card */
.intro-card {
  position: relative;
  z-index: 1;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 20px;
  padding: 45px;
  width: 460px;
  box-shadow: 0 20px 40px rgba(1, 28, 64, 0.08);
  border: 1px solid rgba(167, 235, 242, 0.5);
}

.card-header {
  margin-bottom: 20px;
}

.label-text {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-secondary);
  display: block;
  margin-bottom: 8px;
}

.name-text-wrapper {
  height: 4.5rem; /* Fixed height to prevent layout shift during transition */
  display: flex;
  align-items: center;
}

.name-text {
  font-size: 3.5rem;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(135deg, var(--luna-darkest), var(--luna-medium));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  line-height: 1.2;
  letter-spacing: 2px;
}

/* Name Transition Effects */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.divider {
  height: 2px;
  background: linear-gradient(to right, var(--luna-darkest), var(--luna-light), transparent);
  width: 100%;
  margin: 25px 0;
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
  gap: 10px;
}

.role-list li {
  font-size: 1.1rem;
  color: var(--luna-darkest);
  font-weight: 600;
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
