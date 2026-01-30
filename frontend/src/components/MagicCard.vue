<script setup>
import { ref } from 'vue'

const cardRef = ref(null)
const mouseX = ref(0)
const mouseY = ref(0)

const handleMouseMove = (e) => {
  if (!cardRef.value) return
  const rect = cardRef.value.getBoundingClientRect()
  mouseX.value = e.clientX - rect.left
  mouseY.value = e.clientY - rect.top
}
</script>

<template>
  <div 
    ref="cardRef"
    class="magic-card"
    @mousemove="handleMouseMove"
    :style="{
      '--mouse-x': `${mouseX}px`,
      '--mouse-y': `${mouseY}px`
    }"
  >
    <div class="magic-card-bg"></div>
    <div class="magic-card-content">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.magic-card {
  position: relative;
  border-radius: 12px;
  background-color: #fff;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  transition: transform 0.2s;
}

.magic-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.1);
}

.magic-card-content {
  position: relative;
  z-index: 10;
  padding: 1.5rem;
  height: 100%;
}

/* Spotlight effect */
.magic-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    600px circle at var(--mouse-x) var(--mouse-y),
    rgba(66, 185, 131, 0.1),
    transparent 40%
  );
  opacity: 0;
  transition: opacity 0.5s;
  pointer-events: none;
  z-index: 1;
}

.magic-card:hover::before {
  opacity: 1;
}

/* Border spotlight (optional enhancement) */
.magic-card::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    600px circle at var(--mouse-x) var(--mouse-y),
    rgba(66, 185, 131, 0.4),
    transparent 40%
  );
  opacity: 0;
  z-index: 0;
  pointer-events: none;
}

.magic-card:hover::after {
  opacity: 1;
}
</style>