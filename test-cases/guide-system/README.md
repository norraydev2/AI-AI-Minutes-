# 操作指南系統測試用例

**系統編號:** GUIDE  
**系統名稱:** 操作指南系統 (Guide System)  
**優先級:** P2  
**最後更新日期:** 2026-06-11

---

## 系統概述

操作指南系統提供操作手冊文章的管理功能，包括列表查看、新增、編輯和發佈管理。

**包含模塊:**
1. 操作指南列表 (Guide List) - Figma 節點: `1SK6U`
2. 新增操作指南 (Guide Create) - Figma 節點: `NMmnO`

---

## 測試用例列表

### 操作指南列表模塊 (GUIDE-LIST)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| TC-GUIDE-LIST-001 | 操作指南列表頁面加載驗證 | 高 | P1 | READY |
| TC-GUIDE-LIST-002 | 文章名稱篩選功能驗證 | 中 | P1 | READY |
| TC-GUIDE-LIST-003 | 文章內容篩選功能驗證 | 中 | P1 | READY |
| TC-GUIDE-LIST-004 | 發佈狀態下拉篩選驗證 | 中 | P1 | READY |
| TC-GUIDE-LIST-005 | 搜索按鈕功能驗證 | 高 | P1 | READY |
| TC-GUIDE-LIST-006 | 指南列表表格顯示驗證 | 高 | P1 | READY |
| TC-GUIDE-LIST-007 | 置頂 Toggle 切換功能驗證 | 中 | P2 | READY |
| TC-GUIDE-LIST-008 | 編輯按鈕功能驗證 | 中 | P1 | READY |
| TC-GUIDE-LIST-009 | 刪除按鈕功能驗證 | 中 | P2 | READY |
| TC-GUIDE-LIST-010 | 分頁功能驗證 | 中 | P1 | READY |

### 新增操作指南模塊 (GUIDE-CREATE)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| TC-GUIDE-CREATE-001 | 新增操作指南頁面加載驗證 | 高 | P1 | READY |
| TC-GUIDE-CREATE-002 | 表單欄位驗證 - 文章名稱必填 | 高 | P2 | READY |
| TC-GUIDE-CREATE-003 | 表單欄位驗證 - 文章內容必填 | 高 | P2 | READY |
| TC-GUIDE-CREATE-004 | 表單欄位驗證 - 發佈狀態必選 | 中 | P2 | READY |
| TC-GUIDE-CREATE-005 | 表單提交成功驗證 | 高 | P1 | READY |
| TC-GUIDE-CREATE-006 | 取消按鈕功能驗證 | 低 | P1 | READY |
| TC-GUIDE-CREATE-007 | 日期選擇器功能驗證 | 中 | P1 | READY |
| TC-GUIDE-CREATE-008 | 表單重置功能驗證 | 低 | P2 | READY |

---

## 測試環境要求

1. 用戶已成功登入
2. 測試帳號有管理操作指南的權限

---

## 測試依賴

- 依賴 `TC-AUTH-LOGIN-001` 和 `TC-AUTH-2FA-001` 成功執行完成
