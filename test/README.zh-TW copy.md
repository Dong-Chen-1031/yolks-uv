# uv Python Egg - 一個極快的 Pterodactyl/Pelican Eggs 及 Yolks 映像 

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Dong-Chen-1031/yolks-uv/python.yml?branch=master&label=Build%20Runtime%20Images&style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Dong-Chen-1031/yolks-uv/installer.yml?branch=master&label=Build%20Installer%20Image&style=flat-square)

## 特點
- 比普通的 Python Egg 快 接近 200 倍的伺服器安裝速度、10-100 倍的套件安裝速度。
- 同時支援傳統的 pip 工作流程和現代的 uv 套件管理流程。
- 安裝容器優化，預裝建置依賴，避免不必要的安裝造成時間浪費。
- 允許用戶從 Github 儲存庫拉取自己的 Python 原始碼。

![Optimized egg vs Python Egg](test/test.svg)



## 快速開始

### 匯入 Egg 配置

根據您的面板類型選擇 egg 檔案：

#### Pelican 面板（推薦）
```
https://raw.githubusercontent.com/Dong-Chen-1031/yolks-uv/refs/heads/master/egg/egg-python-uv.json
```

#### Pterodactyl 面板
```
https://raw.githubusercontent.com/Dong-Chen-1031/yolks-uv/refs/heads/master/egg/egg-pterodactyl-python-uv.json
```

**匯入步驟：**
1. 在您的管理面板中，導航至 **Egg** → **Import Egg**
2. 在匯入欄位中貼上上方適當的 URL
3. 點擊匯入，egg 將自動配置完成

