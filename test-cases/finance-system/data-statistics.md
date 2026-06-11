# 數據統計模塊測試用例

**模塊名稱:** 數據統計 (Data Statistics)  
**所屬系統:** 財務數據系統  
**Figma 節點:** `IkSFY`  
**最後更新日期:** 2026-06-11

---

## TC-FIN-STATS-001: 數據統計頁面加載驗證

**優先級:** 高  
**類型:** 功能測試  
**執行階段:** P1

### 前置條件
- 用戶已成功登入
- 點擊側邊欄「財務數據」→「數據統計」

### 預期結果
- URL 包含 `/finance/statistics`
- 側邊欄「數據統計」項高亮
- 三個收入指標卡片可見
- 收入統計圖表可見
- 套餐銷售圖表可見

### 自動化腳本
```python
async def test_finance_stats_loads(page):
    await page.click("#91ej2")  # 財務數據 → 數據統計
    await page.wait_for_load_state("networkidle")
    
    assert "/finance" in page.url
    assert await page.query_selector("#1kAbe")  # 頂部指標行
    assert await page.query_selector("#yRrEC")  # 收入統計卡片
    
    await page.screenshot(path="screenshots/fin_stats_001_load.png")
```

---

## TC-FIN-STATS-002: 三個收入指標卡片顯示驗證

**優先級:** 高  
**類型:** 數據驗證  
**執行階段:** P1

### 預期結果
| 卡片 | 標題 | 格式 |
|------|------|------|
| 總收入 | HK $X,XXX,XXX | 環比百分比 |
| 個人用戶充值收入 | HK $XXX,XXX | 環比百分比 |
| 團隊用戶充值收入 | HK $XXX,XXX | 環比百分比 |

### 自動化腳本
```python
async def test_revenue_cards(page):
    await page.goto("/finance/statistics")
    
    # 驗證總收入
    total_card = await page.query_selector("#YD7jq")
    assert total_card is not None
    
    # 驗證個人收入
    individual_card = await page.query_selector("#yrBC6")
    assert individual_card is not None
    
    # 驗證團隊收入
    team_card = await page.query_selector("#tVJLl")
    assert team_card is not None
    
    await page.screenshot(path="screenshots/fin_stats_002_cards.png")
```

---

## TC-FIN-STATS-003: 收入統計趨勢圖顯示驗證

**優先級:** 中  
**類型:** 圖表測試  
**執行階段:** P1

### 預期結果
- 圖表標題：「收入統計」
- 圖表區域存在（SVG 或 Canvas）
- 顯示趨勢線

### 自動化腳本
```python
async def test_revenue_trend_chart(page):
    await page.goto("/finance/statistics")
    
    chart_wrap = await page.query_selector("#aOGTH")
    assert chart_wrap is not None
    
    # 驗證圖表元素
    chart = await page.query_selector("#aOGTH svg, #aOGTH canvas")
    assert chart is not None
    
    await page.screenshot(path="screenshots/fin_stats_003_trend_chart.png")
```

---

## TC-FIN-STATS-004: 套餐銷售占比圓餅圖顯示驗證

**優先級:** 中  
**類型:** 圖表測試  
**執行階段:** P1

### 預期結果
- 圖表標題：「套餐銷售與收入占比」
- 圓餅圖顯示三種套餐占比
- 圖例顯示 Basic/Pro/Business 百分比

### 自動化腳本
```python
async def test_pie_chart(page):
    await page.goto("/finance/statistics")
    
    pie_chart = await page.query_selector("#ZHIJ5")
    assert pie_chart is not None
    
    # 驗證圖例
    assert await page.query_selector("text=Basic")
    assert await page.query_selector("text=Pro")
    assert await page.query_selector("text=Business")
    
    await page.screenshot(path="screenshots/fin_stats_004_pie_chart.png")
```

---

## TC-FIN-STATS-005: 套餐銷售趨勢折線圖顯示驗證

