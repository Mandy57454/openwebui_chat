# Open WebUI 聊天客戶端

這是一個 Python 程式，可以透過 Open WebUI 的 API 進行聊天，支援文字輸入和檔案上傳的 RAG（檢索增強生成）功能。

## 功能特色

- 🤖 **文字聊天**: 直接與 AI 模型進行對話
- 📄 **檔案上傳**: 支援多種檔案格式上傳
- 🔍 **RAG 功能**: 基於上傳檔案的檢索增強生成
- 💬 **互動式聊天**: 提供友好的互動式介面
- 🔧 **靈活配置**: 支援多種配置方式

## 安裝需求

### Python 版本
- Python 3.6 或更高版本

### 依賴套件
```bash
pip install -r requirements.txt
```

## 快速開始

### 1. 設定 API 金鑰

首先，您需要從 Open WebUI 獲取 API 金鑰：

1. 開啟 Open WebUI 網頁介面
2. 前往 **Settings > Account**
3. 複製您的 API 金鑰

### 2. 設定 API 金鑰

您有兩種方式設定 API 金鑰：

#### 方式一：修改 config.py（推薦）
編輯 `config.py` 檔案，設定您的 API 金鑰：
```python
DEFAULT_API_KEY = "your_api_key_here"
```

#### 方式二：設定環境變數
```bash
# Windows
set OPENWEBUI_API_KEY=your_api_key_here

# Linux/macOS
export OPENWEBUI_API_KEY=your_api_key_here
```

### 3. 基本使用

#### 互動式聊天模式
```bash
python openwebui_chat.py --interactive
```

#### 單次查詢
```bash
python openwebui_chat.py --query "你好，請介紹一下自己"
```

#### 使用檔案進行 RAG 聊天
```bash
python openwebui_chat.py --query "請總結這個文件的內容" --file "document.pdf"
```

## 詳細使用說明

### 命令列參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--url` | Open WebUI 服務 URL | `http://20.228.108.174:3000` |
| `--api-key` | API 金鑰 | 從 config.py 或環境變數讀取 |
| `--model` | 使用的模型 | `llama3.1:8b-instruct-q4_K_M` |
| `--file` | 要上傳的檔案路徑 | 無 |
| `--interactive` | 進入互動式聊天模式 | False |
| `--query` | 單次查詢文字 | 無 |

### 互動式聊天模式指令

在互動式模式下，您可以使用以下指令：

- `quit` 或 `exit` - 退出程式
- `upload <檔案路徑>` - 上傳檔案並在下次對話中使用
- `models` - 查看可用模型列表
- `switch <模型名稱>` - 切換使用的模型

### 支援的檔案格式

- 文字檔案: `.txt`, `.md`, `.json`, `.csv`, `.xml`, `.html`, `.htm`
- 文件檔案: `.pdf`, `.docx`, `.doc`, `.rtf`, `.odt`
- 電子書: `.epub`, `.mobi`

### 使用範例

#### 1. 基本文字聊天
```bash
python openwebui_chat.py --query "解釋什麼是人工智慧"
```

#### 2. 上傳文件並詢問
```bash
python openwebui_chat.py --query "請總結這份報告的重點" --file "report.pdf"
```

#### 3. 互動式聊天
```bash
python openwebui_chat.py --interactive
```

#### 4. 使用不同的模型
```bash
python openwebui_chat.py --interactive --model "llama3.2:3b-instruct-q4_K_M"
```

#### 5. 使用不同的 Open WebUI 實例
```bash
python openwebui_chat.py --url "http://your-server:3000" --interactive
```

## 程式碼範例

### 在 Python 程式中使用

```python
from openwebui_chat import OpenWebUIChat

# 初始化客戶端（使用 config.py 中的預設設定）
chat_client = OpenWebUIChat()

# 或者明確指定參數
chat_client = OpenWebUIChat(
    base_url="http://20.228.108.174:3000",
    api_key="your_api_key_here"
)

# 簡單聊天
response = chat_client.simple_chat(
    model="llama3.1:8b-instruct-q4_K_M",
    user_input="你好！",
    file_path="document.pdf"  # 可選
)

print(response)
```

### 上傳檔案並進行 RAG 聊天

```python
# 上傳檔案
file_id = chat_client.upload_file("document.pdf")

# 使用檔案進行聊天
messages = [{"role": "user", "content": "請總結這個文件"}]
files = [{"type": "file", "id": file_id}]

response = chat_client.chat_completion(
    model="llama3.1:8b-instruct-q4_K_M",
    messages=messages,
    files=files
)
```

## 檔案結構

```
webui_api_py/
├── openwebui_chat.py      # 主要的聊天客戶端程式
├── config.py              # 配置檔案
├── example_usage.py       # 使用範例程式
├── requirements.txt       # Python 依賴套件
├── README.md             # 使用說明文件
└── test_document.txt     # 測試文件
```

### 檔案說明

- **`openwebui_chat.py`**: 核心聊天客戶端，提供完整的 API 功能
- **`config.py`**: 配置檔案，包含預設的 URL、API 金鑰、模型等設定
- **`example_usage.py`**: 使用範例，展示各種功能的用法
- **`requirements.txt`**: 列出所需的 Python 套件
- **`test_document.txt`**: 用於測試檔案上傳和 RAG 功能的範例文件

### 執行範例

```bash
# 執行所有使用範例
python example_usage.py
```

這會展示：
- 基本聊天功能
- 檔案上傳和 RAG 功能
- 進階聊天功能
- 串流回應功能

## 配置選項

您可以透過 `config.py` 檔案自訂配置：

- `DEFAULT_BASE_URL`: 預設的 Open WebUI URL
- `DEFAULT_MODEL`: 預設使用的模型
- `DEFAULT_API_KEY`: 預設的 API 金鑰
- `MAX_FILE_SIZE`: 最大檔案大小限制
- `ALLOWED_FILE_TYPES`: 允許的檔案類型

## 故障排除

### 常見問題

1. **連線失敗**
   - 檢查 Open WebUI 服務是否正在運行
   - 確認 URL 是否正確
   - 檢查防火牆設定

2. **API 金鑰錯誤**
   - 確認 API 金鑰是否正確
   - 檢查環境變數是否設定正確

3. **檔案上傳失敗**
   - 檢查檔案是否存在
   - 確認檔案大小不超過限制
   - 檢查檔案格式是否支援

4. **模型不存在**
   - 使用 `models` 指令查看可用模型
   - 確認模型名稱拼寫正確

### 除錯模式

設定環境變數以啟用詳細日誌：

```bash
export DEBUG=1
python openwebui_chat.py --interactive
```

## 授權

此專案採用 MIT 授權條款。

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 相關連結

- [Open WebUI 官方文件](https://docs.openwebui.com/)
- [Open WebUI API 文件](https://docs.openwebui.com/getting-started/api-endpoints/)
- [Open WebUI GitHub](https://github.com/open-webui/open-webui)
