# Input validation

import re
from typing import List, Optional
import streamlit as st

class InputValidator:
    """Validate user inputs"""

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate OpenAI key format"""
        if not api_key.startswith('sk-'):
            return False
        
        if len(api_key) < 40:
            return False
        
        return True
    
    @staticmethod
    def validate_files(uploaded_files)-> tuple[bool, str]:
        """Validate uploaded files"""
        if not uploaded_files:
            return False, "No files uploaded"

        supported_extenstions = ['.pdf', '.txt', '.docx', '.md']
        max_file_size = 10 * 1024 * 1024 # 10MB

        for file in uploaded_files:
            
            # Check file extension
            file_ext = '.' + file.name.split('.')[-1].lower()
            if file_ext not in supported_extenstions:
                return False, f"Unsupported file type: {file.name}"

            # Check file size
            if hasattr(file, 'size') and file.size > max_file_size:
                return False, f"File too large: {file.name} (max 10MB)"

        return True, "File validated successfully"

    @staticmethod
    def validate_query(query: str)->tuple[bool, str]:
        """Validate user query"""
        if not query or not query.strip():
            return False, "Query cannot be empty"

        if len(query.strip()) < 3:
            return False, "Query too short (minimum 3 characters)"
        
        if len(query) > 1000:
            return False, "Query is too long (maximum 1000 characters)"

        return True, "Query validated sucessfully"
        
