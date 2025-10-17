# Open WebUI 聊天客戶端 | Open WebUI Chat Client

這是一個 Python 程式，可以透過 Open WebUI 的 API 進行聊天，支援文字輸入和檔案上傳的 RAG（檢索增強生成）功能。

This is a Python program that allows you to chat through Open WebUI's API, supporting text input and RAG (Retrieval-Augmented Generation) functionality with file uploads.

## 功能特色 | Features

- 🤖 **文字聊天 | Text Chat**: 直接與 AI 模型進行對話 | Communicate directly with AI models
- 📄 **檔案上傳 | File Upload**: 支援多種檔案格式上傳 | Support multiple file format uploads
- 🔍 **RAG 功能 | RAG Feature**: 基於上傳檔案的檢索增強生成 | Retrieval-Augmented Generation based on uploaded files
- 💬 **互動式聊天 | Interactive Chat**: 提供友好的互動式介面 | Provides a friendly interactive interface
- 🔧 **靈活配置 | Flexible Configuration**: 支援多種配置方式 | Support multiple configuration methods

## 安裝需求 | Requirements

### Python 版本 | Python Version
- Python 3.6 或更高版本 | Python 3.6 or higher

### 依賴套件 | Dependencies
```bash
pip install -r requirements.txt
```

## 快速開始 | Quick Start

### 1. 獲取 API 金鑰 | Get API Key

首先，您需要從 Open WebUI 獲取 API 金鑰：

First, you need to get an API key from Open WebUI:

1. 開啟 Open WebUI 網頁介面 | Open the Open WebUI web interface
2. 前往 **Settings > Account** | Navigate to **Settings > Account**
3. 複製您的 API 金鑰 | Copy your API key

### 2. 設定 API 金鑰 | Configure API Key

您有兩種方式設定 API 金鑰：

You have two ways to configure the API key:

#### 方式一：修改 config.py（推薦）| Method 1: Edit config.py (Recommended)
編輯 `config.py` 檔案，設定您的 API 金鑰：

Edit the `config.py` file and set your API key:
```python
DEFAULT_API_KEY = "your_api_key_here"
```

#### 方式二：設定環境變數 | Method 2: Set Environment Variable
```bash
# Windows
set OPENWEBUI_API_KEY=your_api_key_here

# Linux/macOS
export OPENWEBUI_API_KEY=your_api_key_here
```

### 3. 基本使用 | Basic Usage

#### 互動式聊天模式 | Interactive Chat Mode
```bash
python openwebui_chat.py --interactive
```

#### 單次查詢 | Single Query
```bash
python openwebui_chat.py --query "你好，請介紹一下自己"
# or in English
python openwebui_chat.py --query "Hello, please introduce yourself"
```

#### 使用檔案進行 RAG 聊天 | RAG Chat with File
```bash
python openwebui_chat.py --query "請總結這個文件的內容" --file "document.pdf"
# or in English
python openwebui_chat.py --query "Please summarize this document" --file "document.pdf"
```

## 詳細使用說明 | Detailed Usage Guide

### 命令列參數 | Command Line Arguments

| 參數 Parameter | 說明 Description | 預設值 Default |
|------|------|--------|
| `--url` | Open WebUI 服務 URL<br>Open WebUI service URL | `http://localhost:8080/` |
| `--api-key` | API 金鑰<br>API key | 從 config.py 或環境變數讀取<br>From config.py or environment variable |
| `--model` | 使用的模型<br>Model to use | `gemma3:1b` |
| `--file` | 要上傳的檔案路徑<br>File path to upload | 無 None |
| `--interactive` | 進入互動式聊天模式<br>Enter interactive chat mode | False |
| `--query` | 單次查詢文字<br>Single query text | 無 None |

### 互動式聊天模式指令 | Interactive Chat Mode Commands

在互動式模式下，您可以使用以下指令：

In interactive mode, you can use the following commands:

- `quit` 或 `exit` - 退出程式 | Exit the program
- `upload <檔案路徑>` - 上傳檔案並在下次對話中使用 | Upload a file and use it in the next conversation
- `models` - 查看可用模型列表 | View available models list
- `switch <模型名稱>` - 切換使用的模型 | Switch to a different model

### 支援的檔案格式 | Supported File Formats

- 文字檔案 | Text files: `.txt`, `.md`, `.json`, `.csv`, `.xml`, `.html`, `.htm`
- 文件檔案 | Document files: `.pdf`, `.docx`, `.doc`, `.rtf`, `.odt`
- 電子書 | E-books: `.epub`, `.mobi`

### 使用範例 | Usage Examples

#### 1. 基本文字聊天 | Basic Text Chat
```bash
python openwebui_chat.py --query "解釋什麼是人工智慧"
# or in English
python openwebui_chat.py --query "Explain what is artificial intelligence"
```

#### 2. 上傳文件並詢問 | Upload Document and Ask
```bash
python openwebui_chat.py --query "請總結這份報告的重點" --file "report.pdf"
# or in English
python openwebui_chat.py --query "Please summarize the key points of this report" --file "report.pdf"
```

#### 3. 互動式聊天 | Interactive Chat
```bash
python openwebui_chat.py --interactive
```

