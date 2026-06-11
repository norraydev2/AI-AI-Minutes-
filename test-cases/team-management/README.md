# 團隊管理系統測試用例

**系統編號:** TEAM  
**系統名稱:** 團隊管理系統 (Team Management System)  
**優先級:** P1  
**最後更新日期:** 2026-06-11

---

## 系統概述

團隊管理系統提供團隊列表、團隊詳情和團隊充值記錄管理功能。

**包含模塊:**
1. 團隊列表 (Team List) - Figma 節點: `u1Z3o`
2. 團隊詳情 (Team Detail) - Figma 節點: `UMzLK`
3. 團隊充值紀錄 (Team Recharge) - Figma 節點: `nnAMn`

---

## 測試用例列表

### 團隊列表模塊 (TEAM-LIST)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| TC-TEAM-LIST-001 | 團隊列表頁面加載驗證 | 高 | P1 | READY |
| TC-TEAM-LIST-002 | 團隊名稱篩選功能驗證 | 高 | P1 | READY |
| TC-TEAM-LIST-003 | 團隊 ID 篩選功能驗證 | 高 | P1 | READY |
| TC-TEAM-LIST-004 | 團隊擁有人篩選功能驗證 | 中 | P1 | READY |
| TC-TEAM-LIST-005 | 篩選按鈕功能驗證 | 高 | P1 | READY |
| TC-TEAM-LIST-006 | 表格數據顯示驗證 | 高 | P1 | READY |
| TC-TEAM-LIST-007 | 分頁功能驗證 | 中 | P1 | READY |
| TC-TEAM-LIST-008 | 查看團隊詳情按鈕驗證 | 中 | P1 | READY |

### 團隊詳情模塊 (TEAM-DETAIL)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| TC-TEAM-DETAIL-001 | 團隊詳情頁面加載驗證 | 高 | P1 | READY |
| TC-TEAM-DETAIL-002 | 團隊基本資料顯示驗證 | 高 | P1 | READY |
| TC-TEAM-DETAIL-003 | 團隊成員表格顯示驗證 | 中 | P1 | READY |
| TC-TEAM-DETAIL-004 | 分頁籤切換功能驗證（團隊成員/充值記錄） | 中 | P1 | READY |

### 團隊充值紀錄模塊 (TEAM-RECHARGE)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| TC-TEAM-RECHARGE-001 | 團隊充值紀錄頁面加載驗證 | 高 | P1 | READY |
| TC-TEAM-RECHARGE-002 | 充值記錄表格顯示驗證 | 高 | P1 | READY |
| TC-TEAM-RECHARGE-003 | 返回按鈕功能驗證 | 低 | P1 | READY |

---

## 測試環境要求

1. 用戶已成功登入
2. 測試環境有團隊數據
3. 測試帳號有查看團隊管理的權限

---

## 測試依賴

- 依賴 `TC-AUTH-LOGIN-001` 和 `TC-AUTH-2FA-001` 成功執行完成
