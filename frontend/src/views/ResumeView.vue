<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import axios from 'axios'
import MagicCard from '../components/MagicCard.vue'
import Marquee from '../components/Marquee.vue'

const resumeData = ref(null)
const loading = ref(true)
const error = ref(null)

const activeSection = ref('')

const sections = [
  { id: 'basic-info', title: '关于我' },
  { id: 'keywords', title: '我的KeyWord' },
  { id: 'experience', title: '经历' },
  { id: 'projects', title: '项目' },
  { id: 'tech-stack', title: '我的技能栈' },
  { id: 'education', title: '教育' },
  { id: 'languages', title: '语言' },
  { id: 'certificates', title: '证书' },
]

// Refs for interaction
const projectRefs = ref({})
const skillRefs = ref({})
const contentWrapperRef = ref(null)
const lines = ref([])

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

// Split skills for Marquee rows (All keywords mixed)
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

// Filter Tech Skills for "My Tech Stack" section
const techSkills = computed(() => {
  if (!resumeData.value || !resumeData.value.skills) return []
  // Filter mostly by tech categories or just exclude soft skills/hobbies if needed.
  // Assuming Backend, Frontend, Tools are tech. Role is also somewhat tech related.
  // Let's include everything except Hobbies and Strengths for the tech stack, or just specific lists.
  // Actually, filtering by category is safer.
  const techCategories = ['Backend', 'Frontend', 'Tools', 'Mobile', 'DevOps', 'Language']
  return resumeData.value.skills.filter(s => techCategories.includes(s.category) || !s.category)
})

// Interaction Logic
const handleProjectHover = (project) => {
  if (!project.technologies || !contentWrapperRef.value) return

  const techList = project.technologies.split(',').map(t => t.trim().toLowerCase())
  const newLines = []
  
  // Get container rect for relative positioning
  const containerRect = contentWrapperRef.value.getBoundingClientRect()

  // Get project card rect
  const projectEl = projectRefs.value[project.id]
  if (!projectEl) return
  // Use $el if it's a component, otherwise the element itself
  const pRect = (projectEl.$el || projectEl).getBoundingClientRect()
  
  // Start point (bottom center of project card)
  const x1 = pRect.left + pRect.width / 2 - containerRect.left
  const y1 = pRect.bottom - containerRect.top

  techList.forEach(techName => {
    // Find matching skill card
    // We assume skillRefs are keyed by skill name (lowercase for matching)
    const skillEl = skillRefs.value[techName]
    if (skillEl) {
      const sRect = skillEl.getBoundingClientRect()
      // End point (top center of skill card)
      const x2 = sRect.left + sRect.width / 2 - containerRect.left
      const y2 = sRect.top - containerRect.top
      
      newLines.push({ x1, y1, x2, y2 })
    }
  })
  
  lines.value = newLines
}

const handleProjectLeave = () => {
  lines.value = []
}

// Helper to set refs
const setProjectRef = (el, id) => {
  if (el) projectRefs.value[id] = el
}

const setSkillRef = (el, name) => {
  if (el) skillRefs.value[name.toLowerCase()] = el
}

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
    
    <div v-else class="content-wrapper" ref="contentWrapperRef">
      <!-- SVG Overlay for dynamic lines -->
      <svg class="connections-overlay">
        <line 
          v-for="(line, index) in lines" 
          :key="index"
          :x1="line.x1" 
          :y1="line.y1" 
          :x2="line.x2" 
          :y2="line.y2" 
          class="connection-line"
        />
      </svg>

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

        <!-- Keywords (Marquee) - Previously Skills -->
        <section id="keywords" class="section-card">
          <h3>我的KeyWord</h3>
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
          <div v-else class="empty-state">暂无关键词信息</div>
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
            <MagicCard 
              v-for="project in resumeData.projects" 
              :key="project.id" 
              class="project-card"
              :ref="(el) => setProjectRef(el, project.id)"
              @mouseenter="handleProjectHover(project)"
              @mouseleave="handleProjectLeave"
            >
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

        <!-- My Tech Stack (New Section) -->
        <section id="tech-stack" class="section-card">
          <h3>我的技能栈</h3>
          <div class="tech-stack-grid" v-if="techSkills && techSkills.length">
            <div 
              v-for="skill in techSkills" 
              :key="skill.id" 
              class="tech-card"
              :ref="(el) => setSkillRef(el, skill.name)"
            >
              <span class="tech-icon">⚡</span>
              <div class="tech-info">
                <span class="tech-name">{{ skill.name }}</span>
                <span class="tech-level">熟练度: {{ skill.level }}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: skill.level + '%' }"></div>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">暂无技能栈信息</div>
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
  position: relative;
}

/* Sidebar - Premium Style */
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
  padding: 12px 18px;
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.sidebar nav li:hover {
  background-color: rgba(167, 235, 242, 0.3); /* Luna Lightest tint */
  color: var(--luna-darkest);
}

.sidebar nav li.active {
  background-color: #fff;
  color: var(--luna-darkest);
  box-shadow: 0 4px 15px rgba(1, 28, 64, 0.08);
  font-weight: 700;
  border: 1px solid var(--luna-lightest);
}

.download-pdf {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid rgba(167, 235, 242, 0.5);
}

.btn-pdf {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  padding: 14px;
  background: linear-gradient(135deg, var(--luna-dark), var(--luna-medium));
  color: #fff;
  border-radius: 18px;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(38, 101, 140, 0.25);
}

