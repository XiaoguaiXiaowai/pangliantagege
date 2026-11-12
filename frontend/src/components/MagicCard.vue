<script setup>
import { ref } from 'vue'

/**
 * 全息卡片（Holo Card）
 * - 流动全息渐变描边（conic-gradient + @property 角度动画，hover 时旋转）
 * - 鼠标 3D 倾斜（tilt）+ 全息高光跟随
 * - 对外 API 不变：默认插槽
 */
const cardRef = ref(null)
const mouseX = ref(0)
const mouseY = ref(0)
const rotX = ref(0)
const rotY = ref(0)
const hovering = ref(false)

const handleMouseMove = (e) => {
  if (!cardRef.value) return
  const rect = cardRef.value.getBoundingClientRect()
  mouseX.value = e.clientX - rect.left
  mouseY.value = e.clientY - rect.top
  // 以卡片中心为原点的倾斜角（除数越大越柔和）
  rotX.value = -((mouseY.value - rect.height / 2) / 28)
  rotY.value = (mouseX.value - rect.width / 2) / 28
}

const handleEnter = () => {
  hovering.value = true
}

const handleLeave = () => {
  hovering.value = false
  rotX.value = 0
  rotY.value = 0
}
</script>

<template>
  <div
    ref="cardRef"
    class="magic-card"
    :class="{ hovering }"
    @mousemove="handleMouseMove"
    @mouseenter="handleEnter"
    @mouseleave="handleLeave"
    :style="{
      '--mouse-x': `${mouseX}px`,
      '--mouse-y': `${mouseY}px`,
      transform: `perspective(900px) translateY(${hovering ? -3 : 0}px) rotateX(${rotX}deg) rotateY(${rotY}deg)`
    }"
  >
    <div class="magic-card-content">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.magic-card {
  position: relative;
  border-radius: 14px;
  /* 双层背景：内层卡片底色 + 外层全息渐变描边 */
  background-image:
    linear-gradient(var(--card-bg), var(--card-bg)),
    var(--holo-border);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  border: 1px solid transparent;
  transition: transform 0.18s ease-out, box-shadow 0.3s ease;
  will-change: transform;
}

.magic-card.hovering {
  /* hover 时全息描边流动 + 发光 */
  animation: holo-spin 5s linear infinite;
  box-shadow:
    0 12px 36px -8px var(--holo-glow),
    0 0 0 1px rgba(255, 255, 255, 0.04);
}

.magic-card-content {
  position: relative;
  z-index: 10;
  padding: 1.5rem;
  height: 100%;
}

/* 全息高光：随鼠标移动的虹彩热点 */
.magic-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(
    480px circle at var(--mouse-x) var(--mouse-y),
    var(--holo-glow),
    transparent 45%
  );
  opacity: 0;
  transition: opacity 0.4s;
  pointer-events: none;
  z-index: 1;
}

.magic-card.hovering::before {
  opacity: 1;
}

@media (prefers-reduced-motion: reduce) {
  .magic-card,
  .magic-card.hovering {
    animation: none;
    transform: none !important;
  }
}
</style>
