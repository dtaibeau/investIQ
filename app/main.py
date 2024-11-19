import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ui.streamlit_ui import main as streamlit_main

if __name__ == "__main__":
    streamlit_main()
