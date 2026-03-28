<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import axios from 'axios'
import MagicCard from '../components/MagicCard.vue'
import Marquee from '../components/Marquee.vue'
axios.defaults.withCredentials = true

const resumeData = ref(null)
const loading = ref(true)
const error = ref(null)

const activeSection = ref('')

const sections = [
  { id: 'basic-info', title: '关于我' },
  { id: 'keywords', title: '我的标签' },
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
const activeTechs = ref(new Set())

const titleWrapperRef = ref(null)
const titleMeasureRef = ref(null)
const isTitleOverflowing = ref(false)
let titleResizeObserver = null

// Summary Carousel
const currentSummaryIndex = ref(0)
let summaryInterval = null
let summaryScrollInterval = null
let summaryScrollTimeout = null
const isSummaryHovered = ref(false)
const summaryDescRef = ref(null)

const summarySlides = computed(() => {
  if (!resumeData.value?.basic_info) return []
  const info = resumeData.value.basic_info
  const slides = []
  if (info.summary_experience) slides.push({ title: '工作经验', content: info.summary_experience, icon: '' })
  if (info.summary_skills) slides.push({ title: '专业能力', content: info.summary_skills, icon: '' })
  if (info.summary_management) slides.push({ title: '团队管理', content: info.summary_management, icon: '' })
  
  if (slides.length === 0 && info.summary) {
    slides.push({ title: '个人简介', content: info.summary, icon: '📝' })
  }
  return slides
})

const startSummaryRotation = () => {
  if (summaryInterval) clearInterval(summaryInterval)
  if (summaryScrollInterval) clearInterval(summaryScrollInterval)
  if (summaryScrollTimeout) clearTimeout(summaryScrollTimeout)
  
  if (summarySlides.value.length <= 1) return

  const wrapperEl = summaryDescRef.value
  if (wrapperEl) {
    wrapperEl.scrollTop = 0
  }

  const INITIAL_WAIT_MS = 3000
  const SCROLL_SPEED_MS = 50
  const SCROLL_STEP_PX = 1
  const END_WAIT_MS = 2000

  const processSummarySlide = () => {
    const el = summaryDescRef.value
    if (!el) {
      summaryInterval = setTimeout(() => {
        currentSummaryIndex.value = (currentSummaryIndex.value + 1) % summarySlides.value.length
        startSummaryRotation()
      }, 5000)
      return
    }

    const needsScroll = el.scrollHeight > (el.clientHeight + 2)

    if (!needsScroll) {
      summaryInterval = setTimeout(() => {
        currentSummaryIndex.value = (currentSummaryIndex.value + 1) % summarySlides.value.length
        startSummaryRotation()
      }, 5000)
    } else {
      summaryScrollTimeout = setTimeout(() => {
        summaryScrollInterval = setInterval(() => {
          if (el.scrollTop + el.clientHeight >= el.scrollHeight - 1) {
            clearInterval(summaryScrollInterval)
            summaryScrollTimeout = setTimeout(() => {
              currentSummaryIndex.value = (currentSummaryIndex.value + 1) % summarySlides.value.length
              startSummaryRotation()
            }, END_WAIT_MS)
          } else {
            el.scrollTop += SCROLL_STEP_PX
          }
        }, SCROLL_SPEED_MS)
      }, INITIAL_WAIT_MS)
    }
  }

  nextTick(() => {
    setTimeout(processSummarySlide, 600)
  })
}

const pauseSummaryRotation = () => {
  if (summaryInterval) clearInterval(summaryInterval)
  if (summaryScrollInterval) clearInterval(summaryScrollInterval)
  if (summaryScrollTimeout) clearTimeout(summaryScrollTimeout)
}

const handleSummaryMouseEnter = () => {
  isSummaryHovered.value = true
  pauseSummaryRotation()
}

const handleSummaryMouseLeave = () => {
  isSummaryHovered.value = false
  startSummaryRotation()
}

const setSummaryIndex = (index) => {
  currentSummaryIndex.value = index
  if (!isSummaryHovered.value) {
    startSummaryRotation()
  }
}

// Project Carousel
const projectCarouselState = ref({})
let projectIntervals = {}
let projectScrollIntervals = {}
let projectScrollTimeouts = {}
const projectDescRefs = ref({})

const setProjectDescRef = (el, projectId) => {
  if (el) {
    projectDescRefs.value[projectId] = el
  }
}

const roleWrapperRefs = ref([])
const projectRoleOverflows = ref({})
let roleResizeObserver = null

const checkRoleOverflows = () => {
  roleWrapperRefs.value.forEach(wrapper => {
    if (wrapper) {
      const id = wrapper.dataset.id
      const measure = wrapper.querySelector('.role-badge-measure')
      if (measure) {
        // Calculate max width dynamically based on remaining space
        const headerEl = wrapper.closest('.project-header')
        // Role badge is now fixed to 33.33% of header width minus padding/borders roughly
        const availableWidth = (headerEl.clientWidth * 0.3333) - 24 // 24px for padding
        projectRoleOverflows.value[id] = measure.scrollWidth > availableWidth
      }
    }
  })
}

const getProjectSlides = (project) => {
  const slides = []
  if (project.bg_description) slides.push({ title: '项目背景', content: project.bg_description, icon: '🎯' })
  if (project.duty_description) slides.push({ title: '项目职责', content: project.duty_description, icon: '🛡️' })
  if (project.solution_description) slides.push({ title: '解决方案', content: project.solution_description, icon: '💡' })
  if (project.result_description) slides.push({ title: '项目成果', content: project.result_description, icon: '🏆' })
  
  if (slides.length === 0 && project.description) {
    slides.push({ title: '项目描述', content: project.description, icon: '📝' })
  }
  return slides
}

const initProjectCarousels = () => {
  if (!resumeData.value?.projects) return
  resumeData.value.projects.forEach(project => {
    const slides = getProjectSlides(project)
    if (slides.length > 0) {
      projectCarouselState.value[project.id] = {
        currentIndex: 0,
        isHovered: false,
        slides: slides
      }
      startProjectRotation(project.id)
    }
  })
}

const startProjectRotation = (projectId) => {
  if (projectIntervals[projectId]) clearInterval(projectIntervals[projectId])
  if (projectScrollIntervals[projectId]) clearInterval(projectScrollIntervals[projectId])
  if (projectScrollTimeouts[projectId]) clearTimeout(projectScrollTimeouts[projectId])

  const state = projectCarouselState.value[projectId]
  if (!state || state.slides.length <= 1) return

  // Wrapper element
  const wrapper = projectDescRefs.value[projectId]
  
  if (wrapper) {
    // Reset scroll position when starting a new rotation cycle for this slide
    wrapper.scrollTop = 0
  }

  // Define the base time to show the first screen
  const INITIAL_WAIT_MS = 3000
  const SCROLL_SPEED_MS = 50 // 50ms per tick
  const SCROLL_STEP_PX = 1   // 1px per tick
  const END_WAIT_MS = 2000   // Wait at the bottom before switching

  const processSlide = () => {
    const wrapperEl = projectDescRefs.value[projectId]
    if (!wrapperEl) {
      // If ref is not ready, just fallback to simple interval
      projectIntervals[projectId] = setTimeout(() => {
        state.currentIndex = (state.currentIndex + 1) % state.slides.length
        startProjectRotation(projectId) // recursively call for next slide
      }, 5000)
      return
    }

    // A tiny bit of extra tolerance to prevent precision errors
    const needsScroll = wrapperEl.scrollHeight > (wrapperEl.clientHeight + 2)

    if (!needsScroll) {
      // Normal behavior: wait 5s then switch
      projectIntervals[projectId] = setTimeout(() => {
        state.currentIndex = (state.currentIndex + 1) % state.slides.length
        startProjectRotation(projectId)
      }, 5000)
    } else {
      // Needs scrolling behavior
      projectScrollTimeouts[projectId] = setTimeout(() => {
        // Start scrolling
        projectScrollIntervals[projectId] = setInterval(() => {
          // If hovered during scroll, it will be handled by pauseProjectRotation
          if (wrapperEl.scrollTop + wrapperEl.clientHeight >= wrapperEl.scrollHeight - 1) {
            // Reached bottom
            clearInterval(projectScrollIntervals[projectId])
            projectScrollTimeouts[projectId] = setTimeout(() => {
              state.currentIndex = (state.currentIndex + 1) % state.slides.length
              startProjectRotation(projectId)
            }, END_WAIT_MS)
          } else {
            wrapperEl.scrollTop += SCROLL_STEP_PX
          }
        }, SCROLL_SPEED_MS)
      }, INITIAL_WAIT_MS)
    }
  }

  // Need nextTick because Vue might be transitioning the DOM element
  nextTick(() => {
    // wait a tiny bit for transition to finish so scrollHeight is accurate
    // Increased timeout from 300ms to 600ms to ensure the new slide content is fully rendered and layout is updated
    setTimeout(processSlide, 600) 
  })
}

const pauseProjectRotation = (projectId) => {
  if (projectIntervals[projectId]) clearInterval(projectIntervals[projectId])
  if (projectScrollIntervals[projectId]) clearInterval(projectScrollIntervals[projectId])
  if (projectScrollTimeouts[projectId]) clearTimeout(projectScrollTimeouts[projectId])
}

const handleProjectCarouselMouseEnter = (projectId) => {
  if (projectCarouselState.value[projectId]) {
    projectCarouselState.value[projectId].isHovered = true
    pauseProjectRotation(projectId)
  }
}

const handleProjectCarouselMouseLeave = (projectId) => {
  if (projectCarouselState.value[projectId]) {
    projectCarouselState.value[projectId].isHovered = false
    startProjectRotation(projectId)
  }
}

const setProjectCarouselIndex = (projectId, index) => {
  if (projectCarouselState.value[projectId]) {
    projectCarouselState.value[projectId].currentIndex = index
    if (!projectCarouselState.value[projectId].isHovered) {
      startProjectRotation(projectId)
    }
  }
}

const checkTitleOverflow = () => {
  if (titleWrapperRef.value && titleMeasureRef.value) {
    const parent = titleWrapperRef.value.parentElement
    if (parent) {
      isTitleOverflowing.value = titleMeasureRef.value.scrollWidth > parent.clientWidth
    } else {
      isTitleOverflowing.value = titleMeasureRef.value.scrollWidth > titleWrapperRef.value.clientWidth
    }
  }
}

onMounted(() => {
  window.addEventListener('resize', checkTitleOverflow)
  window.addEventListener('resize', checkRoleOverflows)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkTitleOverflow)
  window.removeEventListener('resize', checkRoleOverflows)
  if (titleResizeObserver) {
    titleResizeObserver.disconnect()
  }
  if (roleResizeObserver) {
    roleResizeObserver.disconnect()
  }
  pauseSummaryRotation()
  Object.keys(projectIntervals).forEach(id => pauseProjectRotation(id))
})

