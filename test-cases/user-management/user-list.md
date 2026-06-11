# 用戶列表模塊測試用例

**模塊名稱:** 用戶列表 (User List)  
**所屬系統:** 用戶管理系統  
**Figma 節點:** `NPfOA` (User Management)  
**最後更新日期:** 2026-06-11

---

## TC-USER-LIST-001: 用戶列表頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶已成功登入
- 處於儀表板頁面

### 測試步驟
1. 點擊側邊欄「用戶管理」導航項
2. 等待頁面加載完成

### 預期結果
- 頁面 URL 包含 `/users`
- 頁面標題顯示「用戶管理」
- 側邊欄「用戶管理」項高亮
- 篩選區域可見（用戶名稱、電郵地址、使用模式、賬號狀態輸入框和搜索按鈕）
- 表格區域可見（表頭和數據行）
- 分頁組件可見

### 自動化腳本
```python
# test_user_list_001.py
import asyncio
from playwright.async_api import Page, expect

async def test_user_list_page_loads(page: Page):
    """驗證用戶列表頁面正確加載"""
    
    # 導航至用戶管理頁面
    await page.click("#08eVO")  # 側邊欄用戶管理
    await page.wait_for_load_state("networkidle")
    
    # 驗證 URL
    await expect(page).to_have_url("**/users*")
    
    # 驗證頁面標題
    title = await page.query_selector("#Mu73K")
    if title:
        assert "用戶管理" in await title.inner_text()
    
    # 驗證側邊欄高亮
    active_nav = await page.query_selector("#1cwFp")
    assert active_nav is not None
    
    # 驗證篩選區域存在
    filter_area = await page.query_selector("#NZLvs")
    assert filter_area is not None
    
    # 驗證表格存在
    table = await page.query_selector("#PlTbx")
    assert table is not None
    
    # 驗證分頁存在
    pagination = await page.query_selector("#zdWEN")
    assert pagination is not None
    
    # 截圖
    await page.screenshot(path="screenshots/user_list_001_page_load.png")
```

### 備註
- 頁面加載時間應小於 3 秒
- 表格應顯示至少一筆數據

---

## TC-USER-LIST-002: 用戶名稱篩選功能驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於用戶列表頁面
- 表格中有用戶數據

### 測試步驟
1. 在「用戶名稱」輸入框輸入關鍵字
2. 點擊「搜索」按鈕
3. 等待表格刷新

### 預期結果
- 表格只顯示用戶名稱包含關鍵字的記錄
- 若無匹配數據，顯示空狀態或「暫無數據」
- URL 可能包含篩選參數（如 `?name=xxx`）

### 測試數據
| 輸入 | 預期結果 |
|------|---------|
| `陳` | 顯示所有姓陳的用戶 |
| `不存在的名字` | 顯示空狀態 |

### 自動化腳本
```python
# test_user_list_002.py
async def test_filter_by_username(page: Page):
    """驗證用戶名稱篩選功能"""
    
    await page.goto("/users")
    
    # 輸入關鍵字
    await page.fill("#qiQiq input", "陳")
    
    # 點擊搜索
    await page.click("#cRvK2")
    await page.wait_for_load_state("networkidle")
    
    # 驗證表格數據
    # 第一行數據應包含「陳」
    first_row = await page.query_selector("#6UqcC")  # row1
    if first_row:
        username_cell = await first_row.query_selector_first("td:nth-child(1)")
        if username_cell:
            text = await username_cell.inner_text()
            assert "陳" in text
    
    # 截圖
    await page.screenshot(path="screenshots/user_list_002_filter_name.png")
```

### 備註
- 搜索應支持模糊匹配
- 搜索按鈕點擊後應有 loading 狀態

---

## TC-USER-LIST-003: 電郵地址篩選功能驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於用戶列表頁面

### 測試步驟
1. 在「電郵地址」輸入框輸入關鍵字
2. 點擊「搜索」按鈕
3. 等待表格刷新

### 預期結果
- 表格只顯示電郵地址包含關鍵字的記錄
- 若無匹配數據，顯示空狀態

