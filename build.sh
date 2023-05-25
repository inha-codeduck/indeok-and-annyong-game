#!/bin/bash

DIST_DIR="dist"
APP_NAME="Indeok-and-annyong-game"
ZIP_FILE="${APP_NAME}-${VERSION}.zip"
PYTHON_VERSION=$(python -V 2>&1)

echo "Python version: $PYTHON_VERSION"

install_pyinstaller() {
    # Install pyinstaller
    echo "Installing pyinstaller..."
    pip install pyinstaller
}

# If Python is already installed
if [[ $PYTHON_VERSION == "Python"* ]]; then
  echo "Python is already installed."
else
  # Install Python using Homebrew on macOS
  if [[ $(uname) == "Darwin" ]]; then
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
      echo "Homebrew is not installed. Installing Homebrew..."
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
      echo "Homebrew is already installed."
    fi
    
    # Install Python
    echo "Installing Python using Homebrew..."
    brew install python

    install_pyinstaller

    # Create .app file
    pyinstaller --onefile --name "Indeok-and-annyong-game" --windowed --icon=icon.icns your_script.py
  fi
  
  # Install Python using Chocolatey on Windows
  if [[ $(uname) == "MINGW"* ]]; then
    # Check if Chocolatey is installed
    if ! command -v choco &> /dev/null; then
      echo "Chocolatey is not installed. Installing Chocolatey..."
      powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    else
      echo "Chocolatey is already installed."
    fi
    
    # Install Python
    echo "Installing Python using Chocolatey..."
    choco install python -y

    install_pyinstaller

    # Create .exe file
    pyinstaller --onefile --name Indeok-and-annyong-game.exe your_script.py
  fi
fi

cd ${DIST_DIR}

# Move .exe file to distribution directory
mv "Indeok-and-annyong-game.exe" "${APP_NAME}"

# Move .app file to distribution directory
mv "Indeok-and-annyong-game.app" "${APP_NAME}.app"

# Compress distribution directory
zip -r ${ZIP_FILE} "${APP_NAME}.app" "${APP_NAME}"

# Print final .zip file path
echo "Build complete: ${DIST_DIR}/${ZIP_FILE}"
