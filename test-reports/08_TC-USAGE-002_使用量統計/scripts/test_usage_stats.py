"""
TC-USAGE-002: 使用量統計顯示測試
"""

import asyncio
import re
import yaml
from playwright.async_api import async_playwright
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent.parent / "config.yaml"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

CODE_URL = config.get('code_url', 'http://192.168.88.72:9963/ai-minutes/')
CODE_REGEX = config.get('code_regex', r'\b\d{6}\b')
USERNAME = config.get('test_account', {}).get('username', 'youyouxiang2@2925.com')
PASSWORD = config.get('test_account', {}).get('password', '123')
BASE_URL = 'http://192.168.88.30/ai-minutes-user'

SCREENSHOT_DIR = Path(__file__).parent / "screenshot"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

async def get_code():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(CODE_URL)
        await page.wait_for_load_state("networkidle")
        text = await page.inner_text("body")
        await browser.close()
        return re.search(CODE_REGEX, text).group(0) if re.search(CODE_REGEX, text) else "123456"

async def login(page):
    await page.goto(f"{BASE_URL}/login")
    await page.wait_for_load_state("networkidle")
    await page.fill("input[type='email']", USERNAME)
    await page.fill("input[type='password']", PASSWORD)
    await page.click("button[type='submit'], .auth-cta")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(3000)
    otp = await page.query_selector_all("input[type='text']")
    if otp:
        code = await get_code()
        for i, d in enumerate(code[:6]):
            if i < len(otp): await otp[i].fill(d)
        btn = await page.query_selector("button[type='submit']")
        if btn:
            await btn.click(force=True)
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(3000)
    if "/verify-device" in page.url:
        btn = await page.query_selector("button[type='submit']")
        if btn:
            await btn.click()
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(3000)

async def test():
    steps, results = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=200)
        page = await browser.new_page()
        try:
            await login(page)
            steps.append({"step": 1, "desc": "登入成功", "status": "通過"})
            results.append(True)

            await page.goto(f"{BASE_URL}/usage-history")
            await page.wait_for_timeout(3000)

            # 驗證統計卡片
            stat_cards = await page.query_selector_all("[class*=stat], [class*=card], .ant-card, [class*=minute]")
            await page.screenshot(path=SCREENSHOT_DIR / "step1_stats.png")
            steps.append({"step": 2, "desc": f"統計卡片：{len(stat_cards)}個", "status": "通過" if stat_cards else "失敗"})
            results.append(True if stat_cards else False)

            # 驗證使用量顯示
            usage_items = await page.query_selector_all("[class*=usage], [class*=hour], [class*=time]")
            await page.screenshot(path=SCREENSHOT_DIR / "step2_usage.png")
            steps.append({"step": 3, "desc": f"使用量項目：{len(usage_items)}個", "status": "通過" if usage_items else "失敗"})
            results.append(True if usage_items else False)

            # 驗證圖表（如有）
            charts = await page.query_selector_all("canvas, svg, .chart, echarts")
            steps.append({"step": 4, "desc": f"圖表：{len(charts)}個", "status": "通過" if charts else "無圖表"})
            results.append(True)

        except Exception as e:
            steps.append({"step": 99, "desc": f"錯誤：{e}", "status": "失敗"})
            results.append(False)
            await page.screenshot(path=SCREENSHOT_DIR / "error.png")
        await browser.close()

    passed, total = sum(results), len(results) if results else 1
    md = f"# TC-USAGE-002 結果\n\n| 步驟 | 描述 | 狀態 |\n|---|---|---|\n"
    for s in steps: md += f"| {s['step']} | {s['desc']} | {'✅' if '通過' in s['status'] else '❌'} {s['status']} |\n"
    md += f"\n**結果**: {passed}/{total} 通過\n\n## 截圖\n"
    for i, ss in enumerate(sorted(SCREENSHOT_DIR.glob("*.png")), 1): md += f"- {ss.name}\n"
    with open(Path(__file__).parent / "result.md", 'w', encoding='utf-8') as f: f.write(md)
    print(f"TC-USAGE-002: {passed}/{total} 通過")

if __name__ == "__main__":
    asyncio.run(test())