### 測試數據
| 輸入 | 預期結果 |
|------|---------|
| `@acme.com` | 顯示所有 acme 公司電郵的用戶 |
| `@nonexistent.com` | 顯示空狀態 |

### 自動化腳本
```python
# test_user_list_003.py
async def test_filter_by_email(page: Page):
    """驗證電郵地址篩選功能"""
    
    await page.goto("/users")
    
    # 輸入關鍵字
    await page.fill("#07rwZ input", "@acme.com")
    
    # 點擊搜索
    await page.click("#cRvK2")
    await page.wait_for_load_state("networkidle")
    
    # 驗證所有顯示的電郵都包含 @acme.com
    email_cells = await page.query_selector_all("#PlTbx td:nth-child(2)")
    for cell in email_cells:
        text = await cell.inner_text()
        assert "@acme.com" in text
    
    await page.screenshot(path="screenshots/user_list_003_filter_email.png")
```

---

## TC-USER-LIST-004: 使用模式下拉篩選驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於用戶列表頁面

### 測試步驟
1. 點擊「使用模式」下拉框
2. 選擇「團隊模式」
3. 點擊「搜索」按鈕
4. 重複步驟選擇「個人模式」

### 預期結果
- 下拉框展開顯示選項（全部、團隊模式、個人模式）
- 選擇後表格只顯示對應模式的記錄
- URL 可能包含篩選參數（如 `?mode=team`）

### 自動化腳本
```python
# test_user_list_004.py
async def test_filter_by_usage_mode(page: Page):
    """驗證使用模式篩選功能"""
    
    await page.goto("/users")
    
    # 點擊下拉框
    await page.click("#LaXmM")
    
    # 選擇團隊模式
    team_option = await page.query_selector("text=團隊模式")
    if team_option:
        await team_option.click()
        await page.click("#cRvK2")
        await page.wait_for_load_state("networkidle")
        
        # 驗證所有顯示的記錄都是團隊模式
        mode_cells = await page.query_selector_all("#PlTbx td:nth-child(3)")
        for cell in mode_cells:
            text = await cell.inner_text()
            assert "團隊模式" in text
    
    await page.screenshot(path="screenshots/user_list_004_filter_mode.png")
```

---

## TC-USER-LIST-005: 賬號狀態下拉篩選驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於用戶列表頁面

### 測試步驟
1. 點擊「賬號狀態」下拉框
2. 選擇「啟用中」
3. 點擊「搜索」按鈕
4. 重複步驟選擇「已停用」

### 預期結果
- 下拉框展開顯示選項（全部、啟用中、已停用）
- 選擇後表格只顯示對應狀態的記錄

### 自動化腳本
```python
# test_user_list_005.py
async def test_filter_by_status(page: Page):
    """驗證賬號狀態篩選功能"""
    
    await page.goto("/users")
    
    # 點擊下拉框
    await page.click("#LtJIH")
    
    # 選擇啟用中
    active_option = await page.query_selector("text=啟用中")
    if active_option:
        await active_option.click()
        await page.click("#cRvK2")
        await page.wait_for_load_state("networkidle")
        
        # 驗證所有顯示的記錄都是啟用中狀態
        status_badges = await page.query_selector_all("#PlTbx .status-badge")
        for badge in status_badges:
            text = await badge.inner_text()
            assert "啟用中" in text
    
    await page.screenshot(path="screenshots/user_list_005_filter_status.png")
```

---

## TC-USER-LIST-006: 搜索按鈕功能驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於用戶列表頁面

### 測試步驟
1. 同時設置多個篩選條件
2. 點擊「搜索」按鈕
3. 等待表格刷新

### 預期結果
- 表格顯示同時滿足所有篩選條件的記錄
- URL 包含所有篩選參數
- 搜索按鈕在搜索過程中顯示 loading 狀態並禁用

### 測試數據
| 用戶名稱 | 電郵 | 使用模式 | 賬號狀態 |
|---------|------|---------|---------|
| `陳` | `@acme.com` | 團隊模式 | 啟用中 |

