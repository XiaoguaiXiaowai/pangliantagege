<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
// ECharts 按需引入，只打包本页用到的图表与组件
import * as echarts from 'echarts/core'
import { BarChart, PieChart, GraphChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  BarChart,
  PieChart,
  GraphChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  CanvasRenderer
])

// ============================================================
// 作品在线地址（占位）—— 部署上线后只需改这一行
// ============================================================
const PROJECT_URL = 'https://your-demo.example.com'
const isUrlPlaceholder = /your-demo|example\.com|待定|todo/i.test(PROJECT_URL)

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

// ---------------- 技术栈 ----------------
const techStack = [
  { icon: '🐍', name: 'Python + FastAPI', why: '轻量结构化后端，可逐行讲解' },
  { icon: '🎛️', name: '自研状态机', why: '显式 TRANSITIONS 表，不套 LangGraph 黑盒' },
  { icon: '🤖', name: 'OpenAI Agents SDK', why: 'Triage → 子 Agent handoff + 原生 HITL 中断/恢复' },
  { icon: '🗄️', name: 'SQLite + 文件系统', why: '状态外部化，单机零成本' },
  { icon: '⚛️', name: 'Next.js 14', why: '贴近真实企业栈，与后端解耦' },
  { icon: '🐳', name: 'Docker Compose + Nginx', why: '阿里云单机 HTTPS 一键上线' }
]

// ---------------- 图表 ----------------
const rerankChartRef = ref(null)
const donutChartRef = ref(null)
const graphChartRef = ref(null)
let charts = []

const initCharts = () => {
  // ① RAG rerank 前后对比柱状图
  if (rerankChartRef.value) {
    const chart = echarts.init(rerankChartRef.value)
    chart.setOption({
      tooltip: {
        trigger: 'axis',
        valueFormatter: (v) => `${(v * 100).toFixed(1)}%`
      },
      legend: { data: ['rerank 关闭', 'rerank 开启'], top: 0, textStyle: { color: '#5a6b7c' } },
      grid: { left: 44, right: 16, top: 42, bottom: 28 },
      xAxis: {
        type: 'category',
        data: ['recall@1', 'MRR', 'nDCG@3'],
        axisTick: { show: false },
        axisLine: { lineStyle: { color: '#c8dbe6' } },
        axisLabel: { color: '#51697d' }
      },
      yAxis: {
        type: 'value',
        max: 1,
        axisLabel: { formatter: (v) => `${Math.round(v * 100)}%`, color: '#51697d' },
        splitLine: { lineStyle: { color: '#e8f1f6' } }
      },
      series: [
        {
          name: 'rerank 关闭',
          type: 'bar',
          data: [0.812, 0.896, 0.923],
          barWidth: 30,
          itemStyle: { color: '#A7EBF2', borderColor: '#54ACBF', borderWidth: 1, borderRadius: [4, 4, 0, 0] },
          label: { show: true, position: 'top', formatter: (p) => `${(p.value * 100).toFixed(1)}%`, color: '#7a8b9c', fontSize: 11 }
        },
        {
          name: 'rerank 开启',
          type: 'bar',
          data: [1.0, 1.0, 1.0],
          barWidth: 30,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: '#26658C' },
                { offset: 1, color: '#023859' }
              ]
            },
            borderRadius: [4, 4, 0, 0],
            shadowColor: 'rgba(2, 56, 89, 0.35)',
            shadowBlur: 10
          },
          label: { show: true, position: 'top', formatter: '100.0%', color: '#023859', fontSize: 11, fontWeight: 700 }
        }
      ]
    })
    charts.push(chart)
  }

  // ② 8 大能力环形图（居中，扇区外直接标注名称）
  if (donutChartRef.value) {
    const chart = echarts.init(donutChartRef.value)
    const donutColors = ['#A7EBF2', '#8FD8E6', '#77C3D6', '#5EAEC4', '#54ACBF', '#3E86A8', '#26658C', '#023859']
    chart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: (p) => `${p.name}：已落地 ✅`
      },
      color: donutColors,
      series: [
        {
          type: 'pie',
          radius: ['50%', '72%'],
          center: ['50%', '46%'],
          data: [
            { name: '① 流程定义', value: 1 },
            { name: '② 业务入口', value: 1 },
            { name: '③ 核心 LOOP', value: 1 },
            { name: '④ 业务出口', value: 1 },
            { name: '⑤ 工具层 MPC-Skill', value: 1 },
            { name: '⑥ Trace', value: 1 },
            { name: '⑦ 监控评估', value: 1 },
            { name: '⑧ 预算', value: 1 }
          ],
          label: {
            show: true,
            position: 'outside',
            fontSize: 10.5,
            color: '#44566a',
            formatter: '{b}'
          },
          labelLine: { length: 12, length2: 8, lineStyle: { color: '#9db8cc' } },
          avoidLabelOverlap: true,
          itemStyle: { borderColor: '#fff', borderWidth: 2 },
          emphasis: { scale: true, scaleSize: 6 }
        }
      ],
      title: {
        text: '8/8',
        subtext: '工程能力落地',
        left: 'center',
        top: '35%',
        textAlign: 'center',
        textStyle: { fontSize: 30, fontWeight: 800, color: '#011C40' },
        subtextStyle: { fontSize: 11, color: '#26658C' }
      }
    })
    charts.push(chart)
  }

  // ③ 工单状态机流转图（坐标按容器宽度自适应）
  const opt = buildGraphOption()
  if (graphChartRef.value) {
    graphChart = echarts.init(graphChartRef.value)
    graphChart.setOption(opt)
    charts.push(graphChart)
  }
}

