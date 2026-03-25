<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
axios.defaults.withCredentials = true

const musicWorks = ref([])
const loading = ref(true)
const error = ref(null)

const fetchMusicWorks = async () => {
  try {
    const isProd = import.meta.env.PROD
    const isDevPort = window.location.port === '5173'
    const hostname = window.location.hostname
    const isPublicIP = hostname.startsWith('8.') || (hostname !== '127.0.0.1' && hostname !== 'localhost' && !hostname.startsWith('192.168.'))

    let finalUrl = '/api/music/works/'
    if (!isProd || isDevPort) {
        finalUrl = `http://${hostname}:8000/api/music/works/`
    }
    if (isPublicIP && isDevPort) {
       finalUrl = `http://${hostname}:8000/api/music/works/`
    }

    const response = await axios.get(finalUrl)
    
    // Process URLs to be absolute if needed
    musicWorks.value = response.data.map(work => {
      let cover = work.cover_image
      let audio = work.audio_file
      let video = work.video_file
      
      if (cover && !cover.startsWith('http')) {
        cover = (!isProd || isDevPort) ? `http://${hostname}:8000${cover}` : cover
      }
      
      if (audio && !audio.startsWith('http')) {
        audio = (!isProd || isDevPort) ? `http://${hostname}:8000${audio}` : audio
      }

      if (video && !video.startsWith('http')) {
        video = (!isProd || isDevPort) ? `http://${hostname}:8000${video}` : video
      }
      
      return { ...work, cover_image: cover, audio_file: audio, video_file: video }
    })
  } catch (err) {
    error.value = '无法加载音乐作品，请稍后再试。'
    console.error('API Error:', err)
  } finally {
    loading.value = false
  }
}

const audioWorks = computed(() => {
  return musicWorks.value.filter(work => work.work_type === 'audio')
})

const videoWorks = computed(() => {
  return musicWorks.value.filter(work => work.work_type === 'video')
})

const photoWorks = computed(() => {
  return musicWorks.value.filter(work => work.work_type === 'photo')
})

// Modal State
const isModalOpen = ref(false)
const currentVideoWork = ref(null)
const isPhotoModalOpen = ref(false)
const currentPhotoWork = ref(null)

const openVideoModal = (work) => {
  if (work.video_file) {
    currentVideoWork.value = work
    isModalOpen.value = true
    document.body.style.overflow = 'hidden' // Prevent background scrolling
  } else if (work.video_url) {
    window.open(work.video_url, '_blank')
  }
}

const closeVideoModal = () => {
  isModalOpen.value = false
  currentVideoWork.value = null
  document.body.style.overflow = '' // Restore scrolling
}

const openPhotoModal = (work) => {
  if (work.cover_image) {
    currentPhotoWork.value = work
    isPhotoModalOpen.value = true
    document.body.style.overflow = 'hidden'
  }
}

const closePhotoModal = () => {
  isPhotoModalOpen.value = false
  currentPhotoWork.value = null
  document.body.style.overflow = ''
}

onMounted(() => {
  fetchMusicWorks()
})
</script>

<template>
  <div class="music-space-container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="musicWorks.length === 0" class="empty-state">
      暂无音乐作品，敬请期待！
    </div>
    
    <div v-else class="content-wrapper">
      <!-- 原创音乐 Section -->
      <section v-if="audioWorks.length > 0" class="work-section">
        <div class="section-header">
          <h2>部分原创音乐</h2>
          <p class="section-desc">木有技巧，全是感情</p>
        </div>
        
        <div class="works-grid">
          <div v-for="work in audioWorks" :key="work.id" class="work-card">
            <div class="cover-wrapper">
              <img v-if="work.cover_image" :src="work.cover_image" :alt="work.title" class="cover-image" />
              <div v-else class="cover-placeholder">
                <span class="music-icon">🎵</span>
              </div>
            </div>
            
            <div class="work-content">
              <h3>{{ work.title }}</h3>
              <p class="description">{{ work.description }}</p>
              
              <div class="media-player">
                <audio v-if="work.audio_file" controls class="audio-player">
                  <source :src="work.audio_file" type="audio/mpeg">
                  您的浏览器不支持 audio 元素。
                </audio>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 演出视频 Section -->
      <section v-if="videoWorks.length > 0" class="work-section">
        <div class="section-header">
          <h2>部分演出视频</h2>
          <p class="section-desc">怀念跟兄弟们一起玩儿音乐的日子啊……</p>
        </div>
        
        <div class="works-grid">
          <div 
            v-for="work in videoWorks" 
            :key="work.id" 
            class="work-card video-card-interactive"
            @click="openVideoModal(work)"
          >
            <div class="cover-wrapper">
              <img v-if="work.cover_image" :src="work.cover_image" :alt="work.title" class="cover-image" />
              <div v-else class="cover-placeholder">
                <span class="music-icon">🎸</span>
              </div>
              <div class="play-overlay">
                <span class="play-icon">▶️</span>
              </div>
            </div>
            
            <div class="work-content">
              <h3>{{ work.title }}</h3>
              <p class="description">{{ work.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 演出照片 Section -->
      <section v-if="photoWorks.length > 0" class="work-section">
        <div class="section-header">
          <h2>部分演出照片</h2>
          <p class="section-desc">一些珍贵的舞台回忆，定格在这些瞬间。</p>
        </div>
        
        <div class="works-grid">
          <div 
            v-for="work in photoWorks" 
            :key="work.id" 
            class="work-card video-card-interactive"
            @click="openPhotoModal(work)"
          >
            <div class="cover-wrapper">
              <img v-if="work.cover_image" :src="work.cover_image" :alt="work.title" class="cover-image" />
              <div v-else class="cover-placeholder">
                <span class="music-icon">📷</span>
              </div>
              <div class="play-overlay">
                <span class="play-icon">🔍</span>
              </div>
            </div>
            
            <div class="work-content">
              <h3>{{ work.title }}</h3>
              <p class="description">{{ work.description }}</p>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Video Modal Overlay -->
    <transition name="modal-fade">
      <div v-if="isModalOpen" class="video-modal-overlay" @click.self="closeVideoModal">
        <div class="video-modal-content">
          <button class="close-modal-btn" @click="closeVideoModal">×</button>
          <div class="modal-header">
            <h3>{{ currentVideoWork?.title }}</h3>
          </div>
          <div class="modal-body">
            <video 
              v-if="currentVideoWork?.video_file" 
              controls 
              autoplay
              class="modal-video-player"
            >
              <source :src="currentVideoWork.video_file" type="video/mp4">
              您的浏览器不支持 video 元素。
            </video>
          </div>
        </div>
      </div>
    </transition>

    <!-- Photo Modal Overlay -->
    <transition name="modal-fade">
      <div v-if="isPhotoModalOpen" class="video-modal-overlay" @click.self="closePhotoModal">
        <div class="photo-modal-content">
          <button class="close-modal-btn" @click="closePhotoModal">×</button>
          <img 
            v-if="currentPhotoWork?.cover_image" 
            :src="currentPhotoWork.cover_image" 
            :alt="currentPhotoWork.title" 
            class="modal-photo-img"
          />
          <div class="photo-caption" v-if="currentPhotoWork?.title">
            {{ currentPhotoWork.title }}
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.music-space-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 0;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 60px;
}

.work-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.section-header {
  border-left: 5px solid var(--luna-medium);
  padding-left: 15px;
}

.section-header h2 {
  font-size: 2rem;
  font-weight: 800;
  margin: 0 0 10px 0;
  color: var(--luna-darkest);
}

.section-desc {
  font-size: 1.05rem;
  color: var(--text-secondary);
  margin: 0;
}

.loading, .error, .empty-state {
  text-align: center;
  padding: 60px;
  font-size: 1.2rem;
  color: var(--text-secondary);
  background: #fff;
  border-radius: var(--card-radius);
  border: 1px solid var(--card-border);
}

.works-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 30px;
}