**優先級:** 中  
**類型:** 圖表測試  
**執行階段:** P1

### 自動化腳本
```python
async def test_package_trend_chart(page):
    await page.goto("/finance/statistics")
    
    line_chart = await page.query_selector("#kCekq")
    assert line_chart is not None
    
    await page.screenshot(path="screenshots/fin_stats_005_line_chart.png")
```

---

## TC-FIN-STATS-006: Basic 套餐數據卡片顯示驗證

**優先級:** 中  
**類型:** 數據驗證  
**執行階段:** P1

### 預期結果
- 卡片標題：「Basic 套餐」
- 顯示銷售套數
- 顯示銷售金額
- 柱狀圖和折線圖可見

### 自動化腳本
```python
async def test_basic_package_card(page):
    await page.goto("/finance/statistics")
    
    basic_card = await page.query_selector("#tZ695")
    assert basic_card is not None
    
    await page.screenshot(path="screenshots/fin_stats_006_basic.png")
```

---

## TC-FIN-STATS-007: Pro 套餐數據卡片顯示驗證

**優先級:** 中  
**類型:** 數據驗證  
**執行階段:** P1

### 預期結果
- 卡片背景：淺藍色 `#E6F4FF`
- 顯示銷售套數、銷售金額
- 圖表可見

### 自動化腳本
```python
async def test_pro_package_card(page):
    await page.goto("/finance/statistics")
    
    pro_card = await page.query_selector("#UfdI8")
    assert pro_card is not None
    
    # 驗證藍色邊框
    style = await pro_card.evaluate("el => el.style.borderColor")
    assert "#91CAFF" in style or "#E6F4FF" in style
    
    await page.screenshot(path="screenshots/fin_stats_007_pro.png")
```

---

## TC-FIN-STATS-008: Business 套餐數據卡片顯示驗證

**優先級:** 中  
**類型:** 數據驗證  
**執行階段:** P1

### 自動化腳本
```python
async def test_business_package_card(page):
    await page.goto("/finance/statistics")
    
    business_card = await page.query_selector("#g3uqZ")
    assert business_card is not None
    
    await page.screenshot(path="screenshots/fin_stats_008_business.png")
```

---

## TC-FIN-STATS-009: 日期範圍篩選功能驗證

**優先級:** 中  
**類型:** 功能測試  
**執行階段:** P1

### 測試步驟
1. 點擊日期範圍選擇器
2. 選擇開始日期和結束日期
3. 點擊查詢或自動刷新

### 預期結果
- 日期選擇器彈出
- 選擇後圖表數據更新
- URL 包含日期參數

### 自動化腳本
```python
async def test_date_filter(page):
    await page.goto("/finance/statistics")
    
    # 點擊日期選擇器
    date_filter = await page.query_selector("#xl0md")
    if date_filter:
        await date_filter.click()
        # 選擇日期邏輯（需根據實際組件實現）
    
    await page.screenshot(path="screenshots/fin_stats_009_date_filter.png")
```

---

## TC-FIN-STATS-010: 側邊欄財務導航展開/收合驗證

**優先級:** 低  
**類型:** 功能測試  
**執行階段:** P1

### 測試步驟
1. 點擊「財務數據」導航項
2. 驗證子選單展開
3. 點擊子選單項目

### 預期結果
- 子選單展開顯示（數據統計、充值紀錄、團隊充值統計、個人充值統計）
- 當前选中項高亮

### 自動化腳本
```python
async def test_finance_submenu(page):
    await page.goto("/finance/statistics")
    
    # 驗證子選單存在
    submenu = await page.query_selector("#MUOKx")
    assert submenu is not None
    
    # 驗證子選單項目
    items = await submenu.query_selector_all("div")
    assert len(items) >= 4  # 至少 4 個子項目
    
    await page.screenshot(path="screenshots/fin_stats_010_submenu.png")
```