let graphChart = null

const buildGraphOption = () => {
  const W = Math.max(graphChartRef.value.clientWidth, 960)
    const fx = (f) => W * f
    return {
      tooltip: {
        trigger: 'item',
        formatter: (p) => {
          if (p.dataType === 'edge') return p.data.label || ''
          return `${p.data.name}`
        }
      },
      animationDuration: 900,
      series: [
        {
          type: 'graph',
          layout: 'none',
          roam: false,
          symbol: 'roundRect',
          symbolSize: [104, 42],
          label: { show: true, position: 'inside', fontSize: 11.5, fontWeight: 600, color: '#fff' },
          edgeLabel: {
            show: true,
            fontSize: 10.5,
            lineHeight: 14,
            color: '#023859',
            backgroundColor: '#ffffff',
            borderColor: 'rgba(84, 172, 191, 0.55)',
            borderWidth: 1,
            borderRadius: 10,
            padding: [3, 7],
            shadowBlur: 8,
            shadowColor: 'rgba(1, 28, 64, 0.18)',
            shadowOffsetY: 2,
            formatter: (p) => p.data.label || ''
          },
          lineStyle: { color: '#9db8cc', width: 1.8, curveness: 0.06 },
          emphasis: {
            focus: 'adjacency',
            lineStyle: { width: 2.6, color: '#26658C' },
            label: { fontSize: 12.5 }
          },
          data: [
            { id: 'created', name: '已创建', x: fx(0.07), y: 60, itemStyle: { color: '#26658C' } },
            { id: 'triaged', name: '已分级', x: fx(0.24), y: 60, itemStyle: { color: '#26658C' } },
            { id: 'gathering', name: '装配中', x: fx(0.41), y: 60, itemStyle: { color: '#26658C' } },
            { id: 'agent_running', name: '执行中', x: fx(0.58), y: 60, itemStyle: { color: '#023859' } },
            { id: 'done', name: '已完成', x: fx(0.75), y: 60, itemStyle: { color: '#023859' } },
            { id: 'archived', name: '已归档', x: fx(0.92), y: 60, itemStyle: { color: '#54ACBF' } },
            { id: 'awaiting_approval', name: '待审批', x: fx(0.58), y: 215, itemStyle: { color: '#f59e0b' } },
            { id: 'running', name: '继续执行', x: fx(0.75), y: 215, itemStyle: { color: '#f59e0b' } },
            { id: 'failed', name: '已失败', x: fx(0.41), y: 215, itemStyle: { color: '#ef4444' } }
          ],
          links: [
            { source: 'created', target: 'triaged', label: '意图分类\n+ 风险分级' },
            { source: 'triaged', target: 'gathering', label: '装配上下文' },
            { source: 'gathering', target: 'agent_running', label: 'LOOP 执行' },
            { source: 'agent_running', target: 'awaiting_approval', label: '高风险工具\n→ HITL 中断', lineStyle: { color: '#f59e0b' } },
            { source: 'awaiting_approval', target: 'running', label: '审批通过\n→ 恢复执行' },
            { source: 'running', target: 'done', label: '执行完成' },
            { source: 'agent_running', target: 'done', label: '收敛\ndone:true' },
            { source: 'done', target: 'archived', label: '只读归档' },
            { source: 'agent_running', target: 'failed', label: '预算/超时\n停止', lineStyle: { color: '#ef4444', type: 'dashed' } }
          ]
        }
      ]
    }
  }

const handleResize = () => {
  charts.forEach((c) => c.resize())
  if (graphChart && graphChartRef.value) {
    graphChart.setOption(buildGraphOption())
  }
}

