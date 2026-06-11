# 充值紀錄模塊測試用例

**模塊名稱:** 充值紀錄 (Recharge Records)  
**所屬系統:** 財務數據系統  
**Figma 節點:** `5kvjX`  
**最後更新日期:** 2026-06-11

---

## TC-FIN-RECORDS-001: 充值紀錄頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_recharge_records_loads(page):
    await page.click("#MgjUV")  # 財務數據 → 充值紀錄
    await page.wait_for_load_state("networkidle")
    
    assert "/finance/recharge" in page.url
    assert await page.query_selector("#Q6WjC")  # 篩選區
    assert await page.query_selector("#rtiua")  # 表格
    
    await page.screenshot(path="screenshots/fin_records_001_load.png")
```

---

## TC-FIN-RECORDS-002: 訂單編號篩選功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_filter_by_order_id(page):
    await page.goto("/finance/recharge")
    
    await page.fill("#Q6WjC input[name='orderId']", "RC202603")
    await page.click("#Q6WjC button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/fin_records_002_order_filter.png")
```

---

## TC-FIN-RECORDS-003: 電郵地址篩選功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_filter_by_email(page):
    await page.goto("/finance/recharge")
    
    await page.fill("#Q6WjC input[name='email']", "@acme.com")
    await page.click("#Q6WjC button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/fin_records_003_email_filter.png")
```

---

## TC-FIN-RECORDS-004: 充值金額範圍篩選驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_filter_by_amount(page):
    await page.goto("/finance/recharge")
    
    await page.fill("#Q6WjC input[name='minAmount']", "1000")
    await page.fill("#Q6WjC input[name='maxAmount']", "10000")
    await page.click("#Q6WjC button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/fin_records_004_amount_filter.png")
```

---

## TC-FIN-RECORDS-005: 支付方式下拉篩選驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_filter_by_payment_method(page):
    await page.goto("/finance/recharge")
    
    await page.click("#Q6WjC select[name='paymentMethod']")
    await page.select_option("#Q6WjC select[name='paymentMethod']", "credit_card")
    await page.click("#Q6WjC button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/fin_records_005_payment_filter.png")
```

---

## TC-FIN-RECORDS-006: 查詢按鈕功能驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_query_button(page):
    await page.goto("/finance/recharge")
    
    # 點擊查詢按鈕
    query_btn = await page.query_selector("#Q6WjC button")
    await query_btn.click()
    await page.wait_for_load_state("networkidle")
    
    # 驗證按鈕恢復可用
    assert await query_btn.is_enabled()
    
    await page.screenshot(path="screenshots/fin_records_006_query.png")
```

---

## TC-FIN-RECORDS-007: 充值紀錄表格顯示驗證

**優先級:** 高  
**類型:** 數據驗證  
**執行階段:** P1

### 預期結果
| 欄位 | 說明 |
|------|------|
| 訂單編號 | RC 開頭的交易 ID |
| 用戶名稱 | 文字 |
| 電郵地址 | 電郵格式 |
| 充值金額 | HK$ 數值 |
| 支付方式 | 信用卡/PPS/Apple Pay 等 |
| 充值狀態 | 成功/失敗/待處理 |
| 充值時間 | 時間格式 |

### 自動化腳本
```python
async def test_recharge_table(page):
    await page.goto("/finance/recharge")
    
    table = await page.query_selector("#rtiua")
    assert table is not None
    
    # 驗證表頭
    headers = await page.query_selector_all("#rtiua th")
    assert len(headers) >= 7
    
    await page.screenshot(path="screenshots/fin_records_007_table.png")
```

---

## TC-FIN-RECORDS-008: 分頁功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_pagination(page):
    await page.goto("/finance/recharge")
    
    # 驗證總記錄
    total = await page.query_selector("#rtiua + div")
    if total:
        text = await total.inner_text()
        assert "共" in text
    
    # 點擊下一頁
    next_btn = await page.query_selector(".pagination .next")
    if next_btn:
        await next_btn.click()
        await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/fin_records_008_pagination.png")
```
