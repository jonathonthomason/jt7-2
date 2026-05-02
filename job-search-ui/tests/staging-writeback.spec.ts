import { test, expect } from '@playwright/test'

function resetState(page: import('@playwright/test').Page) {
  return page.addInitScript(() => {
    window.localStorage.setItem('demo_auth', '1')
    if (!window.sessionStorage.getItem('jt7_mvp_state_reset_done')) {
      window.localStorage.removeItem('jt7_mvp_state_v1_5')
      window.sessionStorage.setItem('jt7_mvp_state_reset_done', '1')
    }
  })
}

test('staging promote hits runtime writeback and updates canonical job state', async ({ page }) => {
  await resetState(page)

  await page.goto('/trust/staging')

  await expect(page.getByRole('heading', { name: 'Staging Intake' })).toBeVisible({ timeout: 10000 })

  const card = page.locator('article').filter({ has: page.getByRole('button', { name: 'Promote' }) }).first()
  await expect(card).toBeVisible({ timeout: 10000 })
  const role = (await card.getByRole('heading').innerText()).trim()
  const companyLine = (await card.locator('p').first().innerText()).trim()
  const company = companyLine.split('·')[0].trim().replace(/^"|"$/g, '')

  await card.getByRole('button', { name: 'Detail' }).click()
  await expect(page.getByRole('button', { name: 'Promote' }).last()).toBeVisible({ timeout: 10000 })
  await page.getByRole('button', { name: 'Promote' }).last().click()

  await expect(page.getByText('Writebacks').locator('..').getByText('1')).toBeVisible({ timeout: 20000 })
  await expect(page.getByText(/Canonical (create|merge) applied via runtime bridge/)).toBeVisible({ timeout: 20000 })
  await page.getByRole('link', { name: 'Jobs' }).click()
  await expect(page.getByRole('heading', { name: 'Jobs' })).toBeVisible({ timeout: 10000 })
  await expect(page.getByRole('row', { name: new RegExp(`${role}.*${company}|${company}.*${role}`) }).first()).toBeVisible({ timeout: 20000 })

  await page.screenshot({ path: 'runtime/staging-writeback-validation.png', fullPage: true })
})

test('staging merge hits runtime writeback and keeps canonical job path', async ({ page }) => {
  await resetState(page)

  await page.goto('/trust/staging')
  await expect(page.getByRole('heading', { name: 'Staging Intake' })).toBeVisible({ timeout: 10000 })

  await expect(page.getByText('Duplicate candidates')).toBeVisible({ timeout: 10000 })
  const duplicateButton = page.locator('button').filter({ hasText: /Ellevation Education — Principal Product Designer/ }).first()
  await expect(duplicateButton).toBeVisible({ timeout: 10000 })

  await duplicateButton.click()
  await expect(page.getByRole('button', { name: 'Merge' }).last()).toBeVisible({ timeout: 10000 })
  await page.getByRole('button', { name: 'Merge' }).last().click()

  await expect(page.getByText('Writebacks').locator('..').getByText('1')).toBeVisible({ timeout: 20000 })
  await expect(page.getByText('Canonical merge applied via runtime bridge')).toBeVisible({ timeout: 20000 })
  await expect(page.getByText('Ellevation Education').last()).toBeVisible({ timeout: 10000 })

  await page.screenshot({ path: 'runtime/staging-merge-validation.png', fullPage: true })
})