const fetchResumeData = async () => {
  try {
    // Determine the base URL dynamically based on current window location
    // If in production, we proxy /api/ to the backend via Nginx.
    // In dev, we might be running vite on 5173 and backend on 8000.
    const isProd = import.meta.env.PROD
    
    // Explicitly check for port 5173 to force backend URL usage even if PROD flag is confusing
    const isDevPort = window.location.port === '5173'
    
    // Check if we are accessing via Public IP (starts with 8.) or local network
    const hostname = window.location.hostname
    const isPublicIP = hostname.startsWith('8.') || hostname !== '127.0.0.1' && hostname !== 'localhost' && !hostname.startsWith('192.168.')

    let finalUrl = '/api/resume/'
    
    if (!isProd || isDevPort) {
        // If local dev or explicitly on dev port, hit backend directly
        // We assume backend is on the same hostname but port 8000
        finalUrl = `http://${hostname}:8000/api/resume/`
    }
    
    // If accessing via Public IP on port 5173, force 8000 port for API
    if (isPublicIP && isDevPort) {
       finalUrl = `http://${hostname}:8000/api/resume/`
    }

    const response = await axios.get(finalUrl)
    resumeData.value = response.data
    startSummaryRotation()
    initProjectCarousels()
    await nextTick()
    setTimeout(() => {
        checkTitleOverflow()
        if (titleWrapperRef.value && titleWrapperRef.value.parentElement && !titleResizeObserver) {
          titleResizeObserver = new ResizeObserver(() => {
            checkTitleOverflow()
          })
          titleResizeObserver.observe(titleWrapperRef.value.parentElement)
        }
        
        checkRoleOverflows()
        if (roleWrapperRefs.value.length > 0 && !roleResizeObserver) {
           roleResizeObserver = new ResizeObserver(() => {
             checkRoleOverflows()
           })
           // Observe the project grid container for resize events
           const grid = document.querySelector('.projects-grid')
           if (grid) roleResizeObserver.observe(grid)
        }
      }, 100)
  } catch (err) {
    error.value = '无法加载简历数据，请稍后再试。'
    if (err?.response?.status === 401) {
      window.location.href = '/login'
    } else {
      console.error('API Error:', err)
    }
  } finally {
    loading.value = false
  }
}

