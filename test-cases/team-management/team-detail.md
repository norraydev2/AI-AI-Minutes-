# 團隊詳情模塊測試用例

**模塊名稱:** 團隊詳情 (Team Detail)  
**所屬系統:** 團隊管理系統  
**Figma 節點:** `UMzLK`  
**最後更新日期:** 2026-06-11

---

## TC-TEAM-DETAIL-001: 團隊詳情頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 前置條件
- 從團隊列表點擊查看按鈕進入

### 測試步驟
1. 導航至團隊詳情頁
2. 等待頁面加載

### 預期結果
- URL 包含團隊 ID
- 麵包屑顯示「團隊管理 / 團隊詳情」
- 團隊基本資料卡片可見
- 團隊成員表格可見

### 自動化腳本
```python
async def test_team_detail_loads(page):
    await page.goto("/teams/TEAM-2026-001")
    await page.wait_for_load_state("networkidle")
    
    assert await page.query_selector("#l31yX")  # 基本資料卡片
    assert await page.query_selector("#NhGWW")  # 成員表格
    
    await page.screenshot(path="screenshots/team_detail_001_load.png")
```

---

## TC-TEAM-DETAIL-002: 團隊基本資料顯示驗證

**優先級:** 高  
**類型:** 數據驗證  
**執行階段:** P1

### 預期結果
| 欄位 | 格式 |
|------|------|
| 團隊名稱 | 文字 |
| 團隊 ID | TEAM-YYYY-NNN |
| 團隊擁有人 | 文字 |
| 可支配分鐘數 | 數字 + 「分鐘」 |
| 成立時間 | YYYY-MM-DD HH:mm:ss |
| 最近充值時間 | YYYY-MM-DD HH:mm:ss |
| 團隊成員數量 | 數字 + 「人」 |
| 累計充值 | HK$ 格式 |

### 自動化腳本
```python
async def test_team_basic_info(page):
    await page.goto("/teams/TEAM-2026-001")
    
    # 驗證團隊 ID 格式
    team_id_el = await page.query_selector("[data-field='teamId']")
    if team_id_el:
        team_id = await team_id_el.inner_text()
        assert re.match(r"TEAM-\d{4}-\d{3}", team_id)
    
    await page.screenshot(path="screenshots/team_detail_002_info.png")
```

---

## TC-TEAM-DETAIL-003: 團隊成員表格顯示驗證

**優先級:** 中  
**類型:** 數據驗證  
**執行階段:** P1

### 預期結果
| 欄位 | 說明 |
|------|------|
| 成員名稱 | 文字 |
| 電郵地址 | 電郵格式 |
| 角色 | 文字 |
| 狀態 | 啟用/禁用 |
| 最後登入時間 | 時間格式 |

### 自動化腳本
```python
async def test_team_members_table(page):
    await page.goto("/teams/TEAM-2026-001")
    
    table = await page.query_selector("#NhGWW")
    assert table is not None
    
    await page.screenshot(path="screenshots/team_detail_003_members.png")
```

---

## TC-TEAM-DETAIL-004: 分頁籤切換功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 測試步驟
1. 點擊「團隊成員」標籤
2. 點擊「充值記錄」標籤

### 預期結果
- 切換顯示對應內容區域
- URL 可能包含 hash（如 `#recharge`）

### 自動化腳本
```python
async def test_tabs_switch(page):
    await page.goto("/teams/TEAM-2026-001")
    
    # 點擊充值記錄標籤
    recharge_tab = await page.query_selector("#krGRT button:nth-child(2)")
    if recharge_tab:
        await recharge_tab.click()
        await page.wait_for_load_state("networkidle")
        
        # 驗證顯示充值記錄表格
        recharge_table = await page.query_selector("#42gys")
        assert recharge_table is not None
    
    await page.screenshot(path="screenshots/team_detail_004_tabs.png")
```
