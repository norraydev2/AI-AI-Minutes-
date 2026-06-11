# 團隊充值紀錄模塊測試用例

**模塊名稱:** 團隊充值紀錄 (Team Recharge)  
**所屬系統:** 團隊管理系統  
**Figma 節點:** `nnAMn`  
**最後更新日期:** 2026-06-11

---

## TC-TEAM-RECHARGE-001: 團隊充值紀錄頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 預期結果
- URL 包含 `/teams/:id/recharge`
- 麵包屑顯示「團隊管理 / 團隊充值紀錄」
- 團隊基本資料卡片可見
- 充值記錄表格可見

### 自動化腳本
```python
async def test_team_recharge_loads(page):
    await page.goto("/teams/TEAM-2026-001/recharge")
    await page.wait_for_load_state("networkidle")
    
    assert await page.query_selector("#jgECo")
    assert await page.query_selector("#16GR9")
    
    await page.screenshot(path="screenshots/team_recharge_001_load.png")
```

---

## TC-TEAM-RECHARGE-002: 充值記錄表格顯示驗證

**優先級:** 高  
**類型:** 數據驗證  
**執行階段:** P1

### 預期結果
| 欄位 | 說明 |
|------|------|
| 充值時間 | YYYY-MM-DD HH:mm:ss |
| 充值成員 | 文字 |
| 充值金額 | HK$ 數值 |
| 支付方式 | 信用卡/PPS 等 |
| 支付狀態 | 成功/失敗/待處理 |
| 交易單號 | 交易 ID |

### 自動化腳本
```python
async def test_recharge_table(page):
    await page.goto("/teams/TEAM-2026-001/recharge")
    
    # 驗證表格
    table = await page.query_selector("#16GR9")
    assert table is not None
    
    # 驗證數據格式
    cells = await page.query_selector_all("#16GR9 td")
    if len(cells) >= 6:
        # 驗證金額格式
        amount = await cells[2].inner_text()
        assert "HK$" in amount
    
    await page.screenshot(path="screenshots/team_recharge_002_table.png")
```

---

## TC-TEAM-RECHARGE-003: 返回按鈕功能驗證

**優先級:** 低  
**類型:** 功能測試  
**執行階段:** P1

### 測試步驟
1. 點擊返回按鈕

### 預期結果
- 返回至團隊詳情頁或列表頁

### 自動化腳本
```python
async def test_back_button(page):
    await page.goto("/teams/TEAM-2026-001/recharge")
    await page.go_back()
    await page.wait_for_load_state("networkidle")
    assert "/teams/" in page.url
    
    await page.screenshot(path="screenshots/team_recharge_003_back.png")
```
