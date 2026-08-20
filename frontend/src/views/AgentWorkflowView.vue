<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

// ============================================================
// 作品在线地址
// ============================================================
const PROJECT_URL = 'https://playground.pangliantagege.top'

// ---------------- 三大支柱 ----------------
const pillars = [
  {
    icon: '🛡️',
    title: '可靠',
    en: 'Reliable',
    color: '#26658C',
    points: [
      '确定性状态机约束动作序列，禁止跳步',
      '幂等重试 + 失败补偿，重复执行不重复授权',
      '步数 / Token / 时间三重预算，触顶即终止',
      '收敛校验 done:true 通过才交付'
    ]
  },
  {
    icon: '🔐',
    title: '可控',
    en: 'Controlled',
    color: '#0e7490',
    points: [
      'IAM 最小权限 + 多租户物理隔离',
      '工具白名单注册表，未登记工具直接拒绝',
      '参数强类型校验 + 敏感信息脱敏',
      '高风险动作交还人工 HITL 审批'
    ]
  },
  {
    icon: '📋',
    title: '可审计',
    en: 'Auditable',
    color: '#7c3aed',
    points: [
      'Trace 全链路回放，一步不差',
      '模型 / 提示词版本逐次留痕',
      '状态迁移、工具调用逐条落库',
      '成功率 / 延迟 / 成本 / 人工接管率可视化'
    ]
  }
]

// ---------------- 8 大工程能力 ----------------
const capabilities = [
  { num: '①', title: '流程定义', desc: '把模糊需求结构化，明确哪些交给 Agent、哪些交给 Workflow，划清风险边界', tags: ['结构化输入', '风险边界'] },
  { num: '②', title: '业务入口', desc: '身份校验、租户隔离、IAM 最小权限、输入风险分级', tags: ['鉴权', '租户隔离', '最小权限'] },
  { num: '③', title: '核心 LOOP', desc: '上下文"选/压/截"、模型路由、四层约束、记忆五分层、异常处理', tags: ['上下文装配', '模型路由'] },
  { num: '④', title: '业务出口', desc: 'HITL 审批、收敛校验 done:true、交付归档', tags: ['HITL 审批', '收敛校验', '归档'] },
  { num: '⑤', title: '工具层 MPC-Skill', desc: '白名单、参数校验、脱敏、HITL、幂等补偿、审计', tags: ['白名单', '脱敏', '幂等'] },
  { num: '⑥', title: 'Trace', desc: '模型/提示词版本、上下文来源、工具调用、状态迁移、延迟留痕', tags: ['版本留痕', '全链路回放'] },
  { num: '⑦', title: '监控评估', desc: '成功率、正确失败率、延迟、成本、人工接管率', tags: ['成功率', '延迟', '成本'] },
  { num: '⑧', title: '预算', desc: '步数 / Token / 时间三重预算，触顶即终止防跑飞', tags: ['步数', 'Token', '时间'] }
]

// ---------------- 架构图 iframe 高度自适应 ----------------
// 完整模式（非 embed）嵌入 archify 架构图：Light/Classic/Present/Export、PATH·MAP·LENS、
// 悬停灰化与连线动效、点击关系透镜详情均为图内原生功能。
// iframe 同源，读取其文档高度，让外层卡片贴合内容高度。
const archFrameRef = ref(null)
let heightTimer = null

const syncArchHeight = () => {
  const frame = archFrameRef.value
  if (!frame) return
  try {
    const doc = frame.contentDocument
    if (!doc || !doc.body) return
    const h = doc.body.scrollHeight
    const current = parseFloat(frame.style.height) || 0
    if (h > 120 && Math.abs(h - current) > 4) {
      frame.style.height = `${h}px`
    }
  } catch (_) {
    /* 跨域不可读时忽略，保持 CSS 初始比例高度 */
  }
}

onMounted(() => {
  window.addEventListener('resize', syncArchHeight)
  // 图内操作（面板展开 / present / 主题与风格切换）会改变文档高度，轻量轮询兜底
  heightTimer = setInterval(syncArchHeight, 800)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', syncArchHeight)
  if (heightTimer) clearInterval(heightTimer)
})
</script>

