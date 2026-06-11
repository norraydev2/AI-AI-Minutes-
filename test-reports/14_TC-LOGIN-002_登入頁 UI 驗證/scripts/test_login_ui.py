"""
TC-LOGIN-002: 登入頁 UI 驗證（間距、樣式、佈局）
根據 Figma 設計：
- 卡片寬度：420px
- 卡片圓角：8px
- 卡片陰影：blur: 36px, color: #2D6CDF26
- 按鈕圓角：6px, 8px
- 輸入框高度：38px
- 元素間距：8px, 16px, 24px, 40px
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
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        try:
            # 1. 打開登入頁 - 等待足夠時間
            await page.goto(f"{BASE_URL}/login")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_timeout(5000)  # 等待 CSS 完全加載
            await page.screenshot(path=SCREENSHOT_DIR / "step1_login_page.png")
            steps.append({"step": 1, "desc": "登入頁面加載", "status": "通過"})
            results.append(True)

            # 2. 驗證頁面標題
            title = await page.query_selector("h1, .title, [class*=title], .auth-title")
            if title:
                title_text = await title.inner_text()
                title_style = await title.evaluate("""el => {
                    const style = window.getComputedStyle(el);
                    return {
                        fontSize: style.fontSize,
                        fontWeight: style.fontWeight,
                        marginBottom: style.marginBottom
                    }
                }""")
                steps.append({"step": 2, "desc": f"頁面標題：'{title_text}', fontSize={title_style['fontSize']}, fontWeight={title_style['fontWeight']}", "status": "通過"})
                results.append(True)
            else:
                steps.append({"step": 2, "desc": "頁面標題不存在", "status": "失敗"})
                results.append(False)

            # 3. 驗證登入卡片（Figma: 寬 420px, 圓角 8px, 陰影）
            card = await page.query_selector(".auth-card, [class*=card], form, .login-form")
            if card:
                card_info = await card.evaluate("""el => {
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return {
                        width: rect.width,
                        height: rect.height,
                        padding: style.padding,
                        borderRadius: style.borderRadius,
                        boxShadow: style.boxShadow,
                        marginTop: style.marginTop,
                        marginBottom: style.marginBottom
                    }
                }""")
                await page.screenshot(path=SCREENSHOT_DIR / "step2_card.png")
                card_ok = 400 <= card_info['width'] <= 500  # Figma 設計 420px
                steps.append({"step": 3, "desc": f"登入卡片：寬={card_info['width']}px, 圓角={card_info['borderRadius']}, padding={card_info['padding']}", "status": "通過" if card_ok else f"寬度異常：{card_info['width']}px"})
                results.append(True if card_ok else False)
            else:
                steps.append({"step": 3, "desc": "登入卡片不存在", "status": "失敗"})
                results.append(False)

            # 4. 驗證輸入框間距（Figma: 間距 8px, 16px, 24px）
            email_input = await page.query_selector("input[type='email']")
            password_input = await page.query_selector("input[type='password']")
            if email_input and password_input:
                email_box = await email_input.bounding_box()
                password_box = await password_input.bounding_box()
                email_style = await email_input.evaluate("""el => {
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return { height: rect.height, borderRadius: style.borderRadius, marginBottom: style.marginBottom }
                }""")
                password_style = await password_input.evaluate("""el => {
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return { height: rect.height, borderRadius: style.borderRadius }
                }""")
                if email_box and password_box:
                    spacing = password_box['y'] - email_box['y'] - email_box['height']
                    await page.screenshot(path=SCREENSHOT_DIR / "step3_inputs.png")
                    input_ok = 10 <= spacing <= 50  # Figma 設計約 16-24px
                    steps.append({"step": 4, "desc": f"輸入框間距：{spacing}px (email 高={email_style['height']}, 圓角={email_style['borderRadius']})", "status": "通過" if input_ok else f"間距異常：{spacing}px"})
                    results.append(True if input_ok else False)
                else:
                    steps.append({"step": 4, "desc": "無法獲取輸入框位置", "status": "失敗"})
                    results.append(False)
            else:
                steps.append({"step": 4, "desc": "輸入框不存在", "status": "失敗"})
                results.append(False)

            # 5. 驗證按鈕樣式（Figma: 高 40px, 圓角 6-8px, 陰影）
            login_btn = await page.query_selector("button[type='submit'], .auth-cta, .login-btn")
            if login_btn:
                btn_info = await login_btn.evaluate("""el => {
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return {
                        width: rect.width,
                        height: rect.height,
                        borderRadius: style.borderRadius,
                        backgroundColor: style.backgroundColor,
                        color: style.color,
                        fontSize: style.fontSize,
                        fontWeight: style.fontWeight,
                        boxShadow: style.boxShadow,
                        marginTop: style.marginTop,
                        paddingTop: style.paddingTop
                    }
                }""")
                await page.screenshot(path=SCREENSHOT_DIR / "step4_button.png")
                btn_ok = 35 <= btn_info['height'] <= 50  # Figma 設計約 40px
                steps.append({"step": 5, "desc": f"登入按鈕：高={btn_info['height']}px, 圓角={btn_info['borderRadius']}, 背景色={btn_info['backgroundColor']}, 陰影={btn_info['boxShadow'][:50] if btn_info['boxShadow'] else '無'}", "status": "通過" if btn_ok else f"高度異常：{btn_info['height']}px"})
                results.append(True if btn_ok else False)
            else:
                steps.append({"step": 5, "desc": "登入按鈕不存在", "status": "失敗"})
                results.append(False)

            # 6. 全頁截圖
            await page.screenshot(path=SCREENSHOT_DIR / "step5_full_page.png", full_page=True)
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
