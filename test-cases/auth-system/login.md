# 登入模塊測試用例

**模塊名稱:** 登入 (Login)  
**所屬系統:** 認證系統  
**Figma 節點:** `DxKBR` (賬號密碼登入)  
**最後更新日期:** 2026-06-11

---

## TC-AUTH-LOGIN-001: 使用有效憑證成功登入

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 測試帳號已註冊並啟用
- 用戶處於登入頁面 (`/login`)
- 瀏覽器 Cookie 和快取已清除

### 測試步驟
1. 導航至登入頁面
2. 在「賬號」輸入框輸入有效電郵地址
3. 在「密碼」輸入框輸入有效密碼
4. 點擊「登入」按鈕

### 預期結果
- 頁面跳轉至儀表板首頁 (`/dashboard`)
- 頁面標題更新為「AI Minutes - 主頁」
- 頂部導航欄顯示用戶名稱
- 側邊欄導航可用
- 無錯誤提示訊息

### 測試數據
| 字段 | 值 |
|------|-----|
| 賬號 | `test@example.com` |
| 密碼 | `Test1234!` |

### 自動化腳本
```python
# test_auth_login_001.py
async def test_valid_login(page):
    await page.goto("/login")
    await page.fill("#eQhn4 input", "test@example.com")
    await page.fill("#qbJ5L input", "Test1234!")
    await page.click("#iyzRC")
    await page.wait_for_url("**/dashboard")
    assert await page.title() == "AI Minutes - 主頁"
```

### 備註
- 本用例為其他用例的前置依賴
- 如需 2FA 驗證，需接續執行 TC-AUTH-2FA-001

---

## TC-AUTH-LOGIN-002: 使用無效賬號登入

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P2 - 邊界異常

### 前置條件
- 用戶處於登入頁面
- 輸入不存在的帳號

### 測試步驟
1. 導航至登入頁面
2. 在「賬號」輸入框輸入不存在的電郵地址
3. 在「密碼」輸入框輸入任意密碼
4. 點擊「登入」按鈕

### 預期結果
- 停留在登入頁面，URL 不變更為 `/dashboard`
- 顯示錯誤提示訊息（如：「帳號或密碼錯誤」）
- 輸入框內容保留或清空（依設計而定）
- 登入按鈕恢復可點擊狀態

### 測試數據
| 字段 | 值 |
|------|-----|
| 賬號 | `invalid@example.com` |
| 密碼 | `AnyPassword123!` |

### 自動化腳本
```python
# test_auth_login_002.py
async def test_invalid_account(page):
    await page.goto("/login")
    await page.fill("#eQhn4 input", "invalid@example.com")
    await page.fill("#qbJ5L input", "AnyPassword123!")
    await page.click("#iyzRC")
    # 應該停留在登入頁
    assert "/login" in page.url
    # 應該顯示錯誤訊息
    error_msg = await page.query_selector(".error-message")
    assert error_msg is not None
```

### 備註
- 錯誤訊息不應洩露帳號是否存在（安全考量）

---

## TC-AUTH-LOGIN-003: 使用無效密碼登入

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P2 - 邊界異常

### 前置條件
- 用戶處於登入頁面
- 使用有效帳號但錯誤密碼

### 測試步驟
1. 導航至登入頁面
2. 在「賬號」輸入框輸入有效電郵地址
3. 在「密碼」輸入框輸入錯誤密碼
4. 點擊「登入」按鈕

### 預期結果
- 停留在登入頁面
- 顯示錯誤提示訊息（如：「帳號或密碼錯誤」）
- 密碼框可能被清空
- 登入按鈕恢復可點擊狀態

### 測試數據
| 字段 | 值 |
|------|-----|
| 賬號 | `test@example.com` |
| 密碼 | `WrongPassword123!` |

### 自動化腳本
```python
# test_auth_login_003.py
async def test_invalid_password(page):
    await page.goto("/login")
    await page.fill("#eQhn4 input", "test@example.com")
    await page.fill("#qbJ5L input", "WrongPassword123!")
    await page.click("#iyzRC")
    assert "/login" in page.url
    error_msg = await page.query_selector(".error-message")
    assert error_msg is not None
```

### 備註
- 錯誤訊息應與 TC-AUTH-LOGIN-002 一致（防止帳號枚舉攻擊）

---

## TC-AUTH-LOGIN-004: 空賬號登入驗證

**優先級:** 中  
**類型:** 表單驗證  
**執行階段:** P2 - 邊界異常

### 前置條件
- 用戶處於登入頁面