.work-card {
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(1, 28, 64, 0.08);
  border: 1px solid rgba(167, 235, 242, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}

.work-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(1, 28, 64, 0.15);
  border-color: var(--luna-medium);
}

.cover-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  background: var(--luna-lightest);
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, rgba(167, 235, 242, 0.3), rgba(38, 101, 140, 0.1));
}

.music-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.type-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--luna-darkest);
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.work-content {
  padding: 25px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.work-content h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--luna-darkest);
  margin: 0 0 10px 0;
}

.description {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 20px 0;
  flex: 1;
}

.media-player {
  margin-top: auto;
  width: 100%;
}

.audio-player {
  width: 100%;
  height: 40px;
  outline: none;
}

.audio-player::-webkit-media-controls-panel {
  background-color: var(--luna-lightest);
}

.video-player {
  width: 100%;
  border-radius: 12px;
  outline: none;
  background: #000;
  max-height: 200px;
  object-fit: contain;
}

.video-link-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, var(--luna-dark), var(--luna-medium));
  color: #fff;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.video-link-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 5px 15px rgba(38, 101, 140, 0.3);
}

/* Video Card Interactive Styles */
.video-card-interactive {
  cursor: pointer;
}

.video-card-interactive .cover-wrapper {
  overflow: hidden;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.play-icon {
  font-size: 3.5rem;
  color: #fff;
  filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));
  transform: scale(0.8);
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.video-card-interactive:hover .play-overlay {
  opacity: 1;
}

.video-card-interactive:hover .play-icon {
  transform: scale(1);
}

/* Video Modal Styles */
.video-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(1, 28, 64, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
}

.video-modal-content {
  background: #000;
  width: 100%;
  max-width: 1000px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  position: relative;
  display: flex;
  flex-direction: column;
}

.modal-header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  padding: 15px 20px;
  background: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent);
  z-index: 2;
  pointer-events: none;
}

.modal-header h3 {
  color: #fff;
  margin: 0;
  font-size: 1.2rem;
  font-weight: 500;
  text-shadow: 0 2px 4px rgba(0,0,0,0.8);
}

.close-modal-btn {
  position: absolute;
  top: 15px;
  right: 20px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: #fff;
  font-size: 1.5rem;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 3;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
}

.close-modal-btn:hover {
  background: rgba(255, 255, 255, 0.4);
  transform: rotate(90deg);
}

.modal-body {
  width: 100%;
  background: #000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-video-player {
  width: 100%;
  max-height: 80vh;
  outline: none;
}

/* Photo Modal Styles */
.photo-modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.modal-photo-img {
  max-width: 100%;
  max-height: 85vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.photo-caption {
  margin-top: 15px;
  color: #fff;
  font-size: 1.2rem;
  font-weight: 500;
  text-shadow: 0 2px 4px rgba(0,0,0,0.8);
  background: rgba(0, 0, 0, 0.6);
  padding: 8px 20px;
  border-radius: 20px;
  backdrop-filter: blur(4px);
}

/* Modal Transition */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-active .video-modal-content,
.modal-fade-leave-active .video-modal-content {
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .video-modal-content {
  transform: scale(0.9) translateY(20px);
}

.modal-fade-leave-to .video-modal-content {
  transform: scale(0.95) translateY(-20px);
}

@media (max-width: 768px) {
  .works-grid {
    grid-template-columns: 1fr;
  }
}
</style>
