#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open WebUI 聊天客戶端配置檔案
"""

import os
from typing import Optional


class Config:
    """配置類別"""
    
    # Open WebUI 服務設定
    DEFAULT_BASE_URL = "http://localhost:8080/"
    DEFAULT_MODEL = "gemma3:1b"
    
    # API 金鑰設定
    API_KEY_ENV_VAR = "OPENWEBUI_API_KEY"
    DEFAULT_API_KEY = "sk-aa929c3a9e0c4ec5bc23a5909e3c367c"
    
    # 檔案上傳設定
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_FILE_TYPES = [
        '.txt', '.pdf', '.docx', '.doc', '.md', '.json', '.csv', '.xml',
        '.html', '.htm', '.rtf', '.odt', '.epub', '.mobi'
    ]
    
    # 聊天設定
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 2048
    DEFAULT_STREAM = True
    
    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """獲取 API 金鑰"""
        return os.getenv(cls.API_KEY_ENV_VAR) or cls.DEFAULT_API_KEY
    
    @classmethod
    def get_base_url(cls) -> str:
        """獲取基礎 URL"""
        return os.getenv('OPENWEBUI_BASE_URL', cls.DEFAULT_BASE_URL)
    
    @classmethod
    def get_default_model(cls) -> str:
        """獲取預設模型"""
        return os.getenv('OPENWEBUI_DEFAULT_MODEL', cls.DEFAULT_MODEL)
    
    @classmethod
    def is_file_type_allowed(cls, file_path: str) -> bool:
        """檢查檔案類型是否允許"""
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in cls.ALLOWED_FILE_TYPES
    
    @classmethod
    def get_file_size(cls, file_path: str) -> int:
        """獲取檔案大小"""
        try:
            return os.path.getsize(file_path)
        except OSError:
            return 0
    
    @classmethod
    def is_file_size_valid(cls, file_path: str) -> bool:
        """檢查檔案大小是否有效"""
        return cls.get_file_size(file_path) <= cls.MAX_FILE_SIZE