onMounted(async () => {
  await nextTick()
  initCharts()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  charts.forEach((c) => c.dispose())
  charts = []
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

      <div class="hero-chips">
        <span class="chip">🛡️ 可靠 Reliable</span>
        <span class="chip">🔐 可控 Controlled</span>
        <span class="chip">📋 可审计 Auditable</span>
      </div>

      <div class="hero-actions">
        <a class="btn-primary" :href="PROJECT_URL" target="_blank" rel="noopener noreferrer">
          🚀 查看在线 Demo
        </a>
        <a class="btn-ghost" href="#capabilities">8 大工程能力 ↓</a>
      </div>
      <p v-if="isUrlPlaceholder" class="hero-hint">🔗 在线 Demo 部署完成后，链接将在此开放</p>

      <div class="hero-stats">
        <div class="stat">
          <div class="num">8</div>
          <div class="label">大工程能力落地</div>
        </div>
        <div class="stat">
          <div class="num">3 重</div>
          <div class="label">预算护栏 · 步数/Token/时间</div>
        </div>
        <div class="stat">
          <div class="num">+18.8%</div>
          <div class="label">rerank 后 recall@1 提升</div>
        </div>
        <div class="stat">
          <div class="num">100%</div>
          <div class="label">离线 reader 兜底可演示</div>
        </div>
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

    <!-- ============ 数据图表 ============ -->
    <section class="section">
      <h2>数据与流程可视化</h2>
      <p class="section-sub">用数据说话，用流程兜底</p>
      <div class="chart-grid">
        <div class="chart-card">
          <h3>RAG 检索评测 · rerank 精排前后对比</h3>
          <p class="chart-desc">16 条真实标注查询 · 双路召回 + RRF 融合 + rerank 精排</p>
          <div ref="rerankChartRef" class="chart-box"></div>
        </div>
        <div class="chart-card">
          <h3>8 大工程能力 · 全部落地</h3>
          <p class="chart-desc">从流程定义到预算控制，每条都有可运行的代码支撑</p>
          <div ref="donutChartRef" class="chart-box"></div>
        </div>
      </div>
      <div class="chart-card chart-wide">
        <h3>工单状态机 · 确定性流程约束</h3>
        <p class="chart-desc">LLM 只负责判断，执行权交给状态机与审批 —— 禁止跳步，状态可追溯</p>
        <div class="graph-scroll">
          <div ref="graphChartRef" class="graph-canvas"></div>
        </div>
      </div>
    </section>

    <!-- ============ 8 大工程能力 ============ -->
    <section class="section" id="capabilities">
      <h2>8 大工程能力</h2>
      <p class="section-sub">每一条都有对应的可运行代码</p>
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

    <!-- ============ 技术栈 ============ -->
    <section class="section">
      <h2>技术栈</h2>
      <p class="section-sub">贴近真实企业栈，每一层都有生产对应物</p>
      <div class="tech-grid">
        <div v-for="t in techStack" :key="t.name" class="tech-card">
          <span class="tech-icon">{{ t.icon }}</span>
          <div>
            <h3>{{ t.name }}</h3>
            <p>{{ t.why }}</p>
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
  margin-bottom: 24px;
}

.hero-sub strong {
  color: #A7EBF2;
}

.hero-chips {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 30px;
}

.chip {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.28);
  backdrop-filter: blur(8px);
  border-radius: 999px;
  padding: 8px 18px;
  font-size: 0.88rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.chip:hover {
  background: rgba(167, 235, 242, 0.18);
  transform: translateY(-2px);
}

.hero-actions {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 10px;
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

.hero-hint {
  position: relative;
  z-index: 1;
  margin: 10px 0 0;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.55);
}

.hero-stats {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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

/* ---------- 图表 ---------- */
.chart-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  background: #fff;
  border: 1px solid var(--card-border);
  border-radius: 20px;
  padding: 24px;
  box-shadow: var(--card-shadow);
}

.chart-card h3 {
  font-size: 1.02rem;
  margin-bottom: 4px;
}

.chart-desc {
  font-size: 0.8rem;
  color: #7a8b9c;
  margin-bottom: 12px;
}

.chart-box {
  width: 100%;
  height: 300px;
}

.graph-scroll {
  overflow-x: auto;
  padding-bottom: 4px;
}

.graph-canvas {
  width: 100%;
  min-width: 960px;
  height: 340px;
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

/* ---------- 技术栈 ---------- */
.tech-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.tech-card {
  background: #fff;
  border: 1px solid var(--card-border);
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: var(--card-shadow);
  min-width: 0;
  transition: all 0.3s ease;
}

.tech-card:hover {
  transform: translateY(-3px);
  border-color: #54ACBF;
}

.tech-icon {
  font-size: 1.6rem;
  flex-shrink: 0;
}

.tech-card h3 {
  font-size: 0.92rem;
  margin-bottom: 2px;
}

.tech-card p {
  font-size: 0.75rem;
  color: #7a8b9c;
  margin: 0;
}

/* ---------- 响应式 ---------- */
@media (max-width: 900px) {
  .pillar-grid,
  .chart-grid {
    grid-template-columns: 1fr;
  }

  .cap-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .tech-grid {
    grid-template-columns: 1fr 1fr;
  }

  .hero {
    padding: 40px 24px 32px;
  }

  .hero-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .agent-workflow-view {
    gap: 40px;
  }

  .cap-grid,
  .tech-grid {
    grid-template-columns: 1fr;
  }
}
</style>