#### 4. 使用不同的模型 | Use Different Model
```bash
python openwebui_chat.py --interactive --model "llama3.2:3b-instruct-q4_K_M"
```

#### 5. 使用不同的 Open WebUI 實例 | Use Different Open WebUI Instance
```bash
python openwebui_chat.py --url "http://your-server:3000" --interactive
```

## 程式碼範例 | Code Examples

### 在 Python 程式中使用 | Use in Python Code

```python
from openwebui_chat import OpenWebUIChat

# 初始化客戶端（使用 config.py 中的預設設定）
# Initialize client (using default settings from config.py)
chat_client = OpenWebUIChat()

# 或者明確指定參數
# Or specify parameters explicitly
chat_client = OpenWebUIChat(
    base_url="http://localhost:8080",
    api_key="your_api_key_here"
)

# 簡單聊天 | Simple chat
response = chat_client.simple_chat(
    model="gemma3:1b",
    user_input="你好！| Hello!",
    file_path="document.pdf"  # 可選 | Optional
)

print(response)
```

### 上傳檔案並進行 RAG 聊天 | Upload File and RAG Chat

```python
# 上傳檔案 | Upload file
file_id = chat_client.upload_file("document.pdf")

# 使用檔案進行聊天 | Chat with file
messages = [{"role": "user", "content": "請總結這個文件 | Please summarize this document"}]
files = [{"type": "file", "id": file_id}]

response = chat_client.chat_completion(
    model="gemma3:1b",
    messages=messages,
    files=files
)
```

## 檔案結構 | File Structure

```
webui_api_py/
├── openwebui_chat.py      # 主要的聊天客戶端程式 | Main chat client program
├── config.py              # 配置檔案 | Configuration file
├── example_usage.py       # 使用範例程式 | Usage example program
├── requirements.txt       # Python 依賴套件 | Python dependencies
├── README.md             # 使用說明文件 | Documentation
└── test_document.txt     # 測試文件 | Test document
```

### 檔案說明 | File Description

- **`openwebui_chat.py`**: 核心聊天客戶端，提供完整的 API 功能 | Core chat client providing complete API functionality
- **`config.py`**: 配置檔案，包含預設的 URL、API 金鑰、模型等設定 | Configuration file with default URL, API key, model settings
- **`example_usage.py`**: 使用範例，展示各種功能的用法 | Usage examples demonstrating various features
- **`requirements.txt`**: 列出所需的 Python 套件 | Lists required Python packages
- **`test_document.txt`**: 用於測試檔案上傳和 RAG 功能的範例文件 | Sample document for testing file upload and RAG features

### 執行範例 | Run Examples

```bash
# 執行所有使用範例 | Run all usage examples
python example_usage.py
```

這會展示：| This will demonstrate:
- 基本聊天功能 | Basic chat functionality
- 檔案上傳和 RAG 功能 | File upload and RAG functionality
- 進階聊天功能 | Advanced chat functionality
- 串流回應功能 | Streaming response functionality

## 配置選項 | Configuration Options

您可以透過 `config.py` 檔案自訂配置：

You can customize configuration through the `config.py` file:

- `DEFAULT_BASE_URL`: 預設的 Open WebUI URL | Default Open WebUI URL
- `DEFAULT_MODEL`: 預設使用的模型 | Default model to use
- `DEFAULT_API_KEY`: 預設的 API 金鑰 | Default API key
- `MAX_FILE_SIZE`: 最大檔案大小限制 | Maximum file size limit
- `ALLOWED_FILE_TYPES`: 允許的檔案類型 | Allowed file types

## 故障排除 | Troubleshooting

### 常見問題 | Common Issues

1. **連線失敗 | Connection Failed**
   - 檢查 Open WebUI 服務是否正在運行 | Check if Open WebUI service is running
   - 確認 URL 是否正確 | Verify the URL is correct
   - 檢查防火牆設定 | Check firewall settings

2. **API 金鑰錯誤 | API Key Error**
   - 確認 API 金鑰是否正確 | Verify the API key is correct
   - 檢查環境變數是否設定正確 | Check if environment variable is set correctly

3. **檔案上傳失敗 | File Upload Failed**
   - 檢查檔案是否存在 | Check if file exists
   - 確認檔案大小不超過限制 | Verify file size doesn't exceed limit
   - 檢查檔案格式是否支援 | Check if file format is supported

4. **模型不存在 | Model Not Found**
   - 使用 `models` 指令查看可用模型 | Use `models` command to view available models
   - 確認模型名稱拼寫正確 | Verify model name spelling is correct

### 除錯模式 | Debug Mode

設定環境變數以啟用詳細日誌：

Set environment variable to enable verbose logging:

```bash
export DEBUG=1
python openwebui_chat.py --interactive
```

## 授權 | License

此專案採用 MIT 授權條款。

This project is licensed under the MIT License.

## 貢獻 | Contributing

歡迎提交 Issue 和 Pull Request！

Issues and Pull Requests are welcome!

## 相關連結 | Related Links

- [Open WebUI 官方文件 | Official Documentation](https://docs.openwebui.com/)
- [Open WebUI API 文件 | API Documentation](https://docs.openwebui.com/getting-started/api-endpoints/)
- [Open WebUI GitHub](https://github.com/open-webui/open-webui)