const getImageUrl = (url) => {
  if (!url) return ''
  // If the URL is already absolute, return it
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  
  const isProd = import.meta.env.PROD
  const isDevPort = window.location.port === '5173'
  const hostname = window.location.hostname
  const isPublicIP = hostname.startsWith('8.') || hostname !== '127.0.0.1' && hostname !== 'localhost' && !hostname.startsWith('192.168.')
  
  // If local dev, prepend backend URL. If deployed (accessed via IP), use relative path.
  // But if accessing via Public IP on port 5173, force 8000 port
  if (!isProd || isDevPort) {
    return `http://${hostname}:8000${url}`
  }
  
  if (isPublicIP && isDevPort) {
     return `http://${hostname}:8000${url}`
  }
  
  return url
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
  if (resumeData.value && resumeData.value.tech_stack && resumeData.value.tech_stack.length > 0) {
    return resumeData.value.tech_stack
  }
  return []
})

// Interaction Logic
const handleProjectHover = (project) => {
  if (!project.technologies || !contentWrapperRef.value) return

  const techList = project.technologies.split(',').map(t => t.trim().toLowerCase())
  const newLines = []
  const newActiveTechs = new Set()
  
  // Get container rect for relative positioning
  const containerRect = contentWrapperRef.value.getBoundingClientRect()

  // Get project card rect
  const projectEl = projectRefs.value[project.id]
  if (!projectEl) return
  // Use $el if it's a component, otherwise the element itself
  const pRect = (projectEl.$el || projectEl).getBoundingClientRect()
  
  // Start point (bottom center of project card)
  // We want to distribute start points along the bottom edge
  const techCount = techList.length
  // Calculate segment width to distribute points
  const segmentWidth = pRect.width / (techCount + 1)
  
  const pBottom = pRect.bottom - containerRect.top
  const pLeft = pRect.left - containerRect.left

  techList.forEach((techName, index) => {
    // Find matching skill card
    // We assume skillRefs are keyed by skill name (lowercase for matching)
    const skillEl = skillRefs.value[techName]
    if (skillEl) {
      const sRect = skillEl.getBoundingClientRect()
      
      // Start point: Distributed along bottom of project card
      const x1 = pLeft + (segmentWidth * (index + 1))
      const y1 = pBottom
      
      // End point (top center of skill card)
      const x2 = sRect.left + sRect.width / 2 - containerRect.left
      const y2 = sRect.top - containerRect.top
      
      newLines.push({ x1, y1, x2, y2 })
      newActiveTechs.add(techName)
    }
  })
  
  lines.value = newLines
  activeTechs.value = newActiveTechs
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
              <img :src="getImageUrl(resumeData.basic_info.avatar)" alt="Avatar" class="avatar" />
            </div>
            <div class="info-text">
              <h1>{{ resumeData.basic_info.name }}</h1>
              <div class="title-wrapper" ref="titleWrapperRef" :class="{ 'is-overflowing': isTitleOverflowing }">
                <h2 class="title-measure" ref="titleMeasureRef">{{ resumeData.basic_info.title }}</h2>
                <Marquee v-if="isTitleOverflowing" pauseOnHover duration="15s" gap="30px" class="title-marquee">
                  <h2 class="title-text">{{ resumeData.basic_info.title }}</h2>
                </Marquee>
                <h2 v-else class="title-text">{{ resumeData.basic_info.title }}</h2>
              </div>
              <p class="contact-info">
                <span v-if="resumeData.basic_info.gender">{{ resumeData.basic_info.gender }}</span>
                <span v-if="resumeData.basic_info.gender" class="dot">·</span>
                <span v-if="resumeData.basic_info.age">{{ resumeData.basic_info.age }}岁</span>
                <span v-if="resumeData.basic_info.age" class="dot">·</span>
                <span>{{ resumeData.basic_info.location }}</span>
                <span class="dot">·</span>
                <span>{{ resumeData.basic_info.email }}</span>
                <span v-if="resumeData.basic_info.phone" class="dot">·</span>
                <span v-if="resumeData.basic_info.phone">{{ resumeData.basic_info.phone }}</span>
              </p>
              
              <div 
                class="summary-carousel" 
                @mouseenter="handleSummaryMouseEnter" 
                @mouseleave="handleSummaryMouseLeave"
                v-if="summarySlides.length > 0"
              >
                <div class="summary-carousel-header">
                  <span class="summary-title">
                    {{ summarySlides[currentSummaryIndex].icon }} {{ summarySlides[currentSummaryIndex].title }}
                  </span>
                  <span class="summary-status" :class="{ 'is-paused': isSummaryHovered }" v-if="summarySlides.length > 1">
                    {{ isSummaryHovered ? '⏸️' : '🔄' }}
                  </span>
                </div>
                
                <div class="summary-content-wrapper" ref="summaryDescRef">
                  <transition name="fade-slide" mode="out-in">
                    <p :key="currentSummaryIndex" class="summary" style="white-space: pre-wrap;">{{ summarySlides[currentSummaryIndex].content }}</p>
                  </transition>
                </div>

                <div class="summary-indicators" v-if="summarySlides.length > 1">
                  <span 
                    v-for="(slide, index) in summarySlides" 
                    :key="index"
                    class="indicator-dot"
                    :class="{ active: index === currentSummaryIndex }"
                    @click="setSummaryIndex(index)"
                  ></span>
                </div>
              </div>

            </div>
          </div>
          <div v-else class="empty-state">暂无基本信息</div>
        </section>

        <!-- Keywords (Marquee) - Previously Skills -->
        <section id="keywords" class="section-card">
          <h3>我的标签</h3>
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
              <p class="description" style="white-space: pre-wrap;">{{ exp.description }}</p>
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
            >
              <div class="project-header">
                <span class="project-name">{{ project.name }}</span>
                <div class="role-badge-wrapper" ref="roleWrapperRefs" :data-id="project.id">
                  <span class="role-badge-measure">{{ project.role }}</span>
                  <Marquee v-if="projectRoleOverflows[project.id]" pauseOnHover duration="10s" gap="20px" class="role-marquee">
                    <span class="role-badge-text">{{ project.role }}</span>
                  </Marquee>
                  <span v-else class="role-badge-text">{{ project.role }}</span>
                </div>
              </div>
              <p class="project-date" v-if="project.start_date">{{ project.start_date }} - {{ project.end_date || '至今' }}</p>
              
              <div 
                class="summary-carousel project-desc-carousel" 
                @mouseenter="handleProjectCarouselMouseEnter(project.id)" 
                @mouseleave="handleProjectCarouselMouseLeave(project.id)"
                v-if="projectCarouselState[project.id] && projectCarouselState[project.id].slides.length > 0"
              >
                <div class="summary-carousel-header">
                  <span class="summary-title">
                    {{ projectCarouselState[project.id].slides[projectCarouselState[project.id].currentIndex].icon }} {{ projectCarouselState[project.id].slides[projectCarouselState[project.id].currentIndex].title }}
                  </span>
                  <span class="summary-status" :class="{ 'is-paused': projectCarouselState[project.id].isHovered }" v-if="projectCarouselState[project.id].slides.length > 1">
                    {{ projectCarouselState[project.id].isHovered ? '⏸️' : '🔄' }}
                  </span>
                </div>
                
                <div 
                  class="summary-content-wrapper project-desc-wrapper"
                  :ref="(el) => setProjectDescRef(el, project.id)"
                >
                  <transition name="fade-slide" mode="out-in">
                    <p :key="projectCarouselState[project.id].currentIndex" class="summary" style="white-space: pre-wrap;">{{ projectCarouselState[project.id].slides[projectCarouselState[project.id].currentIndex].content }}</p>
                  </transition>
                </div>

                <div class="summary-indicators" v-if="projectCarouselState[project.id].slides.length > 1">
                  <span 
                    v-for="(slide, index) in projectCarouselState[project.id].slides" 
                    :key="index"
                    class="indicator-dot"
                    :class="{ active: index === projectCarouselState[project.id].currentIndex }"
                    @click="setProjectCarouselIndex(project.id, index)"
                  ></span>
                </div>
              </div>

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
              :class="{ 'active-tech': activeTechs.has(skill.name.toLowerCase()) }"
              :ref="(el) => setSkillRef(el, skill.name)"
            >
              <span class="tech-icon">{{ skill.icon || '⚡' }}</span>
              <div class="tech-info">
                <span class="tech-name">{{ skill.name }}</span>
                <span class="tech-level">经验: {{ skill.years }}年</span>
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
  align-items: flex-start;
}

