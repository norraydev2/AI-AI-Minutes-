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
| [TC-DASH-OVERVIEW-001](./overview.md#tc-dash-overview-001) | 儀表板頁面加載驗證 | 高 | P1 | READY |
| [TC-DASH-OVERVIEW-002](./overview.md#tc-dash-overview-002) | 四個指標卡片數據顯示驗證 | 高 | P1 | READY |
| [TC-DASH-OVERVIEW-003](./overview.md#tc-dash-overview-003) | 新增用戶柱狀圖顯示驗證 | 中 | P1 | READY |
| [TC-DASH-OVERVIEW-004](./overview.md#tc-dash-overview-004) | 活躍用戶柱狀圖顯示驗證 | 中 | P1 | READY |
| [TC-DASH-OVERVIEW-005](./overview.md#tc-dash-overview-005) | 充值金額折線圖顯示驗證 | 中 | P1 | READY |
| [TC-DASH-OVERVIEW-006](./overview.md#tc-dash-overview-006) | 轉錄分鐘數折線圖顯示驗證 | 中 | P1 | READY |
| [TC-DASH-OVERVIEW-007](./overview.md#tc-dash-overview-007) | 側邊欄導航功能驗證 | 高 | P1 | READY |
| [TC-DASH-OVERVIEW-008](./overview.md#tc-dash-overview-008) | 儀表板 UI 完整性驗證 | 低 | P1 | READY |

---

## 測試環境要求

1. 用戶已成功登入
2. 測試環境有足夠的歷史數據（至少 7 天）
3. 圖表渲染引擎正常運作

---

## 測試依賴

- 依賴 `TC-AUTH-LOGIN-001` 和 `TC-AUTH-2FA-001` 成功執行完成

---

## 執行順序建議

1. 先執行 TC-DASH-OVERVIEW-001（頁面加載）
2. 執行 TC-DASH-OVERVIEW-002（指標卡片）
3. 執行 TC-DASH-OVERVIEW-003~006（圖表測試）
4. 執行 TC-DASH-OVERVIEW-007（導航測試）
5. 最後執行 TC-DASH-OVERVIEW-008（UI 完整性）
