# 團隊列表模塊測試用例

**模塊名稱:** 團隊列表 (Team List)  
**所屬系統:** 團隊管理系統  
**Figma 節點:** `u1Z3o` (Team Management - Team List)  
**最後更新日期:** 2026-06-11

---

## TC-TEAM-LIST-001: 團隊列表頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶已成功登入
- 處於儀表板頁面

### 測試步驟
1. 點擊側邊欄「團隊管理」導航項
2. 等待頁面加載完成

### 預期結果
- 頁面 URL 包含 `/teams`
- 頁面標題顯示「團隊管理」
- 側邊欄「團隊管理」項高亮
- 篩選區域可見（團隊名稱、團隊 ID、團隊擁有人輸入框和篩選按鈕）
- 表格區域可見（表頭和數據行）
- 分頁組件可見

### 自動化腳本
```python
# test_team_list_001.py
async def test_team_list_page_loads(page):
    await page.click("#ffNGp")  # 側邊欄團隊管理
    await page.wait_for_load_state("networkidle")
    
    # 驗證 URL
    assert "/teams" in page.url
    
    # 驗證側邊欄高亮
    active_nav = await page.query_selector("#ffNGp")
    assert active_nav is not None
    
    # 驗證篩選區域存在
    filter_area = await page.query_selector("#q9D87")
    assert filter_area is not None
    
    # 驗證表格存在
    table = await page.query_selector("#ibZey")
    assert table is not None
    
    # 驗證分頁存在
    pagination = await page.query_selector("#PHUKG")
    assert pagination is not None
    
    await page.screenshot(path="screenshots/team_list_001_page_load.png")
```

---

## TC-TEAM-LIST-002: 團隊名稱篩選功能驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於團隊列表頁面

### 測試步驟
1. 在「團隊名稱」輸入框輸入關鍵字
2. 點擊「篩選」按鈕
3. 等待表格刷新

### 預期結果
- 表格只顯示團隊名稱包含關鍵字的記錄
- 若無匹配數據，顯示空狀態

### 測試數據
| 輸入 | 預期結果 |
|------|---------|
| `產品` | 顯示「產品研發組」等 |
| `不存在的團隊` | 顯示空狀態 |

### 自動化腳本
```python
# test_team_list_002.py
async def test_filter_by_team_name(page):
    await page.goto("/teams")
    
    await page.fill("#q9D87 input[name='teamName']", "產品")
    await page.click("#q9D87 button")
    await page.wait_for_load_state("networkidle")
    
    # 驗證所有顯示的團隊名稱都包含「產品」
    name_cells = await page.query_selector_all("#ibZey td:nth-child(1)")
    for cell in name_cells:
        text = await cell.inner_text()
        assert "產品" in text
    
    await page.screenshot(path="screenshots/team_list_002_filter_name.png")
```

---

## TC-TEAM-LIST-003: 團隊 ID 篩選功能驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於團隊列表頁面

### 測試步驟
1. 在「團隊 ID」輸入框輸入關鍵字
2. 點擊「篩選」按鈕

### 預期結果
- 表格只顯示團隊 ID 包含輸入字的記錄

### 測試數據
| 輸入 | 預期結果 |
|------|---------|
| `2026` | 顯示所有 2026 年創建的團隊 |
| `001` | 顯示 TEAM-2026-001 等 |

### 自動化腳本
```python
# test_team_list_003.py
async def test_filter_by_team_id(page):
    await page.goto("/teams")
    
    await page.fill("#q9D87 input[name='teamId']", "001")
    await page.click("#q9D87 button")
    await page.wait_for_load_state("networkidle")
    
    # 驗證所有顯示的團隊 ID 都包含 001
    id_cells = await page.query_selector_all("#ibZey td:nth-child(2)")
    for cell in id_cells:
        text = await cell.inner_text()
        assert "001" in text
    
    await page.screenshot(path="screenshots/team_list_003_filter_id.png")
```

---

## TC-TEAM-LIST-004: 團隊擁有人篩選功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於團隊列表頁面

### 測試步驟
1. 在「團隊擁有人」輸入框輸入關鍵字
2. 點擊「篩選」按鈕

### 預期結果
- 表格只顯示團隊擁有人包含輸入字的記錄

### 自動化腳本
```python
# test_team_list_004.py
async def test_filter_by_owner(page):
    await page.goto("/teams")
    
    await page.fill("#q9D87 input[name='owner']", "Thomas")
    await page.click("#q9D87 button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/team_list_004_filter_owner.png")
```

---

## TC-TEAM-LIST-005: 篩選按鈕功能驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於團隊列表頁面