.avatar {
  width: 140px;
  height: 140px;
  border-radius: 40px; /* Soft Squircle */
  object-fit: cover;
  box-shadow: 0 15px 35px rgba(1, 28, 64, 0.15);
  border: 4px solid #fff;
}

.info-text {
  flex: 1;
  min-width: 0;
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

.title-wrapper {
  max-width: 100%;
  margin: 0 0 20px 0;
  background: rgba(167, 235, 242, 0.3);
  border-radius: 12px;
  overflow: hidden;
  display: inline-flex;
  position: relative;
  align-items: center;
}

.title-wrapper.is-overflowing {
  width: 100%;
}

.title-marquee {
  width: 100%;
}

.title-measure {
  position: absolute;
  visibility: hidden;
  pointer-events: none;
  white-space: nowrap;
  font-size: 1.25rem;
  font-weight: 600;
  padding: 4px 12px;
  margin: 0;
}

.title-text {
  font-size: 1.25rem;
  color: var(--luna-medium);
  font-weight: 600;
  padding: 4px 12px;
  margin: 0;
  white-space: nowrap;
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

.summary-carousel {
  margin-top: 15px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(167, 235, 242, 0.4);
  border-radius: 16px;
  padding: 20px;
  position: relative;
  transition: all 0.3s ease;
}

.summary-carousel:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: var(--luna-light);
  box-shadow: 0 4px 15px rgba(167, 235, 242, 0.2);
}

.summary-carousel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  border-bottom: 1px dashed rgba(167, 235, 242, 0.5);
  padding-bottom: 8px;
}

