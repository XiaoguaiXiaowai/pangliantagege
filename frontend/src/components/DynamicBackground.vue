<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const circles = ref([])
const CIRCLE_COUNT = 2
const RADIUS = 75

let animationId

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
      x = innerWidth / 2 + (i * 10)
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
      radius: RADIUS,
      color: 'transparent'
    })
  }
  
  circles.value = newCircles
}

const updatePosition = () => {
  const { innerWidth, innerHeight } = window
  
  // 1. Move and Wall Collision
  circles.value.forEach(c => {
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
      
      // If colliding
      if (distance < c1.radius + c2.radius) {
        // Resolve overlap (move apart)
        const overlap = (c1.radius + c2.radius - distance) / 2
        // Avoid division by zero
        const safeDist = distance || 0.001
        const nx = dx / safeDist
        const ny = dy / safeDist
        
        c1.x -= nx * overlap
        c1.y -= ny * overlap
        c2.x += nx * overlap
        c2.y += ny * overlap
        
        // Elastic collision physics
        // Normal vector (n) = (nx, ny)
        // Tangent vector (t) = (-ny, nx)
        
        const tx = -ny
        const ty = nx
        
        // Project velocities onto Normal and Tangent
        const v1n = c1.dx * nx + c1.dy * ny
        const v1t = c1.dx * tx + c1.dy * ty
        
        const v2n = c2.dx * nx + c2.dy * ny
        const v2t = c2.dx * tx + c2.dy * ty
        
        // Swap normal components (equal mass)
        // v1n_new = v2n
        // v2n_new = v1n
        
        // Convert scalar normal/tangent velocities back to vectors
        c1.dx = v2n * nx + v1t * tx
        c1.dy = v2n * ny + v1t * ty
        
        c2.dx = v1n * nx + v2t * tx
        c2.dy = v1n * ny + v2t * ty
      }
    }
  }

  animationId = requestAnimationFrame(updatePosition)
}

onMounted(() => {
  initCircles()
  updatePosition()
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>

<template>
  <div class="dynamic-background">
    <div 
      v-for="circle in circles"
      :key="circle.id"
      class="floating-circle"
      :style="{
        left: `${circle.x}px`,
        top: `${circle.y}px`,
        width: `${circle.radius * 2}px`,
        height: `${circle.radius * 2}px`,
        backgroundColor: circle.color
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
  background-color: var(--bg-body);
}

.floating-circle {
  position: absolute;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  will-change: transform, left, top;
  border: 10px solid rgba(205, 233, 239, 0.6); /* Luna Light border */
  box-sizing: border-box;
}
</style>
