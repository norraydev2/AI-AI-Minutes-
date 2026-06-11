# 用戶管理系統測試用例

**系統編號:** USER  
**系統名稱:** 用戶管理系統 (User Management System)  
**優先級:** P1  
**最後更新日期:** 2026-06-11

---

## 系統概述

用戶管理系統提供用戶列表查看、篩選、詳情查看和賬號狀態管理功能。

**包含模塊:**
1. 用戶列表 (User List) - Figma 節點: `NPfOA`
2. 用戶詳情 (User Profile Detail) - Figma 節點: `yvijQ`

---

## 測試用例列表

### 用戶列表模塊 (USER-LIST)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| [TC-USER-LIST-001](./user-list.md#tc-user-list-001) | 用戶列表頁面加載驗證 | 高 | P1 | READY |
| [TC-USER-LIST-002](./user-list.md#tc-user-list-002) | 用戶名稱篩選功能驗證 | 高 | P1 | READY |
| [TC-USER-LIST-003](./user-list.md#tc-user-list-003) | 電郵地址篩選功能驗證 | 高 | P1 | READY |
| [TC-USER-LIST-004](./user-list.md#tc-user-list-004) | 使用模式下拉篩選驗證 | 中 | P1 | READY |
| [TC-USER-LIST-005](./user-list.md#tc-user-list-005) | 賬號狀態下拉篩選驗證 | 中 | P1 | READY |
| [TC-USER-LIST-006](./user-list.md#tc-user-list-006) | 搜索按鈕功能驗證 | 高 | P1 | READY |
| [TC-USER-LIST-007](./user-list.md#tc-user-list-007) | 表格數據顯示驗證 | 高 | P1 | READY |
| [TC-USER-LIST-008](./user-list.md#tc-user-list-008) | 分頁功能驗證 | 中 | P1 | READY |
| [TC-USER-LIST-009](./user-list.md#tc-user-list-009) | 賬號狀態 Toggle 切換驗證 | 高 | P2 | READY |
| [TC-USER-LIST-010](./user-list.md#tc-user-list-010) | 查看用戶詳情按鈕驗證 | 中 | P1 | READY |

### 用戶詳情模塊 (USER-DETAIL)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| [TC-USER-DETAIL-001](./user-detail.md#tc-user-detail-001) | 用戶詳情頁面加載驗證 | 高 | P1 | READY |
| [TC-USER-DETAIL-002](./user-detail.md#tc-user-detail-002) | 用戶基本資料顯示驗證 | 高 | P1 | READY |
| [TC-USER-DETAIL-003](./user-detail.md#tc-user-detail-003) | 充值記錄表格顯示驗證 | 中 | P1 | READY |
| [TC-USER-DETAIL-004](./user-detail.md#tc-user-detail-004) | 返回按鈕功能驗證 | 低 | P1 | READY |

---

## 測試環境要求

1. 用戶已成功登入
2. 測試環境有用戶數據
3. 測試帳號有查看用戶管理頁面的權限

---

## 測試依賴

- 依賴 `TC-AUTH-LOGIN-001` 和 `TC-AUTH-2FA-001` 成功執行完成
