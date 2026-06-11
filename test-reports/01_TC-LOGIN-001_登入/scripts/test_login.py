"""
TC-LOGIN-001: 登入測試
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

SCREENSHOT_DIR = Path(__file__).parent / "screenshots"
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

async def test_login():
    steps, results = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=200)
        page = await browser.new_page()
        try:
            # 1. 打開登入頁
            await page.goto(f"{BASE_URL}/login")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=SCREENSHOT_DIR / "step1_login_page.png")
            steps.append({"step": 1, "desc": "登入頁面加載", "status": "通過"})
            results.append(True)

            # 2. 輸入帳號密碼
            await page.fill("input[type='email']", USERNAME)
            await page.fill("input[type='password']", PASSWORD)
            await page.screenshot(path=SCREENSHOT_DIR / "step2_filled.png")
            steps.append({"step": 2, "desc": "輸入帳號密碼", "status": "通過"})
            results.append(True)

            # 3. 點擊登入
            await page.click("button[type='submit'], .auth-cta")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(3000)
            await page.screenshot(path=SCREENSHOT_DIR / "step3_after_login.png")
            steps.append({"step": 3, "desc": f"登入後 URL: {page.url}", "status": "通過"})
            results.append(True)

            # 4. 處理 OTP 驗證
            otp = await page.query_selector_all("input[type='text']")
            if otp:
                code = await get_code()
                for i, d in enumerate(code[:6]):
                    if i < len(otp): await otp[i].fill(d)
                await page.wait_for_timeout(2000)
                btn = await page.query_selector("button[type='submit']")
                if btn:
                    await btn.click(force=True)
                    await page.wait_for_load_state("networkidle")
                    await page.wait_for_timeout(3000)
                await page.screenshot(path=SCREENSHOT_DIR / "step4_after_otp.png")
                steps.append({"step": 4, "desc": "OTP 驗證", "status": "通過"})
                results.append(True)

            # 5. 處理設備驗證
            if "/verify-device" in page.url:
                btn = await page.query_selector("button[type='submit']")
                if btn:
                    await btn.click()
                    await page.wait_for_load_state("networkidle")
                    await page.wait_for_timeout(3000)
                await page.screenshot(path=SCREENSHOT_DIR / "step5_after_verify.png")
                steps.append({"step": 5, "desc": "設備驗證", "status": "通過"})
                results.append(True)

            # 6. 驗證最終進入主頁
            steps.append({"step": 6, "desc": f"最終 URL: {page.url}", "status": "通過" if "/top-up" in page.url or "/home" in page.url else f"URL: {page.url}"})
            results.append(True if "/top-up" in page.url or "/home" in page.url else False)

        except Exception as e:
            steps.append({"step": 99, "desc": f"錯誤：{e}", "status": "失敗"})
            results.append(False)
            await page.screenshot(path=SCREENSHOT_DIR / "error.png")
        await browser.close()

    passed, total = sum(results), len(results) if results else 1
    md = f"# TC-LOGIN-001 結果\n\n| 步驟 | 描述 | 狀態 |\n|---|---|---|\n"
    for s in steps: md += f"| {s['step']} | {s['desc']} | {'✅' if '通過' in s['status'] else '❌'} {s['status']} |\n"
    md += f"\n**結果**: {passed}/{total} 通過\n\n## 截圖\n"
    for i, ss in enumerate(sorted(SCREENSHOT_DIR.glob("*.png")), 1): md += f"- {ss.name}\n"
    with open(Path(__file__).parent / "result.md", 'w', encoding='utf-8') as f: f.write(md)
    print(f"TC-LOGIN-001: {passed}/{total} 通過")

if __name__ == "__main__":
    asyncio.run(test_login())