.btn-pdf:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 25px rgba(38, 101, 140, 0.35);
  filter: brightness(1.1);
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 40px;
  min-width: 0; /* Prevent flex item from overflowing */
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
  background-image: radial-gradient(circle at top right, rgba(167, 235, 242, 0.3), transparent 40%);
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 30px;
  color: var(--luna-darkest);
  position: relative;
  display: inline-block;
  font-weight: 700;
}

h3::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 50px;
  height: 5px;
  background: linear-gradient(to right, var(--luna-medium), var(--luna-light));
  border-radius: 3px;
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
  box-shadow: 0 15px 35px rgba(1, 28, 64, 0.15);
  border: 4px solid #fff;
}

.info-text h1 {
  margin: 0 0 10px 0;
  font-size: 2.5rem;
  background: linear-gradient(135deg, var(--luna-darkest), var(--luna-dark));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 800;
}

.info-text h2 {
  margin: 0 0 20px 0;
  font-size: 1.25rem;
  color: var(--luna-medium);
  font-weight: 600;
  background: rgba(167, 235, 242, 0.3);
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
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
  color: var(--luna-light);
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
  box-shadow: 0 4px 12px rgba(1, 28, 64, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  font-weight: 600;
  margin: 5px;
  transition: all 0.3s ease;
}

.skill-pill:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(1, 28, 64, 0.1);
}

/* Coloring skill pills with Luna palette */
.skill-pill:nth-child(5n+1) { border-color: var(--luna-darkest); color: var(--luna-darkest); background: rgba(1, 28, 64, 0.05); }
.skill-pill:nth-child(5n+2) { border-color: var(--luna-dark); color: var(--luna-dark); background: rgba(2, 56, 89, 0.05); }
.skill-pill:nth-child(5n+3) { border-color: var(--luna-medium); color: var(--luna-medium); background: rgba(38, 101, 140, 0.05); }
.skill-pill:nth-child(5n+4) { border-color: var(--luna-light); color: var(--luna-light); background: rgba(84, 172, 191, 0.1); }
.skill-pill:nth-child(5n+5) { border-color: var(--luna-lightest); color: var(--luna-dark); background: rgba(167, 235, 242, 0.2); }

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
  background: #fff;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.project-name {
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--luna-darkest);
}

.role-badge {
  background-color: var(--luna-lightest);
  color: var(--luna-dark);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  white-space: nowrap;
  margin-left: 10px;
  font-weight: 700;
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
  font-size: 0.8rem;
  padding: 4px 10px;
  background-color: rgba(167, 235, 242, 0.2); /* Luna Lightest tint */
  color: var(--luna-dark);
  border-radius: 6px;
  font-weight: 500;
}

.project-link {
  display: inline-block;
  color: var(--luna-medium);
  font-weight: 600;
  text-decoration: none;
  margin-top: auto;
  transition: all 0.2s;
}

.project-link:hover {
  color: var(--luna-darkest);
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
  background: rgba(84, 172, 191, 0.3); /* Luna Light line */
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
  background: var(--luna-light);
  border: 3px solid #fff;
  border-radius: 50%;
  z-index: 1;
  box-shadow: 0 0 0 3px rgba(167, 235, 242, 0.5); /* Luna Lightest shadow */
}

.company, .school {
  font-weight: 700;
  font-size: 1.2rem;
  display: block;
  margin-bottom: 4px;
  grid-column: 2;
  color: var(--luna-darkest);
}

.position, .degree {
  grid-column: 2;
  font-weight: 600;
  color: var(--luna-medium);
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
  background: #fff;
  padding: 24px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  border: 1px solid rgba(167, 235, 242, 0.5);
}

.grid-item:hover {
  background: #fff;
  box-shadow: 0 10px 30px rgba(1, 28, 64, 0.08);
  border-color: var(--luna-medium);
  transform: translateY(-4px);
}

.grid-name {
  font-weight: 700;
  margin-bottom: 8px;
  font-size: 1.1rem;
  color: var(--luna-darkest);
}

.grid-value {
  color: var(--luna-light);
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
  color: var(--text-secondary);
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
    border-left: 2px solid rgba(167, 235, 242, 0.5);
  }
  
  .timeline-item::after, .edu-item::after {
    display: none;
  }
  
  .date {
    grid-column: 1;
    text-align: left;
    padding-right: 0;
    margin-bottom: 4px;
    color: var(--luna-medium);
    font-weight: 600;
  }
  
  .date::after {
    left: -26px; /* -20px padding - 6px approx center of line */
    right: auto;
    top: 4px;
    box-shadow: 0 0 0 3px rgba(167, 235, 242, 0.5);
  }
  
  .company, .school, .position, .degree, .description {
    grid-column: 1;
  }
}

/* Dynamic Lines Overlay */
.connections-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 5; /* Above background, below content if content has higher z-index */
  overflow: hidden;
}

.connection-line {
  stroke: var(--luna-light);
  stroke-width: 2px;
  stroke-dasharray: 5;
  animation: dash 1s linear infinite;
  opacity: 0.6;
}

@keyframes dash {
  to {
    stroke-dashoffset: -10;
  }
}

/* Tech Stack Section */
.tech-stack-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.tech-card {
  background: #fff;
  border: 1px solid rgba(167, 235, 242, 0.5);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  transition: all 0.3s ease;
}

.tech-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(1, 28, 64, 0.08);
  border-color: var(--luna-medium);
}

.tech-icon {
  font-size: 1.5rem;
  background: rgba(167, 235, 242, 0.2);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  color: var(--luna-dark);
}

.tech-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tech-name {
  font-weight: 700;
  color: var(--luna-darkest);
}

.tech-level {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.progress-bar {
  height: 6px;
  background: rgba(167, 235, 242, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(to right, var(--luna-medium), var(--luna-light));
  border-radius: 3px;
}
</style>
