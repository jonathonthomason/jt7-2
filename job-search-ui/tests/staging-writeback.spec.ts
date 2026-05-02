import { test, expect } from '@playwright/test'

test('staging promote hits runtime writeback and shows success', async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.setItem('demo_auth', '1')
    window.localStorage.removeItem('jt7_mvp_state_v1_5')
  })

  await page.goto('/trust/staging')

  await expect(page.getByRole('heading', { name: 'Staging Intake' })).toBeVisible({ timeout: 10000 })

  const card = page.locator('article').filter({ has: page.getByRole('button', { name: 'Promote' }) }).first()
  await expect(card).toBeVisible({ timeout: 10000 })
  const companyLine = (await card.locator('p').first().innerText()).trim()
  const company = companyLine.split('·')[0].trim().replace(/^"|"$/g, '')

  await card.getByRole('button', { name: 'Promote' }).click()

  await expect(page.getByText('Writebacks').locator('..').getByText('1')).toBeVisible({ timeout: 20000 })
  await page.getByRole('link', { name: 'Jobs' }).click()
  await expect(page.getByRole('heading', { name: /Jobs/i })).toBeVisible({ timeout: 10000 })
  await expect(page.getByText(company).first()).toBeVisible({ timeout: 10000 })

  await page.screenshot({ path: 'runtime/staging-writeback-validation.png', fullPage: true })
})
