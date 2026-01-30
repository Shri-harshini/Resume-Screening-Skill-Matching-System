import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package}: {e}")
        return False

def setup_environment():
    print("=" * 60)
    print("Setting up Resume Screening System...")
    print("=" * 60)
    
    # Create necessary directories
    print("\nCreating directories...")
    Path("uploads").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    
    # Install required packages
    print("\nInstalling required packages...")
    with open("requirements.txt") as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    success = True
    for package in packages:
        if not install_package(package):
            success = False
    
    if not success:
        print("\nWarning: Some packages failed to install. The application may not work correctly.")
    
    # Install spaCy model
    print("\nDownloading spaCy model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("Successfully downloaded spaCy model")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading spaCy model: {e}")
        print("You can install it manually with: python -m spacy download en_core_web_sm")
    
    # Download NLTK data
    print("\nDownloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        print("Successfully downloaded NLTK data")
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")
        print("You may need to install NLTK data manually.")
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Setup completed successfully!")
    else:
        print("⚠️  Setup completed with some warnings. See above for details.")
    
    print("\nTo run the application, use:")
    print("  streamlit run app.py")
    print("\nThen open your browser and go to: http://localhost:8501")
    print("=" * 60)

if __name__ == "__main__":
    setup_environment()
