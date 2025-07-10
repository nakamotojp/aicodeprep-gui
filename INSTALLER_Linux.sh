#!/bin/bash

# ============================================================================
# aicodeprep-gui Installer for Linux
# ============================================================================
# This script attempts to automate the installation of aicodeprep-gui.
# It detects the package manager to install Python dependencies if needed,
# then uses pipx to install the application.
# ============================================================================

# Function to print and log messages
LOG_FILE="install_log_linux.txt"
log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# Ensure the log file is clean on new run
> "$LOG_FILE"

log "--- Starting aicodeprep-gui Installer for Linux ---"
log "--- $(date) ---"
log ""

# Stop script on any error
set -e

# --- Step 1: Detect Package Manager and Install Dependencies ---
log "Step 1: Checking for dependencies (python3, python3-pip)..."

if ! command -v python3 &> /dev/null || ! python3 -m pip --version &> /dev/null; then
    log "Python3 or pip is missing. Attempting to install them."
    log "This will require administrative privileges (sudo) and will ask for your password."

    if command -v apt-get &> /dev/null; then
        log "Detected Debian/Ubuntu based system (apt)."
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip
    elif command -v dnf &> /dev/null; then
        log "Detected Fedora/CentOS based system (dnf)."
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        log "Detected Arch based system (pacman)."
        sudo pacman -Syu --noconfirm python python-pip
    elif command -v zypper &> /dev/null; then
        log "Detected OpenSUSE based system (zypper)."
        sudo zypper install -y python3 python3-pip
    else
        log "\nERROR: Could not detect a supported package manager (apt, dnf, pacman, zypper)."
        log "Please install 'python3' and 'python3-pip' manually using your system's package manager, then run this script again."
        exit 1
    fi
    log "Dependencies should now be installed."
else
    log "Dependencies (python3 and pip) are already installed."
fi
log ""

# --- Step 2: Install/Upgrade Pipx ---
log "Step 2: Installing/upgrading pipx..."
log "pipx is a tool to install Python applications in isolated environments."
python3 -m pip install --user --upgrade pipx
log "pipx installed successfully."
log ""

# --- Step 3: Add Pipx to PATH ---
log "Step 3: Ensuring pipx is in your system's PATH..."
# Note: pipx ensurepath returns a non-zero exit code if paths are already present,
# which would stop the script if `set -e` is active. So we run it carefully.
set +e
python3 -m pipx ensurepath
set -e
log "pipx paths are configured. The output above gives details."
log "You might need to add the indicated directory to your ~/.bashrc or ~/.zshrc file if it's not already there."
log ""


# --- Step 4: Install aicodeprep-gui ---
log "Step 4: Installing aicodeprep-gui..."
log "This may take a minute or two..."
# The PATH might not be updated in this current session, so we call pipx via python
python3 -m pipx install aicodeprep-gui

log ""
log "============================================================================"
log "  SUCCESS! aicodeprep-gui has been installed."
log "============================================================================"
log ""
log "  \e[1m\e[31mIMPORTANT:\e[0m You MUST close this Terminal window and open a NEW one"
log "  for the changes to take effect."
log ""
log "  After opening a new terminal, you can run the app from any"
log "  folder by typing:"
log "  \e[1maicp\e[0m"
log ""
log "============================================================================"
log "Installation script finished."

# Unset error checking
set +e
exit 0