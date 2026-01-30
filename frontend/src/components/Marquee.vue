<script setup>
defineProps({
  reverse: { type: Boolean, default: false },
  pauseOnHover: { type: Boolean, default: false },
  vertical: { type: Boolean, default: false },
  repeat: { type: Number, default: 2 },
  duration: { type: String, default: '30s' },
  gap: { type: String, default: '20px' }
})
</script>

<template>
  <div 
    class="marquee-group"
    :class="{ 'vertical': vertical }"
    :style="{ 
      '--duration': duration,
      '--gap': gap
    }"
  >
    <div 
      v-for="i in repeat" 
      :key="i"
      class="marquee-content"
      :class="{ 
        'reverse': reverse, 
        'pause-on-hover': pauseOnHover,
        'vertical': vertical
      }"
    >
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.marquee-group {
  display: flex;
  overflow: hidden;
  user-select: none;
  gap: var(--gap);
  width: 100%;
  mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
  -webkit-mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
}

.marquee-group.vertical {
  flex-direction: column;
  height: 100%;
  mask-image: linear-gradient(to bottom, transparent, black 10%, black 90%, transparent);
  -webkit-mask-image: linear-gradient(to bottom, transparent, black 10%, black 90%, transparent);
}

.marquee-content {
  flex-shrink: 0;
  display: flex;
  justify-content: space-around;
  gap: var(--gap);
  min-width: 100%;
  animation: scroll var(--duration) linear infinite;
}

.marquee-content.vertical {
  flex-direction: column;
  min-height: 100%;
  min-width: auto;
  animation-name: scroll-vertical;
}

@keyframes scroll {
  from { transform: translateX(0); }
  to { transform: translateX(calc(-100% - var(--gap))); }
}

@keyframes scroll-vertical {
  from { transform: translateY(0); }
  to { transform: translateY(calc(-100% - var(--gap))); }
}

.marquee-content.reverse {
  animation-direction: reverse;
}

.marquee-content.pause-on-hover:hover {
  animation-play-state: paused;
}
</style>
