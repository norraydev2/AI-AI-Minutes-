# 兩因素驗證模塊測試用例

**模塊名稱:** 電郵驗證 (2FA Email Verification)  
**所屬系統:** 認證系統  
**Figma 節點:** `XftgV` (電郵驗證碼)  
**最後更新日期:** 2026-06-11

---

## TC-AUTH-2FA-001: 輸入正確驗證碼成功登入

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶已完成賬號密碼登入步驟
- 系統要求進行兩因素驗證
- 用戶已收到電郵驗證碼
- 用戶處於驗證頁面 (`/2fa-verify`)

### 測試步驟
1. 確認頁面顯示「設備驗證」標題
2. 確認提示訊息顯示「驗證碼已發送至您的電郵」
3. 在「電郵驗證碼」輸入框輸入 6 位數字驗證碼
4. 點擊「驗證並登入」按鈕

### 預期結果
- 頁面跳轉至儀表板首頁 (`/dashboard`)
- 頁面標題更新為「AI Minutes - 主頁」
- 登入成功，會話建立
- 側邊欄導航可用
- 無錯誤提示訊息

### 測試數據
| 字段 | 值 |
|------|-----|
| 驗證碼 | `123456` (示例，實際從電郵獲取) |

### 自動化腳本
```python
# test_auth_2fa_001.py
import re

async def test_valid_2fa_code(page, code_url=None):
    await page.goto("/2fa-verify")
    
    # 從電郵來源獲取驗證碼
    if code_url:
        code_page = await page.context.new_page()
        await code_page.goto(code_url)
        text = await code_page.inner_text("body")
        match = re.search(r'\b\d{6}\b', text)
        code = match.group(0) if match else None
        await code_page.close()
    else:
        code = "123456"  # 測試環境固定碼
    
    # 輸入驗證碼
    await page.fill("#89hRJ input", code)
    await page.click("#uvYyE")
    
    # 驗證跳轉
    await page.wait_for_url("**/dashboard")
    assert await page.title() == "AI Minutes - 主頁"
```

### 備註
- 本用例為其他系統用例的前置依賴
- 驗證碼通常有 5-10 分鐘有效期

---

## TC-AUTH-2FA-002: 輸入錯誤驗證碼

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P2 - 邊界異常

### 前置條件
- 用戶處於驗證頁面
- 輸入錯誤的 6 位數字

### 測試步驟
1. 導航至驗證頁面
2. 在「電郵驗證碼」輸入框輸入錯誤的 6 位數字
3. 點擊「驗證並登入」按鈕

### 預期結果
- 停留在驗證頁面，URL 不變更
- 顯示錯誤提示訊息（如：「驗證碼錯誤，請重試」）
- 輸入框內容可能被清空
- 「驗證並登入」按鈕恢復可點擊狀態
- 「發送驗證碼」按鈕仍可用

### 測試數據
| 字段 | 值 |
|------|-----|
| 驗證碼 | `000000` (錯誤碼) |

### 自動化腳本
```python
# test_auth_2fa_002.py
async def test_invalid_2fa_code(page):
    await page.goto("/2fa-verify")
    
    # 輸入錯誤驗證碼
    await page.fill("#89hRJ input", "000000")
    await page.click("#uvYyE")
    
    # 應該停留在驗證頁
    assert "/2fa-verify" in page.url
    
    # 應該顯示錯誤訊息
    error_msg = await page.query_selector(".error-message")
    assert error_msg is not None
    
    # 按鈕應恢復可點擊
    login_btn = await page.query_selector("#uvYyE")
    assert await login_btn.is_enabled()
```

### 備註
- 錯誤次數過多可能觸發帳號鎖定（需確認業務規則）

---

## TC-AUTH-2FA-003: 空驗證碼提交

**優先級:** 中  
**類型:** 表單驗證  
**執行階段:** P2 - 邊界異常

### 前置條件
- 用戶處於驗證頁面

### 測試步驟
1. 導航至驗證頁面
2. 保持「電郵驗證碼」輸入框為空
3. 點擊「驗證並登入」按鈕

### 預期結果
- 阻止表單提交
- 顯示驗證錯誤訊息（如：「請輸入驗證碼」）
- 輸入框獲得焦點
- 「驗證並登入」按鈕可能被禁用或點擊後無效

### 測試數據
| 字段 | 值 |
|------|-----|
| 驗證碼 | `(空)` |

### 自動化腳本
```python
# test_auth_2fa_003.py
async def test_empty_2fa_code(page):
    await page.goto("/2fa-verify")
    
    # 嘗試提交空表單
    await page.click("#uvYyE")
    
    # 應該顯示驗證錯誤
    await page.wait_for_selector(".validation-error")
    code_input = await page.query_selector("#89hRJ")
    assert code_input is not None
```

### 備註
- 前端驗證應在提交前攔截

---

## TC-AUTH-2FA-004: 重新發送驗證碼

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於驗證頁面
- 距離上次發送已過一定時間（如 60 秒）

### 測試步驟
1. 導航至驗證頁面
2. 點擊「發送驗證碼」按鈕
3. 等待發送完成提示
4. 檢查電郵是否收到新驗證碼

