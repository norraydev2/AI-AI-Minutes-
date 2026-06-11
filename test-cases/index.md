# AI Minutes Web 測試用例索引

**專案名稱:** AI Minutes Web 後台管理系統  
**設計版本:** Figma AI Minutes.pen  
**測試用例版本:** v1.0  
**最後更新日期:** 2026-06-11

---

## 測試系統總覽

| 系統編號 | 系統名稱 | 模塊數 | 測試用例數 | 優先級 |
|---------|---------|-------|-----------|--------|
| AUTH | 認證系統 | 2 | 12 | P0 |
| DASH | 儀表板系統 | 1 | 8 | P1 |
| USER | 用戶管理系統 | 2 | 15 | P1 |
| TEAM | 團隊管理系統 | 3 | 18 | P1 |
| FIN | 財務數據系統 | 4 | 20 | P2 |
| GUIDE | 操作指南系統 | 2 | 10 | P2 |
| **總計** | - | **14** | **83** | - |

---

## 目錄結構

```
test-cases/
├── index.md                      # 本索引文件
├── auth-system/
│   ├── README.md                 # 系統說明
│   ├── login.md                  # 登入模塊測試用例
│   └── 2fa-verify.md             # 兩因素驗證測試用例
├── dashboard-system/
│   ├── README.md
│   └── overview.md               # 儀表板總覽測試用例
├── user-management/
│   ├── README.md
│   ├── user-list.md              # 用戶列表測試用例
│   └── user-detail.md            # 用戶詳情測試用例
├── team-management/
│   ├── README.md
│   ├── team-list.md              # 團隊列表測試用例
│   ├── team-detail.md            # 團隊詳情測試用例
│   └── team-recharge.md          # 團隊充值紀錄測試用例
├── finance-system/
│   ├── README.md
│   ├── data-statistics.md        # 數據統計測試用例
│   ├── recharge-records.md       # 充值紀錄測試用例
│   ├── team-stats.md             # 團隊充值統計測試用例
│   └── individual-stats.md       # 個人充值統計測試用例
└── guide-system/
    ├── README.md
    ├── guide-list.md             # 操作指南列表測試用例
    └── guide-create.md           # 新增操作指南測試用例
```

---

## 測試用例編號規則

格式：`TC-[系統縮寫]-[模塊縮寫]-[序號]`

例如：
- `TC-AUTH-LOGIN-001`: 認證系統 - 登入模塊 - 第 1 號用例
- `TC-USER-LIST-005`: 用戶管理 - 用戶列表 - 第 5 號用例

---

## 測試階段定義

| 階段 | 名稱 | 說明 |
|------|------|------|
| P0 | 前置準備 | 創建數據、初始化狀態、登入 |
| P1 | 核心功能 | 正常流程的主功能驗證 |
| P2 | 邊界異常 | 錯誤處理、權限驗證、邊界條件 |
| P3 | 清理驗證 | 刪除、還原、狀態終結驗證 |

---

## 測試用例狀態

| 狀態 | 說明 |
|------|------|
| TODO | 未開始編寫 |
| READY | 已編寫完成，待執行 |
| PASS | 執行通過 |
| FAIL | 執行失敗 |
| SKIP | 跳過（需註明原因） |

---

## 快速連結

### 按系統瀏覽
- [ 認證系統測試用例](./auth-system/README.md)
- [📋 儀表板系統測試用例](./dashboard-system/README.md)
- [📋 用戶管理系統測試用例](./user-management/README.md)
- [📋 團隊管理系統測試用例](./team-management/README.md)
- [📋 財務數據系統測試用例](./finance-system/README.md)
- [📋 操作指南系統測試用例](./guide-system/README.md)

---

## 測試執行記錄

| 執行日期 | 執行範圍 | 通過率 | 報告連結 |
|---------|---------|-------|---------|
| - | - | - | - |

---

**備註:** 本測試用例基於 Figma 設計文件生成，實際執行時需配合測試環境配置。
