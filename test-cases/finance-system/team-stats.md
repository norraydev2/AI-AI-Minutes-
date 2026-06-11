# 團隊充值統計模塊測試用例

**模塊名稱:** 團隊充值統計 (Team Stats)  
**所屬系統:** 財務數據系統  
**Figma 節點:** `yEhir`  
**最後更新日期:** 2026-06-11

---

## TC-FIN-TEAM-001: 團隊充值統計頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_team_stats_loads(page):
    await page.click("#AxF22")  # 財務數據 → 團隊充值統計
    await page.wait_for_load_state("networkidle")
    
    assert "/finance/team-stats" in page.url
    assert await page.query_selector("#dSdQj")
    assert await page.query_selector("#i2eRJ")
    
    await page.screenshot(path="screenshots/fin_team_001_load.png")
```

---

## TC-FIN-TEAM-002: 團隊 ID 篩選功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_filter_by_team_id(page):
    await page.goto("/finance/team-stats")
    
    await page.fill("#dSdQj input[name='teamId']", "T-2026")
    await page.click("#dSdQj button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/fin_team_002_id_filter.png")
```

---

## TC-FIN-TEAM-003: 團隊名稱篩選功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_filter_by_team_name(page):
    await page.goto("/finance/team-stats")
    
    await page.fill("#dSdQj input[name='teamName']", "Alpha")
    await page.click("#dSdQj button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/fin_team_003_name_filter.png")
```

---

## TC-FIN-TEAM-004: 充值日期範圍篩選驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_filter_by_date_range(page):
    await page.goto("/finance/team-stats")
    
    # 選擇日期範圍（需根據實際組件實現）
    await page.click("#dSdQj input[name='startDate']")
    await page.click("#dSdQj input[name='endDate']")
    await page.click("#dSdQj button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/fin_team_004_date_filter.png")
```

---

## TC-FIN-TEAM-005: 團隊充值統計表格顯示驗證

**優先級:** 高  
**類型:** 數據驗證  
**執行階段:** P1

### 預期結果
| 欄位 | 說明 |
|------|------|
| 團隊 ID | T-YYYY-NNNN |
| 團隊名稱 | 文字 |
| 團隊擁有人 | 文字 |
| 團隊成員數 | 數字 |
| 充值總金額 | HK$ 數值 |

### 自動化腳本
```python
async def test_team_stats_table(page):
    await page.goto("/finance/team-stats")
    
    table = await page.query_selector("#i2eRJ")
    assert table is not None
    
    # 驗證總金額顯示
    total_amount = await page.query_selector("text=充值總金額")
    if total_amount:
        assert "HK$" in await total_amount.inner_text()
    
    await page.screenshot(path="screenshots/fin_team_005_table.png")
```

---

## TC-FIN-TEAM-006: 搜尋年齡 Checkbox 功能驗證

**優先級:** 低  
**類型:** 功能測試  
**執行階段:** P2

### 自動化腳本
```python
async def test_search_age_checkbox(page):
    await page.goto("/finance/team-stats")
    
    checkbox = await page.query_selector("#dSdQj input[type='checkbox']")
    if checkbox:
        initial_state = await checkbox.evaluate("el => el.checked")
        await checkbox.click()
        new_state = await checkbox.evaluate("el => el.checked")
        assert initial_state != new_state
    
    await page.screenshot(path="screenshots/fin_team_006_checkbox.png")
```
