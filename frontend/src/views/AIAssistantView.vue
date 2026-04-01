<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

const messages = ref([
  {
    role: 'assistant',
    content: '你好！我是基于私域RAG模型的李佳的智能助手。请问有什么我可以帮你的吗？'
  }
])
const inputMessage = ref('')
const isLoading = ref(false)
const chatContainer = ref(null)

// Connection status state: 'checking' | 'connected' | 'error'
const connectionStatus = ref('checking')

const chatHistory = ref([])

// Check RAG service connection status
const checkConnectionStatus = async () => {
  connectionStatus.value = 'checking'
  try {
    const isProd = import.meta.env.PROD
    const isDevPort = window.location.port === '5173'
    const hostname = window.location.hostname
    
    // We ping the Django backend which will check the RAG service
    let healthApiUrl = '/api/ai/health/'
    
    if (!isProd || isDevPort) {
        healthApiUrl = `http://${hostname}:8000/api/ai/health/`
    }

    const response = await axios.get(healthApiUrl, { timeout: 3000 })
    if (response.data && response.data.status === 'ok') {
      connectionStatus.value = 'connected'
    } else {
      connectionStatus.value = 'error'
    }
  } catch (error) {
    console.error('Failed to check RAG service connection:', error)
    connectionStatus.value = 'error'
  }
}

onMounted(() => {
  checkConnectionStatus()
})

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value) return

  const userQuestion = inputMessage.value.trim()
  
  // Add user message to UI
  messages.value.push({
    role: 'user',
    content: userQuestion
  })
  
  inputMessage.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    const isProd = import.meta.env.PROD
    const isDevPort = window.location.port === '5173'
    const hostname = window.location.hostname
    
    // 默认使用相对路径，借助 Vite 代理或 Nginx 解决跨域问题
    let apiUrl = '/api/chat'
    
    // 如果在非开发环境且没有使用网关代理，强制指向初始指定的 RAG 服务器 IP (后续可通过 Nginx 动态代理覆盖)
    if (!isProd && !isDevPort && hostname !== 'localhost' && hostname !== '127.0.0.1') {
      apiUrl = `http://139.28.178.226:8001/api/chat`
    } else if (isProd) {
      // 生产环境下，通常我们希望直接打给 Prod 服务器自己的 Nginx，让 Nginx 去代理到动态的 MacBook IP
      // 这里保持相对路径 '/api/chat'，让 Prod 的 Nginx 接管
      apiUrl = '/api/chat'
    }

    const payload = {
      question: userQuestion,
      chat_history: chatHistory.value
    }

    const response = await axios.post(apiUrl, payload)
    
    // Parse response
    let assistantReply = '抱歉，我没有理解返回的数据格式。'
    if (response.data) {
      if (typeof response.data === 'string') {
        assistantReply = response.data
      } else if (response.data.answer) {
        assistantReply = response.data.answer
      } else if (response.data.response) {
        assistantReply = response.data.response
      } else if (response.data.text) {
        assistantReply = response.data.text
      } else {
        assistantReply = JSON.stringify(response.data)
      }
    }

    // Add assistant message to UI
    messages.value.push({
      role: 'assistant',
      content: assistantReply
    })
    
    // Update chat history for next request
    chatHistory.value.push(
      { role: "user", content: userQuestion },
      { role: "assistant", content: assistantReply }
    )

  } catch (error) {
    console.error('AI Request Error:', error)
    let errorMsg = '请求失败，请检查本地 AI 服务是否已启动 (端口 8001)。'
    if (error.response && error.response.data && error.response.data.detail) {
      errorMsg += ` 错误信息: ${JSON.stringify(error.response.data.detail)}`
    }
    
    messages.value.push({
      role: 'assistant',
      content: errorMsg,
      isError: true
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}
</script>

<template>
  <div class="ai-assistant-view">
    <div class="chat-container">
      <div class="chat-header">
        <div class="header-title">
          <span class="emoji-icon">🛸</span>
          <h2>私域RAG智能助手</h2>
        </div>
        <div class="header-status" :class="connectionStatus">
          <span class="status-dot"></span>
          <span>
            {{ 
              connectionStatus === 'checking' ? '服务链接中' : 
              (connectionStatus === 'connected' ? '服务已连接' : '服务链接失败') 
            }}
          </span>
        </div>
      </div>

      <div class="chat-messages" ref="chatContainer">
        <div 
          v-for="(msg, index) in messages" 
          :key="index"
          class="message-wrapper"
          :class="msg.role === 'user' ? 'message-user' : 'message-assistant'"
        >
          <div class="avatar">
            {{ msg.role === 'user' ? '👤' : '👧' }}
          </div>
          <div class="message-bubble" :class="{ 'error-msg': msg.isError }">
            <div class="message-content">{{ msg.content }}</div>
          </div>
        </div>
        
        <div v-if="isLoading" class="message-wrapper message-assistant">
          <div class="avatar">👧</div>
          <div class="message-bubble loading-bubble">
            <div class="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <div class="input-wrapper">
          <textarea
            v-model="inputMessage"
            placeholder="输入你的问题... (Enter 发送，Shift+Enter 换行)"
            @keydown="handleKeydown"
            :disabled="isLoading"
            rows="1"
          ></textarea>
          <button 
            class="send-btn" 
            @click="sendMessage"
            :disabled="!inputMessage.trim() || isLoading"
          >
            <span class="send-icon">🚀</span>
            发送
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ai-assistant-view {
  height: calc(100vh - 160px); /* Adjust based on header/footer */
  min-height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
}

.chat-container {
  width: 100%;
  max-width: 900px;
  height: 100%;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 20px;
  border: 1px solid rgba(167, 235, 242, 0.4);
  box-shadow: 0 10px 30px rgba(1, 28, 64, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid rgba(167, 235, 242, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.5);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.emoji-icon {
  font-size: 1.5rem;
}

.header-title h2 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--luna-darkest);
  font-weight: 700;
}

.header-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

/* Status: Connected (Green) */
.header-status.connected {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}
.header-status.connected .status-dot {
  background-color: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
}

/* Status: Checking (Yellow/Orange) */
.header-status.checking {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.1);
}
.header-status.checking .status-dot {
  background-color: #f59e0b;
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
  animation: pulse-dot 1.5s infinite;
}

/* Status: Error (Red) */
.header-status.error {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}
.header-status.error .status-dot {
  background-color: #ef4444;
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.5);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

@keyframes pulse-dot {
  0% { transform: scale(0.8); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 1; }
  100% { transform: scale(0.8); opacity: 0.5; }
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  scroll-behavior: smooth;
}

/* Custom Scrollbar for messages */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}
.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}
.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(167, 235, 242, 0.5);
  border-radius: 10px;
}

