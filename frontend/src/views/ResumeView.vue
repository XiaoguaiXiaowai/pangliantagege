<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const resumeData = ref(null)
const loading = ref(true)
const error = ref(null)

const activeSection = ref('')

const sections = [
  { id: 'basic-info', title: '基本信息' },
  { id: 'skills', title: '技能栈' },
  { id: 'experience', title: '工作经历' },
  { id: 'projects', title: '项目经历' },
  { id: 'education', title: '教育背景' },
]

const fetchResumeData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/resume/')
    resumeData.value = response.data
  } catch (err) {
    error.value = '无法加载简历数据，请稍后再试。'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const scrollToSection = (id) => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

// Intersection Observer for scroll spy
onMounted(() => {
  fetchResumeData()

  const observer = new IntersectionObserver((entries) => {
    // Find the entry that is intersecting and has the largest intersection ratio
    // Or simply the first one that is intersecting
    const visibleEntry = entries.find(entry => entry.isIntersecting)
    if (visibleEntry) {
      activeSection.value = visibleEntry.target.id
    }
  }, {
    root: null,
    rootMargin: '-20% 0px -60% 0px', // Adjust detection area
    threshold: 0
  })

  sections.forEach((section) => {
    const el = document.getElementById(section.id)
    if (el) observer.observe(el)
  })
})
</script>

<template>
  <div class="resume-container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="content-wrapper">
      <!-- Sidebar -->
      <aside class="sidebar">
        <nav>
          <ul>
            <li 
              v-for="section in sections" 
              :key="section.id"
              :class="{ active: activeSection === section.id }"
              @click="scrollToSection(section.id)"
            >
              {{ section.title }}
            </li>
          </ul>
        </nav>
        <div class="download-pdf">
          <a href="#" class="btn-pdf">下载 PDF 简历</a>
        </div>
      </aside>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Basic Info -->
        <section id="basic-info" class="section-card">
          <div class="profile-header" v-if="resumeData.basic_info">
            <div class="avatar-container" v-if="resumeData.basic_info.avatar">
              <img :src="resumeData.basic_info.avatar" alt="Avatar" class="avatar" />
            </div>
            <div class="info-text">
              <h1>{{ resumeData.basic_info.name }}</h1>
              <h2>{{ resumeData.basic_info.title }}</h2>
              <p class="contact-info">
                <span>📍 {{ resumeData.basic_info.location }}</span>
                <span>📧 {{ resumeData.basic_info.email }}</span>
                <span v-if="resumeData.basic_info.phone">📞 {{ resumeData.basic_info.phone }}</span>
              </p>
              <p class="summary">{{ resumeData.basic_info.summary }}</p>
            </div>
          </div>
          <div v-else class="empty-state">暂无基本信息</div>
        </section>

        <!-- Skills -->
        <section id="skills" class="section-card">
          <h3>🛠 技能栈</h3>
          <div class="skills-grid" v-if="resumeData.skills && resumeData.skills.length">
            <div v-for="skill in resumeData.skills" :key="skill.id" class="skill-item">
              <span class="skill-name">{{ skill.name }}</span>
              <div class="skill-bar">
                <div class="skill-level" :style="{ width: skill.level + '%' }"></div>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">暂无技能信息</div>
        </section>

        <!-- Experience -->
        <section id="experience" class="section-card">
          <h3>💼 工作经历</h3>
          <div class="timeline" v-if="resumeData.experiences && resumeData.experiences.length">
            <div v-for="exp in resumeData.experiences" :key="exp.id" class="timeline-item">
              <div class="timeline-header">
                <span class="company">{{ exp.company }}</span>
                <span class="date">{{ exp.start_date }} - {{ exp.end_date || '至今' }}</span>
              </div>
              <div class="position">{{ exp.position }}</div>
              <p class="description">{{ exp.description }}</p>
            </div>
          </div>
           <div v-else class="empty-state">暂无工作经历</div>
        </section>

        <!-- Projects -->
        <section id="projects" class="section-card">
          <h3>🚀 项目经历</h3>
          <div class="projects-list" v-if="resumeData.projects && resumeData.projects.length">
            <div v-for="project in resumeData.projects" :key="project.id" class="project-item">
              <div class="project-header">
                <span class="project-name">{{ project.name }}</span>
                <span class="role-badge">{{ project.role }}</span>
              </div>
              <p class="project-date" v-if="project.start_date">{{ project.start_date }} - {{ project.end_date || '至今' }}</p>
              <p class="project-desc">{{ project.description }}</p>
              <div class="tech-stack" v-if="project.technologies">
                <span v-for="tech in project.technologies.split(',')" :key="tech" class="tech-tag">
                  {{ tech.trim() }}
                </span>
              </div>
              <a v-if="project.link" :href="project.link" target="_blank" class="project-link">查看项目</a>
            </div>
          </div>
          <div v-else class="empty-state">暂无项目经历</div>
        </section>

        <!-- Education -->
        <section id="education" class="section-card">
          <h3>🎓 教育背景</h3>
          <div class="education-list" v-if="resumeData.educations && resumeData.educations.length">
            <div v-for="edu in resumeData.educations" :key="edu.id" class="edu-item">
              <div class="edu-header">
                <span class="school">{{ edu.school }}</span>
                <span class="date">{{ edu.start_date }} - {{ edu.end_date || '至今' }}</span>
              </div>
              <div class="degree">{{ edu.degree }} - {{ edu.major }}</div>
            </div>
          </div>
          <div v-else class="empty-state">暂无教育背景</div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.resume-container {
  display: flex;
  min-height: 80vh;
  position: relative;
}

.content-wrapper {
  display: flex;
  width: 100%;
  gap: 40px;
}

/* Sidebar */
.sidebar {
  width: 200px;
  position: sticky;
  top: 20px;
  height: fit-content;
  border-right: 1px solid #eee;
  padding-right: 20px;
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
}

.sidebar nav li {
  padding: 10px 15px;
  cursor: pointer;
  border-left: 3px solid transparent;
  transition: all 0.3s;
  color: #666;
}

.sidebar nav li:hover,
.sidebar nav li.active {
  border-left-color: #42b983;
  color: #42b983;
  background-color: #f9f9f9;
  font-weight: bold;
}

.download-pdf {
  margin-top: 30px;
}

.btn-pdf {
  display: block;
  text-align: center;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  font-size: 0.9rem;
}

.btn-pdf:hover {
  background-color: #3aa876;
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.section-card {
  scroll-margin-top: 80px; /* Offset for sticky header if any, or just spacing */
}

h3 {
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 20px;
  color: #333;
  position: sticky;
  top: 0;
  background-color: #fff;
  z-index: 10;
  padding-top: 10px;
}

/* Basic Info */
.profile-header {
  display: flex;
  gap: 30px;
  align-items: center;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #fff;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.info-text h1 {
  margin: 0;
  font-size: 2.5rem;
  color: #333;
}

.info-text h2 {
  margin: 5px 0 15px;
  font-size: 1.2rem;
  color: #666;
  font-weight: normal;
}

.contact-info {
  display: flex;
  gap: 15px;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 15px;
}

.summary {
  line-height: 1.6;
  color: #555;
}

/* Skills */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.skill-item {
  margin-bottom: 10px;
}

.skill-name {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.skill-bar {
  height: 8px;
  background-color: #eee;
  border-radius: 4px;
  overflow: hidden;
}

.skill-level {
  height: 100%;
  background-color: #42b983;
  border-radius: 4px;
}

/* Timeline (Experience & Education) */
.timeline-item, .edu-item, .project-item {
  margin-bottom: 30px;
  padding-left: 20px;
  border-left: 2px solid #eee;
  position: relative;
}

.timeline-item::before, .edu-item::before, .project-item::before {
  content: '';
  position: absolute;
  left: -6px;
  top: 5px;
  width: 10px;
  height: 10px;
  background-color: #42b983;
  border-radius: 50%;
}

.timeline-header, .edu-header, .project-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.company, .school, .project-name {
  font-weight: bold;
  font-size: 1.1rem;
}

.date, .project-date {
  color: #888;
  font-size: 0.9rem;
}

.position, .degree {
  color: #555;
  margin-bottom: 10px;
  font-weight: 500;
}

.description, .project-desc {
  color: #666;
  line-height: 1.6;
}

/* Projects */
.role-badge {
  background-color: #e0f2f1;
  color: #00695c;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
  margin-left: 10px;
}

.tech-stack {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.tech-tag {
  background-color: #f5f5f5;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #666;
}

.project-link {
  display: inline-block;
  margin-top: 10px;
  color: #42b983;
  font-size: 0.9rem;
}

/* Loading & Error */
.loading, .error, .empty-state {
  text-align: center;
  padding: 50px;
  color: #888;
}

.error {
  color: #e53935;
}

/* Responsive */
@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    position: static;
    border-right: none;
    border-bottom: 1px solid #eee;
    padding-bottom: 20px;
    margin-bottom: 20px;
  }

  .sidebar nav ul {
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
    gap: 10px;
  }

  .sidebar nav li {
    border-left: none;
    border-bottom: 3px solid transparent;
  }

  .sidebar nav li:hover,
  .sidebar nav li.active {
    border-left: none;
    border-bottom-color: #42b983;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .contact-info {
    justify-content: center;
    flex-wrap: wrap;
  }
}
</style>
