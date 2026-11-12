<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

/**
 * 深空星野背景（Deep Space × Holo 主题）
 * - Canvas 三层视差星野：随鼠标轻微漂移，各自闪烁
 * - 偶发流星划过
 * - 两条 CSS 轨道环 + 金色行星，呼应「深空轨道」叙事
 * - 颜色全部读取 CSS 变量，深浅主题自动适配；尊重 prefers-reduced-motion
 */

const canvasRef = ref(null)

let ctx = null
let stars = []
let meteor = null
let animationId = null
let meteorTimer = null
let reducedMotion = false
let themeObserver = null
let palette = { star: 'rgba(230,238,255,0.85)', gold: '#FFD479' }

// 鼠标视差：目标值与实际值（lerp 平滑）
const parallax = { tx: 0, ty: 0, x: 0, y: 0 }

const LAYERS = [
  { depth: 0.25, size: [0.6, 1.2], alpha: 0.5 },  // 远层
  { depth: 0.55, size: [1.0, 1.8], alpha: 0.75 }, // 中层
  { depth: 1.0, size: [1.4, 2.4], alpha: 1.0 }    // 近层
]

const prefersReducedMotion = () =>
  window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false

const readPalette = () => {
  const cs = getComputedStyle(document.documentElement)
  palette = {
    star: cs.getPropertyValue('--star-color').trim() || palette.star,
    gold: cs.getPropertyValue('--star-gold').trim() || palette.gold
  }
}

const resize = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  const dpr = Math.min(window.devicePixelRatio || 1, 2)
  canvas.width = window.innerWidth * dpr
  canvas.height = window.innerHeight * dpr
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  initStars()
  if (reducedMotion) drawStatic()
}

const initStars = () => {
  const { innerWidth: w, innerHeight: h } = window
  const count = Math.min(220, Math.floor((w * h) / 9000))
  stars = []
  for (let i = 0; i < count; i++) {
    const layer = LAYERS[i % LAYERS.length]
    stars.push({
      x: Math.random() * w,
      y: Math.random() * h,
      r: layer.size[0] + Math.random() * (layer.size[1] - layer.size[0]),
      depth: layer.depth,
      baseAlpha: layer.alpha * (0.5 + Math.random() * 0.5),
      phase: Math.random() * Math.PI * 2,
      speed: 0.4 + Math.random() * 1.2,
      gold: Math.random() < 0.08 // 少量金色恒星点缀
    })
  }
}

const spawnMeteor = () => {
  const { innerWidth: w } = window
  meteor = {
    x: w * 0.2 + Math.random() * w * 0.6,
    y: -20,
    vx: -(3 + Math.random() * 3),
    vy: 4 + Math.random() * 2,
    life: 1
  }
}

const drawStar = (s, t) => {
  const twinkle = 0.55 + 0.45 * Math.sin(t * 0.001 * s.speed + s.phase)
  const x = s.x + parallax.x * s.depth * 18
  const y = s.y + parallax.y * s.depth * 18
  ctx.globalAlpha = s.baseAlpha * twinkle
  ctx.fillStyle = s.gold ? palette.gold : palette.star
  ctx.beginPath()
  ctx.arc(x, y, s.r, 0, Math.PI * 2)
  ctx.fill()
}

const drawMeteor = () => {
  if (!meteor) return
  meteor.x += meteor.vx
  meteor.y += meteor.vy
  meteor.life -= 0.012
  if (meteor.life <= 0 || meteor.y > window.innerHeight + 40) {
    meteor = null
    return
  }
  const tail = 14
  const grad = ctx.createLinearGradient(
    meteor.x, meteor.y,
    meteor.x - meteor.vx * tail, meteor.y - meteor.vy * tail
  )
  grad.addColorStop(0, palette.star)
  grad.addColorStop(1, 'transparent')
  ctx.globalAlpha = Math.max(meteor.life, 0) * 0.9
  ctx.strokeStyle = grad
  ctx.lineWidth = 1.6
  ctx.beginPath()
  ctx.moveTo(meteor.x, meteor.y)
  ctx.lineTo(meteor.x - meteor.vx * tail, meteor.y - meteor.vy * tail)
  ctx.stroke()
}

