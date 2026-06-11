# 用戶詳情模塊測試用例

**模塊名稱:** 用戶詳情 (User Profile Detail)  
**所屬系統:** 用戶管理系統  
**Figma 節點:** `yvijQ` (User Profile Detail)  
**最後更新日期:** 2026-06-11

---

## TC-USER-DETAIL-001: 用戶詳情頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶已成功登入
- 從用戶列表點擊「查看」按鈕進入詳情頁
- 或直接導航至用戶詳情頁 URL

### 測試步驟
1. 從用戶列表點擊查看按鈕進入
2. 等待頁面加載完成

### 預期結果
- 頁面 URL 包含用戶 ID（如 `/users/:id`）
- 麵包屑顯示「用戶管理 / 用戶基本信息」
- 用戶基本資料卡片可見
- 充值記錄表格可見
- 返回按鈕可見（如有）

### 自動化腳本
```python
# test_user_detail_001.py
async def test_user_detail_page_loads(page):
    await page.goto("/users/12345")  # 或使用實際用戶 ID
    await page.wait_for_load_state("networkidle")
    
    # 驗證麵包屑
    crumb = await page.query_selector("#kvWfo")
    assert crumb is not None
    
    # 驗證基本資料卡片存在
    basic_card = await page.query_selector("#sKjkC")
    assert basic_card is not None
    
    # 驗證充值記錄表格存在
    recharge_table = await page.query_selector("#xgXni")
    assert recharge_table is not None
    
    await page.screenshot(path="screenshots/user_detail_001_page_load.png")
```

---

## TC-USER-DETAIL-002: 用戶基本資料顯示驗證

**優先級:** 高  
**類型:** 數據驗證  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶詳情頁面已加載

### 測試步驟
1. 驗證用戶基本資料卡片所有欄位
2. 驗證各欄位數據格式

### 預期結果
| 欄位 | 預期格式 |
|------|---------|
| 用戶名稱 | 文字 |
| 電郵地址 | 有效電郵格式 |
| 註冊模式 | 「團隊模式」或「個人模式」 |
| 剩餘分鐘數 | 數字 + 「分鐘」 |
| 註冊時間 | YYYY-MM-DD HH:mm:ss |
| 最後登入時間 | YYYY-MM-DD HH:mm:ss |
| 賬號狀態 | Toggle + 狀態文字 |
| 累計充值金額 | 貨幣格式（HK$ X,XXX） |

### 自動化腳本
```python
# test_user_detail_002.py
import re

async def test_user_basic_info(page):
    await page.goto("/users/12345")
    
    # 驗證各欄位
    fields = {
        "username": None,  # 需根據實際 selector 調整
        "email": None,
        "mode": None,
        "minutes": None,
        "register_time": None,
        "login_time": None,
        "total_recharge": None
    }
    
    # 驗證電郵格式
    email_el = await page.query_selector("[data-field='email']")
    if email_el:
        email = await email_el.inner_text()
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email)
    
    # 驗證分鐘數為數字
    minutes_el = await page.query_selector("[data-field='minutes']")
    if minutes_el:
        minutes = await minutes_el.inner_text()
        assert re.match(r"[\d,]+", minutes.replace(",", ""))
    
    # 驗證累計充值為貨幣格式
    recharge_el = await page.query_selector("[data-field='total_recharge']")
    if recharge_el:
        recharge = await recharge_el.inner_text()
        assert "HK$" in recharge or "$" in recharge
    
    await page.screenshot(path="screenshots/user_detail_002_basic_info.png")
```

---

## TC-USER-DETAIL-003: 充值記錄表格顯示驗證

**優先級:** 中  
**類型:** 數據驗證  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶詳情頁面已加載
- 該用戶有充值記錄

### 測試步驟
1. 驗證充值記錄表格表頭
2. 驗證表格數據行
3. 驗證各欄位數據格式

### 預期結果
| 欄位 | 預期內容 |
|------|---------|
| 充值時間 | YYYY-MM-DD HH:mm:ss |
| 充值金額 | HK$ 數值 |
| 支付方式 | 信用卡/PPS/Apple Pay/銀行轉賬等 |
| 使用模式 | 團隊模式 |
| 支付狀態 | 「成功」(綠) 或「失敗」(紅) |
| 交易單號 | 交易 ID 字串 |

### 自動化腳本
```python
# test_user_detail_003.py
import re

async def test_recharge_history_table(page):
    await page.goto("/users/12345")
    
    # 驗證表格存在
    table = await page.query_selector("#xgXni")
    assert table is not None
    
    # 驗證表頭
    headers = await page.query_selector_all("#xgXni th, #xgXni .header-cell")
    assert len(headers) >= 6  # 至少 6 個欄位
    
    # 驗證第一行數據
    first_row = await page.query_selector("#xgXni tr:nth-child(2)")
    if first_row:
        cells = await first_row.query_selector_all("td")
        
        # 驗證時間格式
        if len(cells) >= 1:
            time_text = await cells[0].inner_text()
            assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", time_text)
        
        # 驗證金額格式
        if len(cells) >= 2:
            amount_text = await cells[1].inner_text()
            assert "HK$" in amount_text or "$" in amount_text
        
        # 驗證支付狀態
        if len(cells) >= 5:
            status_text = await cells[4].inner_text()
            assert status_text in ["成功", "失敗", "待處理"]
    
    await page.screenshot(path="screenshots/user_detail_003_recharge_table.png")
```

---

## TC-USER-DETAIL-004: 返回按鈕功能驗證

**優先級:** 低  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於用戶詳情頁面

### 測試步驟
1. 點擊返回按鈕（或瀏覽器返回）
2. 驗證跳轉

### 預期結果
- 返回至用戶列表頁面
- URL 變更為 `/users`

### 自動化腳本
```python
# test_user_detail_004.py
async def test_back_button(page):
    await page.goto("/users/12345")
    
    # 使用瀏覽器返回
    await page.go_back()
    await page.wait_for_load_state("networkidle")
    
    # 驗證返回至列表頁
    assert "/users" in page.url
    
    # 或尋找頁面上的返回按鈕
    # back_btn = await page.query_selector(".back-btn")
    # if back_btn:
    #     await back_btn.click()
    #     await page.wait_for_load_state("networkidle")
    #     assert "/users" in page.url
    
    await page.screenshot(path="screenshots/user_detail_004_back.png")
```

---

## 測試執行摘要模板

| 執行日期 | 執行者 | 通過 | 失敗 | 跳過 | 備註 |
|---------|-------|------|------|------|------|
| - | - | - | - | - | - |