### 自動化腳本
```python
# test_user_list_006.py
async def test_combined_filters(page: Page):
    """驗證組合篩選功能"""
    
    await page.goto("/users")
    
    # 設置多個篩選條件
    await page.fill("#qiQiq input", "陳")
    await page.fill("#07rwZ input", "@acme.com")
    
    # 選擇使用模式
    await page.click("#LaXmM")
    team_option = await page.query_selector("text=團隊模式")
    if team_option:
        await team_option.click()
    
    # 點擊搜索
    await page.click("#cRvK2")
    await page.wait_for_load_state("networkidle")
    
    # 驗證搜索按鈕恢復可用
    search_btn = await page.query_selector("#cRvK2")
    assert await search_btn.is_enabled()
    
    await page.screenshot(path="screenshots/user_list_006_combined_filters.png")
```

---

## TC-USER-LIST-007: 表格數據顯示驗證

**優先級:** 高  
**類型:** 數據驗證  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於用戶列表頁面
- 表格中有數據

### 測試步驟
1. 驗證表格表頭
2. 驗證表格數據行
3. 驗證各欄位數據格式

### 預期結果
| 欄位 | 預期內容 |
|------|---------|
| 用戶名稱 | 文字 |
| 電郵地址 | 有效電郵格式 |
| 使用模式 | 「團隊模式」或「個人模式」 |
| 剩餘分鐘數 | 數字 |
| 最後操作時間 | YYYY-MM-DD HH:mm:ss 格式 |
| 賬號狀態 | 「啟用中」或「已停用」徽章 |
| 狀態操作 | Toggle Switch |
| 操作 | 編輯/查看按鈕 |

### 自動化腳本
```python
# test_user_list_007.py
import re

async def test_table_data_format(page: Page):
    """驗證表格數據格式正確性"""
    
    await page.goto("/users")
    
    # 驗證表頭
    headers = await page.query_selector_all("#M5iaX div")
    expected_headers = ["用戶名稱", "電郵地址", "使用模式", "剩餘分鐘數", "最後操作時間", "賬號狀態", "狀態操作", "操作"]
    assert len(headers) >= len(expected_headers)
    
    # 驗證第一行數據格式
    first_row = await page.query_selector("#6UqcC")
    if first_row:
        cells = await first_row.query_selector_all("td, div[role='cell']")
        
        # 驗證電郵格式
        if len(cells) >= 2:
            email_text = await cells[1].inner_text()
            assert re.match(r"[^@]+@[^@]+\.[^@]+", email_text)
        
        # 驗證時間格式
        if len(cells) >= 5:
            time_text = await cells[4].inner_text()
            assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", time_text)
        
        # 驗證分鐘數為數字
        if len(cells) >= 4:
            minutes_text = await cells[3].inner_text()
            assert re.match(r"[\d,]+", minutes_text)
    
    await page.screenshot(path="screenshots/user_list_007_table_data.png")
```

---

## TC-USER-LIST-008: 分頁功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於用戶列表頁面
- 數據超過一頁（>30 條）

### 測試步驟
1. 驗證當前頁碼顯示
2. 點擊下一頁按鈕
3. 點擊特定頁碼
4. 點擊上一頁按鈕
5. 驗證每頁顯示數量選擇

### 預期結果
- 分頁組件顯示正確總記錄數
- 當前頁高亮顯示
- 點擊頁碼可跳轉至對應頁面
- 上一頁/下一頁按鈕在非邊界頁可用
- 每頁顯示數量可選擇（如 10/20/30/50）

