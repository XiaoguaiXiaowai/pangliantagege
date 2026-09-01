<script setup>
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const router = useRouter()
const goHome = () => router.push('/')
</script>

<template>
  <div class="notfound-container">
    <div class="card">
      <div class="emoji">🧭</div>
      <h1>{{ t('notfound.title') }}</h1>
      <p>{{ t('notfound.desc') }}</p>
      <button class="btn" @click="goHome">{{ t('notfound.backHome') }}</button>
    </div>
  </div>
  </template>

<style scoped>
.notfound-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
}
.card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid var(--card-border);
  box-shadow: var(--card-shadow);
  padding: 40px 30px;
  max-width: 520px;
  text-align: center;
}
.emoji {
  font-size: 3rem;
  margin-bottom: 10px;
}
h1 {
  margin: 0 0 10px 0;
  font-size: 1.8rem;
  color: var(--luna-darkest);
}
p {
  margin: 0 0 20px 0;
  color: var(--text-secondary);
  line-height: 1.7;
}
.btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, var(--luna-dark), var(--luna-medium));
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}
</style>
