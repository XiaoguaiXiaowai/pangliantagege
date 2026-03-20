<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

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

onMounted(() => {
  fetchMusicWorks()
})
</script>

<template>
  <div class="music-space-container">
    <div class="header-section">
      <h1>音乐小空间</h1>
      <p>这里记录了我的音乐作品和一些演出视频，音乐是我生活中的重要部分。</p>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="musicWorks.length === 0" class="empty-state">
      暂无音乐作品，敬请期待！
    </div>
    
    <div v-else class="works-grid">
      <div v-for="work in musicWorks" :key="work.id" class="work-card">
        <div class="cover-wrapper">
          <img v-if="work.cover_image" :src="work.cover_image" :alt="work.title" class="cover-image" />
          <div v-else class="cover-placeholder">
            <span class="music-icon">🎵</span>
          </div>
          <div class="type-badge">{{ work.work_type === 'audio' ? '音频' : '视频' }}</div>
        </div>
        
        <div class="work-content">
          <h3>{{ work.title }}</h3>
          <p class="description">{{ work.description }}</p>
          
          <div class="media-player">
            <!-- Audio Player -->
            <audio v-if="work.work_type === 'audio' && work.audio_file" controls class="audio-player">
              <source :src="work.audio_file" type="audio/mpeg">
              您的浏览器不支持 audio 元素。
            </audio>
            
            <!-- Video Player (Direct Upload) -->
            <video v-else-if="work.work_type === 'video' && work.video_file" controls class="video-player">
              <source :src="work.video_file" type="video/mp4">
              您的浏览器不支持 video 元素。
            </video>

            <!-- Video Link (Fallback to external URL like Bilibili) -->
            <a v-else-if="work.work_type === 'video' && work.video_url" :href="work.video_url" target="_blank" class="video-link-btn">
              <span>观看外部演出视频</span>
              <span class="icon">▶️</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.music-space-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px 0;
}

.header-section {
  text-align: center;
  margin-bottom: 50px;
}

.header-section h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 15px;
  background: linear-gradient(135deg, var(--luna-darkest), var(--luna-medium));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.header-section p {
  font-size: 1.1rem;
  color: var(--text-secondary);
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
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
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

@media (max-width: 768px) {
  .works-grid {
    grid-template-columns: 1fr;
  }
}
</style>