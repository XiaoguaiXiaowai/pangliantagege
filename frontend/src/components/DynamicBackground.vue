<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const circles = ref([])
const stars = ref([])
const CIRCLE_COUNT = 2
const RADIUS = 75
const STAR_COUNT = 28

let animationId = null
let reducedMotion = false

const prefersReducedMotion = () =>
  window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false

const initStars = () => {
  const { innerWidth, innerHeight } = window
  const list = []
  for (let i = 0; i < STAR_COUNT; i++) {
    list.push({
      id: i,
      x: Math.random() * innerWidth,
      y: Math.random() * innerHeight,
      size: 1 + Math.random() * 2.4,
      delay: Math.random() * 6,
      duration: 3 + Math.random() * 5
    })
  }
  stars.value = list
}

const initCircles = () => {
  const { innerWidth, innerHeight } = window
  const newCircles = []

  for (let i = 0; i < CIRCLE_COUNT; i++) {
    let x, y
    let overlap = true
    let attempts = 0

    // Find non-overlapping position
    while (overlap && attempts < 100) {
      attempts++
      x = Math.random() * (innerWidth - RADIUS * 2) + RADIUS
      y = Math.random() * (innerHeight - RADIUS * 2) + RADIUS

      overlap = false
      for (let j = 0; j < newCircles.length; j++) {
        const other = newCircles[j]
        const d = Math.sqrt((x - other.x) ** 2 + (y - other.y) ** 2)
        if (d < RADIUS * 2) {
          overlap = true
          break
        }
      }
    }

    // If we couldn't find a spot, just place it somewhere safeish
    if (overlap) {
      x = innerWidth / 2 + i * 10
      y = innerHeight / 2
    }

    const speed = 1.5
    const angle = Math.random() * Math.PI * 2
    const dx = Math.cos(angle) * speed
    const dy = Math.sin(angle) * speed

    newCircles.push({
      id: i,
      x,
      y,
      dx,
      dy,
      radius: RADIUS
    })
  }

  circles.value = newCircles
}

const updatePosition = () => {
  const { innerWidth, innerHeight } = window

  // 1. Move and Wall Collision
  circles.value.forEach((c) => {
    c.x += c.dx
    c.y += c.dy

    if (c.x + c.radius > innerWidth) {
      c.x = innerWidth - c.radius
      c.dx = -Math.abs(c.dx)
    } else if (c.x - c.radius < 0) {
      c.x = c.radius
      c.dx = Math.abs(c.dx)
    }

    if (c.y + c.radius > innerHeight) {
      c.y = innerHeight - c.radius
      c.dy = -Math.abs(c.dy)
    } else if (c.y - c.radius < 0) {
      c.y = c.radius
      c.dy = Math.abs(c.dy)
    }
  })

  // 2. Circle Collision
  for (let i = 0; i < circles.value.length; i++) {
    for (let j = i + 1; j < circles.value.length; j++) {
      const c1 = circles.value[i]
      const c2 = circles.value[j]

      const dx = c2.x - c1.x
      const dy = c2.y - c1.y
      const distance = Math.sqrt(dx * dx + dy * dy)

      if (distance < c1.radius + c2.radius) {
        const overlap = (c1.radius + c2.radius - distance) / 2
        const safeDist = distance || 0.001
        const nx = dx / safeDist
        const ny = dy / safeDist

        c1.x -= nx * overlap
        c1.y -= ny * overlap
        c2.x += nx * overlap
        c2.y += ny * overlap

        const tx = -ny
        const ty = nx

        const v1n = c1.dx * nx + c1.dy * ny
        const v1t = c1.dx * tx + c1.dy * ty

        const v2n = c2.dx * nx + c2.dy * ny
        const v2t = c2.dx * tx + c2.dy * ty

        c1.dx = v2n * nx + v1t * tx
        c1.dy = v2n * ny + v1t * ty

        c2.dx = v1n * nx + v2t * tx
        c2.dy = v1n * ny + v2t * ty
      }
    }
  }

  animationId = requestAnimationFrame(updatePosition)
}

const startAnimation = () => {
  if (animationId) cancelAnimationFrame(animationId)
  if (reducedMotion) return
  updatePosition()
}

const handleMotionChange = () => {
  reducedMotion = prefersReducedMotion()
  startAnimation()
}

onMounted(() => {
  reducedMotion = prefersReducedMotion()
  initCircles()
  initStars()
  startAnimation()
  window.matchMedia?.('(prefers-reduced-motion: reduce)').addEventListener?.('change', handleMotionChange)
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
  window.matchMedia?.('(prefers-reduced-motion: reduce)').removeEventListener?.('change', handleMotionChange)
})
</script>

<template>
  <div class="dynamic-background" aria-hidden="true">
    <!-- 星空粒子（静态 + 轻微闪烁） -->
    <div
      v-for="star in stars"
      :key="'star-' + star.id"
      class="star"
      :style="{
        left: `${star.x}px`,
        top: `${star.y}px`,
        width: `${star.size}px`,
        height: `${star.size}px`,
        animationDelay: `${star.delay}s`,
        animationDuration: `${star.duration}s`
      }"
    ></div>
    <!-- 漂浮光晕环（transform 定位，GPU 合成，避免逐帧重排） -->
    <div
      v-for="circle in circles"
      :key="'circle-' + circle.id"
      class="floating-circle"
      :style="{
        transform: `translate3d(${circle.x}px, ${circle.y}px, 0) translate(-50%, -50%)`
      }"
    ></div>
  </div>
</template>

<style scoped>
.dynamic-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
  /* 透明，露出 body 上的氛围光晕渐变 */
  background: transparent;
}

.star {
  position: absolute;
  border-radius: 50%;
  background-color: var(--star-color);
  animation: star-twinkle 4s ease-in-out infinite;
  will-change: opacity;
}

@keyframes star-twinkle {
  0%, 100% { opacity: 0.25; }
  50% { opacity: 1; }
}

.floating-circle {
  position: absolute;
  top: 0;
  left: 0;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  /* 渐变光晕环：内芯淡色填充 + 描边环 + 内外发光 */
  background: radial-gradient(circle at 50% 50%, var(--ring-fill) 0%, transparent 62%);
  border: 10px solid var(--ring-color);
  box-shadow:
    0 0 32px 6px var(--ring-glow),
    inset 0 0 24px 4px var(--ring-glow);
  will-change: transform;
}

/* 减弱动态效果：静止展示，不跑物理动画 */
@media (prefers-reduced-motion: reduce) {
  .star {
    animation: none;
    opacity: 0.6;
  }
}
</style>