<template>
  <div class="agent-workflow-view">
    <!-- ============ Hero ============ -->
    <section class="hero">
      <span class="hero-badge">🤖 作品 · 企业级 Agent 工程实践</span>
      <h1 class="hero-title">企业级混合 Agent 工作流</h1>
      <p class="hero-sub">
        一个企业 IT 工单智能处理系统 —— 不是演示 AI 多聪明，<br />
        而是演示 <strong>AI 如何被可靠、可控、可审计地接进企业业务</strong>。
      </p>

      <div class="hero-actions">
        <a class="btn-primary" :href="PROJECT_URL" target="_blank" rel="noopener noreferrer">
          🚀 查看在线 Demo
        </a>
        <a class="btn-ghost" href="#architecture">系统架构图</a>
        <a class="btn-ghost" href="#capabilities">八大工程能力</a>
      </div>
    </section>

    <!-- ============ 三大支柱 ============ -->
    <section class="section">
      <h2>为什么是"企业级"？</h2>
      <p class="section-sub">把不可控的 Agent，变成可控的流程</p>
      <div class="pillar-grid">
        <div v-for="p in pillars" :key="p.title" class="pillar-card">
          <div class="pillar-icon" :style="{ background: `linear-gradient(135deg, ${p.color}, #011C40)` }">
            {{ p.icon }}
          </div>
          <h3>{{ p.title }} <span class="pillar-en">{{ p.en }}</span></h3>
          <ul>
            <li v-for="(pt, i) in p.points" :key="i">{{ pt }}</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ============ 系统架构图（完整交互模式） ============ -->
    <section class="section" id="architecture">
      <h2>系统架构图</h2>
      <p class="section-sub">
        完整交互模式 —— 请使用工具栏（主题 / 风格 / 演示 / 导出）、PATH·MAP·LENS 控件、悬停与点击组件了解系统架构关系与详情
      </p>
      <div class="arch-card">
        <iframe
          ref="archFrameRef"
          class="arch-frame"
          src="/agent-harness-architecture.html?theme=light"
          title="企业级混合 Agent 工作流 · 系统架构图"
          loading="lazy"
          @load="syncArchHeight"
        ></iframe>
      </div>
    </section>

    <!-- ============ 八大工程能力 ============ -->
    <section class="section" id="capabilities">
      <h2>八大工程能力</h2>
      <p class="section-sub">可靠、可控、可审计的具体落地实现</p>
      <div class="cap-grid">
        <div v-for="cap in capabilities" :key="cap.num" class="cap-card">
          <span class="cap-num">{{ cap.num }}</span>
          <h3>{{ cap.title }}</h3>
          <p>{{ cap.desc }}</p>
          <div class="cap-tags">
            <span v-for="t in cap.tags" :key="t" class="cap-tag">{{ t }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.agent-workflow-view {
  display: flex;
  flex-direction: column;
  gap: 56px;
  padding-bottom: 16px;
}

/* ---------- Hero ---------- */
.hero {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #011C40 0%, #023859 55%, #26658C 120%);
  border-radius: 24px;
  padding: 56px 48px 40px;
  color: #fff;
  text-align: center;
  box-shadow: 0 20px 50px rgba(1, 28, 64, 0.28);
}

.hero::before,
.hero::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.35;
  pointer-events: none;
}

.hero::before {
  width: 380px;
  height: 380px;
  background: #54ACBF;
  top: -160px;
  right: -100px;
}

.hero::after {
  width: 320px;
  height: 320px;
  background: #A7EBF2;
  bottom: -140px;
  left: -80px;
}

.hero-badge {
  position: relative;
  z-index: 1;
  display: inline-block;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(8px);
  border-radius: 999px;
  padding: 6px 18px;
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: #A7EBF2;
  margin-bottom: 20px;
}

.hero-title {
  position: relative;
  z-index: 1;
  color: #fff;
  font-size: clamp(1.9rem, 4.5vw, 2.8rem);
  margin-bottom: 16px;
  text-shadow: 0 2px 20px rgba(167, 235, 242, 0.35);
}

.hero-sub {
  position: relative;
  z-index: 1;
  color: rgba(255, 255, 255, 0.82);
  font-size: 1.02rem;
  line-height: 1.8;
  margin-bottom: 28px;
}

.hero-sub strong {
  color: #A7EBF2;
}

.hero-actions {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
}

