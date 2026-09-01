<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useLocaleStore } from '../stores/locale'
import { SUPPORTED_LOCALES } from '../i18n'

const localeStore = useLocaleStore()

const open = ref(false)
const currentLabel = computed(() => localeStore.currentLabel)

const toggle = () => {
  open.value = !open.value
}

const select = (code) => {
  localeStore.setLocale(code)
  open.value = false
}

const onKeydown = (e) => {
  if (open.value && e.key === 'Escape') {
    open.value = false
    triggerRef.value?.focus()
  }
}

const triggerRef = ref(null)

const onDocumentClick = () => {
  open.value = false
}

onMounted(() => {
  document.addEventListener('click', onDocumentClick)
  document.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocumentClick)
  document.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div class="language-switcher" @click.stop>
    <button
      ref="triggerRef"
      class="lang-trigger"
      :aria-label="currentLabel"
      :aria-expanded="open"
      aria-haspopup="menu"
      @click="toggle"
    >
      <span class="lang-globe" aria-hidden="true">🌐</span>
      <span class="lang-current">{{ currentLabel }}</span>
      <span class="lang-caret" :class="{ 'is-open': open }" aria-hidden="true">▾</span>
    </button>

    <transition name="lang-pop">
      <ul v-if="open" class="lang-menu" role="menu" :aria-label="currentLabel">
        <li
          v-for="lang in SUPPORTED_LOCALES"
          :key="lang.code"
          role="menuitemradio"
          :aria-checked="localeStore.locale === lang.code"
          :class="{ 'is-active': localeStore.locale === lang.code }"
          @click="select(lang.code)"
        >
          <span class="lang-option-label">{{ lang.label }}</span>
          <span v-if="localeStore.locale === lang.code" class="lang-check" aria-hidden="true">✓</span>
        </li>
      </ul>
    </transition>
  </div>
</template>

<style scoped>
.language-switcher {
  position: relative;
  flex-shrink: 0;
}

.lang-trigger {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  /* 与导航项同高：按钮高度不随语言字形度量变化 */
  height: 40px;
  padding: 0 14px;
  border-radius: 20px;
  background: var(--card-bg-soft);
  border: 1px solid var(--card-border);
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.lang-trigger:hover {
  color: var(--text-primary);
  background-color: var(--nav-hover-bg);
}

.lang-globe {
  font-size: 1rem;
  line-height: 1;
}

.lang-current {
  white-space: nowrap;
}

.lang-caret {
  font-size: 0.7rem;
  color: var(--luna-medium);
  transition: transform 0.25s ease;
}

.lang-caret.is-open {
  transform: rotate(180deg);
}

.lang-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  margin: 0;
  padding: 6px;
  list-style: none;
  min-width: 140px;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 14px;
  box-shadow: var(--card-shadow);
  z-index: 200;
}

.lang-menu li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 9px 14px;
  border-radius: 10px;
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.lang-menu li:hover {
  background: var(--nav-hover-bg);
  color: var(--text-primary);
}

.lang-menu li.is-active {
  color: var(--text-primary);
  background: var(--nav-hover-bg);
}

.lang-check {
  color: var(--luna-medium);
  font-weight: 800;
}

.lang-pop-enter-active,
.lang-pop-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
  transform-origin: top right;
}

.lang-pop-enter-from,
.lang-pop-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.98);
}
</style>