import os
import sys
import subprocess

# Function to run the Streamlit app
def run_streamlit():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == '__main__':
    run_streamlit()
