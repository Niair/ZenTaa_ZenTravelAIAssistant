#!/usr/bin/env python3
"""
Streamlit runner script for ZenTravel AI Assistant
"""

import os
import sys
import subprocess

def main():
    """Run the Streamlit app"""
    streamlit_app_path = os.path.join(os.path.dirname(__file__), 'app', 'app.py')
    
    if not os.path.exists(streamlit_app_path):
        print(f"❌ Streamlit app not found at: {streamlit_app_path}")
        print("Please make sure the app directory and streamlit_app.py exist.")
        return
    
    print("🚀 Starting ZenTravel AI Assistant...")
    print("📱 Opening Streamlit interface...")
    print("⏳ Please wait for the browser to open automatically...")
    print("💡 If the browser doesn't open, go to: http://localhost:8501")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_app_path])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")

if __name__ == "__main__":
    main()