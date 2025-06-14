# Entry point

import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.streamlit_app import main as run_app

if __name__ == "main":
    run_app()