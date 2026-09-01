import i18n from '../i18n'

/**
 * 按当前语言重算浏览器标题（document.title）。
 * @param {object|undefined} route vue-router 的 route 对象（含 meta.titleKey），未传时只显示站点名
 */
export function applyDocumentTitle(route) {
  const t = i18n.global.t
  const pageKey = route?.meta?.titleKey
  const pageTitle = pageKey ? t(`route.${pageKey}`) : ''
  document.title = pageTitle
    ? `${t('common.siteTitle')} - ${pageTitle}`
    : t('common.siteTitle')
}