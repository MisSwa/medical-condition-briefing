import { test, expect } from '@playwright/test'

test('submit button is disabled when input is empty', async ({ page }) => {
  await page.goto('/')

  const button = page.getByRole('button', { name: /generate brief/i })
  await expect(button).toBeDisabled()

  const input = page.getByLabel('Medical condition')
  await input.fill('   ')
  await expect(button).toBeDisabled()

  await input.fill('asthma')
  await expect(button).toBeEnabled()

  await input.clear()
  await expect(button).toBeDisabled()
})

test('generates and renders a brief for a real condition', async ({ page }) => {
  await page.goto('/')

  const input = page.getByLabel('Medical condition')
  await input.fill('asthma')

  await page.getByRole('button', { name: /generate brief/i }).click()

  // Button should become disabled and show loading state while request is in flight
  await expect(page.getByRole('button', { name: /generating/i })).toBeVisible()

  // Wait for brief to appear (backend + Claude may take up to 90s)
  const brief = page.locator('.brief')
  await expect(brief).toBeVisible({ timeout: 90000 })

  // Heading reflects the searched condition
  await expect(brief.locator('h2')).toContainText('asthma', { ignoreCase: true })

  // All four sections must be present
  await expect(brief.getByRole('heading', { name: /standard of care/i })).toBeVisible()
  await expect(brief.getByRole('heading', { name: /emerging treatments/i })).toBeVisible()
  await expect(brief.getByRole('heading', { name: /key organizations/i })).toBeVisible()
  await expect(brief.getByRole('heading', { name: /sources/i })).toBeVisible()

  // At least one source link must be present
  const sourcesList = brief.locator('.sources a')
  await expect(sourcesList.first()).toBeVisible()
})
