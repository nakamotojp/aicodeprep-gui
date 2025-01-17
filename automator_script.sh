#!/bin/zsh

# Log file for debugging
LOG_FILE="$HOME/aicodeprep_service.log"

# Log start time and arguments
/bin/date >> "$LOG_FILE"
echo "Current directory: $PWD" >> "$LOG_FILE"
echo "Arguments: $@" >> "$LOG_FILE"

# Function to handle paths with spaces
handle_path() {
    local path="$1"
    # Remove any file:// prefix and decode URL encoding
    path="${path#file://}"
    path="$(/usr/local/bin/python3 -c 'import sys, urllib.parse; print(urllib.parse.unquote(sys.argv[1]))' "$path")"
    echo "$path"
}

# Process each input path
for filepath in "$@"; do
    path=$(handle_path "$filepath")
    echo "Processing path: $path" >> "$LOG_FILE"
    
    # Create AppleScript to open Terminal in the correct directory
    /usr/bin/osascript <<EOF
tell application "Terminal"
    activate
    do script "cd \"$(/usr/bin/dirname "$path")\" && /usr/local/bin/python3 -c 'import aicodeprep_gui_c.main; aicodeprep_gui_c.main.main()' \"$path\" 2>&1 | tee -a \"$LOG_FILE\"; exec /bin/zsh"
end tell
EOF
done