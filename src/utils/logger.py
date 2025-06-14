# Logging setup

import logging
import os
from datetime import datetime

class Logger:
    """Application logger"""

    def __init__(self, name: str = "AdvancedRAG"):
        self.logger = logging.getLogger(name)
        self.setup_logger()

    def setup_loader(self):
        """Setup logging configuration"""
        if not self.logger.handlers:
            # Create logs directory
            os.makedirs("logs", exist_ok=True)
            
            # File Handler
            log_file = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)

            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_handler)
            console_handler.setFormatter(formatter)

            # Add handlers
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            self.logger.setLevel(logging.INFO)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def debug(self, message: str):
        self.logger.debug(message)