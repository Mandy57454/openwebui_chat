#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open WebUI 聊天客戶端
支援文字聊天和檔案上傳的 RAG 功能
"""

import requests
import json
import os
import sys
from typing import Optional, List, Dict, Any
import argparse
from pathlib import Path
from config import Config


class OpenWebUIChat:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        初始化 Open WebUI 聊天客戶端
        
        Args:
            base_url: Open WebUI 服務的基礎 URL，如果為 None 則從 config.py 讀取
            api_key: API 金鑰，如果為 None 則從環境變數讀取
        """
        self.base_url = (base_url or Config.get_base_url()).rstrip('/')
        self.api_key = api_key or Config.get_api_key()
        
        if not self.api_key:
            raise ValueError("請提供 API 金鑰或設定 OPENWEBUI_API_KEY 環境變數 | Please provide API key or set OPENWEBUI_API_KEY environment variable")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # 測試連線
        self._test_connection()
    
    def _test_connection(self):
        """測試與 Open WebUI 的連線"""
        try:
            response = requests.get(f"{self.base_url}/api/models", headers=self.headers)
            if response.status_code == 200:
                print("✅ 成功連接到 Open WebUI | Successfully connected to Open WebUI")
            else:
                print(f"⚠️  連線測試失敗，狀態碼: {response.status_code} | Connection test failed, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ 無法連接到 Open WebUI: {e} | Unable to connect to Open WebUI: {e}")
            sys.exit(1)
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        獲取可用的模型列表
        
        Returns:
            模型列表
        """
        try:
            response = requests.get(f"{self.base_url}/api/models", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # 處理不同的回應格式
            if isinstance(data, dict) and 'data' in data:
                return data['data']
            elif isinstance(data, list):
                return data
            else:
                print(f"⚠️  未知的模型列表格式: {data} | Unknown model list format: {data}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 獲取模型列表失敗: {e} | Failed to get model list: {e}")
            return []
    
    def upload_file(self, file_path: str) -> Optional[str]:
        """
        上傳檔案到 Open WebUI
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            檔案 ID，如果上傳失敗則返回 None
        """
        if not os.path.exists(file_path):
            print(f"❌ 檔案不存在: {file_path} | File does not exist: {file_path}")
            return None
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Accept': 'application/json'
                }
                
                response = requests.post(
                    f"{self.base_url}/api/v1/files/",
                    headers=headers,
                    files=files
                )
                response.raise_for_status()
                
                result = response.json()
                file_id = result.get('id')
                print(f"✅ 檔案上傳成功: {os.path.basename(file_path)} (ID: {file_id}) | File uploaded successfully: {os.path.basename(file_path)} (ID: {file_id})")
                return file_id
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 檔案上傳失敗: {e} | File upload failed: {e}")
            return None
        except Exception as e:
            print(f"❌ 檔案上傳時發生錯誤: {e} | Error occurred during file upload: {e}")
            return None
    
    def chat_completion(self, 
                       model: str, 
                       messages: List[Dict[str, str]], 
                       files: Optional[List[Dict[str, str]]] = None,
                       stream: bool = False) -> Dict[str, Any]:
        """
        發送聊天完成請求
        
        Args:
            model: 使用的模型名稱
            messages: 聊天訊息列表
            files: 可選的檔案列表，用於 RAG
            stream: 是否使用串流模式
            
        Returns:
            API 回應
        """
        payload = {
            'model': model,
            'messages': messages
        }
        
        if files:
            payload['files'] = files
        
        if stream:
            payload['stream'] = True
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat/completions",
                headers=self.headers,
                json=payload,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return self._handle_stream_response(response)
            else:
                return response.json()
                
        except requests.exceptions.HTTPError as e:
            print(f"❌ 聊天請求失敗 (HTTP {response.status_code}): {e} | Chat request failed (HTTP {response.status_code}): {e}")
            try:
                error_detail = response.json()
                print(f"錯誤詳情: {error_detail} | Error details: {error_detail}")
            except:
                print(f"回應內容: {response.text} | Response content: {response.text}")
            return {}
        except requests.exceptions.RequestException as e:
            print(f"❌ 聊天請求失敗: {e} | Chat request failed: {e}")
            return {}
    
    def _handle_stream_response(self, response):
        """處理串流回應"""
        print("\n🤖 AI 回應 | AI Response:")
        print("-" * 50)
        
        full_content = ""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]  # 移除 'data: ' 前綴
                    if data.strip() == '[DONE]':
                        break
                    try:
                        json_data = json.loads(data)
                        if 'choices' in json_data and len(json_data['choices']) > 0:
                            delta = json_data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                content = delta['content']
                                print(content, end='', flush=True)
                                full_content += content
                    except json.JSONDecodeError:
                        continue
        
        print("\n" + "-" * 50)
        return {'content': full_content}
    
    def simple_chat(self, model: str, user_input: str, file_path: Optional[str] = None) -> str:
        """
        簡單的聊天介面
        
        Args:
            model: 使用的模型
            user_input: 使用者輸入
            file_path: 可選的檔案路徑
            
        Returns:
            AI 的回應
        """
        messages = [{'role': 'user', 'content': user_input}]
        files = None
        
        # 如果有提供檔案，先上傳
        if file_path:
            file_id = self.upload_file(file_path)
            if file_id:
                files = [{'type': 'file', 'id': file_id}]
                print(f"📄 使用檔案進行 RAG 聊天: {os.path.basename(file_path)} | Using file for RAG chat: {os.path.basename(file_path)}")
        
        print(f"🤖 使用模型 | Using model: {model}")
        print(f"👤 您的問題 | Your question: {user_input}")
        
        response = self.chat_completion(model, messages, files, stream=True)
        
        if 'content' in response:
            return response['content']
        else:
            return "抱歉，無法獲取回應。| Sorry, unable to get response."
    
    def interactive_chat(self, model: str):
        """
        互動式聊天模式
        
        Args:
            model: 使用的模型
        """
        print(f"\n🎯 進入互動式聊天模式 (模型: {model}) | Entering interactive chat mode (model: {model})")
        print("💡 提示 | Tips:")
        print("   - 輸入 'quit' 或 'exit' 退出 | Type 'quit' or 'exit' to quit")
        print("   - 輸入 'upload <檔案路徑>' 上傳檔案並在下次對話中使用 | Type 'upload <file_path>' to upload a file")
        print("   - 輸入 'models' 查看可用模型 | Type 'models' to view available models")
        print("   - 輸入 'switch <模型名稱>' 切換模型 | Type 'switch <model_name>' to switch model")
        print("-" * 60)
        
        current_file_id = None
        
        while True:
            try:
                user_input = input("\n👤 您: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("👋 再見！| Goodbye!")
                    break
                
                if user_input.lower() == 'models':
                    models = self.get_available_models()
                    if models:
                        print("\n📋 可用模型 | Available models:")
                        for i, model_info in enumerate(models, 1):
                            model_name = model_info.get('id', 'Unknown')
                            print(f"   {i}. {model_name}")
                    else:
                        print("❌ 無法獲取模型列表 | Unable to get model list")
                    continue
                
                if user_input.lower().startswith('switch '):
                    new_model = user_input[7:].strip()
                    model = new_model
                    print(f"✅ 已切換到模型: {model} | Switched to model: {model}")
                    continue
                
                if user_input.lower().startswith('upload '):
                    file_path = user_input[7:].strip()
                    file_id = self.upload_file(file_path)
                    if file_id:
                        current_file_id = file_id
                        print(f"✅ 檔案已上傳，將在下次對話中使用 | File uploaded and will be used in next conversation")
                    continue
                
                # 準備檔案列表
                files = None
                if current_file_id:
                    files = [{'type': 'file', 'id': current_file_id}]
                
                # 發送聊天請求
                messages = [{'role': 'user', 'content': user_input}]
                response = self.chat_completion(model, messages, files, stream=True)
                
            except KeyboardInterrupt:
                print("\n👋 再見！| Goodbye!")
                break
            except Exception as e:
                print(f"❌ 發生錯誤: {e} | Error occurred: {e}")


def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='Open WebUI 聊天客戶端')
    parser.add_argument('--url', default=Config.get_base_url(), 
                       help=f'Open WebUI 服務 URL (預設: {Config.get_base_url()})')
    parser.add_argument('--api-key', help='API 金鑰 (也可透過 OPENWEBUI_API_KEY 環境變數設定)')
    parser.add_argument('--model', default=Config.get_default_model(), help=f'使用的模型 (預設: {Config.get_default_model()})')
    parser.add_argument('--file', help='要上傳的檔案路徑')
    parser.add_argument('--interactive', action='store_true', help='進入互動式聊天模式')
    parser.add_argument('--query', help='單次查詢文字')
    
    args = parser.parse_args()
    
    try:
        # 初始化聊天客戶端
        chat_client = OpenWebUIChat(args.url, args.api_key)
        
        # 顯示可用模型
        models = chat_client.get_available_models()
        if models:
            print("\n📋 可用模型 | Available models:")
            for model_info in models:
                if isinstance(model_info, dict):
                    model_name = model_info.get('id', 'Unknown')
                else:
                    model_name = str(model_info)
                print(f"   - {model_name}")
        
        if args.interactive:
            # 互動式模式
            chat_client.interactive_chat(args.model)
        elif args.query:
            # 單次查詢模式
            response = chat_client.simple_chat(args.model, args.query, args.file)
            print(f"\n🤖 AI 回應 | AI Response: {response}")
        else:
            # 預設進入互動式模式
            chat_client.interactive_chat(args.model)
            
    except ValueError as e:
        print(f"❌ 配置錯誤: {e} | Configuration error: {e}")
        print("💡 請設定 API 金鑰 | Please set API key:")
        print("   1. 使用 --api-key 參數 | Use --api-key parameter")
        print("   2. 或設定 OPENWEBUI_API_KEY 環境變數 | Or set OPENWEBUI_API_KEY environment variable")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 程式執行失敗: {e} | Program execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
