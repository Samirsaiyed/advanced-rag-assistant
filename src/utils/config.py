# Configuration manager

import os
from typing import Dict, Any
import yaml
from dataclasses import dataclass

@dataclass
class AppConfig:
    """Application configuration"""
    # Database settings
    persist_directory: str = "./advanced_chroma_db"
    collection_name: str = "advanced_knowledge_base"

    # Chunking settings
    chunk_size: int = 1000
    chunk_overlap = 200

    # Memory settings
    memory_type: str = "summary_buffer" # buffer, summary, window, summary_buffer
    max_memory_tokens: int = 1000
    memory_window_size: int = 10

    # Retrieval settings
    retrieval_k: int = 4
    search_type: str = "hybrid" # similarity, mmr, hybrid

    # LLM settings
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.0

    # UI settings
    page_title: str = "Advanced RAG Assistant"

class ConfigManager:
    """Manage application congiguration"""

    def __init__(self) -> None:
        self.config = AppConfig()
        self.load_config()

    def load_config(self):
        """Load the configuration from file if exists"""
        config_file = "config/app_config.yaml"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    yaml_config = yaml.safe_load(f)
                    for key, value in yaml_config.items():
                        if hasattr(self.config, key):
                            setattr(self.config, key, value)
            except Exception as e:
                print(f"Error loading config: {e}")

    def get_config(self)-> AppConfig:
        return self.config

    def update_config(self, **kwargs):
        """Update configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                
