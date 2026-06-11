# 儀表板系統測試用例

**系統編號:** DASH  
**系統名稱:** 儀表板系統 (Dashboard System)  
**優先級:** P1  
**最後更新日期:** 2026-06-11

---

## 系統概述

儀表板系統提供後台管理首頁，顯示關鍵業務指標和數據可視化圖表。

**Figma 節點:** `bi8Au` (Dashboard Overview)

---

## 測試用例列表

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| [TC-DASH-OVERVIEW-001](#tc-dash-overview-001) | 儀表板頁面加載驗證 | 高 | P1 | READY |
| [TC-DASH-OVERVIEW-002](#tc-dash-overview-002) | 四個指標卡片數據顯示驗證 | 高 | P1 | READY |
| [TC-DASH-OVERVIEW-003](#tc-dash-overview-003) | 新增用戶柱狀圖顯示驗證 | 中 | P1 | READY |
| [TC-DASH-OVERVIEW-004](#tc-dash-overview-004) | 活躍用戶柱狀圖顯示驗證 | 中 | P1 | READY |
| [TC-DASH-OVERVIEW-005](#tc-dash-overview-005) | 充值金額折線圖顯示驗證 | 中 | P1 | READY |
| [TC-DASH-OVERVIEW-006](#tc-dash-overview-006) | 轉錄分鐘數折線圖顯示驗證 | 中 | P1 | READY |
| [TC-DASH-OVERVIEW-007](#tc-dash-overview-007) | 側邊欄導航功能驗證 | 高 | P1 | READY |
| [TC-DASH-OVERVIEW-008](#tc-dash-overview-008) | 儀表板 UI 完整性驗證 | 低 | P1 | READY |

---

## 測試環境要求

1. 用戶已成功登入
2. 測試環境有足夠的歷史數據（至少 7 天）
3. 圖表渲染引擎正常運作

---

## 測試依賴

- 依賴 `TC-AUTH-LOGIN-001` 和 `TC-AUTH-2FA-001` 成功執行完成
- 登入後自動跳轉至儀表板頁面

---

## TC-DASH-OVERVIEW-001: 儀表板頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶已成功登入
- 處於儀表板頁面

### 測試步驟
1. 從登入頁面成功登入後自動跳轉
2. 或直接導航至 `/dashboard`
3. 等待頁面完全加載

### 預期結果
- 頁面 URL 為 `/dashboard` 或 `/`
- 頁面標題包含「AI Minutes - 主頁」
- 側邊欄導航可見
- 頂部導航欄可見
- 四個指標卡片可見
- 四個圖表卡片可見
- 無加載中狀態或錯誤訊息

### 自動化腳本
```python
# test_dash_overview_001.py
async def test_dashboard_loads(page):
    await page.goto("/dashboard")
    
    # 驗證 URL
    assert "/dashboard" in page.url or page.url.endswith("/")
    
    # 驗證頁面標題
    title = await page.title()
    assert "主頁" in title or "Dashboard" in title
    
    # 驗證側邊欄存在
    sidebar = await page.query_selector("#olLI5")
    assert sidebar is not None
    
    # 驗證主內容區存在
    main_content = await page.query_selector("#K4bQD")
    assert main_content is not None
    
    # 驗證四個指標卡片存在
    metric_cards = await page.query_selector_all("#2vPOU > div")
    assert len(metric_cards) >= 4
    
    # 驗證圖表區域存在
    charts = await page.query_selector("#TqadL")
    assert charts is not None
    
    # 截圖驗證
    await page.screenshot(path="screenshots/dash_001_full.png")
```

### 備註
- 頁面加載時間應小於 3 秒

---

## TC-DASH-OVERVIEW-002: 四個指標卡片數據顯示驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 儀表板頁面已完全加載

### 測試步驟
1. 驗證「近 7 日新增用戶數量」卡片
2. 驗證「近 7 日活躍用戶數量」卡片
3. 驗證「近 7 日充值金額」卡片
4. 驗證「近 7 日轉錄分鐘數」卡片

### 預期結果
| 卡片 | 標題 | 數值格式 | 顏色 |
|------|------|---------|------|
| 卡片 1 | 近 7 日新增用戶數量 | 數字（如 1,286） | 藍色 `#1677ff` |
| 卡片 2 | 近 7 日活躍用戶數量 | 數字（如 5,742） | 綠色 `#237804` |
| 卡片 3 | 近 7 日充值金額 | 貨幣格式（如 $93,820） | 橙色 `#fa8c16` |
| 卡片 4 | 近 7 日轉錄分鐘數 | 數字（如 48,560） | 紫色 `#722ED1` |

### 自動化腳本
```python
# test_dash_overview_002.py
async def test_metric_cards_display(page):
    await page.goto("/dashboard")
    await page.wait_for_selector("#2vPOU")
    
    # 卡片 1: 新增用戶
    card1_title = await page.query_selector("#eouAp #Aa8jP")
    card1_value = await page.query_selector("#eouAp #JfmER")
    assert await card1_title.inner_text() == "近 7 日新增用戶數量"
    assert re.match(r"[\d,]+", await card1_value.inner_text())
    
    # 卡片 2: 活躍用戶
    card2_title = await page.query_selector("#c2VCc #TKFLq")
    card2_value = await page.query_selector("#c2VCc #Kd1dh")
    assert await card2_title.inner_text() == "近 7 日活躍用戶數量"
    
    # 卡片 3: 充值金額
    card3_title = await page.query_selector("#fSc2c #OL6QJ")
    card3_value = await page.query_selector("#fSc2c #IM1jL")
    assert await card3_title.inner_text() == "近 7 日充值金額"
    
    # 卡片 4: 轉錄分鐘數
    card4_title = await page.query_selector("#aOmyG #u1NW4")
    card4_value = await page.query_selector("#aOmyG #inFya")
    assert await card4_title.inner_text() == "近 7 日轉錄分鐘數"
    
    # 截圖
    await page.screenshot(path="screenshots/dash_002_metrics.png", clip={"x": 0, "y": 0, "width": 1440, "height": 200})
```

### 備註
- 數值應為實時數據，非硬編碼
- 數字應有千分位分隔符

---

## TC-DASH-OVERVIEW-003: 新增用戶柱狀圖顯示驗證

**優先級:** 中  
**類型:* 圖表測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 儀表板頁面已完全加載
- 有至少 7 天的用戶數據

### 測試步驟
1. 定位「近 7 日新增用戶數量」柱狀圖
2. 驗證圖表標題
3. 驗證 X 軸標籤（日期）
4. 驗證 Y 軸標籤（數量）
5. 驗證柱狀圖渲染

### 預期結果
- 圖表標題：「近 7 日新增用戶數量（柱狀圖）」
- X 軸顯示 7 個日期標籤
- Y 軸顯示數量刻度
- 7 根柱子，顏色從淺藍到深藍漸層
- 柱子高度與數值成正比

### 自動化腳本
```python
# test_dash_overview_003.py
async def test_new_user_chart(page):
    await page.goto("/dashboard")
    
    # 驗證圖表容器存在
    chart_card = await page.query_selector("#80JiT")
    assert chart_card is not None
    
    # 驗證圖表標題
    chart_title = await page.query_selector("#80JiT #card1K")
    assert "新增用戶" in await chart_title.inner_text()
    
    # 驗證圖表區域存在（SVG 或 Canvas）
    chart_area = await page.query_selector("#80JiT svg, #80JiT canvas")
    assert chart_area is not None
    
    # 截圖驗證
    await page.screenshot(path="screenshots/dash_003_new_users_chart.png")
```

### 備註
- 圖表可能使用 SVG 或 Canvas 渲染
- 需視覺驗證柱狀圖的正確性

---

## TC-DASH-OVERVIEW-004: 活躍用戶柱狀圖顯示驗證

**優先級:** 中  
**類型:** 圖表測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 儀表板頁面已完全加載

### 測試步驟
1. 定位「近 7 日活躍用戶數量」柱狀圖
2. 驗證圖表標題
3. 驗證圖表渲染

### 預期結果
- 圖表標題：「近 7 日活躍用戶數量（柱狀圖）」
- 柱子顏色從淺綠到深綠漸層
- 其他同 TC-DASH-OVERVIEW-003

### 自動化腳本
```python
# test_dash_overview_004.py
async def test_active_user_chart(page):
    await page.goto("/dashboard")
    
    chart_card = await page.query_selector("#W6QkR")
    assert chart_card is not None
    
    chart_title = await page.query_selector("#W6QkR #card2K")
    assert "活躍用戶" in await chart_title.inner_text()
    
    await page.screenshot(path="screenshots/dash_004_active_users_chart.png")
```

---

## TC-DASH-OVERVIEW-005: 充值金額折線圖顯示驗證

**優先級:** 中  
**類型:** 圖表測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 儀表板頁面已完全加載

### 測試步驟
1. 定位「近 7 日充值金額」折線圖
2. 驗證圖表標題
3. 驗證折線渲染

### 預期結果
- 圖表標題：「近 7 日充值金額（折線圖）」
- 折線顏色為橙色
- X 軸顯示 7 個日期
- Y 軸顯示金額刻度

### 自動化腳本
```python
# test_dash_overview_005.py
async def test_revenue_chart(page):
    await page.goto("/dashboard")
    
    chart_card = await page.query_selector("#Hr7qi")
    assert chart_card is not None
    
    chart_title = await page.query_selector("#Hr7qi #card3K")
    assert "充值金額" in await chart_title.inner_text()
    
    await page.screenshot(path="screenshots/dash_005_revenue_chart.png")
```

---

## TC-DASH-OVERVIEW-006: 轉錄分鐘數折線圖顯示驗證

**優先級:** 中  
**類型:** 圖表測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 儀表板頁面已完全加載

### 測試步驟
1. 定位「近 7 日轉錄分鐘數」折線圖
2. 驗證圖表標題
3. 驗證折線渲染

### 預期結果
- 圖表標題：「近 7 日轉錄分鐘數（折線圖）」
- 折線顏色為紫色
- X 軸顯示 7 個日期
- Y 軸顯示分鐘數刻度

### 自動化腳本
```python
# test_dash_overview_006.py
async def test_transcription_minutes_chart(page):
    await page.goto("/dashboard")
    
    chart_card = await page.query_selector("#GAVlE")
    assert chart_card is not None
    
    chart_title = await page.query_selector("#GAVlE #card4K")
    assert "轉錄分鐘數" in await chart_title.inner_text()
    
    await page.screenshot(path="screenshots/dash_006_minutes_chart.png")
```

---

## TC-DASH-OVERVIEW-007: 側邊欄導航功能驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1 - 核心功能

### 前置條件
- 用戶已登入儀表板頁面

### 測試步驟
1. 驗證側邊欄所有導航項可見
2. 點擊「主頁」（當前頁）
3. 點擊「用戶管理」
4. 點擊「團隊管理」
5. 點擊「財務數據」
6. 點擊「操作指南」

### 預期結果
| 導航項 | 點擊後跳轉 |
|--------|-----------|
| 主頁 | `/dashboard`（當前頁，應高亮） |
| 用戶管理 | `/users` |
| 團隊管理 | `/teams` |
| 財務數據 | `/finance`（或展開子選單） |
| 操作指南 | `/guides` |

### 自動化腳本
```python
# test_dash_overview_007.py
async def test_sidebar_navigation(page):
    await page.goto("/dashboard")
    
    # 驗證側邊欄存在
    sidebar = await page.query_selector("#EqKdc")
    assert sidebar is not None
    
    # 驗證各導航項
    nav_items = {
        "主頁": "#QP1RH",
        "用戶管理": "#08eVO",
        "團隊管理": "#2aNq6",
        "財務數據": "#nawmL",
        "操作指南": "#EaU1w"
    }
    
    for name, selector in nav_items.items():
        nav_item = await page.query_selector(selector)
        assert nav_item is not None, f"{name} 導航項不存在"
        text = await nav_item.inner_text()
        assert name in text, f"{name} 文字不正確"
    
    # 驗證當前頁高亮
    active_nav = await page.query_selector("#QP1RH")
    assert "#F0F5FF" in await active_nav.evaluate("el => el.style.backgroundColor")
    
    # 測試跳轉
    await page.click("#08eVO")
    await page.wait_for_url("**/users*")
    assert "/users" in page.url
```

### 備註
- 「財務數據」可能有展開的子選單

---

## TC-DASH-OVERVIEW-008: 儀表板 UI 完整性驗證

**優先級:** 低  
**類型:* UI 測試  
**執行階段:* P1 - 核心功能

### 前置條件
- 儀表板頁面已完全加載

### 測試步驟
1. 截取完整頁面截圖
2. 驗證所有 UI 元素位置和樣式

### 預期結果
| 元素 | 預期位置/樣式 |
|------|--------------|
| Logo | 左上角，28x28px 藍色框 + 「AI Minutes」文字 |
| 側邊欄 | 左側，240px 寬，白色背景 |
| 頂部導航 | 頂部，64px 高，白色背景 |
| 指標卡片行 | 4 個卡片橫向排列，間距 14px |
| 圖表卡片 | 2x2 網格佈局 |

### 自動化腳本
```python
# test_dash_overview_008.py
async def test_dashboard_ui_complete(page):
    await page.goto("/dashboard")
    await page.wait_for_load_state("networkidle")
    
    # 全頁截圖
    await page.screenshot(path="screenshots/dash_008_full_page.png", full_page=True)
    
    # 驗證 Logo
    logo_box = await page.query_selector("#C4B4a")
    assert logo_box is not None
    
    logo_text = await page.query_selector("#tpfL2")
    assert await logo_text.inner_text() == "AI Minutes"
    
    # 驗證側邊欄寬度
    sidebar = await page.query_selector("#olLI5")
    sidebar_width = await sidebar.evaluate("el => el.offsetWidth")
    assert sidebar_width == 240
    
    # 驗證指標卡片行
    metric_row = await page.query_selector("#2vPOU")
    cards = await metric_row.query_selector_all("> div")
    assert len(cards) == 4
```

---

## 測試執行摘要模板

| 執行日期 | 執行者 | 通過 | 失敗 | 跳過 | 備註 |
|---------|-------|------|------|------|------|
| - | - | - | - | - | - |
