# 新增操作指南模塊測試用例

**模塊名稱:** 新增操作指南 (Guide Create)  
**所屬系統:** 操作指南系統  
**Figma 節點:** `NMmnO`  
**最後更新日期:** 2026-06-11

---

## TC-GUIDE-CREATE-001: 新增操作指南頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 前置條件
- 從操作指南列表點擊「新增」按鈕
- 或直接導航至 `/guides/create`

### 預期結果
- URL 包含 `/guides/create` 或 `/guides/new`
- 麵包屑顯示「操作指南 / 新增操作指南」
- 表單卡片可見
- 所有表單欄位可見

### 自動化腳本
```python
# test_guide_create_001.py
async def test_guide_create_page_loads(page):
    await page.goto("/guides/create")
    await page.wait_for_load_state("networkidle")
    
    assert "/guides" in page.url and ("/create" in page.url or "/new" in page.url)
    
    # 驗證表單卡片存在
    form_card = await page.query_selector("#sXwdu")
    assert form_card is not None
    
    # 驗證標題
    title = await page.query_selector("#oaTnR")
    assert title is not None
    
    await page.screenshot(path="screenshots/guide_create_001_load.png")
```

---

## TC-GUIDE-CREATE-002: 表單欄位驗證 - 文章名稱必填

**優先級:** 高  
**類型:** 表單驗證  
**執行階段:** P2

### 測試步驟
1. 保持「文章名稱」為空
2. 點擊「保存」按鈕

### 預期結果
- 阻止表單提交
- 顯示驗證錯誤訊息
- 文章名稱輸入框獲得焦點或標紅

### 自動化腳本
```python
# test_guide_create_002.py
async def test_title_required(page):
    await page.goto("/guides/create")
    
    # 清空文章名稱（如果預設有值）
    await page.fill("#MnV9G input", "")
    
    # 點擊保存
    save_btn = await page.query_selector("#d2JV6")
    await save_btn.click()
    
    # 等待驗證錯誤
    await page.wait_for_selector("#MnV9G .validation-error, .error-message")
    
    # 驗證錯誤訊息顯示
    error = await page.query_selector("#MnV9G .validation-error")
    assert error is not None
    
    await page.screenshot(path="screenshots/guide_create_002_title_required.png")
```

---

## TC-GUIDE-CREATE-003: 表單欄位驗證 - 文章內容必填

**優先級:** 高  
**類型:** 表單驗證  
**執行階段:** P2

### 測試步驟
1. 填寫文章名稱
2. 保持「文章內容」為空
3. 點擊「保存」按鈕

### 預期結果
- 阻止表單提交
- 顯示驗證錯誤訊息

### 自動化腳本
```python
# test_guide_create_003.py
async def test_content_required(page):
    await page.goto("/guides/create")
    
    # 填寫文章名稱
    await page.fill("#MnV9G input", "測試文章")
    
    # 清空文章內容
    await page.fill("#JVc7b textarea", "")
    
    # 點擊保存
    save_btn = await page.query_selector("#d2JV6")
    await save_btn.click()
    
    # 等待驗證錯誤
    await page.wait_for_selector("#JVc7b .validation-error, .error-message")
    
    await page.screenshot(path="screenshots/guide_create_003_content_required.png")
```

---

## TC-GUIDE-CREATE-004: 表單欄位驗證 - 發佈狀態必選

**優先級:** 中  
**類型:** 表單驗證  
**執行階段:** P2

### 自動化腳本
```python
# test_guide_create_004.py
async def test_status_required(page):
    await page.goto("/guides/create")
    
    # 填寫必填欄位
    await page.fill("#MnV9G input", "測試文章")
    await page.fill("#JVc7b textarea", "測試內容")
    
    # 選擇空白的發佈狀態（如果可能）
    await page.click("#Zwgfn")
    
    # 點擊保存
    save_btn = await page.query_selector("#d2JV6")
    await save_btn.click()
    
    # 可能有驗證錯誤，或系統有默認值
    await page.wait_for_timeout(1000)
    
    await page.screenshot(path="screenshots/guide_create_004_status_validation.png")
```

---

## TC-GUIDE-CREATE-005: 表單提交成功驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 測試步驟
1. 填寫所有必填欄位
2. 點擊「保存」按鈕
3. 等待提交完成