.summary-title {
  font-weight: 700;
  color: var(--luna-darkest);
  font-size: 1.1rem;
}

.summary-status {
  font-size: 0.8rem;
  color: var(--text-secondary);
  opacity: 0.6;
  transition: all 0.3s ease;
  background: rgba(167, 235, 242, 0.2);
  padding: 2px 8px;
  border-radius: 10px;
}

.summary-status.is-paused {
  color: var(--luna-dark);
  background: rgba(255, 200, 0, 0.2);
  opacity: 1;
  font-weight: 600;
}

.summary-content-wrapper {
  /* 5 lines * 1.8 line-height * 1.05rem font-size ≈ 9.45rem */
  height: 9.45rem;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 5px;
  display: block;
  scroll-behavior: smooth;
}

/* Custom Scrollbar for summary */
.summary-content-wrapper::-webkit-scrollbar {
  width: 4px;
}

.summary-content-wrapper::-webkit-scrollbar-track {
  background: rgba(167, 235, 242, 0.2);
  border-radius: 4px;
}

.summary-content-wrapper::-webkit-scrollbar-thumb {
  background: rgba(38, 101, 140, 0.3);
  border-radius: 4px;
}

.summary-content-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(38, 101, 140, 0.6);
}

.summary {
  line-height: 1.8;
  color: var(--text-primary);
  font-size: 1.05rem;
  margin: 0;
  width: 100%;
}