### 測試步驟
1. 同時設置多個篩選條件
2. 點擊「篩選」按鈕
3. 驗證表格刷新

### 預期結果
- 表格顯示同時滿足所有篩選條件的記錄
- 篩選按鈕在搜索過程中顯示 loading 狀態

### 自動化腳本
```python
# test_team_list_005.py
async def test_combined_filters(page):
    await page.goto("/teams")
    
    # 設置多個篩選條件
    await page.fill("#q9D87 input[name='teamName']", "產品")
    await page.fill("#q9D87 input[name='teamId']", "2026")
    
    # 點擊篩選
    await page.click("#q9D87 button")
    await page.wait_for_load_state("networkidle")
    
    # 驗證篩選按鈕恢復可用
    filter_btn = await page.query_selector("#q9D87 button")
    assert await filter_btn.is_enabled()
    
    await page.screenshot(path="screenshots/team_list_005_combined_filters.png")
```

---

## TC-TEAM-LIST-006: 表格數據顯示驗證

**優先級:** 高  
**類型:** 數據驗證  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於團隊列表頁面

### 測試步驟
1. 驗證表格表頭
2. 驗證表格數據行
3. 驗證各欄位數據格式

### 預期結果
| 欄位 | 預期內容 |
|------|---------|
| 團隊名稱 | 文字 |
| 團隊 ID | TEAM-YYYY-NNN 格式 |
| 團隊擁有人 | 文字 |
| 成員數 | 數字 |
| 最近充值時間 | YYYY-MM-DD HH:mm:ss |
| 操作 | 查看按鈕 |

### 自動化腳本
```python
# test_team_list_006.py
import re

async def test_table_data_format(page):
    await page.goto("/teams")
    
    # 驗證表頭
    headers = await page.query_selector_all("#sbsvM div")
    expected = ["團隊名稱", "團隊 ID", "團隊擁有人", "成員數", "最近充值時間", "操作"]
    assert len(headers) >= len(expected)
    
    # 驗證第一行數據
    first_row = await page.query_selector("#JXQcw")
    if first_row:
        cells = await first_row.query_selector_all("td, div[role='cell']")
        
        # 驗證團隊 ID 格式
        if len(cells) >= 2:
            team_id = await cells[1].inner_text()
            assert re.match(r"TEAM-\d{4}-\d{3}", team_id)
        
        # 驗證成員數為數字
        if len(cells) >= 4:
            count = await cells[3].inner_text()
            assert re.match(r"\d+", count)
        
        # 驗證時間格式
        if len(cells) >= 5:
            time_text = await cells[4].inner_text()
            assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", time_text)
    
    await page.screenshot(path="screenshots/team_list_006_table_data.png")
```

---

## TC-TEAM-LIST-007: 分頁功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於團隊列表頁面
- 數據超過一頁

### 測試步驟
1. 驗證總記錄數顯示
2. 點擊下一頁
3. 點擊頁碼

### 預期結果
- 分頁組件正確顯示總記錄數（如「共 18 個團隊」）
- 頁碼可點擊跳轉
- 上一頁/下一頁按鈕可用

### 自動化腳本
```python
# test_team_list_007.py
async def test_pagination(page):
    await page.goto("/teams")
    
    # 驗證總記錄數
    total = await page.query_selector("#15rDZ")
    if total:
        text = await total.inner_text()
        assert "共" in text and "個團隊" in text
    
    # 點擊下一頁
    next_btn = await page.query_selector("#5Cswt")
    if next_btn and await next_btn.is_enabled():
        await next_btn.click()
        await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/team_list_007_pagination.png")
```

---

## TC-TEAM-LIST-008: 查看團隊詳情按鈕驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於團隊列表頁面

### 測試步驟
1. 找到任意一筆團隊記錄
2. 點擊該團隊的「查看」按鈕

### 預期結果
- 跳轉至該團隊的詳情頁面
- URL 包含團隊 ID

### 自動化腳本
```python
# test_team_list_008.py
async def test_view_team_detail(page):
    await page.goto("/teams")
    
    # 找到第一個查看按鈕
    view_btn = await page.query_selector("#tTKQj button")
    
    if view_btn:
        await view_btn.click()
        await page.wait_for_load_state("networkidle")
        
        # 驗證跳轉至詳情頁
        assert "/teams/" in page.url
        
        await page.screenshot(path="screenshots/team_list_008_view_detail.png")
```

---

## 測試執行摘要模板

| 執行日期 | 執行者 | 通過 | 失敗 | 跳過 | 備註 |
|---------|-------|------|------|------|------|
| - | - | - | - | - | - |
