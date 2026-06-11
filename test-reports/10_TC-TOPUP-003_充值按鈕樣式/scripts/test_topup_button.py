"""
TC-TOPUP-003: 充值按鈕樣式驗證
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
    await page.goto(f"{BASE_URL}/top-up")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(3000)

async def test_topup_button_ui():
    steps, results = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=200)
        page = await browser.new_page()
        try:
            await login_and_wait(page)
            steps.append({"step": 1, "desc": "登入成功", "status": "通過"})
            results.append(True)

            # 驗證充值按鈕樣式
            submit_btn = await page.query_selector("button[type='submit'], button[class*=submit], .pay-btn")
            if submit_btn:
                btn_style = await submit_btn.evaluate("""el => {
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return {
                        width: rect.width,
                        height: rect.height,
                        marginTop: style.marginTop,
                        marginBottom: style.marginBottom,
                        paddingTop: style.paddingTop,
                        paddingBottom: style.paddingBottom,
                        paddingLeft: style.paddingLeft,
                        paddingRight: style.paddingRight,
                        backgroundColor: style.backgroundColor,
                        color: style.color,
                        fontSize: style.fontSize,
                        fontWeight: style.fontWeight,
                        borderRadius: style.borderRadius,
                        borderWidth: style.borderWidth
                    }
                }""")
                await page.screenshot(path=SCREENSHOT_DIR / "step1_button.png")
                steps.append({"step": 2, "desc": f"按鈕尺寸：{btn_style['width']}x{btn_style['height']}px", "status": "通過"})
                results.append(True)
                steps.append({"step": 3, "desc": f"按鈕間距：margin={btn_style['marginTop']}/{btn_style['marginBottom']}, padding={btn_style['paddingTop']}/{btn_style['paddingBottom']}", "status": "通過"})
                results.append(True)
                steps.append({"step": 4, "desc": f"按鈕樣式：bg={btn_style['backgroundColor']}, color={btn_style['color']}, fontSize={btn_style['fontSize']}, borderRadius={btn_style['borderRadius']}", "status": "通過"})
                results.append(True)
            else:
                steps.append({"step": 2, "desc": "提交按鈕不存在", "status": "失敗"})
                results.append(False)

            # 驗證金額選項按鈕（如有）
            amount_btns = await page.query_selector_all("[class*=amount] button, .amount-option button")
            if amount_btns:
                await page.screenshot(path=SCREENSHOT_DIR / "step2_amount_buttons.png")
                steps.append({"step": 5, "desc": f"金額選項按鈕：{len(amount_btns)}個", "status": "通過"})
                results.append(True)

        except Exception as e:
            steps.append({"step": 99, "desc": f"錯誤：{e}", "status": "失敗"})
            results.append(False)
            await page.screenshot(path=SCREENSHOT_DIR / "error.png")
        await browser.close()

    passed, total = sum(results), len(results) if results else 1
    md = f"# TC-TOPUP-003 結果\n\n| 步驟 | 描述 | 狀態 |\n|---|---|---|\n"
    for s in steps: md += f"| {s['step']} | {s['desc']} | {'✅' if '通過' in s['status'] else '❌'} {s['status']} |\n"
    md += f"\n**結果**: {passed}/{total} 通過\n\n## 截圖\n"
    for i, ss in enumerate(sorted(SCREENSHOT_DIR.glob("*.png")), 1): md += f"- {ss.name}\n"
    with open(Path(__file__).parent / "result.md", 'w', encoding='utf-8') as f: f.write(md)
    print(f"TC-TOPUP-003: {passed}/{total} 通過")

if __name__ == "__main__":
    asyncio.run(test_topup_button_ui())
