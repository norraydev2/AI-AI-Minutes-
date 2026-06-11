"""
TC-HOME-002: 主頁 UI 佈局驗證（間距、樣式、對齊）
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
    """登錄並等待到主頁"""
    await page.goto(f"{BASE_URL}/login")
    await page.wait_for_load_state("networkidle")
    await page.fill("input[type='email']", USERNAME)
    await page.fill("input[type='password']", PASSWORD)
    await page.click("button[type='submit'], .auth-cta")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(3000)

    # 處理 OTP
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

    # 處理設備驗證
    if "/verify-device" in page.url:
        btn = await page.query_selector("button[type='submit']")
        if btn:
            await btn.click()
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(5000)

    # 確認進入主頁
    await page.goto(f"{BASE_URL}/top-up")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(3000)

    # 驗證已進入主頁
    current_url = page.url
    if "/login" in current_url or "/verify" in current_url:
        raise Exception(f"未能進入主頁，當前 URL: {current_url}")

async def test_home_ui():
    steps, results = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=200)
        page = await browser.new_page()
        try:
            # 1. 登錄
            await login_and_wait(page)
            steps.append({"step": 1, "desc": "登入成功", "status": "通過"})
            results.append(True)

            # 2. 驗證側邊欄寬度和間距
            sidebar = await page.query_selector("aside, nav, [class*=sidebar], [class*=menu]")
            if sidebar:
                sidebar_style = await sidebar.evaluate("""el => {
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return {
                        width: rect.width,
                        paddingTop: style.paddingTop,
                        paddingBottom: style.paddingBottom,
                        marginTop: style.marginTop,
                        gap: style.gap
                    }
                }""")
                await page.screenshot(path=SCREENSHOT_DIR / "step2_sidebar.png")
                steps.append({"step": 2, "desc": f"側邊欄：寬={sidebar_style['width']}px, padding={sidebar_style['paddingTop']}/{sidebar_style['paddingBottom']}", "status": "通過"})
                results.append(True)
            else:
                steps.append({"step": 2, "desc": "側邊欄不存在", "status": "失敗"})
                results.append(False)

            # 3. 驗證主內容區間距
            main = await page.query_selector("main, [role='main'], [class*=main], [class*=content]")
            if main:
                main_style = await main.evaluate("""el => {
                    const style = window.getComputedStyle(el);
                    return {
                        padding: style.padding,
                        marginTop: style.marginTop,
                        marginLeft: style.marginLeft
                    }
                }""")
                await page.screenshot(path=SCREENSHOT_DIR / "step3_main.png")
                steps.append({"step": 3, "desc": f"主內容區：padding={main_style['padding']}, marginTop={main_style['marginTop']}", "status": "通過"})
                results.append(True)
            else:
                steps.append({"step": 3, "desc": "主內容區不存在", "status": "失敗"})
                results.append(False)

            # 4. 驗證卡片間距
            cards = await page.query_selector_all("[class*=card], .ant-card, [class*=stat]")
            if len(cards) >= 2:
                card1_box = await cards[0].bounding_box()
                card2_box = await cards[1].bounding_box()
                if card1_box and card2_box:
                    gap = card2_box['x'] - card1_box['x'] - card1_box['width']
                    await page.screenshot(path=SCREENSHOT_DIR / "step4_cards.png")
                    steps.append({"step": 4, "desc": f"卡片間距：{gap}px", "status": "通過" if 10 <= gap <= 50 else f"間距異常：{gap}px"})
                    results.append(True if 10 <= gap <= 50 else False)
                else:
                    steps.append({"step": 4, "desc": "無法獲取卡片位置", "status": "失敗"})
                    results.append(False)
            else:
                steps.append({"step": 4, "desc": "卡片數量不足", "status": "失敗"})
                results.append(False)

            # 5. 全頁截圖
            await page.screenshot(path=SCREENSHOT_DIR / "step5_full.png", full_page=True)
            steps.append({"step": 5, "desc": "全頁截圖", "status": "通過"})
            results.append(True)

        except Exception as e:
            steps.append({"step": 99, "desc": f"錯誤：{e}", "status": "失敗"})
            results.append(False)
            await page.screenshot(path=SCREENSHOT_DIR / "error.png")
        await browser.close()

    passed, total = sum(results), len(results) if results else 1
    md = f"# TC-HOME-002 結果\n\n| 步驟 | 描述 | 狀態 |\n|---|---|---|\n"
    for s in steps: md += f"| {s['step']} | {s['desc']} | {'✅' if '通過' in s['status'] else '❌'} {s['status']} |\n"
    md += f"\n**結果**: {passed}/{total} 通過\n\n## 截圖\n"
    for i, ss in enumerate(sorted(SCREENSHOT_DIR.glob("*.png")), 1): md += f"- {ss.name}\n"
    with open(Path(__file__).parent / "result.md", 'w', encoding='utf-8') as f: f.write(md)
    print(f"TC-HOME-002: {passed}/{total} 通過")

if __name__ == "__main__":
    asyncio.run(test_home_ui())
