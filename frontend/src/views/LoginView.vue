<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from 'axios'
import { useRouter } from 'vue-router'

const { t } = useI18n()

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

axios.defaults.withCredentials = true

const getCsrfToken = async () => {
  const isProd = import.meta.env.PROD
  const isDevPort = window.location.port === '5173'
  const hostname = window.location.hostname
  const isPublicIP = hostname.startsWith('8.') || (hostname !== '127.0.0.1' && hostname !== 'localhost' && !hostname.startsWith('192.168.'))

  let url = '/api/auth/csrf/'
  if (!isProd || isDevPort) {
    url = `http://${hostname}:8000/api/auth/csrf/`
  }
  if (isPublicIP && isDevPort) {
    url = `http://${hostname}:8000/api/auth/csrf/`
  }
  const resp = await axios.get(url)
  return resp.data?.csrfToken
}

const getCookie = (name) => {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
  if (match) return match[2]
  return ''
}

const onSubmit = async () => {
  try {
    loading.value = true
    error.value = ''
    await getCsrfToken()
    const csrftoken = getCookie('csrftoken')

    const isProd = import.meta.env.PROD
    const isDevPort = window.location.port === '5173'
    const hostname = window.location.hostname
    const isPublicIP = hostname.startsWith('8.') || (hostname !== '127.0.0.1' && hostname !== 'localhost' && !hostname.startsWith('192.168.'))

    let url = '/api/auth/login/'
    if (!isProd || isDevPort) {
      url = `http://${hostname}:8000/api/auth/login/`
    }
    if (isPublicIP && isDevPort) {
      url = `http://${hostname}:8000/api/auth/login/`
    }

    await axios.post(url, { username: username.value, password: password.value }, {
      headers: { 'X-CSRFToken': csrftoken }
    })
    router.push('/')
  } catch (e) {
    error.value = t('login.error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <h1>{{ t('login.title') }}</h1>
      <p class="desc">{{ t('login.desc') }}</p>
      <form @submit.prevent="onSubmit">
        <div class="field">
          <label>{{ t('login.username') }}</label>
          <input v-model="username" type="text" required />
        </div>
        <div class="field">
          <label>{{ t('login.password') }}</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit" :disabled="loading">{{ loading ? t('login.submitting') : t('login.submit') }}</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}
.login-card {
  width: 100%;
  max-width: 420px;
  background: var(--card-bg);
  border-radius: 16px;
  border: 1px solid var(--card-border);
  box-shadow: var(--card-shadow);
  padding: 30px;
}
h1 {
  margin: 0 0 10px 0;
  font-size: 1.6rem;
  color: var(--luna-darkest);
}
.desc {
  margin: 0 0 20px 0;
  color: var(--text-secondary);
}
.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}
label {
  font-size: 0.9rem;
  color: var(--text-secondary);
}
input {
  padding: 10px 12px;
  border: 1px solid var(--card-border);
  border-radius: 10px;
  outline: none;
  background: var(--card-bg-soft);
  color: var(--text-primary);
}
button {
  width: 100%;
  padding: 12px;
  background: var(--btn-primary-bg);
  color: var(--btn-primary-color);
  border-radius: 12px;
  border: none;
  font-weight: 600;
  cursor: pointer;
}
.error {
  color: #c0392b;
  margin-top: 12px;
}
</style>