.summary-indicators {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 15px;
}

.indicator-dot {
  width: 24px;
  height: 4px;
  border-radius: 2px;
  background: rgba(167, 235, 242, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator-dot.active {
  background: var(--luna-medium);
  width: 32px;
}

.indicator-dot:hover {
  background: var(--luna-light);
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
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
  gap: 15px;
}

.project-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--luna-darkest);
  flex: 1;
  min-width: 0;
  white-space: normal;
  word-break: break-word;
}

.role-badge-wrapper {
  background: linear-gradient(135deg, var(--luna-light), var(--luna-medium));
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(38, 101, 140, 0.2);
  display: inline-flex;
  align-items: center;
  overflow: hidden;
  width: 33.33%;
  flex-shrink: 0;
  position: relative;
  margin-top: 2px;
}

.role-marquee {
  width: 100%;
}

.role-badge-measure {
  position: absolute;
  visibility: hidden;
  pointer-events: none;
  white-space: nowrap;
}

.role-badge-text {
  white-space: nowrap;
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

.project-desc-carousel {
  margin-top: 10px;
  margin-bottom: 20px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
}

.project-desc-wrapper {
  /* 8 lines * 1.6 line-height * 0.9rem font-size ≈ 11.52rem */
  height: 11.52rem; 
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 5px;
  display: block; /* Override default flex */
  scroll-behavior: smooth;
}

/* Custom Scrollbar for project description */
.project-desc-wrapper::-webkit-scrollbar {
  width: 4px;
}

.project-desc-wrapper::-webkit-scrollbar-track {
  background: rgba(167, 235, 242, 0.2);
  border-radius: 4px;
}

.project-desc-wrapper::-webkit-scrollbar-thumb {
  background: rgba(38, 101, 140, 0.3);
  border-radius: 4px;
}

.project-desc-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(38, 101, 140, 0.6);
}

.project-desc-carousel .summary {
  font-size: 0.9rem;
  line-height: 1.6;
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
  padding: 12px 20px;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
}

.tech-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(1, 28, 64, 0.08);
  border-color: var(--luna-medium);
}

.tech-card.active-tech {
  background: rgba(167, 235, 242, 0.4); /* Deeper background for selected state */
  border-color: var(--luna-medium);
  box-shadow: 0 0 15px rgba(84, 172, 191, 0.3);
  transform: translateY(-2px);
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
  flex: 1;
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
