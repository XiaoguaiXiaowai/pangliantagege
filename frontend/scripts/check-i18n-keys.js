#!/usr/bin/env node
/**
 * i18n 语言文件 key 一致性校验。
 * 用法：node scripts/check-i18n-keys.js   （或 npm run i18n:check）
 *
 * 校验三个语言文件（zh-CN / en / ja）的 key 结构完全一致，
 * 防止新增文案时漏译或多译。退出码非 0 表示校验失败。
 */
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const LOCALES_DIR = join(__dirname, '..', 'src', 'i18n', 'locales')
const FILES = ['zh-CN.json', 'en.json', 'ja.json']

function collectKeys(obj, prefix = '') {
  const keys = []
  for (const [key, value] of Object.entries(obj)) {
    const path = prefix ? `${prefix}.${key}` : key
    if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
      keys.push(...collectKeys(value, path))
    } else {
      keys.push(path)
    }
  }
  return keys
}

function load(name) {
  return JSON.parse(readFileSync(join(LOCALES_DIR, name), 'utf-8'))
}

const messages = {}
for (const file of FILES) {
  messages[file] = load(file)
}

// 以 zh-CN.json 为 key 基准
const baseKeys = new Set(collectKeys(messages[FILES[0]]))
let failed = false

for (const file of FILES.slice(1)) {
  const otherKeys = collectKeys(messages[file])
  const onlyInOther = otherKeys.filter((k) => !baseKeys.has(k))
  const onlyInBase = [...baseKeys].filter((k) => !otherKeys.includes(k))

  if (onlyInBase.length > 0) {
    failed = true
    console.error(`[${file}] 缺少以下 key（请补译）：\n  ${onlyInBase.join('\n  ')}`)
  }
  if (onlyInOther.length > 0) {
    failed = true
    console.error(`[${file}] 存在未在基准文件中的多余 key：\n  ${onlyInOther.join('\n  ')}`)
  }
}

if (failed) {
  console.error('\ni18n key 校验失败 ✗')
  process.exit(1)
}

const count = baseKeys.size
console.log(`i18n key 校验通过 ✓（${FILES.length} 个语言文件，${count} 个 key 完全一致）`)