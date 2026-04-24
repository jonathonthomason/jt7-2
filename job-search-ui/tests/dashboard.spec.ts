import { test, expect } from '@playwright/test'

test('today dashboard renders JT7 operator surface', async ({ page }) => {
  const errors: string[] = []
  page.on('pageerror', (error) => errors.push(String(error)))

  await page.goto('/auth/sign-in')
  await page.getByRole('button', { name: 'Sign in' }).click()
  await page.waitForURL('**/app/dashboard')

  await expect(page.getByText('Today’s Plan')).toBeVisible()
  await expect(page.getByText('Start here')).toBeVisible()
  await expect(page.getByRole('heading', { name: /Thomson Reuters/i }).first()).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Recent signals' })).toBeVisible()
  await expect(page.getByText('Thomson Reuters').first()).toBeVisible()

  await page.screenshot({ path: 'runtime/dashboard-validation.png', fullPage: true })

  const cards = await page.locator('article').count()
  const url = page.url()
  const bodyText = await page.locator('body').innerText()

  console.log('VALIDATION_URL', url)
  console.log('EXECUTION_CARDS', cards)
  console.log('HAS_JT7_DATA', bodyText.includes('Thomson Reuters'))
  console.log('PAGE_ERRORS', JSON.stringify(errors))

  expect(cards).toBeGreaterThan(0)
  expect(errors).toEqual([])
})