const frame = (t) => {
  const { innerWidth: w, innerHeight: h } = window
  ctx.clearRect(0, 0, w, h)

  // 视差平滑逼近
  parallax.x += (parallax.tx - parallax.x) * 0.04
  parallax.y += (parallax.ty - parallax.y) * 0.04

  stars.forEach((s) => drawStar(s, t))
  drawMeteor()
  ctx.globalAlpha = 1
  animationId = requestAnimationFrame(frame)
}

const drawStatic = () => {
  const { innerWidth: w, innerHeight: h } = window
  ctx.clearRect(0, 0, w, h)
  stars.forEach((s) => drawStar(s, 0))
  ctx.globalAlpha = 1
}

const onMouseMove = (e) => {
  parallax.tx = (e.clientX / window.innerWidth - 0.5) * 2
  parallax.ty = (e.clientY / window.innerHeight - 0.5) * 2
}

const start = () => {
  stop()
  if (reducedMotion) {
    drawStatic()
    return
  }
  animationId = requestAnimationFrame(frame)
  meteorTimer = setInterval(() => {
    if (!meteor && Math.random() < 0.5) spawnMeteor()
  }, 6000)
}

const stop = () => {
  if (animationId) cancelAnimationFrame(animationId)
  if (meteorTimer) clearInterval(meteorTimer)
  animationId = null
  meteorTimer = null
}

const handleMotionChange = () => {
  reducedMotion = prefersReducedMotion()
  start()
}

onMounted(() => {
  ctx = canvasRef.value.getContext('2d')
  reducedMotion = prefersReducedMotion()
  readPalette()
  resize()
  start()

  window.addEventListener('resize', resize)
  window.addEventListener('mousemove', onMouseMove, { passive: true })
  window.matchMedia?.('(prefers-reduced-motion: reduce)').addEventListener?.('change', handleMotionChange)

  // 主题切换时重读调色板
  themeObserver = new MutationObserver(readPalette)
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] })
})

onUnmounted(() => {
  stop()
  window.removeEventListener('resize', resize)
  window.removeEventListener('mousemove', onMouseMove)
  window.matchMedia?.('(prefers-reduced-motion: reduce)').removeEventListener?.('change', handleMotionChange)
  themeObserver?.disconnect()
})
</script>

<template>
  <div class="dynamic-background" aria-hidden="true">
    <canvas ref="canvasRef" class="starfield"></canvas>
    <!-- 远景轨道环：缓慢旋转 + 金色行星 -->
    <div class="orbit-ring ring-a"><span class="planet"></span></div>
    <div class="orbit-ring ring-b"><span class="planet"></span></div>
  </div>
</template>

<style scoped>
.dynamic-background {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
  background: transparent;
}

.starfield {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

/* 轨道环：超大虚线圆，缓慢自转；行星为环上一点 */
.orbit-ring {
  position: absolute;
  border: 1px dashed var(--orbit-line);
  border-radius: 50%;
  will-change: transform;
}

.ring-a {
  width: 130vmax;
  height: 130vmax;
  top: -80vmax;
  right: -45vmax;
  animation: orbit-spin 180s linear infinite;
}

.ring-b {
  width: 100vmax;
  height: 100vmax;
  bottom: -75vmax;
  left: -40vmax;
  animation: orbit-spin-reverse 240s linear infinite;
}

.planet {
  position: absolute;
  top: 12%;
  left: 50%;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--orbit-planet);
  box-shadow: 0 0 14px 2px var(--orbit-planet);
}

.ring-b .planet {
  top: auto;
  bottom: 18%;
  width: 7px;
  height: 7px;
  opacity: 0.8;
}

@keyframes orbit-spin {
  to { transform: rotate(360deg); }
}

@keyframes orbit-spin-reverse {
  to { transform: rotate(-360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .orbit-ring {
    animation: none;
  }
}
</style>
