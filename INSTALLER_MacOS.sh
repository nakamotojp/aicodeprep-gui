#!/bin/bash

# ============================================================================
# aicodeprep-gui Installer for macOS
# ============================================================================
# This script automates the installation of aicodeprep-gui using Homebrew
# and pipx, which is the most robust method for macOS.
# ============================================================================

# Function to print and log messages
LOG_FILE="install_log_macos.txt"
log() {
    echo "$1" | tee -a "$LOG_FILE"
}

# Ensure the log file is clean on new run
> "$LOG_FILE"

log "--- Starting aicodeprep-gui Installer for macOS ---"
log "--- $(date) ---"
log ""

# Stop script on any error
set -e

# --- Step 1: Check for Homebrew ---
log "Step 1: Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
    log "ERROR: Homebrew is not installed. Homebrew is the recommended package manager for macOS and is required by this script."
    log ""
    log "To install Homebrew, open a new Terminal window and run this command:"
    log '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    log ""
    log "After Homebrew is installed, please run this script again."
    exit 1
fi
log "Homebrew is installed."
log ""

# --- Step 2: Install/Upgrade Pipx using Homebrew ---
log "Step 2: Installing/upgrading pipx via Homebrew..."
log "pipx is a tool to install Python applications in isolated environments."
log "This may take a moment and might ask for your password..."
brew install pipx
log "pipx installed successfully."
log ""

# --- Step 3: Add Pipx to PATH ---
log "Step 3: Ensuring pipx is in your system's PATH..."
pipx ensurepath
log "pipx paths are configured. The output above gives details."
log ""

# --- Step 4: Install aicodeprep-gui ---
log "Step 4: Installing aicodeprep-gui..."
log "This may take a minute or two..."
pipx install aicodeprep-gui

log ""
log "============================================================================"
log "  SUCCESS! aicodeprep-gui has been installed."
log "============================================================================"
log ""
log "  IMPORTANT: You MUST close this Terminal window and open a NEW one"
log "  for the changes to take effect."
log ""
log "  After opening a new terminal, you can run the app from any"
log "  folder by typing:"
log "  aicp"
log ""
log "============================================================================"
log "Installation script finished."

# Unset error checking to prevent exit on non-zero from here
set +e
exit 0