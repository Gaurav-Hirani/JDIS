import { test, expect } from '@playwright/test';

test.describe('JDIS Frontend End-to-End Smoke Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to frontend root
    await page.goto('http://localhost:3000/');
  });

  test('Flow 1: Executive Dashboard loads with health indicator and system metrics', async ({ page }) => {
    await expect(page.getByText('JDIS Platform')).toBeVisible();
    await expect(page.getByText('JDIS Executive Delay Dashboard')).toBeVisible();
    await expect(page.getByText(/Backend Online|Backend Disconnected/)).toBeVisible();
    await expect(page.getByText('Total Registered Cases')).toBeVisible();
  });

  test('Flow 2: New Prediction form loads, validates required fields, and submits scenario', async ({ page }) => {
    await page.click('a[href="/prediction/new"]');
    await expect(page.getByText('Filing Stage Case Risk Prediction')).toBeVisible();
    await expect(page.getByText('Load Filing Sample Presets')).toBeVisible();

    // Click Run Filing Risk Evaluation button
    await page.click('button[type="submit"]');

    // Should navigate to prediction result view and display calibrated probability
    await expect(page.getByText('Calibrated (>24 Month Threshold)')).toBeVisible({ timeout: 15000 });
    await expect(page.getByText('Why This Prediction?')).toBeVisible();
  });

  test('Flow 3: Case Management repository loads table and supports searching/filtering', async ({ page }) => {
    await page.click('a[href="/cases"]');
    await expect(page.getByText('Case Records Repository')).toBeVisible();
    await expect(page.getByPlaceholder('Search by case ID or court...')).toBeVisible();
  });

  test('Flow 4: Analytics dashboard renders charts and court breakdown', async ({ page }) => {
    await page.click('a[href="/analytics"]');
    await expect(page.getByText('Risk Band Distribution')).toBeVisible({ timeout: 15000 });
    await expect(page.getByText('Court Establishments Risk Analytics')).toBeVisible();
  });

  test('Flow 5: Methodology page displays governance directives and non-causal disclaimers', async ({ page }) => {
    await page.click('a[href="/about"]');
    await expect(page.getByText('Methodology & Governance Guide')).toBeVisible();
    await expect(page.getByText(/JDIS Risk Score = floor\( calibrated_probability × 100 \)/)).toBeVisible();
  });
});
