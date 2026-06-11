"""
TC-LOGIN-002: 登入頁 UI 驗證（間距、樣式、佈局）
"""

import asyncio
import re
import yaml
from playwright.async_api import async_playwright
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent.parent / "config.yaml"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

USERNAME = config.get('test_account', {}).get('username', 'youyouxiang2@2925.com')
PASSWORD = config.get('test_account', {}).get('password', '123')
BASE_URL = 'http://192.168.88.30/ai-minutes-user'

SCREENSHOT_DIR = Path(__file__).parent / "screenshot"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

async def test_login_ui():
    steps, results = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=200)
        page = await browser.new_page()
        try:
            # 1. 打開登入頁
            await page.goto(f"{BASE_URL}/login")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(3000)
            await page.screenshot(path=SCREENSHOT_DIR / "step1_login_page.png")
            steps.append({"step": 1, "desc": "登入頁面加載", "status": "通過"})
            results.append(True)

            # 2. 驗證頁面標題
            title = await page.query_selector("h1, .title, [class*=title]")
            if title:
                title_text = await title.inner_text()
                steps.append({"step": 2, "desc": f"頁面標題：{title_text}", "status": "通過"})
                results.append(True)
            else:
                steps.append({"step": 2, "desc": "頁面標題不存在", "status": "失敗"})
                results.append(False)

            # 3. 驗證輸入框間距
            email_input = await page.query_selector("input[type='email']")
            password_input = await page.query_selector("input[type='password']")
            if email_input and password_input:
                email_box = await email_input.bounding_box()
                password_box = await password_input.bounding_box()
                if email_box and password_box:
                    spacing = password_box['y'] - email_box['y'] - email_box['height']
                    steps.append({"step": 3, "desc": f"輸入框間距：{spacing}px", "status": "通過" if 10 <= spacing <= 50 else f"間距異常：{spacing}px"})
                    results.append(True if 10 <= spacing <= 50 else False)
                else:
                    steps.append({"step": 3, "desc": "無法獲取輸入框位置", "status": "失敗"})
                    results.append(False)
            else:
                steps.append({"step": 3, "desc": "輸入框不存在", "status": "失敗"})
                results.append(False)

            # 4. 驗證按鈕樣式
            login_btn = await page.query_selector("button[type='submit'], .auth-cta")
            if login_btn:
                btn_style = await login_btn.evaluate("""el => {
                    const style = window.getComputedStyle(el);
                    return {
                        marginTop: style.marginTop,
                        marginBottom: style.marginBottom,
                        paddingTop: style.paddingTop,
                        paddingBottom: style.paddingBottom,
                        backgroundColor: style.backgroundColor,
                        borderRadius: style.borderRadius
                    }
                }""")
                await page.screenshot(path=SCREENSHOT_DIR / "step2_button_style.png")
                steps.append({"step": 4, "desc": f"按鈕樣式：margin={btn_style['marginTop']}/{btn_style['marginBottom']}, padding={btn_style['paddingTop']}/{btn_style['paddingBottom']}", "status": "通過"})
                results.append(True)
            else:
                steps.append({"step": 4, "desc": "登入按鈕不存在", "status": "失敗"})
                results.append(False)

            # 5. 驗證卡片容器間距
            card = await page.query_selector(".auth-card, [class*=card], form")
            if card:
                card_style = await card.evaluate("""el => {
                    const style = window.getComputedStyle(el);
                    return {
                        padding: style.padding,
                        margin: style.margin
                    }
                }""")
                steps.append({"step": 5, "desc": f"卡片容器：padding={card_style['padding']}, margin={card_style['margin']}", "status": "通過"})
                results.append(True)
            else:
                steps.append({"step": 5, "desc": "卡片容器不存在", "status": "失敗"})
                results.append(False)

            # 6. 全頁截圖
            await page.screenshot(path=SCREENSHOT_DIR / "step3_full_page.png", full_page=True)
            steps.append({"step": 6, "desc": "全頁截圖", "status": "通過"})
            results.append(True)

        except Exception as e:
            steps.append({"step": 99, "desc": f"錯誤：{e}", "status": "失敗"})
            results.append(False)
            await page.screenshot(path=SCREENSHOT_DIR / "error.png")
        await browser.close()

    passed, total = sum(results), len(results) if results else 1
    md = f"# TC-LOGIN-002 結果\n\n| 步驟 | 描述 | 狀態 |\n|---|---|---|\n"
    for s in steps: md += f"| {s['step']} | {s['desc']} | {'✅' if '通過' in s['status'] else '❌'} {s['status']} |\n"
    md += f"\n**結果**: {passed}/{total} 通過\n\n## 截圖\n"
    for i, ss in enumerate(sorted(SCREENSHOT_DIR.glob("*.png")), 1): md += f"- {ss.name}\n"
    with open(Path(__file__).parent / "result.md", 'w', encoding='utf-8') as f: f.write(md)
    print(f"TC-LOGIN-002: {passed}/{total} 通過")

if __name__ == "__main__":
    asyncio.run(test_login_ui())
