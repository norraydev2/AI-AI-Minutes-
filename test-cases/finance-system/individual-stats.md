# 個人充值統計模塊測試用例

**模塊名稱:** 個人充值統計 (Individual Stats)  
**所屬系統:** 財務數據系統  
**Figma 節點:** `EH2Cx`  
**最後更新日期:** 2026-06-11

---

## TC-FIN-INDIVIDUAL-001: 個人充值統計頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_individual_stats_loads(page):
    await page.click("#Bo6R6")  # 財務數據 → 個人充值統計
    await page.wait_for_load_state("networkidle")
    
    assert "/finance/individual-stats" in page.url
    assert await page.query_selector("#Gi9WX")
    assert await page.query_selector("#FmwWu")
    
    await page.screenshot(path="screenshots/fin_individual_001_load.png")
```

---

## TC-FIN-INDIVIDUAL-002: 用戶名稱篩選功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_filter_by_username(page):
    await page.goto("/finance/individual-stats")
    
    await page.fill("#Gi9WX input[name='username']", "陳")
    await page.click("#Gi9WX button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/fin_individual_002_name_filter.png")
```

---

## TC-FIN-INDIVIDUAL-003: 電郵地址篩選功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_filter_by_email(page):
    await page.goto("/finance/individual-stats")
    
    await page.fill("#Gi9WX input[name='email']", "@gmail.com")
    await page.click("#Gi9WX button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/fin_individual_003_email_filter.png")
```

---

## TC-FIN-INDIVIDUAL-004: 個人充值統計表格顯示驗證

**優先級:** 高  
**類型:** 數據驗證  
**執行階段:** P1

### 預期結果
| 欄位 | 說明 |
|------|------|
| 用戶名稱 | 文字 |
| 電郵地址 | 電郵格式 |
| 充值總金額 | HK$ 數值 |

### 自動化腳本
```python
async def test_individual_stats_table(page):
    await page.goto("/finance/individual-stats")
    
    table = await page.query_selector("#FmwWu")
    assert table is not None
    
    # 驗證總金額顯示
    total = await page.query_selector("text=充值總金額")
    if total:
        assert "HK$" in await total.inner_text()
    
    await page.screenshot(path="screenshots/fin_individual_004_table.png")
```
