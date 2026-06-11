# AI Minutes Web - 測試套件總索引

**專案名稱:** AI Minutes Web 後台管理系統  
**測試版本:** v1.0  
**最後更新:** 2026-06-11

---

## 專案結構

```
C:/Users/User/AI_test/
├── test-suite/                      # 測試套件主目錄
│   ├── test-cases/                  # 測試用例文檔
│   │   ├── index.md                 # 本索引文件
│   │   ├── auth-system/             # 認證系統
│   │   ├── dashboard-system/        # 儀表板系統
│   │   ├── user-management/         # 用戶管理系統
│   │   ├── team-management/         # 團隊管理系統
│   │   ├── finance-system/          # 財務數據系統
│   │   └── guide-system/            # 操作指南系統
│   └── test-reports/                # 測試執行報告
│       ├── config.yaml              # 測試配置
│       ├── run_tests.py             # 測試運行器
│       └── run_all_tests.py         # 主測試運行器
│
└── aim-test/
    └── test-results/                # 測試執行結果
        ├── scripts/                 # 測試腳本
        ├── screenshots/             # 截圖
        ├── videos/                  # 錄像
        ├── reports/                 # 報告
        ├── README.md                # 使用說明
        └── result.md                # 執行結果模板
```

---

## 測試用例統計