**替代下載方式：**
- [Pelican: egg-python-uv.json](https://raw.githubusercontent.com/Dong-Chen-1031/yolks-uv/refs/heads/master/egg/egg-python-uv.json)
- [Pterodactyl: egg-pterodactyl-python-uv.json](https://raw.githubusercontent.com/Dong-Chen-1031/yolks-uv/refs/heads/master/egg/egg-pterodactyl-python-uv.json)

### 部署您的應用程式

匯入 egg 後：
1. 使用「uv Python」egg 建立新伺服器
2. 從 Docker 映像下拉選單中選擇所需的 Python 版本
3. 選擇 Dependency Install Mode：
   - **pip**（預設）：使用 requirements.txt + Additional Python packages，透過 `uv pip install`
   - **uv**：使用 pyproject.toml + uv.lock，透過 `uv sync`
4. 配置其他環境變數（如 GIT_ADDRESS、PY_FILE 等）
5. 啟動您的伺服器，應用程式將自動部署
> 請注意，修改 Git 儲存庫後，伺服器需要重新安裝以應用變更。

## 原理

## 組件

### 1. 運行時 Docker 映像 (Yolks)
預建的 Python 映像（3.8-3.14），內建 UV 套件管理器，託管於 GitHub Container Registry。這些輕量級映像以非 root 使用者（`container:container`）執行，提供增強的安全性，並作為您 Python 應用程式的運行時環境。

**映像 URL**：`ghcr.io/dong-chen-1031/yolks:python_uv_3.{8-14}`

### 2. 安裝器 Docker 映像
專用的安裝時容器，以 root 權限執行並預裝所有建置依賴。這消除了套件編譯期間的權限問題，並移除了安裝腳本中對 apt 命令的需求。

**映像 URL**：`ghcr.io/dong-chen-1031/yolks:python_uv_installer`

**預裝依賴**：
- 基礎工具：git、curl、jq、file、unzip、make、gcc、g++、libtool、ca-certificates
- 編譯函式庫：pkg-config、libffi-dev、libssl-dev、zlib1g-dev、libbz2-dev、libreadline-dev、libsqlite3-dev、libncurses5-dev、libxml2-dev、libxmlsec1-dev、liblzma-dev

### 3. Pterodactyl/Pelican Eggs
完整的 egg 配置檔案，利用雙容器架構：
- **安裝階段**：使用 `python_uv_installer`（root、所有依賴）
- **運行階段**：使用特定版本映像（非 root、安全）

可用的 eggs：
- **Pelican 面板**（PLCN_v3）：[egg-python-uv.json](egg/egg-python-uv.json)
- **Pterodactyl 面板**（PTDL_v2）：[egg-pterodactyl-python-uv.json](egg/egg-pterodactyl-python-uv.json)

### 4. 自動化 Egg 生成 (hen.py)
智慧型自動化系統，從模板和腳本生成 eggs：
- **模板**：[script/hens/](script/hens/) - Pelican 和 Pterodactyl 格式的 egg 模板
- **腳本**：[script/install.sh](script/install.sh)、[script/start.sh](script/start.sh) - 安裝和啟動邏輯
- **生成器**：[script/hen.py](script/hen.py) - 自動將腳本注入模板，並進行格式特定的轉義
- **輸出**：[egg/](egg/) - 準備好分發的最終生成 eggs

生成器自動處理格式差異：
- Pelican：標準 JSON 轉義、`startup_commands.Default` 欄位
- Pterodactyl：`\r\n` 換行、反斜線轉義、`startup` 欄位

## 功能特性

### 核心功能
- **UV 套件管理器**：以 Rust 編寫的極速 Python 套件安裝器和解析器（比 pip 快 10-100 倍）
- **雙重安裝模式**：
  - **pip 模式**：使用 requirements.txt 的 `uv pip install`（傳統工作流程）
  - **uv 模式**：使用 pyproject.toml + uv.lock 的 `uv sync`（現代專案管理）
- **多版本支援**：支援 Python 3.8 到 3.14 版本
- **多架構支援**：可用於 `linux/amd64` 和 `linux/arm64`

### 安全性與可靠性
- **雙容器架構**：
  - 安裝使用具有所有依賴的 root 容器
  - 運行使用非 root 容器以增強安全性
- **無權限問題**：預裝的建置依賴消除了 `apt` 權限錯誤
- **隔離環境**：每個專案在自己的容器中運行，具有適當的隔離

### 開發者體驗
- **自動更新**：內建支援啟動時自動更新 git 儲存庫
- **靈活的依賴管理**：支援 requirements.txt、pyproject.toml 或直接安裝套件
- **零手動維護**：透過 hen.py 自動生成 egg，保持配置同步
- **CI/CD 就緒**：GitHub Actions 工作流程自動建置映像和生成 eggs

## 為什麼選擇 UV？

[UV](https://github.com/astral-sh/uv) 是 pip 的替代品，提供：
- 10-100 倍更快的套件安裝速度
- 更好的依賴解析
- 改進的快取機制
- 以 Rust 編寫，實現最佳效能

## 配置選項

eggs 透過環境變數支援全面的配置：

### 核心設定
- **GIT_ADDRESS**：您的 git 儲存庫 URL（例如：`https://github.com/username/repo`）
- **BRANCH**：要複製的特定分支（選填，預設為儲存庫的預設分支）
- **USERNAME/ACCESS_TOKEN**：Git 身份驗證憑證（用於私有儲存庫）
- **AUTO_UPDATE**：啟用啟動時自動 git pull（`0` = 停用、`1` = 啟用）
- **USER_UPLOAD**：如果您手動上傳檔案，則跳過 git 複製（`0` = false、`1` = true）

### Python 配置
- **PY_FILE**：要執行的主要 Python 檔案（預設：`app.py`）
- **DEPENDENCY_INSTALL_MODE**：選擇依賴安裝方法
  - `pip`（預設）：使用 `uv pip install` 搭配 requirements.txt + 額外套件
  - `uv`：使用 `uv sync` 搭配 pyproject.toml（忽略 requirements.txt 和 PY_PACKAGES）

### 套件管理（僅限 pip 模式）
- **REQUIREMENTS_FILE**：Requirements 檔案名稱（預設：`requirements.txt`）
- **PY_PACKAGES**：要安裝的額外套件（以空格分隔，例如：`flask requests`）

### UV 模式（當 DEPENDENCY_INSTALL_MODE=uv 時）
使用 uv 模式時，依賴透過以下方式管理：
- **pyproject.toml**：專案配置和直接依賴
- **uv.lock**：鎖定的依賴版本（由 uv 自動生成）
- 環境：`/home/container/.local/uv`（透過 UV_PROJECT_ENVIRONMENT 設定）


## 可用映像

所有映像均託管於 GitHub Container Registry (ghcr.io)，並為 amd64 和 arm64 架構建置。

### 運行時映像（Python with UV）

* [`python_uv_3.14`](/python_uv/3.14) - Python 3.14 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.14`
* [`python_uv_3.13`](/python_uv/3.13) - Python 3.13 with UV  
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.13`
* [`python_uv_3.12`](/python_uv/3.12) - Python 3.12 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.12`
* [`python_uv_3.11`](/python_uv/3.11) - Python 3.11 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.11`
* [`python_uv_3.10`](/python_uv/3.10) - Python 3.10 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.10`
* [`python_uv_3.9`](/python_uv/3.9) - Python 3.9 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.9`
* [`python_uv_3.8`](/python_uv/3.8) - Python 3.8 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.8`

### 安裝器映像

* [`python_uv_installer`](/python_uv/installer) - 專用安裝環境
  * `ghcr.io/dong-chen-1031/yolks:python_uv_installer`
  * 基於 Python 3.13，包含所有建置依賴
  * 以 root 身份執行以進行套件編譯
  * 僅在 egg 安裝階段使用

## 安裝與啟動流程

### 安裝階段（首次設定）

安裝腳本在 `python_uv_installer` 容器中以 root 權限執行：

1. **儲存庫複製**
   - 將您的 git 儲存庫複製到 `/mnt/server`
   - 支援透過 USERNAME/ACCESS_TOKEN 進行身份驗證
   - 處理分支選擇

2. **依賴安裝**（基於 DEPENDENCY_INSTALL_MODE）
   
   **pip 模式**（傳統）：
   ```bash
   uv pip install -U --prefix .local ${PY_PACKAGES}
   uv pip install -U --prefix .local -r requirements.txt
   ```
   
   **uv 模式**（現代）：
   ```bash
   uv sync  # 使用 pyproject.toml + uv.lock
   ```

### 運行階段（每次啟動）

啟動腳本在特定版本的運行時容器中以非 root 使用者執行：

1. **自動更新**（如果啟用）
   - 從 git 儲存庫拉取最新更改
   
2. **應用程式啟動**（基於 DEPENDENCY_INSTALL_MODE）
   
   **pip 模式**：
   ```bash
   export PATH=/home/container/.local/bin:$PATH
   export PYTHONPATH=/home/container/.local
   python ${PY_FILE}
   ```
   
   **uv 模式**：
   ```bash
   export UV_PROJECT_ENVIRONMENT="/home/container/.local/uv"
   uv run ${PY_FILE}
   ```

### 為什麼使用雙容器？

- **安裝**：需要 root 存取權限來編譯帶有 C 擴展的套件（如 cryptography、lxml 等）
- **運行**：以非 root 執行以提升安全性（Pterodactyl/Pelican 最佳實踐）
- **關注點分離**：建置依賴不會膨脹運行時映像

## 建置與開發

### 自動化建置

映像透過 GitHub Actions 工作流程自動建置：

#### 運行時映像 ([.github/workflows/python.yml](.github/workflows/python.yml))
- **觸發條件**：推送到 `python_uv/3.*/**`、每週排程（週一）、手動調度
- **輸出**：`ghcr.io/dong-chen-1031/yolks:python_uv_3.{8-14}`
- **架構**：linux/amd64、linux/arm64

#### 安裝器映像 ([.github/workflows/installer.yml](.github/workflows/installer.yml))
- **觸發條件**：推送到 `python_uv/installer/**`、每週排程（週一）、手動調度
- **輸出**：`ghcr.io/dong-chen-1031/yolks:python_uv_installer`
- **架構**：linux/amd64、linux/arm64

#### Egg 生成 ([.github/workflows/hen.yml](.github/workflows/hen.yml))
- **觸發條件**：推送到 `script/install.sh`、`script/start.sh`、`script/hens/**`、`script/hen.py`、手動調度
- **過程**：執行 `hen.py` 從模板重新生成 eggs
- **輸出**：自動提交更新的 eggs 到 `egg/` 目錄

### 本地建置

建置運行時映像：
```bash
docker build -t python_uv:3.13 ./python_uv/3.13
```

建置安裝器映像：
```bash
docker build -t python_uv_installer ./python_uv/installer
```

在本地生成 eggs：
```bash
cd script
python3 hen.py
```

### 開發工作流程

1. **修改腳本**：編輯 `script/install.sh` 或 `script/start.sh`
2. **更新模板**：如需要，修改 `script/hens/` 中的 egg 模板
3. **本地測試**：執行 `python3 hen.py` 驗證生成
4. **推送變更**：GitHub Actions 自動重新生成並提交 eggs
5. **禁止手動編輯 Egg**：永遠不要直接編輯 `egg/` 中的檔案 - 它們是自動生成的！

## 專案結構

```
yolks-uv/
├── .github/workflows/
│   ├── python.yml          # 建置運行時映像（3.8-3.14）
│   ├── installer.yml       # 建置安裝器映像
│   └── hen.yml            # 從模板自動生成 eggs
├── python_uv/
│   ├── 3.8/ ... 3.14/     # 運行時映像 Dockerfiles
│   └── installer/         # 安裝器映像 Dockerfile
├── script/
│   ├── hens/              # Egg 模板（真實來源）
│   │   ├── egg-python-uv.json              # Pelican 模板
│   │   └── egg-pterodactyl-python-uv.json  # Pterodactyl 模板
│   ├── hen.py             # Egg 生成器（母雞 🐔）
│   ├── install.sh         # 安裝腳本
│   └── start.sh           # 啟動腳本
├── egg/                   # 生成的 eggs（請勿編輯）
│   ├── egg-python-uv.json              # 自動生成的 Pelican egg
│   └── egg-pterodactyl-python-uv.json  # 自動生成的 Pterodactyl egg
├── LICENSE.md
└── README.md
```

### 關鍵概念

- **模板 (hens/)**：egg 元資料、變數和結構的真實來源
- **腳本 (*.sh)**：可重用的安裝和啟動邏輯
- **生成器 (hen.py)**：將腳本注入模板並進行適當的轉義
- **輸出 (egg/)**：準備好匯入的最終 eggs（自動生成，永不手動編輯）

「hen」的隱喻：母雞 (hen.py) 從模板和腳本下蛋 🐔→🥚

## 貢獻

歡迎貢獻！以下是如何新增功能：

### 新增新的 Python 版本

1. 建立目錄：`python_uv/3.XX/`
2. 基於現有版本新增 Dockerfile
3. 更新 `.github/workflows/python.yml` 矩陣：
   ```yaml
   python-version: ['3.8', '3.9', '3.10', '3.11', '3.12', '3.13', '3.14', '3.XX']
   ```
4. 更新 `script/hens/` 中的 egg 模板，在 `docker_images` 中包含新版本
5. 執行 `hen.py` 重新生成 eggs
6. 更新 README，加入新版本

### 修改安裝/啟動邏輯

1. 編輯 `script/install.sh` 或 `script/start.sh`
2. 在本地測試變更
3. 執行 `python3 script/hen.py` 重新生成 eggs
4. 驗證 `egg/` 目錄中生成的 eggs
5. 推送變更 - GitHub Actions 將自動更新 eggs

### 新增建置依賴

編輯 `python_uv/installer/Dockerfile` 並在 `apt-get install` 命令中新增套件。

### 更新 Egg 變數

編輯 `script/hens/` 中的模板：
- `egg-python-uv.json` 用於 Pelican（PLCN_v3 格式）
- `egg-pterodactyl-python-uv.json` 用於 Pterodactyl（PTDL_v2 格式）

然後使用 `hen.py` 重新生成。

## 疑難排解

### 常見問題

#### 安裝期間權限被拒絕
**解決方案**：確保您使用最新的 egg，其使用 `python_uv_installer` 作為安裝容器。此容器以 root 身份執行並具有所有必要的權限。

#### 套件編譯失敗
**解決方案**：檢查 `python_uv/installer/Dockerfile` 中是否包含所需的編譯函式庫。可以將常見缺失的函式庫新增到 apt-get install 命令中。

#### UV 模式無法運作
**解決方案**：確保您的儲存庫中同時有 `pyproject.toml` 和 `uv.lock`。在 egg 配置中設定 `DEPENDENCY_INSTALL_MODE=uv`。

#### 自動更新未拉取最新變更
**解決方案**：設定 `AUTO_UPDATE=1` 並確保您的 git 儲存庫可存取。對於私有儲存庫，配置 USERNAME 和 ACCESS_TOKEN。

#### 生成的 Eggs 與模板不符
**解決方案**：在本地執行 `python3 script/hen.py` 重新生成。永遠不要直接編輯 `egg/` 中的檔案 - 它們會被自動化覆蓋。

## 常見問題 (FAQ)

**問：pip 模式和 uv 模式有什麼區別？**
- **pip 模式**：使用 requirements.txt 的傳統工作流程，與現有專案相容
- **uv 模式**：使用 pyproject.toml + uv.lock 的現代方法，用於可重現的建置

**問：為什麼要分離安裝器和運行時映像？**
- 安全性：運行時以非 root 使用者執行
- 效率：建置工具不會膨脹運行時映像
- 可靠性：安裝期間的 root 存取權限可防止權限錯誤

**問：我可以將此用於私有 GitHub 儲存庫嗎？**
可以！在您的 egg 配置中設定 USERNAME 和 ACCESS_TOKEN 變數。

**問：為什麼叫做「hen.py」？**
母雞會下蛋！🐔 生成器 (hen.py) 從模板 (hens/) 和腳本建立 eggs。

**問：更改腳本後是否需要手動更新 eggs？**
不需要！GitHub Actions 會在腳本變更時自動執行 hen.py 並提交更新的 eggs。

**問：我應該使用哪個 Python 版本？**
除非您有特定的相容性要求，否則請使用最新的穩定版本（3.13）。支援所有 3.8-3.14 版本。

## 授權條款

詳見 [LICENSE.md](LICENSE.md)。

## 致謝

- **Docker 映像**：基於 [Pelican Eggs Yolks](https://github.com/pelican-eggs/yolks) 並整合 UV
- **Egg 配置**：基於 [Pelican Eggs Generic](https://github.com/pelican-eggs/generic) 並增強 UV 支援
- **UV 套件管理器**：[astral-sh/uv](https://github.com/astral-sh/uv) - 極快的 Python 套件安裝器和解析器

## 連結

- **儲存庫**：[Dong-Chen-1031/yolks-uv](https://github.com/Dong-Chen-1031/yolks-uv)
- **Docker 映像**：[ghcr.io/dong-chen-1031/yolks](https://github.com/Dong-Chen-1031/yolks-uv/pkgs/container/yolks)
- **上游專案**：
  - [Pelican Eggs](https://github.com/pelican-eggs)
  - [UV Package Manager](https://github.com/astral-sh/uv)
  - [Pterodactyl Panel](https://pterodactyl.io/)

---

**由 hen.py 自動化系統製作 🐔**