### 預期結果
- 顯示成功提示（如：「驗證碼已重新發送」）
- 「發送驗證碼」按鈕進入倒數計時（如 60 秒）
- 倒數期間按鈕禁用
- 倒數結束後按鈕恢復可用
- 新驗證碼發送至註冊電郵

### 自動化腳本
```python
# test_auth_2fa_004.py
async def test_resend_code(page):
    await page.goto("/2fa-verify")
    
    # 點擊發送驗證碼
    await page.click("#61Zol")
    
    # 等待成功提示
    await page.wait_for_selector(".success-message")
    success_msg = await page.query_selector(".success-message")
    assert "已發送" in await success_msg.inner_text()
    
    # 驗證按鈕進入倒數
    resend_btn = await page.query_selector("#61Zol")
    assert await resend_btn.get_attribute("disabled") is not None
    
    # 驗證倒數文字（如：「60s 後重發」）
    btn_text = await resend_btn.inner_text()
    assert "s 後重發" in btn_text or " resend" in btn_text.lower()
```

### 備註
- 倒數時間通常為 60 秒
- 需確認是否有每日發送次數限制

---

## TC-AUTH-2FA-005: 驗證碼頁面 UI 驗證

**優先級:** 低  
**類型:** UI 測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶處於驗證頁面

### 測試步驟
1. 導航至驗證頁面
2. 驗證頁面所有可見元素

### 預期結果
| 元素 | 預期內容/屬性 |
|------|--------------|
| 品牌標題 | 「AI Minutes 後台管理系統」 |
| 卡片標題 | 「設備驗證」 |
| 提示文字 | 「驗證碼已發送至您的電郵，請再下方輸入您的電郵驗證碼」 |
| 驗證碼標籤 | 「電郵驗證碼」 |
| 驗證碼輸入框 | 高度 38px，白色背景，灰色邊框 |
| 發送驗證碼按鈕 | 白色背景，藍色邊框 `#91CAFF` |
| 驗證並登入按鈕 | 藍色漸層 `#2286FF` → `#19A7FF` |

### 自動化腳本
```python
# test_auth_2fa_005.py
async def test_2fa_page_ui(page):
    await page.goto("/2fa-verify")
    
    # 驗證品牌標題
    brand = await page.query_selector("#Bi0Bx")
    assert await brand.inner_text() == "AI Minutes 後台管理系統"
    
    # 驗證卡片標題
    title = await page.query_selector("#SDTHO")
    assert await title.inner_text() == "設備驗證"
    
    # 驗證提示文字
    notice = await page.query_selector("#R1O78")
    assert "驗證碼" in await notice.inner_text()
    
    # 驗證標籤
    label = await page.query_selector("#Mtrsf")
    assert await label.inner_text() == "電郵驗證碼"
    
    # 驗證按鈕文字
    send_btn = await page.query_selector("#61Zol")
    assert "發送驗證碼" in await send_btn.inner_text()
    
    login_btn = await page.query_selector("#uvYyE")
    assert await login_btn.inner_text() == "驗證並登入"
```

### 備註
- 需截取完整頁面截圖進行 UI 比對

---

## TC-AUTH-2FA-006: 驗證碼格式驗證（非 6 位數字）

**優先級:** 中  
**類型:** 表單驗證  
**執行階段:** P2 - 邊界異常

### 前置條件
- 用戶處於驗證頁面

### 測試步驟
1. 導航至驗證頁面
2. 在「電郵驗證碼」輸入框輸入非 6 位數字（如 5 位或 7 位）
3. 點擊「驗證並登入」按鈕
4. 或輸入包含字母的字串

### 預期結果
| 測試場景 | 預期結果 |
|---------|---------|
| 少於 6 位（如 5 位） | 阻止提交，顯示「驗證碼格式錯誤」 |
| 多於 6 位（如 7 位） | 阻止提交，顯示「驗證碼格式錯誤」 |
| 包含字母 | 阻止提交，顯示「驗證碼格式錯誤」或輸入框拒絕字母 |

### 測試數據
| 測試場景 | 輸入值 |
|---------|--------|
| 少於 6 位 | `12345` |
| 多於 6 位 | `1234567` |
| 包含字母 | `123abc` |

### 自動化腳本
```python
# test_auth_2fa_006.py
async def test_invalid_2fa_format(page):
    await page.goto("/2fa-verify")
    
    # 測試 5 位數字
    await page.fill("#89hRJ input", "12345")
    await page.click("#uvYyE")
    await page.wait_for_selector(".validation-error")
    
    # 測試 7 位數字
    await page.fill("#89hRJ input", "1234567")
    await page.click("#uvYyE")
    await page.wait_for_selector(".validation-error")
    
    # 測試包含字母
    await page.fill("#89hRJ input", "123abc")
    await page.click("#uvYyE")
    await page.wait_for_selector(".validation-error")
```

### 備註
- 輸入框可設置 `type="tel"` 並添加 `pattern="\d{6}"` 進行前端限制
- 或通過 `inputmode="numeric"` 限制為數字輸入

---

## 測試執行摘要模板

| 執行日期 | 執行者 | 通過 | 失敗 | 跳過 | 備註 |
|---------|-------|------|------|------|------|
| - | - | - | - | - | - |
