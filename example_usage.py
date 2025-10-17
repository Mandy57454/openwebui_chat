#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open WebUI 聊天客戶端使用範例
"""

import os
from openwebui_chat import OpenWebUIChat
from config import Config


def example_basic_chat():
    """基本聊天範例"""
    print("=== 基本聊天範例 | Basic Chat Example ===")
    
    # 初始化客戶端
    chat_client = OpenWebUIChat()
    
    # 簡單聊天
    response = chat_client.simple_chat(
        model="gemma3:1b",
        user_input="你好！請介紹一下自己。"
    )
    
    print(f"AI 回應 | AI Response: {response}")


def example_file_upload_and_rag():
    """檔案上傳和 RAG 範例"""
    print("\n=== 檔案上傳和 RAG 範例 | File Upload and RAG Example ===")
    
    # 初始化客戶端
    chat_client = OpenWebUIChat()
    
    # 創建一個測試文件
    test_file = "test_document.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("""
人工智慧（Artificial Intelligence，AI）是電腦科學的一個分支，
旨在創建能夠執行通常需要人類智慧的任務的系統。

主要應用領域包括：
1. 自然語言處理
2. 機器學習
3. 電腦視覺
4. 機器人技術
5. 專家系統

AI 的發展歷史可以追溯到 1950 年代，當時艾倫·圖靈提出了著名的圖靈測試。
        """)
    
    try:
        # 上傳檔案
        file_id = chat_client.upload_file(test_file)
        
        if file_id:
            # 使用檔案進行 RAG 聊天
            response = chat_client.simple_chat(
                model="gemma3:1b",
                user_input="請總結這個文件的主要內容，並列出 AI 的主要應用領域。",
                file_path=test_file
            )
            
            print(f"AI 回應 | AI Response: {response}")
        else:
            print("檔案上傳失敗 | File upload failed")
            
    finally:
        # 清理測試文件
        if os.path.exists(test_file):
            os.remove(test_file)


def example_advanced_chat():
    """進階聊天範例"""
    print("\n=== 進階聊天範例 | Advanced Chat Example ===")
    
    # 初始化客戶端
    chat_client = OpenWebUIChat()
    
    # 獲取可用模型
    models = chat_client.get_available_models()
    print("可用模型 | Available models:")
    for model in models:
        print(f"  - {model.get('id', 'Unknown')}")
    
    # 多輪對話
    conversation = [
        {"role": "user", "content": "你好！"},
        {"role": "assistant", "content": "你好！我是 AI 助手，很高興為您服務。"},
        {"role": "user", "content": "請告訴我 Python 的基本語法。"}
    ]
    
    response = chat_client.chat_completion(
        model="gemma3:1b",
        messages=conversation
    )
    
    if 'choices' in response and len(response['choices']) > 0:
        ai_response = response['choices'][0]['message']['content']
        print(f"AI 回應 | AI Response: {ai_response}")


def example_streaming_chat():
    """串流聊天範例"""
    print("\n=== 串流聊天範例 | Streaming Chat Example ===")
    
    # 初始化客戶端
    chat_client = OpenWebUIChat()
    
    # 串流聊天
    messages = [{"role": "user", "content": "請詳細解釋什麼是機器學習，並舉例說明。"}]
    
    response = chat_client.chat_completion(
        model="gemma3:1b",
        messages=messages,
        stream=True
    )
    
    print(f"完整回應 | Full response: {response.get('content', '無回應 | No response')}")


def main():
    """主函數"""
    print("Open WebUI 聊天客戶端使用範例 | Open WebUI Chat Client Examples")
    print("=" * 50)
    
    # 檢查 API 金鑰
    api_key = Config.get_api_key()
    if not api_key:
        print("❌ 無法獲取 API 金鑰 | Unable to get API key")
        print("請檢查 config.py 中的 DEFAULT_API_KEY 設定 | Please check DEFAULT_API_KEY setting in config.py")
        return
    
    try:
        # 執行範例
        example_basic_chat()
        example_file_upload_and_rag()
        example_advanced_chat()
        example_streaming_chat()
        
    except Exception as e:
        print(f"❌ 執行範例時發生錯誤: {e} | Error occurred while running examples: {e}")


if __name__ == "__main__":
    main()