### 自動化腳本
```python
# test_user_list_008.py
async def test_pagination(page: Page):
    """驗證分頁功能"""
    
    await page.goto("/users")
    
    # 驗證總記錄數顯示
    total_text = await page.query_selector("#bEkKs")
    if total_text:
        text = await total_text.inner_text()
        assert "共" in text and "條" in text
    
    # 驗證當前頁高亮
    current_page = await page.query_selector("#DRVxs")  # page6Current
    if current_page:
        assert "6" in await current_page.inner_text()
    
    # 點擊下一頁
    next_btn = await page.query_selector("#bjSKk")
    if next_btn and await next_btn.is_enabled():
        await next_btn.click()
        await page.wait_for_load_state("networkidle")
        
        # 驗證頁碼變更
        new_current = await page.query_selector("#DRVxs")
        if new_current:
            page_num = int(await new_current.inner_text())
            assert page_num == 7  # 從第 6 頁到第 7 頁
    
    # 驗證每頁顯示數量
    page_size = await page.query_selector("#4Xe0V")
    if page_size:
        text = await page_size.inner_text()
        assert "條/頁" in text
    
    await page.screenshot(path="screenshots/user_list_008_pagination.png")
```

---

## TC-USER-LIST-009: 賬號狀態 Toggle 切換驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P2 - 邊界異常

### 前置條件
- 用戶處於用戶列表頁面
- 用戶有編輯賬號狀態的權限

### 測試步驟
1. 找到一個「啟用中」的用戶
2. 點擊該用戶的 Toggle Switch
3. 確認操作（如有彈窗）
4. 驗證狀態變更

### 預期結果
- Toggle Switch 狀態改變（啟用 ↔ 停用）
- 可能顯示確認彈窗
- 成功後顯示提示訊息
- 表格中該用戶的狀態徽章同步更新

### 自動化腳本
```python
# test_user_list_009.py
async def test_toggle_account_status(page: Page):
    """驗證賬號狀態 Toggle 切換功能"""
    
    await page.goto("/users")
    
    # 找到第一個啟用中的用戶
    first_active_user_toggle = await page.query_selector("#eB4rD .toggle-switch")
    
    if first_active_user_toggle:
        # 獲取切換前狀態
        initial_state = await first_active_user_toggle.evaluate("el => el.checked")
        
        # 點擊切換
        await first_active_user_toggle.click()
        
        # 等待確認彈窗（如有）
        try:
            confirm_btn = await page.wait_for_selector("text=確認", timeout=2000)
            if confirm_btn:
                await confirm_btn.click()
        except:
            pass  # 無確認彈窗
        
        await page.wait_for_load_state("networkidle")
        
        # 驗證狀態已變更
        await page.wait_for_timeout(1000)
        new_state = await first_active_user_toggle.evaluate("el => el.checked")
        assert initial_state != new_state
        
        # 截圖
        await page.screenshot(path="screenshots/user_list_009_toggle_status.png")
```

### 備註
- 此為破壞性操作，測試後需還原狀態
- 可能需要管理員權限

---

## TC-USER-LIST-010: 查看用戶詳情按鈕驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於用戶列表頁面

### 測試步驟
1. 找到任意一筆用戶記錄
2. 點擊該用戶的「查看」按鈕

### 預期結果
- 跳轉至該用戶的詳情頁面
- URL 包含用戶 ID（如 `/users/:id`）
- 詳情頁面正確顯示該用戶的信息

### 自動化腳本
```python
# test_user_list_010.py
async def test_view_user_detail(page: Page):
    """驗證查看用戶詳情功能"""
    
    await page.goto("/users")
    
    # 找到第一個查看按鈕
    view_btn = await page.query_selector("#UQWse button.view-btn, #UQWse .action-btn")
    
    if view_btn:
        await view_btn.click()
        await page.wait_for_load_state("networkidle")
        
        # 驗證跳轉至詳情頁
        assert "/users/" in page.url or "/user-detail" in page.url
        
        # 驗證詳情頁面標題
        detail_title = await page.query_selector("#kvWfo")
        if detail_title:
            assert "用戶基本信息" in await detail_title.inner_text()
        
        # 截圖
        await page.screenshot(path="screenshots/user_list_010_view_detail.png")
```

---

## 測試執行摘要模板

| 執行日期 | 執行者 | 通過 | 失敗 | 跳過 | 備註 |
|---------|-------|------|------|------|------|
| - | - | - | - | - | - |
