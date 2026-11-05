import { expect, test } from '@playwright/test';

test('desktop mission and shadow controls render without overflow', async ({ page }, testInfo) => {
  const consoleErrors: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });

  await page.goto('/');
  await expect(page.getByRole('heading', { name: /Break the method/i })).toBeVisible();
  await expect(page.locator('.k4-strip-compact .k4-cell')).toHaveCount(97);
  await expect(page.getByText('EASTNORTHEAST', { exact: true })).toBeVisible();
  await expect(page.getByText('BERLINCLOCK', { exact: true })).toBeVisible();

  const width = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(width).toBeLessThanOrEqual(1441);
  expect(consoleErrors).toEqual([]);
  await page.screenshot({ path: testInfo.outputPath('mission-desktop.png'), fullPage: true });

  await page.getByRole('button', { name: /Shadow Runs/ }).click();
  await expect(page.getByRole('heading', { name: 'Shadow runs' })).toBeVisible();
  await expect(page.getByText('ALL SYSTEMS CONSISTENT')).toBeVisible();
  await expect(page.locator('.run-card')).toHaveCount(5);
  await expect(page.locator('.run-result')).toHaveText(['PASS', 'PASS', 'PASS', 'PASS', 'PASS']);
});

test('cipher lab executes the K1 control through the interface', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: /Cipher Lab/ }).click();
  await page.getByRole('button', { name: 'K1', exact: true }).click();
  const output = page.locator('#lab-output');
  await expect(output).toHaveValue(/BETWEENSUBTLESHADING/);
  await expect(output).toHaveValue(/IQLUSION/);
  await expect(page.getByText('63', { exact: true }).first()).toBeVisible();
});

test('mobile navigation, K4 map, and method registry remain usable', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  const menu = page.getByRole('button', { name: 'Open navigation' });
  await expect(page.locator('#primary-sidebar')).toHaveJSProperty('inert', true);
  await menu.click();
  await expect(page.getByRole('banner').getByRole('button', { name: 'Close navigation' })).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('Escape');
  await expect(menu).toBeFocused();
  await menu.click();
  await page.getByRole('button', { name: /Crib Bench/ }).click();
  await expect(page.getByRole('heading', { name: 'Crib bench' })).toBeVisible();
  await expect(page.locator('.crib-map-panel .k4-cell')).toHaveCount(97);

  let width = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(width).toBeLessThanOrEqual(391);

  await page.getByRole('button', { name: 'Open navigation' }).click();
  await page.getByRole('button', { name: /Methods/ }).click();
  await expect(page.getByRole('heading', { name: 'Technique registry' })).toBeVisible();
  await expect(page.getByText(/methods shown/)).toBeVisible();
  width = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(width).toBeLessThanOrEqual(391);
  await page.screenshot({ path: testInfo.outputPath('methods-mobile.png'), fullPage: true });
});

test('method checkmarks and notebook runs persist across reloads', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: /Methods/ }).click();
  await page.getByLabel('Search methods').fill('Gromark');
  await expect(page.locator('.technique-row')).toHaveCount(1);
  await page.getByRole('checkbox', { name: 'Check Gromark' }).click();
  await expect(page.locator('.technique-row .status-badge')).toHaveText('Tested');

  await page.reload();
  await page.getByRole('button', { name: /Methods/ }).click();
  await page.getByLabel('Search methods').fill('Gromark');
  await expect(page.locator('.technique-row .status-badge')).toHaveText('Tested');

  await page.getByRole('button', { name: /Cipher Lab/ }).click();
  await page.getByRole('button', { name: 'K1', exact: true }).click();
  await page.getByRole('button', { name: 'Log experiment' }).click();
  await page.getByRole('button', { name: /Notebook/ }).click();
  await expect(page.getByText('K1 / Kryptos keyed Vigenere')).toBeVisible();

  await page.reload();
  await page.getByRole('button', { name: /Notebook/ }).click();
  await expect(page.getByText('K1 / Kryptos keyed Vigenere')).toBeVisible();
});

test('every desktop workspace opens without global horizontal overflow', async ({ page }) => {
  await page.goto('/');
  const workspaces = [
    ['Cipher Lab', 'Cipher lab'],
    ['Crib Bench', 'Crib bench'],
    ['Methods', 'Technique registry'],
    ['Shadow Runs', 'Shadow runs'],
    ['Research', 'Research record'],
    ['Notebook', 'Experiment notebook'],
  ] as const;

  for (const [navigation, heading] of workspaces) {
    await page.getByRole('button', { name: new RegExp(navigation) }).click();
    await expect(page.getByRole('heading', { name: heading })).toBeVisible();
    if (navigation === 'Research') {
      await expect(page.getByText(/Power resides with a secret, not without it/).first()).toBeVisible();
      await expect(page.getByText(/semi ephemeral, undetectable and carefully hidden/).first()).toBeVisible();
      await expect(page.getByText(/None fixes a new K4 plaintext position/)).toBeVisible();
    }
    const width = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(width, `${navigation} overflowed`).toBeLessThanOrEqual(1441);
  }
});

test('edited lab input is logged as custom with matching artifacts', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: /Cipher Lab/ }).click();
  await page.locator('#lab-input').fill('ATTACKATDAWN');
  await page.getByRole('button', { name: 'Log experiment' }).click();
  await page.getByRole('button', { name: /Notebook/ }).click();
  await expect(page.locator('.experiment-rail')).toHaveText('custom');
  await page.getByText('Inspect complete artifacts').click();
  await expect(page.locator('.artifact-grid pre').first()).toHaveText('ATTACKATDAWN');
});

test('invalid persisted data is quarantined and recoverable', async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.setItem('k4-fieldbook-experiments-v1', '{"unexpected":true}');
  });
  await page.goto('/');
  await expect(page.getByText('Local save error')).toBeVisible();
  page.on('dialog', (dialog) => dialog.accept());
  await page.getByRole('button', { name: 'Inspect and reset affected data' }).click();
  await expect(page.getByText('Local storage only')).toBeVisible();
  expect(
    await page.evaluate(() => window.localStorage.getItem('k4-fieldbook-experiments-v1')),
  ).toBe('[]');
});

test('notebook import requires the declared schema and complete records', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: /Notebook/ }).click();
  await page.locator('input[type="file"]').setInputFiles({
    name: 'invalid.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ schema: 'unknown', experiments: [] })),
  });
  await expect(page.getByText(/Import rejected: expected schema/)).toBeVisible();
});

test('technique changes synchronize across open tabs', async ({ context, page }) => {
  const secondPage = await context.newPage();
  await Promise.all([page.goto('/'), secondPage.goto('/')]);
  for (const current of [page, secondPage]) {
    await current.getByRole('button', { name: /Methods/ }).click();
    await current.getByLabel('Search methods').fill('Gromark');
  }
  await page.bringToFront();
  await expect(page.getByRole('checkbox', { name: 'Check Gromark' })).toBeVisible();
  await page.getByRole('checkbox', { name: 'Check Gromark' }).click();
  await expect(secondPage.locator('.technique-row .status-badge')).toHaveText('Tested');
});
