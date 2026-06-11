# 財務數據系統測試用例

**系統編號:** FIN  
**系統名稱:** 財務數據系統 (Finance System)  
**優先級:** P2  
**最後更新日期:** 2026-06-11

---

## 系統概述

財務數據系統提供收入統計、充值記錄和團隊/個人充值數據分析功能。

**包含模塊:**
1. 數據統計 (Data Statistics) - Figma 節點: `IkSFY`
2. 充值紀錄 (Recharge Records) - Figma 節點: `5kvjX`
3. 團隊充值統計 (Team Stats) - Figma 節點: `yEhir`
4. 個人充值統計 (Individual Stats) - Figma 節點: `EH2Cx`

---

## 測試用例列表

### 數據統計模塊 (FIN-STATS)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| TC-FIN-STATS-001 | 數據統計頁面加載驗證 | 高 | P1 | READY |
| TC-FIN-STATS-002 | 三個收入指標卡片顯示驗證 | 高 | P1 | READY |
| TC-FIN-STATS-003 | 收入統計趨勢圖顯示驗證 | 中 | P1 | READY |
| TC-FIN-STATS-004 | 套餐銷售占比圓餅圖顯示驗證 | 中 | P1 | READY |
| TC-FIN-STATS-005 | 套餐銷售趨勢折線圖顯示驗證 | 中 | P1 | READY |
| TC-FIN-STATS-006 | Basic 套餐數據卡片顯示驗證 | 中 | P1 | READY |
| TC-FIN-STATS-007 | Pro 套餐數據卡片顯示驗證 | 中 | P1 | READY |
| TC-FIN-STATS-008 | Business 套餐數據卡片顯示驗證 | 中 | P1 | READY |
| TC-FIN-STATS-009 | 日期範圍篩選功能驗證 | 中 | P1 | READY |
| TC-FIN-STATS-010 | 側邊欄財務導航展開/收合驗證 | 低 | P1 | READY |

### 充值紀錄模塊 (FIN-RECORDS)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| TC-FIN-RECORDS-001 | 充值紀錄頁面加載驗證 | 高 | P1 | READY |
| TC-FIN-RECORDS-002 | 訂單編號篩選功能驗證 | 中 | P1 | READY |
| TC-FIN-RECORDS-003 | 電郵地址篩選功能驗證 | 中 | P1 | READY |
| TC-FIN-RECORDS-004 | 充值金額範圍篩選驗證 | 中 | P1 | READY |
| TC-FIN-RECORDS-005 | 支付方式下拉篩選驗證 | 中 | P1 | READY |
| TC-FIN-RECORDS-006 | 查詢按鈕功能驗證 | 高 | P1 | READY |
| TC-FIN-RECORDS-007 | 充值紀錄表格顯示驗證 | 高 | P1 | READY |
| TC-FIN-RECORDS-008 | 分頁功能驗證 | 中 | P1 | READY |

### 團隊充值統計模塊 (FIN-TEAM)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| TC-FIN-TEAM-001 | 團隊充值統計頁面加載驗證 | 高 | P1 | READY |
| TC-FIN-TEAM-002 | 團隊 ID 篩選功能驗證 | 中 | P1 | READY |
| TC-FIN-TEAM-003 | 團隊名稱篩選功能驗證 | 中 | P1 | READY |
| TC-FIN-TEAM-004 | 充值日期範圍篩選驗證 | 中 | P1 | READY |
| TC-FIN-TEAM-005 | 團隊充值統計表格顯示驗證 | 高 | P1 | READY |
| TC-FIN-TEAM-006 | 搜尋年齡 Checkbox 功能驗證 | 低 | P2 | READY |

### 個人充值統計模塊 (FIN-INDIVIDUAL)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| TC-FIN-INDIVIDUAL-001 | 個人充值統計頁面加載驗證 | 高 | P1 | READY |
| TC-FIN-INDIVIDUAL-002 | 用戶名稱篩選功能驗證 | 中 | P1 | READY |
| TC-FIN-INDIVIDUAL-003 | 電郵地址篩選功能驗證 | 中 | P1 | READY |
| TC-FIN-INDIVIDUAL-004 | 個人充值統計表格顯示驗證 | 高 | P1 | READY |

---

## 測試環境要求

1. 用戶已成功登入
2. 測試環境有財務數據
3. 測試帳號有查看財務數據的權限

---

## 測試依賴

- 依賴 `TC-AUTH-LOGIN-001` 和 `TC-AUTH-2FA-001` 成功執行完成
