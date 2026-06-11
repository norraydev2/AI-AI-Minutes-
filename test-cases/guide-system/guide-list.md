# 操作指南列表模塊測試用例

**模塊名稱:** 操作指南列表 (Guide List)  
**所屬系統:** 操作指南系統  
**Figma 節點:** `1SK6U`  
**最後更新日期:** 2026-06-11

---

## TC-GUIDE-LIST-001: 操作指南列表頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 前置條件
- 用戶已成功登入
- 點擊側邊欄「操作指南」

### 預期結果
- URL 包含 `/guides`
- 側邊欄「操作指南」項高亮
- 篩選區域可見
- 表格區域可見
- 分頁組件可見

### 自動化腳本
```python
# test_guide_list_001.py
async def test_guide_list_page_loads(page):
    await page.click("#AQnMo")  # 側邊欄操作指南
    await page.wait_for_load_state("networkidle")
    
    assert "/guides" in page.url
    
    # 驗證篩選區存在
    filter_area = await page.query_selector("#JDkCS")
    assert filter_area is not None
    
    # 驗證表格存在
    table = await page.query_selector("#qPa1I")
    assert table is not None
    
    # 驗證分頁存在
    pagination = await page.query_selector("#XjkmV")
    assert pagination is not None
    
    await page.screenshot(path="screenshots/guide_list_001_load.png")
```

---

## TC-GUIDE-LIST-002: 文章名稱篩選功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 測試步驟
1. 在「文章名稱」輸入框輸入關鍵字
2. 點擊「搜索」按鈕

### 預期結果
- 表格只顯示文章名稱包含關鍵字的記錄

### 自動化腳本
```python
# test_guide_list_002.py
async def test_filter_by_title(page):
    await page.goto("/guides")
    
    await page.fill("#JDkCS input[name='title']", "快速")
    await page.click("#JDkCS button")
    await page.wait_for_load_state("networkidle")
    
    # 驗證所有顯示的文章名稱都包含「快速」
    title_cells = await page.query_selector_all("#qPa1I td:nth-child(1)")
    for cell in title_cells:
        text = await cell.inner_text()
        assert "快速" in text
    
    await page.screenshot(path="screenshots/guide_list_002_filter_title.png")
```

---

## TC-GUIDE-LIST-003: 文章內容篩選功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
# test_guide_list_003.py
async def test_filter_by_content(page):
    await page.goto("/guides")
    
    await page.fill("#JDkCS input[name='content']", "功能")
    await page.click("#JDkCS button")
    await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/guide_list_003_filter_content.png")
```

---

## TC-GUIDE-LIST-004: 發佈狀態下拉篩選驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
# test_guide_list_004.py
async def test_filter_by_status(page):
    await page.goto("/guides")
    
    # 點擊下拉框
    await page.click("#JDkCS select[name='status']")
    
    # 選擇「已發佈」
    await page.select_option("#JDkCS select[name='status']", "published")
    await page.click("#JDkCS button")
    await page.wait_for_load_state("networkidle")
    
    # 驗證所有顯示的文章狀態都是已發佈
    status_cells = await page.query_selector_all("#qPa1I .status-badge")
    for badge in status_cells:
        text = await badge.inner_text()
        assert "已發佈" in text
    
    await page.screenshot(path="screenshots/guide_list_004_filter_status.png")
```

---

## TC-GUIDE-LIST-005: 搜索按鈕功能驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
# test_guide_list_005.py
async def test_search_button(page):
    await page.goto("/guides")
    
    # 設置篩選條件
    await page.fill("#JDkCS input[name='title']", "快速")
    
    # 點擊搜索
    search_btn = await page.query_selector("#JDkCS button")
    await search_btn.click()
    await page.wait_for_load_state("networkidle")
    
    # 驗證按鈕恢復可用
    assert await search_btn.is_enabled()
    
    await page.screenshot(path="screenshots/guide_list_005_search.png")
```

---

## TC-GUIDE-LIST-006: 指南列表表格顯示驗證

**優先級:** 高  
**類型:** 數據驗證  
**執行階段:** P1

### 預期結果
| 欄位 | 說明 |
|------|------|
| 文章名稱 | 文字 |
| 文章內容 | 摘要文字 |
| 發佈日期 | YYYY-MM-DD |
| 發佈狀態 | 已發佈 (綠) / 草稿 (灰) |
| 置頂 | Toggle Switch |
| 操作 | 編輯/刪除/複製按鈕 |

### 自動化腳本
```python
# test_guide_list_006.py
async def test_guide_table(page):
    await page.goto("/guides")
    
    table = await page.query_selector("#qPa1I")
    assert table is not None
    
    # 驗證表頭
    headers = await page.query_selector_all("#vs6Ml div")
    expected = ["文章名稱", "文章內容", "發佈日期", "發佈狀態", "置頂", "操作"]
    assert len(headers) >= len(expected)
    
    # 驗證第一行數據
    first_row = await page.query_selector("#GOW7F")
    if first_row:
        cells = await first_row.query_selector_all("td, div[role='cell']")
        assert len(cells) >= 6
    
    await page.screenshot(path="screenshots/guide_list_006_table.png")
```

---

## TC-GUIDE-LIST-007: 置頂 Toggle 切換功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P2

### 自動化腳本
```python
# test_guide_list_007.py
async def test_pin_toggle(page):
    await page.goto("/guides")
    
    # 找到第一個 Toggle
    toggle = await page.query_selector("#3tVLE .toggle-switch")
    if toggle:
        initial_state = await toggle.evaluate("el => el.checked")
        await toggle.click()
        await page.wait_for_load_state("networkidle")
        
        # 驗證狀態變更
        new_state = await toggle.evaluate("el => el.checked")
        assert initial_state != new_state
    
    await page.screenshot(path="screenshots/guide_list_007_toggle.png")
```

---

## TC-GUIDE-LIST-008: 編輯按鈕功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
# test_guide_list_008.py
async def test_edit_button(page):
    await page.goto("/guides")
    
    # 找到第一個編輯按鈕
    edit_btn = await page.query_selector("#CnGtM button.edit-btn")
    if edit_btn:
        await edit_btn.click()
        await page.wait_for_load_state("networkidle")
        
        # 驗證跳轉至編輯頁
        assert "/guides/" in page.url and "/edit" in page.url
    
    await page.screenshot(path="screenshots/guide_list_008_edit.png")
```

---

## TC-GUIDE-LIST-009: 刪除按鈕功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P2

### 自動化腳本
```python
# test_guide_list_009.py
async def test_delete_button(page):
    await page.goto("/guides")
    
    # 找到第一個刪除按鈕
    delete_btn = await page.query_selector("#CnGtM button.delete-btn")
    if delete_btn:
        # 點擊刪除
        await delete_btn.click()
        
        # 等待確認彈窗
        confirm_btn = await page.wait_for_selector("text=確認刪除", timeout=2000)
        if confirm_btn:
            await confirm_btn.click()
            await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/guide_list_009_delete.png")
```

---

## TC-GUIDE-LIST-010: 分頁功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 自動化腳本
```python
# test_guide_list_010.py
async def test_pagination(page):
    await page.goto("/guides")
    
    # 驗證總記錄
    total = await page.query_selector("#aDGrl")
    if total:
        text = await total.inner_text()
        assert "共" in text and "條" in text
    
    # 點擊下一頁
    next_btn = await page.query_selector("#et2iW")
    if next_btn and await next_btn.is_enabled():
        await next_btn.click()
        await page.wait_for_load_state("networkidle")
    
    await page.screenshot(path="screenshots/guide_list_010_pagination.png")
```