### 測試步驟
1. 導航至登入頁面
2. 保持「賬號」輸入框為空
3. 在「密碼」輸入框輸入任意值
4. 點擊「登入」按鈕（或嘗試提交表單）

### 預期結果
- 阻止表單提交
- 顯示驗證錯誤訊息（如：「請輸入賬號」）
- 賬號輸入框獲得焦點
- 登入按鈕可能被禁用或點擊後無效

### 測試數據
| 字段 | 值 |
|------|-----|
| 賬號 | `(空)` |
| 密碼 | `AnyPassword123!` |

### 自動化腳本
```python
# test_auth_login_004.py
async def test_empty_account(page):
    await page.goto("/login")
    await page.fill("#qbJ5L input", "AnyPassword123!")
    await page.click("#iyzRC")
    # 應該顯示驗證錯誤
    await page.wait_for_selector(".validation-error")
    assert await page.query_selector("#eQhn4 .validation-error") is not None
```

### 備註
- 前端驗證應在提交前攔截

---

## TC-AUTH-LOGIN-005: 空密碼登入驗證

**優先級:** 中  
**類型:** 表單驗證  
**執行階段:** P2 - 邊界異常

### 前置條件
- 用戶處於登入頁面

### 測試步驟
1. 導航至登入頁面
2. 在「賬號」輸入框輸入有效電郵地址
3. 保持「密碼」輸入框為空
4. 點擊「登入」按鈕

### 預期結果
- 阻止表單提交
- 顯示驗證錯誤訊息（如：「請輸入密碼」）
- 密碼輸入框獲得焦點
- 登入按鈕可能被禁用或點擊後無效

### 測試數據
| 字段 | 值 |
|------|-----|
| 賬號 | `test@example.com` |
| 密碼 | `(空)` |

### 自動化腳本
```python
# test_auth_login_005.py
async def test_empty_password(page):
    await page.goto("/login")
    await page.fill("#eQhn4 input", "test@example.com")
    await page.click("#iyzRC")
    await page.wait_for_selector(".validation-error")
    assert await page.query_selector("#qbJ5L .validation-error") is not None
```

### 備註
- 前端驗證應在提交前攔截

---

## TC-AUTH-LOGIN-006: 登入頁面 UI 驗證

**優先級:** 低  
**類型:** UI 測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於登入頁面

### 測試步驟
1. 導航至登入頁面
2. 驗證頁面標題顯示「AI Minutes 後台管理系統」
3. 驗證卡片標題顯示「登入」
4. 驗證「賬號」標籤存在
5. 驗證「密碼」標籤存在
6. 驗證賬號輸入框存在且可輸入
7. 驗證密碼輸入框存在且可輸入
8. 驗證「登入」按鈕存在且可點擊
9. 驗證輸入框 placeholder 文字顯示

### 預期結果
| 元素 | 預期內容/屬性 |
|------|--------------|
| 品牌標題 | 「AI Minutes 後台管理系統」 |
| 卡片標題 | 「登入」 |
| 賬號標籤 | 「賬號」 |
| 密碼標籤 | 「密碼」 |
| 賬號 placeholder | 「請輸入賬號」 |
| 密碼 placeholder | 「請輸入密碼」 |
| 登入按鈕文字 | 「登入」 |
| 登入按鈕顏色 | 藍色漸層 `#2286FF` → `#19A7FF` |

### 自動化腳本
```python
# test_auth_login_006.py
async def test_login_page_ui(page):
    await page.goto("/login")
    
    # 驗證品牌標題
    brand = await page.query_selector("#ZvFX4")
    assert await brand.inner_text() == "AI Minutes 後台管理系統"
    
    # 驗證卡片標題
    title = await page.query_selector("#X4UlN")
    assert await title.inner_text() == "登入"
    
    # 驗證輸入框標籤
    account_label = await page.query_selector("#XJvrR")
    assert await account_label.inner_text() == "賬號"
    
    password_label = await page.query_selector("#wktF9")
    assert await password_label.inner_text() == "密碼"
    
    # 驗證 placeholder
    account_input = await page.query_selector("#eQhn4 input")
    assert await account_input.get_attribute("placeholder") == "請輸入賬號"
    
    # 驗證登入按鈕
    login_btn = await page.query_selector("#iyzRC")
    assert await login_btn.inner_text() == "登入"
    assert login_btn.is_enabled()
```

### 備註
- 本用例驗證 Figma 設計的 UI 實現準確性
- 需截取完整頁面截圖進行比對

---

## 測試執行摘要模板

| 執行日期 | 執行者 | 通過 | 失敗 | 跳過 | 備註 |
|---------|-------|------|------|------|------|
| - | - | - | - | - | - |
