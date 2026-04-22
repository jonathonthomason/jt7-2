import { test, expect } from '@playwright/test'

test('jobs page loads', async ({ page }) => {
  await page.goto('/jobs')
  await expect(page.getByRole('heading', { name: 'Jobs' })).toBeVisible()
})