.message-wrapper {
  display: flex;
  gap: 12px;
  max-width: 85%;
}

.message-user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-assistant {
  align-self: flex-start;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;
  background: #fff;
  border: 1px solid rgba(167, 235, 242, 0.5);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
}

.message-user .avatar {
  background: var(--luna-lightest);
  border-color: var(--luna-medium);
}

.message-bubble {
  padding: 14px 18px;
  border-radius: 18px;
  font-size: 0.95rem;
  line-height: 1.6;
  word-break: break-word;
  white-space: pre-wrap;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.message-user .message-bubble {
  background: linear-gradient(135deg, var(--luna-medium), var(--luna-dark));
  color: #fff;
  border-top-right-radius: 4px;
}

.message-assistant .message-bubble {
  background: #fff;
  color: var(--text-primary);
  border: 1px solid rgba(167, 235, 242, 0.3);
  border-top-left-radius: 4px;
}

.error-msg {
  background: #fef2f2 !important;
  color: #ef4444 !important;
  border-color: #fca5a5 !important;
}

.loading-bubble {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  padding: 14px 20px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background-color: var(--luna-medium);
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}
.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

.chat-input-area {
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.7);
  border-top: 1px solid rgba(167, 235, 242, 0.3);
}

.input-wrapper {
  display: flex;
  gap: 12px;
  background: #fff;
  border: 1px solid rgba(167, 235, 242, 0.6);
  border-radius: 16px;
  padding: 8px 12px;
  box-shadow: 0 4px 12px rgba(1, 28, 64, 0.05);
  transition: border-color 0.3s, box-shadow 0.3s;
}

.input-wrapper:focus-within {
  border-color: var(--luna-medium);
  box-shadow: 0 4px 15px rgba(38, 101, 140, 0.15);
}

textarea {
  flex: 1;
  border: none;
  background: transparent;
  resize: none;
  padding: 8px;
  font-family: inherit;
  font-size: 0.95rem;
  color: var(--text-primary);
  outline: none;
  max-height: 120px;
  min-height: 24px;
  overflow-y: auto;
}

textarea::placeholder {
  color: #a0aec0;
}

.send-btn {
  background: var(--luna-medium);
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 0 20px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.send-btn:hover:not(:disabled) {
  background: var(--luna-dark);
  transform: translateY(-1px);
}

.send-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
  opacity: 0.7;
}

.send-icon {
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .ai-assistant-view {
    height: calc(100vh - 120px);
    padding: 0;
  }
  
  .chat-container {
    border-radius: 0;
    border: none;
  }
  
  .message-wrapper {
    max-width: 95%;
  }
}
</style>