.btn-primary {
  display: inline-block;
  background: linear-gradient(135deg, #A7EBF2, #54ACBF);
  color: #011C40;
  font-weight: 800;
  font-size: 1rem;
  padding: 14px 36px;
  border-radius: 999px;
  box-shadow: 0 8px 24px rgba(84, 172, 191, 0.45);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(84, 172, 191, 0.6);
  opacity: 1;
  color: #011C40;
}

.btn-ghost {
  display: inline-block;
  border: 1.5px solid rgba(255, 255, 255, 0.45);
  color: #fff;
  font-weight: 600;
  padding: 13px 28px;
  border-radius: 999px;
  transition: all 0.3s ease;
}

.btn-ghost:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  opacity: 1;
}

.hero-stats {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 36px;
  padding-top: 28px;
  border-top: 1px solid rgba(255, 255, 255, 0.16);
}

.stat .num {
  font-size: 1.55rem;
  font-weight: 800;
  color: #A7EBF2;
  margin-bottom: 4px;
}

.stat .label {
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.72);
  line-height: 1.5;
}

/* ---------- Section 通用 ---------- */
.section h2 {
  text-align: center;
  font-size: 1.7rem;
  margin-bottom: 6px;
}

.section-sub {
  text-align: center;
  color: #5a6b7c;
  font-size: 0.92rem;
  margin-bottom: 30px;
}

/* ---------- 三大支柱 ---------- */
.pillar-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.pillar-card {
  background: #fff;
  border: 1px solid var(--card-border);
  border-radius: 20px;
  padding: 28px 24px;
  box-shadow: var(--card-shadow);
  transition: all 0.3s ease;
}

.pillar-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 16px 40px rgba(1, 28, 64, 0.14);
}

.pillar-icon {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  margin-bottom: 16px;
  box-shadow: 0 6px 16px rgba(1, 28, 64, 0.2);
}

.pillar-card h3 {
  margin-bottom: 12px;
  font-size: 1.15rem;
}

.pillar-en {
  font-size: 0.72rem;
  font-weight: 600;
  color: #7a8b9c;
  letter-spacing: 0.06em;
  margin-left: 4px;
}

.pillar-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.pillar-card li {
  font-size: 0.86rem;
  color: #44566a;
  line-height: 1.55;
  padding-left: 20px;
  position: relative;
}

.pillar-card li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #54ACBF;
  font-weight: 800;
  font-size: 0.8rem;
}

/* ---------- 系统架构图 ---------- */
.arch-card {
  background: #fff;
  border: 1px solid var(--card-border);
  border-radius: 20px;
  padding: 16px;
  box-shadow: var(--card-shadow);
  overflow: hidden;
}

.arch-frame {
  display: block;
  width: 100%;
  aspect-ratio: 1300 / 760; /* 初始兜底高度，加载后由 JS 按内容自适应 */
  border: 0;
  border-radius: 12px;
  background: #f8fafc;
}

/* ---------- 8 大能力 ---------- */
.cap-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.cap-card {
  background: #fff;
  border: 1px solid var(--card-border);
  border-radius: 16px;
  padding: 20px;
  box-shadow: var(--card-shadow);
  display: flex;
  flex-direction: column;
  min-width: 0;
  transition: all 0.3s ease;
}

.cap-card:hover {
  transform: translateY(-4px);
  border-color: #54ACBF;
  box-shadow: 0 12px 30px rgba(38, 101, 140, 0.16);
}

.cap-num {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #26658C, #011C40);
  color: #fff;
  font-size: 1.2rem;
  font-weight: 800;
  margin-bottom: 14px;
  box-shadow: 0 6px 14px rgba(2, 56, 89, 0.3);
}

.cap-card h3 {
  font-size: 0.98rem;
  margin-bottom: 8px;
}

.cap-card p {
  font-size: 0.8rem;
  color: #5a6b7c;
  line-height: 1.6;
  flex: 1;
  margin-bottom: 12px;
}

.cap-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.cap-tag {
  background: #eef8fb;
  border: 1px solid rgba(167, 235, 242, 0.8);
  color: #26658C;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 999px;
  white-space: nowrap;
}

/* ---------- 响应式 ---------- */
@media (max-width: 900px) {
  .pillar-grid {
    grid-template-columns: 1fr;
  }

  .cap-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .hero {
    padding: 40px 24px 32px;
  }
}

@media (max-width: 600px) {
  .agent-workflow-view {
    gap: 40px;
  }

  .cap-grid {
    grid-template-columns: 1fr;
  }
}
</style>
