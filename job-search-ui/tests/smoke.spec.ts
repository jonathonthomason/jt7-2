import { test, expect } from '@playwright/test'

test('review queue and staging intake load', async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.setItem('demo_auth', '1')
  })

  await page.goto('/review-queue')

  await expect(page.getByRole('heading', { name: 'Review Queue' })).toBeVisible({ timeout: 10000 })
  await expect(page.getByText(/pending reviews/i).first()).toBeVisible()
  await expect(page.getByText(/Thomson Reuters|LinkedIn Job Alerts|Ford/i).first()).toBeVisible()

  await page.getByRole('link', { name: 'Staging Intake' }).click()
  await expect(page.getByRole('heading', { name: 'Staging Intake' })).toBeVisible({ timeout: 10000 })
  await expect(page.getByText(/nothing in this view is canonical tracker truth/i)).toBeVisible()
})