### 預期結果
- 表單提交成功
- 顯示成功提示訊息
- 跳轉至操作指南列表頁
- 新文章出現在列表中

### 自動化腳本
```python
# test_guide_create_005.py
async def test_form_submit_success(page):
    await page.goto("/guides/create")
    
    # 填寫表單
    await page.fill("#MnV9G input", "測試文章-" + str(int(time.time())))
    await page.fill("#JVc7b textarea", "這是測試文章的內容")
    
    # 選擇發佈狀態
    await page.click("#Zwgfn")
    await page.click("text=已發佈")
    
    # 選擇日期
    await page.click("#OCMnQ")
    # 選擇今天（具體實現取決於日期組件）
    
    # 點擊保存
    save_btn = await page.query_selector("#d2JV6")
    await save_btn.click()
    
    # 等待跳轉
    await page.wait_for_load_state("networkidle")
    
    # 驗證跳轉至列表頁
    assert "/guides" in page.url
    
    # 驗證成功提示
    success_msg = await page.query_selector(".success-message, .toast-success")
    if success_msg:
        assert "成功" in await success_msg.inner_text()
    
    await page.screenshot(path="screenshots/guide_create_005_success.png")
```

---

## TC-GUIDE-CREATE-006: 取消按鈕功能驗證

**優先級:** 低  
**類型:** 功能測試  
**執行階段:** P1

### 測試步驟
1. 點擊「取消」按鈕

### 預期結果
- 不提交表單
- 跳轉至操作指南列表頁
- 已填寫的內容不保存

### 自動化腳本
```python
# test_guide_create_006.py
async def test_cancel_button(page):
    await page.goto("/guides/create")
    
    # 填寫一些內容
    await page.fill("#MnV9G input", "測試文章")
    
    # 點擊取消
    cancel_btn = await page.query_selector("#jGsQI")
    await cancel_btn.click()
    await page.wait_for_load_state("networkidle")
    
    # 驗證跳轉至列表頁
    assert "/guides" in page.url
    
    await page.screenshot(path="screenshots/guide_create_006_cancel.png")
```

---

## TC-GUIDE-CREATE-007: 日期選擇器功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 測試步驟
1. 點擊「生效日期」輸入框
2. 選擇一個日期

### 預期結果
- 日期選擇器彈出
- 選擇後日期顯示在輸入框中
- 格式為 YYYY-MM-DD

### 自動化腳本
```python
# test_guide_create_007.py
async def test_date_picker(page):
    await page.goto("/guides/create")
    
    # 點擊日期選擇器
    date_input = await page.query_selector("#OCMnQ")
    await date_input.click()
    
    # 等待日期面板出現
    date_panel = await page.wait_for_selector(".date-picker-panel, .ant-picker-panel", timeout=2000)
    if date_panel:
        # 選擇今天
        today_btn = await date_panel.query_selector(".ant-picker-today-btn")
        if today_btn:
            await today_btn.click()
        
        # 驗證日期已填寫
        date_text = await date_input.inner_text()
        assert re.match(r"\d{4}-\d{2}-\d{2}", date_text)
    
    await page.screenshot(path="screenshots/guide_create_007_date_picker.png")
```

---

## TC-GUIDE-CREATE-008: 表單重置功能驗證

**優先級:** 低  
**類型:** 功能測試  
**執行階段:** P2

### 測試步驟
1. 填寫部分表單內容
2. 點擊「取消」或刷新頁面
3. 驗證表單是否清空

### 自動化腳本
```python
# test_guide_create_008.py
async def test_form_reset(page):
    await page.goto("/guides/create")
    
    # 填寫表單
    await page.fill("#MnV9G input", "測試文章")
    await page.fill("#JVc7b textarea", "測試內容")
    
    # 刷新頁面
    await page.reload()
    await page.wait_for_load_state("networkidle")
    
    # 驗證表單已清空
    title_value = await page.input_value("#MnV9G input")
    content_value = await page.input_value("#JVc7b textarea")
    assert title_value == ""
    assert content_value == ""
    
    await page.screenshot(path="screenshots/guide_create_008_reset.png")
```

---

## 測試執行摘要模板

| 執行日期 | 執行者 | 通過 | 失敗 | 跳過 | 備註 |
|---------|-------|------|------|------|------|
| - | - | - | - | - | - |