| 系統 | 模塊數 | 測試用例數 | 優先級 |
|------|--------|-----------|--------|
| [認證系統](#認證系統) | 2 | 12 | P0 |
| [儀表板系統](#儀表板系統) | 1 | 8 | P1 |
| [用戶管理系統](#用戶管理系統) | 2 | 15 | P1 |
| [團隊管理系統](#團隊管理系統) | 3 | 18 | P1 |
| [財務數據系統](#財務數據系統) | 4 | 20 | P2 |
| [操作指南系統](#操作指南系統) | 2 | 10 | P2 |
| **總計** | **14** | **83** | - |

---

## 認證系統 (AUTH)

**Figma 節點:** `DxKBR` (登入), `XftgV` (電郵驗證)

### 測試用例清單

| 編號 | 名稱 | 優先級 | 階段 | 腳本 |
|------|------|--------|------|------|
| TC-AUTH-LOGIN-001 | 使用有效憑證成功登入 | 高 | P1 | `test_login.py` |
| TC-AUTH-LOGIN-002 | 使用無效賬號登入 | 高 | P2 | `test_login.py` |
| TC-AUTH-LOGIN-003 | 使用無效密碼登入 | 高 | P2 | `test_login.py` |
| TC-AUTH-LOGIN-004 | 空賬號登入驗證 | 中 | P2 | `test_login.py` |
| TC-AUTH-LOGIN-005 | 空密碼登入驗證 | 中 | P2 | `test_login.py` |
| TC-AUTH-LOGIN-006 | 登入頁面 UI 驗證 | 低 | P1 | `test_login.py` |
| TC-AUTH-2FA-001 | 輸入正確驗證碼成功登入 | 高 | P1 | `test_2fa_verify.py` |
| TC-AUTH-2FA-002 | 輸入錯誤驗證碼 | 高 | P2 | `test_2fa_verify.py` |
| TC-AUTH-2FA-003 | 空驗證碼提交 | 中 | P2 | `test_2fa_verify.py` |
| TC-AUTH-2FA-004 | 重新發送驗證碼 | 中 | P1 | `test_2fa_verify.py` |
| TC-AUTH-2FA-005 | 驗證碼頁面 UI 驗證 | 低 | P1 | `test_2fa_verify.py` |
| TC-AUTH-2FA-006 | 驗證碼格式驗證 | 中 | P2 | `test_2fa_verify.py` |

**執行命令:**
```bash
python run_all_tests.py --module auth-system
```

---

## 儀表板系統 (DASH)

**Figma 節點:** `bi8Au` (Dashboard Overview)

### 測試用例清單

| 編號 | 名稱 | 優先級 | 階段 | 腳本 |
|------|------|--------|------|------|
| TC-DASH-OVERVIEW-001 | 儀表板頁面加載驗證 | 高 | P1 | `test_overview.py` |
| TC-DASH-OVERVIEW-002 | 四個指標卡片數據顯示驗證 | 高 | P1 | `test_overview.py` |
| TC-DASH-OVERVIEW-003 | 新增用戶柱狀圖顯示驗證 | 中 | P1 | `test_overview.py` |
| TC-DASH-OVERVIEW-004 | 活躍用戶柱狀圖顯示驗證 | 中 | P1 | `test_overview.py` |
| TC-DASH-OVERVIEW-005 | 充值金額折線圖顯示驗證 | 中 | P1 | `test_overview.py` |
| TC-DASH-OVERVIEW-006 | 轉錄分鐘數折線圖顯示驗證 | 中 | P1 | `test_overview.py` |
| TC-DASH-OVERVIEW-007 | 側邊欄導航功能驗證 | 高 | P1 | `test_overview.py` |
| TC-DASH-OVERVIEW-008 | 儀表板 UI 完整性驗證 | 低 | P1 | `test_overview.py` |

**執行命令:**
```bash
python run_all_tests.py --module dashboard-system
```

---

## 用戶管理系統 (USER)

**Figma 節點:** `NPfOA` (用戶列表), `yvijQ` (用戶詳情)

### 測試用例清單

| 編號 | 名稱 | 優先級 | 階段 | 腳本 |
|------|------|--------|------|------|
| TC-USER-LIST-001 | 用戶列表頁面加載驗證 | 高 | P1 | `test_user_list.py` |
| TC-USER-LIST-002 | 用戶名稱篩選功能驗證 | 高 | P1 | `test_user_list.py` |
| TC-USER-LIST-003 | 電郵地址篩選功能驗證 | 高 | P1 | `test_user_list.py` |
| TC-USER-LIST-004 | 使用模式下拉篩選驗證 | 中 | P1 | `test_user_list.py` |
| TC-USER-LIST-005 | 賬號狀態下拉篩選驗證 | 中 | P1 | `test_user_list.py` |
| TC-USER-LIST-006 | 搜索按鈕功能驗證 | 高 | P1 | `test_user_list.py` |
| TC-USER-LIST-007 | 表格數據顯示驗證 | 高 | P1 | `test_user_list.py` |
| TC-USER-LIST-008 | 分頁功能驗證 | 中 | P1 | `test_user_list.py` |
| TC-USER-LIST-009 | 賬號狀態 Toggle 切換驗證 | 高 | P2 | `test_user_list.py` |
| TC-USER-LIST-010 | 查看用戶詳情按鈕驗證 | 中 | P1 | `test_user_list.py` |
| TC-USER-DETAIL-001 | 用戶詳情頁面加載驗證 | 高 | P1 | `test_user_detail.py` |
| TC-USER-DETAIL-002 | 用戶基本資料顯示驗證 | 高 | P1 | `test_user_detail.py` |
| TC-USER-DETAIL-003 | 充值記錄表格顯示驗證 | 中 | P1 | `test_user_detail.py` |
| TC-USER-DETAIL-004 | 返回按鈕功能驗證 | 低 | P1 | `test_user_detail.py` |

**執行命令:**
```bash
python run_all_tests.py --module user-management
```

---

## 團隊管理系統 (TEAM)

**Figma 節點:** `u1Z3o` (團隊列表), `UMzLK` (團隊詳情), `nnAMn` (團隊充值)

### 測試用例清單

| 編號 | 名稱 | 優先級 | 階段 | 腳本 |
|------|------|--------|------|------|
| TC-TEAM-LIST-001 | 團隊列表頁面加載驗證 | 高 | P1 | `test_team_list.py` |
| TC-TEAM-LIST-002 | 團隊名稱篩選功能驗證 | 高 | P1 | `test_team_list.py` |
| TC-TEAM-LIST-003 | 團隊 ID 篩選功能驗證 | 高 | P1 | `test_team_list.py` |
| TC-TEAM-LIST-004 | 團隊擁有人篩選功能驗證 | 中 | P1 | `test_team_list.py` |
| TC-TEAM-LIST-005 | 篩選按鈕功能驗證 | 高 | P1 | `test_team_list.py` |
| TC-TEAM-LIST-006 | 表格數據顯示驗證 | 高 | P1 | `test_team_list.py` |
| TC-TEAM-LIST-007 | 分頁功能驗證 | 中 | P1 | `test_team_list.py` |
| TC-TEAM-LIST-008 | 查看團隊詳情按鈕驗證 | 中 | P1 | `test_team_list.py` |
| TC-TEAM-DETAIL-001 | 團隊詳情頁面加載驗證 | 高 | P1 | `test_team_detail.py` |
| TC-TEAM-DETAIL-002 | 團隊基本資料顯示驗證 | 高 | P1 | `test_team_detail.py` |
| TC-TEAM-DETAIL-003 | 團隊成員表格顯示驗證 | 中 | P1 | `test_team_detail.py` |
| TC-TEAM-DETAIL-004 | 分頁籤切換功能驗證 | 中 | P1 | `test_team_detail.py` |
| TC-TEAM-RECHARGE-001 | 團隊充值紀錄頁面加載驗證 | 高 | P1 | `test_team_recharge.py` |
| TC-TEAM-RECHARGE-002 | 充值記錄表格顯示驗證 | 高 | P1 | `test_team_recharge.py` |
| TC-TEAM-RECHARGE-003 | 返回按鈕功能驗證 | 低 | P1 | `test_team_recharge.py` |

**執行命令:**
```bash
python run_all_tests.py --module team-management
```

---

## 財務數據系統 (FIN)

**Figma 節點:** `IkSFY` (數據統計), `5kvjX` (充值紀錄), `yEhir` (團隊統計), `EH2Cx` (個人統計)

### 測試用例清單

| 編號 | 名稱 | 優先級 | 階段 | 腳本 |
|------|------|--------|------|------|
| TC-FIN-STATS-001~010 | 數據統計測試 (10 例) | 高/中 | P1 | `test_data_statistics.py` |
| TC-FIN-RECORDS-001~008 | 充值紀錄測試 (8 例) | 高/中 | P1 | `test_recharge_records.py` |
| TC-FIN-TEAM-001~006 | 團隊充值統計測試 (6 例) | 高/中 | P1 | `test_team_stats.py` |
| TC-FIN-INDIVIDUAL-001~004 | 個人充值統計測試 (4 例) | 高/中 | P1 | `test_individual_stats.py` |

**執行命令:**
```bash
python run_all_tests.py --module finance-system
```

---

## 操作指南系統 (GUIDE)

**Figma 節點:** `1SK6U` (指南列表), `NMmnO` (新增指南)

### 測試用例清單

| 編號 | 名稱 | 優先級 | 階段 | 腳本 |
|------|------|--------|------|------|
| TC-GUIDE-LIST-001~010 | 操作指南列表測試 (10 例) | 高/中/低 | P1/P2 | `test_guide_list.py` |
| TC-GUIDE-CREATE-001~008 | 新增操作指南測試 (8 例) | 高/中/低 | P1/P2 | `test_guide_create.py` |

**執行命令:**
```bash
python run_all_tests.py --module guide-system
```

---

## 快速開始

### 1. 安裝依賴

```bash
pip install playwright pytest pytest-asyncio pytest-html pyyaml
playwright install chromium
```

### 2. 配置測試環境

編輯 `test-suite/test-reports/config.yaml`:

```yaml
base_url: "http://localhost:3000"
username: "test@example.com"
password: "your-password"
```

### 3. 運行測試

```bash
# 所有測試
cd C:/Users/User/AI_test/test-suite/test-reports
python run_all_tests.py

# 指定模塊
python run_all_tests.py --module auth-system
```

### 4. 查看報告

- HTML 報告：`test-reports/report_YYYYMMDD_HHMMSS.html`
- 截圖：`aim-test/test-results/screenshots/`
- 結果模板：`aim-test/test-results/result.md`

---

## 版本歷史

| 版本 | 日期 | 變更內容 |
|------|------|---------|
| v1.0 | 2026-06-11 | 初始版本，基於 Figma 設計生成 83 個測試用例 |

---

**聯絡資訊:**
- 測試負責人：[姓名]
- 郵箱：[email]
