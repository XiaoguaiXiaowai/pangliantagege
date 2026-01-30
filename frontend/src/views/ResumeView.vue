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
  { id: 'basic-info', title: '关于我' },
  { id: 'skills', title: '技能' },
  { id: 'experience', title: '经历' },
  { id: 'projects', title: '项目' },
  { id: 'education', title: '教育' },
  { id: 'languages', title: '语言' },
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
    const offset = 100; // Adjust for sticky header
    const bodyRect = document.body.getBoundingClientRect().top;
    const elementRect = element.getBoundingClientRect().top;
    const elementPosition = elementRect - bodyRect;
    const offsetPosition = elementPosition - offset;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}

// Split skills for Marquee rows
const firstRowSkills = computed(() => {
  if (!resumeData.value || !resumeData.value.skills) return []
  if (resumeData.value.skills.length < 4) return resumeData.value.skills
  const mid = Math.ceil(resumeData.value.skills.length / 2)
  return resumeData.value.skills.slice(0, mid)
})

const secondRowSkills = computed(() => {
  if (!resumeData.value || !resumeData.value.skills) return []
  if (resumeData.value.skills.length < 4) return resumeData.value.skills 
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
    rootMargin: '-20% 0px -60% 0px', 
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
      <!-- Sidebar / Navigation Rail -->
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
          <a href="/media/resume/resume.pdf" class="btn-pdf" target="_blank" download>
            <span>↓</span> 简历 PDF
          </a>
        </div>
      </aside>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Basic Info (Hero Card) -->
        <section id="basic-info" class="section-card hero-card">
          <div class="profile-header" v-if="resumeData && resumeData.basic_info">
            <div class="avatar-container" v-if="resumeData.basic_info.avatar">
              <img :src="resumeData.basic_info.avatar" alt="Avatar" class="avatar" />
            </div>
            <div class="info-text">
              <h1>{{ resumeData.basic_info.name }}</h1>
              <h2>{{ resumeData.basic_info.title }}</h2>
              <p class="contact-info">
                <span>{{ resumeData.basic_info.location }}</span>
                <span class="dot">·</span>
                <span>{{ resumeData.basic_info.email }}</span>
                <span v-if="resumeData.basic_info.phone" class="dot">·</span>
                <span v-if="resumeData.basic_info.phone">{{ resumeData.basic_info.phone }}</span>
              </p>
              <p class="summary">{{ resumeData.basic_info.summary }}</p>
            </div>
          </div>
          <div v-else class="empty-state">暂无基本信息</div>
        </section>

        <!-- Skills (Marquee) -->
        <section id="skills" class="section-card">
          <h3>技能栈</h3>
          <div class="skills-marquee-container" v-if="resumeData && resumeData.skills && resumeData.skills.length">
            <Marquee pauseOnHover duration="40s" class="mb-4">
              <div v-for="skill in firstRowSkills" :key="skill.id" class="skill-pill">
                <span class="skill-name">{{ skill.name }}</span>
              </div>
            </Marquee>
            <Marquee reverse pauseOnHover duration="40s">
              <div v-for="skill in secondRowSkills" :key="skill.id" class="skill-pill">
                <span class="skill-name">{{ skill.name }}</span>
              </div>
            </Marquee>
          </div>
          <div v-else class="empty-state">暂无技能信息</div>
        </section>

        <!-- Experience -->
        <section id="experience" class="section-card">
          <h3>工作经历</h3>
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
          <h3>项目经历</h3>
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
              <a v-if="project.link" :href="project.link" target="_blank" class="project-link">查看项目 →</a>
            </MagicCard>
          </div>
          <div v-else class="empty-state">暂无项目经历</div>
        </section>

        <!-- Education -->
        <section id="education" class="section-card">
          <h3>教育背景</h3>
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
          <h3>语言能力</h3>
          <div class="grid-list" v-if="resumeData && resumeData.languages && resumeData.languages.length">
            <div v-for="lang in resumeData.languages" :key="lang.id" class="grid-item">
              <span class="grid-name">{{ lang.name }}</span>
              <span class="grid-value">{{ lang.proficiency }}</span>
            </div>
          </div>
          <div v-else class="empty-state">暂无语言能力信息</div>
        </section>

        <!-- Certificates -->
        <section id="certificates" class="section-card">
          <h3>证书</h3>
          <div class="grid-list" v-if="resumeData && resumeData.certificates && resumeData.certificates.length">
            <div v-for="cert in resumeData.certificates" :key="cert.id" class="grid-item certificate">
              <div class="cert-info">
                <span class="grid-name">{{ cert.name }}</span>
                <span class="grid-sub">{{ cert.issuer }}</span>
              </div>
              <span class="grid-date">{{ cert.date }}</span>
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
  gap: 50px;
}

/* Sidebar - Soft & Clean */
.sidebar {
  width: 180px;
  position: sticky;
  top: 100px;
  height: fit-content;
  padding-top: 20px;
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar nav li {
  padding: 10px 16px;
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.sidebar nav li:hover {
  background-color: rgba(255, 255, 255, 0.5);
  color: var(--color-blue);
}

.sidebar nav li.active {
  background-color: #fff;
  color: var(--color-purple);
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  font-weight: 600;
}

.download-pdf {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid rgba(0,0,0,0.03);
}

.btn-pdf {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: linear-gradient(135deg, var(--color-blue), var(--color-purple));
  color: #fff;
  border-radius: 16px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(139, 174, 182, 0.4);
}

.btn-pdf:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 174, 182, 0.5);
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.section-card {
  scroll-margin-top: 100px;
  background: var(--card-bg);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  padding: 40px;
  border: 1px solid var(--card-border);
  transition: transform 0.3s ease;
}

/* Hero Card (Basic Info) */
.hero-card {
  background: #fff;
}

h3 {
  font-size: 1.4rem;
  margin-bottom: 30px;
  color: #2c3e50;
  position: relative;
  display: inline-block;
}

h3::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 40px;
  height: 4px;
  background: linear-gradient(to right, var(--color-purple), var(--color-pink));
  border-radius: 2px;
}

/* Basic Info */
.profile-header {
  display: flex;
  gap: 40px;
  align-items: center;
}

.avatar {
  width: 140px;
  height: 140px;
  border-radius: 40px; /* Soft Squircle */
  object-fit: cover;
  box-shadow: 0 10px 30px rgba(139, 134, 190, 0.2);
  border: 4px solid #fff;
}

.info-text h1 {
  margin: 0 0 10px 0;
  font-size: 2.5rem;
  background: linear-gradient(135deg, #2c3e50, #4a4a4a);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 700;
}

.info-text h2 {
  margin: 0 0 20px 0;
  font-size: 1.2rem;
  color: var(--color-purple);
  font-weight: 500;
}

.contact-info {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 15px;
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.dot {
  color: var(--color-pink);
  font-weight: bold;
}

.summary {
  line-height: 1.8;
  color: var(--text-primary);
  font-size: 1.05rem;
}

/* Skills (Pills) */
.skills-marquee-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.skill-pill {
  padding: 10px 24px;
  background: #fff;
  border: 1px solid rgba(0,0,0,0.05);
  border-radius: 50px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  font-weight: 500;
  color: var(--text-primary);
  margin: 5px;
}

/* Coloring skill pills cyclically */
.skill-pill:nth-child(5n+1) { border-color: var(--color-purple); color: var(--color-purple); background: rgba(139, 134, 190, 0.05); }
.skill-pill:nth-child(5n+2) { border-color: var(--color-pink); color: var(--color-pink); background: rgba(215, 173, 188, 0.05); }
.skill-pill:nth-child(5n+3) { border-color: var(--color-yellow); color: var(--color-yellow); background: rgba(234, 182, 104, 0.05); }
.skill-pill:nth-child(5n+4) { border-color: var(--color-green); color: var(--color-green); background: rgba(204, 212, 141, 0.05); }
.skill-pill:nth-child(5n+5) { border-color: var(--color-blue); color: var(--color-blue); background: rgba(139, 174, 182, 0.05); }

.skill-name {
  font-size: 0.95rem;
}

/* Projects Grid */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
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
  margin-bottom: 15px;
}

.project-name {
  font-weight: 700;
  font-size: 1.2rem;
  color: #2c3e50;
}

.role-badge {
  background-color: rgba(139, 174, 182, 0.15); /* Blue tint */
  color: var(--color-blue);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  white-space: nowrap;
  margin-left: 10px;
  font-weight: 600;
}

.project-date {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 15px;
}

.project-desc {
  font-size: 1rem;
  color: var(--text-primary);
  margin-bottom: 20px;
  line-height: 1.6;
  flex-grow: 1;
}

.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 25px;
}

.tech-tag {
  background-color: #F5F7FA;
  color: var(--text-secondary);
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
}

.project-link {
  display: inline-block;
  text-align: center;
  color: var(--color-purple);
  text-decoration: none;
  font-weight: 600;
  margin-top: auto;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.project-link:hover {
  color: var(--color-blue);
  transform: translateX(4px);
}

/* Timeline (Experience & Education) */
.timeline-item, .edu-item {
  margin-bottom: 40px;
  padding-left: 0;
  border-left: none;
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 30px;
  position: relative;
}

.timeline-item::after, .edu-item::after {
  content: '';
  position: absolute;
  left: 140px;
  top: 0;
  bottom: -40px;
  width: 1px;
  background: rgba(0,0,0,0.05);
  transform: translateX(-50%);
}

.timeline-item:last-child::after, .edu-item:last-child::after {
  display: none;
}

.timeline-header, .edu-header {
  display: contents;
}

.date {
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
  grid-column: 1;
  text-align: right;
  padding-right: 30px;
  position: relative;
}

/* Dot on the timeline */
.date::after {
  content: '';
  position: absolute;
  right: -5px; /* Half of gap (30/2) - half of dot (10/2) approx */
  top: 6px;
  width: 10px;
  height: 10px;
  background: #fff;
  border: 3px solid var(--color-pink);
  border-radius: 50%;
  z-index: 1;
  box-shadow: 0 0 0 4px #fff; /* fake gap */
}

.company, .school {
  font-weight: 700;
  font-size: 1.2rem;
  display: block;
  margin-bottom: 4px;
  grid-column: 2;
  color: #2c3e50;
}

.position, .degree {
  grid-column: 2;
  font-weight: 600;
  color: var(--color-purple);
  margin-bottom: 12px;
  display: block;
}

.description {
  grid-column: 2;
  color: var(--text-primary);
  line-height: 1.7;
}

/* Grid List (Language & Certificate) */
.grid-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.grid-item {
  background: #F9FAFB;
  padding: 24px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.grid-item:hover {
  background: #fff;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  border-color: rgba(0,0,0,0.05);
  transform: translateY(-4px);
}

.grid-name {
  font-weight: 700;
  margin-bottom: 8px;
  font-size: 1.1rem;
  color: #2c3e50;
}

.grid-value {
  color: var(--color-green);
  font-size: 0.95rem;
  font-weight: 600;
}

.grid-sub {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.grid-date {
  margin-top: auto;
  font-size: 0.85rem;
  color: #aaa;
  text-align: right;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
    gap: 30px;
  }
  
  .sidebar {
    width: 100%;
    position: relative;
    top: 0;
    padding-top: 0;
    margin-bottom: 20px;
  }
  
  .sidebar nav ul {
    flex-direction: row;
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 10px;
    padding-bottom: 10px;
  }
  
  .sidebar nav li {
    white-space: nowrap;
    background: #fff;
    border: 1px solid rgba(0,0,0,0.05);
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .contact-info {
    justify-content: center;
  }
  
  .timeline-item, .edu-item {
    grid-template-columns: 1fr;
    gap: 10px;
    padding-left: 20px;
    border-left: 2px solid rgba(0,0,0,0.05);
  }
  
  .timeline-item::after, .edu-item::after {
    display: none;
  }
  
  .date {
    grid-column: 1;
    text-align: left;
    padding-right: 0;
    margin-bottom: 4px;
    color: var(--color-pink);
    font-weight: 600;
  }
  
  .date::after {
    left: -26px; /* -20px padding - 6px approx center of line */
    right: auto;
    top: 4px;
  }
  
  .company, .school, .position, .degree, .description {
    grid-column: 1;
  }
}
</style>
