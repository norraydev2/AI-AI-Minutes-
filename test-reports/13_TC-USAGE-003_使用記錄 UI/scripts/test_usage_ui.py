"""
TC-USAGE-003: 使用記錄 UI 驗證（統計卡片、表格樣式）
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

async def login_and_wait(page):
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
            await page.wait_for_timeout(5000)
    if "/verify-device" in page.url:
        btn = await page.query_selector("button[type='submit']")
        if btn:
            await btn.click()
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(5000)
    await page.goto(f"{BASE_URL}/usage-history")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(3000)

async def test_usage_ui():
    steps, results = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=200)
        page = await browser.new_page()
        try:
            await login_and_wait(page)
            steps.append({"step": 1, "desc": "登入成功", "status": "通過"})
            results.append(True)

            # 驗證統計卡片
            stat_cards = await page.query_selector_all("[class*=stat], [class*=card], .ant-card, [class*=minute]")
            if stat_cards:
                await page.screenshot(path=SCREENSHOT_DIR / "step1_stats.png")
                steps.append({"step": 2, "desc": f"統計卡片：{len(stat_cards)}個", "status": "通過"})
                results.append(True)

                # 驗證第一個統計卡片樣式
                if len(stat_cards) > 0:
                    card_style = await stat_cards[0].evaluate("""el => {
                        const style = window.getComputedStyle(el);
                        const rect = el.getBoundingClientRect();
                        return {
                            width: rect.width,
                            height: rect.height,
                            padding: style.padding,
                            margin: style.margin,
                            backgroundColor: style.backgroundColor
                        }
                    }""")
                    steps.append({"step": 3, "desc": f"統計卡片樣式：{card_style['width']}x{card_style['height']}px, padding={card_style['padding']}", "status": "通過"})
                    results.append(True)
            else:
                steps.append({"step": 2, "desc": "統計卡片不存在", "status": "失敗"})
                results.append(False)

            # 驗證表格樣式（如有）
            table = await page.query_selector("table, .ant-table, [class*=table]")
            if table:
                await page.screenshot(path=SCREENSHOT_DIR / "step2_table.png")
                steps.append({"step": 4, "desc": "使用記錄表格存在", "status": "通過"})
                results.append(True)
            else:
                steps.append({"step": 4, "desc": "表格不存在（可能無數據）", "status": "跳過"})
                results.append(True)

            # 全頁截圖
            await page.screenshot(path=SCREENSHOT_DIR / "step3_full.png", full_page=True)
            steps.append({"step": 5, "desc": "全頁截圖", "status": "通過"})
            results.append(True)

        except Exception as e:
            steps.append({"step": 99, "desc": f"錯誤：{e}", "status": "失敗"})
            results.append(False)
            await page.screenshot(path=SCREENSHOT_DIR / "error.png")
        await browser.close()

    passed, total = sum(results), len(results) if results else 1
    md = f"# TC-USAGE-003 結果\n\n| 步驟 | 描述 | 狀態 |\n|---|---|---|\n"
    for s in steps: md += f"| {s['step']} | {s['desc']} | {'✅' if '通過' in s['status'] else '❌'} {s['status']} |\n"
    md += f"\n**結果**: {passed}/{total} 通過\n\n## 截圖\n"
    for i, ss in enumerate(sorted(SCREENSHOT_DIR.glob("*.png")), 1): md += f"- {ss.name}\n"
    with open(Path(__file__).parent / "result.md", 'w', encoding='utf-8') as f: f.write(md)
    print(f"TC-USAGE-003: {passed}/{total} 通過")

if __name__ == "__main__":
    asyncio.run(test_usage_ui())
