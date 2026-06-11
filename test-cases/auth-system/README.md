# 認證系統測試用例

**系統編號:** AUTH  
**系統名稱:** 認證系統 (Authentication System)  
**優先級:** P0 (最高優先級)  
**最後更新日期:** 2026-06-11

---

## 系統概述

認證系統負責用戶登入、身份驗證和會話管理。包含兩個主要模塊：
1. **登入模塊** - 賬號密碼登入
2. **驗證模塊** - 電郵驗證碼（兩因素驗證）

---

## 測試用例列表

### 登入模塊 (LOGIN)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| [TC-AUTH-LOGIN-001](./login.md#tc-auth-login-001) | 使用有效憑證成功登入 | 高 | P1 | READY |
| [TC-AUTH-LOGIN-002](./login.md#tc-auth-login-002) | 使用無效賬號登入 | 高 | P2 | READY |
| [TC-AUTH-LOGIN-003](./login.md#tc-auth-login-003) | 使用無效密碼登入 | 高 | P2 | READY |
| [TC-AUTH-LOGIN-004](./login.md#tc-auth-login-004) | 空賬號登入驗證 | 中 | P2 | READY |
| [TC-AUTH-LOGIN-005](./login.md#tc-auth-login-005) | 空密碼登入驗證 | 中 | P2 | READY |
| [TC-AUTH-LOGIN-006](./login.md#tc-auth-login-006) | 登入頁面 UI 驗證 | 低 | P1 | READY |

### 兩因素驗證模塊 (2FA)

| 用例編號 | 用例名稱 | 優先級 | 執行階段 | 狀態 |
|---------|---------|--------|---------|------|
| [TC-AUTH-2FA-001](./2fa-verify.md#tc-auth-2fa-001) | 輸入正確驗證碼成功登入 | 高 | P1 | READY |
| [TC-AUTH-2FA-002](./2fa-verify.md#tc-auth-2fa-002) | 輸入錯誤驗證碼 | 高 | P2 | READY |
| [TC-AUTH-2FA-003](./2fa-verify.md#tc-auth-2fa-003) | 空驗證碼提交 | 中 | P2 | READY |
| [TC-AUTH-2FA-004](./2fa-verify.md#tc-auth-2fa-004) | 重新發送驗證碼 | 中 | P1 | READY |
| [TC-AUTH-2FA-005](./2fa-verify.md#tc-auth-2fa-005) | 驗證碼頁面 UI 驗證 | 低 | P1 | READY |
| [TC-AUTH-2FA-006](./2fa-verify.md#tc-auth-2fa-006) | 驗證碼格式驗證（非 6 位數字） | 中 | P2 | READY |

---

## 測試環境要求

1. 測試環境可訪問
2. 測試帳號已註冊並啟用
3. 電郵服務可訪問（用於獲取驗證碼）
4. 瀏覽器環境：Chrome/Chromium

---

## 測試數據

| 數據類型 | 測試值 | 說明 |
|---------|--------|------|
| 有效帳號 | `test@example.com` | 已啟用的測試帳號 |
| 有效密碼 | `Test1234!` | 符合密碼規範 |
| 無效帳號 | `invalid@example.com` | 不存在的帳號 |
| 錯誤密碼 | `Wrong1234!` | 錯誤的密碼 |

---

## 依賴關係

```
TC-AUTH-LOGIN-001 → 成功登入 → 可執行其他系統的 P1/P2 用例
TC-AUTH-2FA-001   → 完成驗證 → 進入主頁面
```

---

## 執行順序建議

1. 先執行所有 P1 核心功能用例
2. 再執行 P2 邊界異常用例
3. 最後執行 P3 清理用例（如適用）
