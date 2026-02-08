<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const circle = ref({
  x: 0,
  y: 0,
  radius: 85, // Further reduced radius (was 150)
  dx: 2,
  dy: 2,
  color: 'transparent' // Transparent center
})

let animationId

const updatePosition = () => {
  const { innerWidth, innerHeight } = window
  const c = circle.value
  
  c.x += c.dx
  c.y += c.dy

  // Bounce logic
  // We check if the edge of the circle hits the screen edge
  if (c.x + c.radius > innerWidth) {
    c.x = innerWidth - c.radius
    c.dx = -c.dx
  } else if (c.x - c.radius < 0) {
    c.x = c.radius
    c.dx = -c.dx
  }

  if (c.y + c.radius > innerHeight) {
    c.y = innerHeight - c.radius
    c.dy = -c.dy
  } else if (c.y - c.radius < 0) {
    c.y = c.radius
    c.dy = -c.dy
  }

  animationId = requestAnimationFrame(updatePosition)
}

onMounted(() => {
  const { innerWidth, innerHeight } = window
  // Initialize random position within bounds (ensuring full circle is initially visible or at least safe)
  // Safe zone: radius -> width-radius
  const safeX = Math.max(circle.value.radius, innerWidth - circle.value.radius)
  const safeY = Math.max(circle.value.radius, innerHeight - circle.value.radius)
  
  // If screen is too small, just center it roughly
  if (innerWidth < circle.value.radius * 2) {
    circle.value.x = innerWidth / 2
  } else {
    circle.value.x = Math.random() * (innerWidth - circle.value.radius * 2) + circle.value.radius
  }

  if (innerHeight < circle.value.radius * 2) {
    circle.value.y = innerHeight / 2
  } else {
    circle.value.y = Math.random() * (innerHeight - circle.value.radius * 2) + circle.value.radius
  }
  
  // Random velocity (arbitrary angle)
  const speed = 1.0 // Slow movement
  const angle = Math.random() * Math.PI * 2
  circle.value.dx = Math.cos(angle) * speed
  circle.value.dy = Math.sin(angle) * speed
  
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
  z-index: 0; /* Changed from -1 to 0 */
  pointer-events: none; /* Let clicks pass through */
  overflow: hidden;
  background-color: var(--bg-body); /* Ensure base background is present */
}

.floating-circle {
  position: absolute;
  border-radius: 50%;
  transform: translate(-50%, -50%); /* Center the div on x,y */
  will-change: transform, left, top;
  border: 15px solid rgba(199, 227, 234, 0.6); /* Slightly obvious color (Luna Light) */
  box-sizing: border-box;
}
</style>
