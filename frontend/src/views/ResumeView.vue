<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import MagicCard from '../components/MagicCard.vue'
import Marquee from '../components/Marquee.vue'

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
  { id: 'languages', title: '语言能力' },
  { id: 'certificates', title: '证书' },
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

// Split skills for Marquee rows
const firstRowSkills = computed(() => {
  if (!resumeData.value || !resumeData.value.skills) return []
  // If fewer than 4 skills, just return all for first row to ensure it's not empty
  if (resumeData.value.skills.length < 4) return resumeData.value.skills
  const mid = Math.ceil(resumeData.value.skills.length / 2)
  return resumeData.value.skills.slice(0, mid)
})

const secondRowSkills = computed(() => {
  if (!resumeData.value || !resumeData.value.skills) return []
  if (resumeData.value.skills.length < 4) return resumeData.value.skills // Duplicate for second row if few
  const mid = Math.ceil(resumeData.value.skills.length / 2)
  return resumeData.value.skills.slice(mid)
})

// Intersection Observer for scroll spy
onMounted(() => {
  fetchResumeData()

  const observer = new IntersectionObserver((entries) => {
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
          <a href="/media/resume/resume.pdf" class="btn-pdf" target="_blank" download>下载 PDF 简历</a>
        </div>
      </aside>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Basic Info -->
        <section id="basic-info" class="section-card">
          <div class="profile-header" v-if="resumeData && resumeData.basic_info">
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

        <!-- Skills (Marquee) -->
        <section id="skills" class="section-card">
          <h3>🛠 技能栈</h3>
          <div class="skills-marquee-container" v-if="resumeData && resumeData.skills && resumeData.skills.length">
            <Marquee pauseOnHover duration="40s" class="mb-4">
              <div v-for="skill in firstRowSkills" :key="skill.id" class="skill-card">
                <span class="skill-name">{{ skill.name }}</span>
                <div class="skill-bar">
                  <div class="skill-level" :style="{ width: skill.level + '%' }"></div>
                </div>
              </div>
            </Marquee>
            <Marquee reverse pauseOnHover duration="40s">
              <div v-for="skill in secondRowSkills" :key="skill.id" class="skill-card">
                <span class="skill-name">{{ skill.name }}</span>
                <div class="skill-bar">
                  <div class="skill-level" :style="{ width: skill.level + '%' }"></div>
                </div>
              </div>
            </Marquee>
          </div>
          <div v-else class="empty-state">暂无技能信息</div>
        </section>

        <!-- Experience -->
        <section id="experience" class="section-card">
          <h3>💼 工作经历</h3>
          <div class="timeline" v-if="resumeData && resumeData.experiences && resumeData.experiences.length">
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

        <!-- Projects (MagicCard) -->
        <section id="projects" class="section-card">
          <h3>🚀 项目经历</h3>
          <div class="projects-grid" v-if="resumeData && resumeData.projects && resumeData.projects.length">
            <MagicCard v-for="project in resumeData.projects" :key="project.id" class="project-card">
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
            </MagicCard>
          </div>
          <div v-else class="empty-state">暂无项目经历</div>
        </section>

        <!-- Education -->
        <section id="education" class="section-card">
          <h3>🎓 教育背景</h3>
          <div class="education-list" v-if="resumeData && resumeData.educations && resumeData.educations.length">
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

        <!-- Languages -->
        <section id="languages" class="section-card">
          <h3>🌐 语言能力</h3>
          <div class="language-list" v-if="resumeData && resumeData.languages && resumeData.languages.length">
            <div v-for="lang in resumeData.languages" :key="lang.id" class="language-item">
              <span class="language-name">{{ lang.name }}</span>
              <span class="language-proficiency">{{ lang.proficiency }}</span>
            </div>
          </div>
          <div v-else class="empty-state">暂无语言能力信息</div>
        </section>

        <!-- Certificates -->
        <section id="certificates" class="section-card">
          <h3>📜 证书</h3>
          <div class="certificate-list" v-if="resumeData && resumeData.certificates && resumeData.certificates.length">
            <div v-for="cert in resumeData.certificates" :key="cert.id" class="certificate-item">
              <div class="certificate-header">
                <span class="certificate-name">{{ cert.name }}</span>
                <span class="certificate-date">{{ cert.date }}</span>
              </div>
              <div class="certificate-issuer">{{ cert.issuer }}</div>
              <a v-if="cert.link" :href="cert.link" target="_blank" class="certificate-link">查看证书</a>
            </div>
          </div>
          <div v-else class="empty-state">暂无证书信息</div>
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
  overflow: hidden; /* Prevent marquee overflow */
}

.section-card {
  scroll-margin-top: 80px; 
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

/* Skills (Marquee) */
.skills-marquee-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.mb-4 {
  margin-bottom: 1rem;
}

.skill-card {
  width: 200px;
  padding: 15px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.skill-name {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  text-align: center;
}

.skill-bar {
  height: 6px;
  background-color: #eee;
  border-radius: 3px;
  overflow: hidden;
}

.skill-level {
  height: 100%;
  background-color: #42b983;
  border-radius: 3px;
}

/* Projects (MagicCard Grid) */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.project-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.project-name {
  font-weight: bold;
  font-size: 1.1rem;
  color: #333;
}

.role-badge {
  background-color: #e8f5e9;
  color: #42b983;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  white-space: nowrap;
  margin-left: 10px;
}

.project-date {
  font-size: 0.85rem;
  color: #999;
  margin-bottom: 10px;
}

.project-desc {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 15px;
  line-height: 1.5;
  flex-grow: 1;
}

.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.tech-tag {
  background-color: #f0f0f0;
  color: #666;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.project-link {
  display: inline-block;
  color: #42b983;
  text-decoration: none;
  font-weight: 500;
  margin-top: auto;
}

.project-link:hover {
  text-decoration: underline;
}

/* Timeline (Experience & Education) */
.timeline-item, .edu-item {
  margin-bottom: 30px;
  padding-left: 20px;
  border-left: 2px solid #eee;
  position: relative;
}

.timeline-item::before, .edu-item::before {
  content: '';
  position: absolute;
  left: -6px;
  top: 5px;
  width: 10px;
  height: 10px;
  background-color: #42b983;
  border-radius: 50%;
}

.timeline-header, .edu-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.company, .school {
  font-weight: bold;
  font-size: 1.1rem;
}

.date {
  color: #888;
}

/* Language & Certificate */
.language-list, .certificate-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.language-item {
  display: flex;
  justify-content: space-between;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.certificate-item {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.certificate-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.certificate-name {
  font-weight: bold;
}

.certificate-date {
  color: #888;
  font-size: 0.9rem;
}

.certificate-link {
  color: #42b983;
  text-decoration: none;
  font-size: 0.9rem;
}
</style>
