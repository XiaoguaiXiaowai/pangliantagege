<script setup>
import { computed } from 'vue'
import { useThemeStore } from '../stores/theme'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)
</script>

<template>
  <button
    class="theme-toggle"
    type="button"
    role="switch"
    :aria-checked="isDark"
    :aria-label="isDark ? '切换到浅色模式' : '切换到深色模式'"
    :title="isDark ? '切换到浅色模式' : '切换到深色模式'"
    @click="themeStore.toggle()"
  >
    <span class="toggle-icon" :class="{ 'is-dark': isDark }" aria-hidden="true">
      <!-- 太阳 -->
      <svg
        class="icon-sun"
        viewBox="0 0 24 24"
        width="18"
        height="18"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
      >
        <circle cx="12" cy="12" r="4.5" />
        <path d="M12 2.5v2.4M12 19.1v2.4M4.3 4.3l1.7 1.7M18 18l1.7 1.7M2.5 12h2.4M19.1 12h2.4M4.3 19.7 6 18M18 6l1.7-1.7" />
      </svg>
      <!-- 月亮 -->
      <svg class="icon-moon" viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
        <path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a6.5 6.5 0 0 0 9.8 9.8Z" />
      </svg>
    </span>
  </button>
</template>

<style scoped>
.theme-toggle {
  height: 40px;
  width: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--card-bg-soft);
  border: 1px solid var(--card-border);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
  position: relative;
}

.theme-toggle:hover {
  color: var(--text-primary);
  border-color: var(--luna-medium);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(38, 101, 140, 0.15);
}

[data-theme='dark'] .theme-toggle:hover {
  box-shadow: 0 4px 12px rgba(95, 199, 220, 0.2);
}

.toggle-icon {
  position: relative;
  display: block;
  width: 18px;
  height: 18px;
}

.icon-sun,
.icon-moon {
  position: absolute;
  inset: 0;
  transition: opacity 0.35s ease, transform 0.35s ease;
}

.icon-moon {
  opacity: 0;
  transform: rotate(-90deg) scale(0.6);
}

.toggle-icon.is-dark .icon-sun {
  opacity: 0;
  transform: rotate(90deg) scale(0.6);
}

.toggle-icon.is-dark .icon-moon {
  opacity: 1;
  transform: rotate(0deg) scale(1);
}
</style>
