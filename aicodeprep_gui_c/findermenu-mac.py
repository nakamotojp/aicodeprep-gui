import os
import sys
import plistlib
import subprocess
from pathlib import Path
import uuid

class FinderServiceManager:
    def __init__(self, service_name, command):
        self.service_name = service_name
        self.command = command
        self.service_dir = Path(f"~/Library/Services/{service_name}.workflow").expanduser()
        self.contents_dir = self.service_dir / "Contents"
        self.info_plist_path = self.contents_dir / "Info.plist"
        self.document_plist_path = self.contents_dir / "document.wflow"

    def create_service(self):
        """Create the service directory structure and required files"""
        try:
            # Create directory structure
            self.contents_dir.mkdir(parents=True, exist_ok=True)

            # Create Info.plist with proper service configuration
            info_plist = {
                'NSServices': [{
                    'NSMenuItem': {'default': self.service_name},
                    'NSMessage': 'runWorkflowAsService',
                    'NSReturnTypes': [],
                    'NSIconName': 'NSActionTemplate',
                    'NSKeyEquivalent': {'default': 'p'},
                    'NSModifiers': {'default': 1048576},  # Command key
                    'NSUserData': f'com.yourdomain.{self.service_name}',
                    'NSSendFileTypes': ['public.item'],
                    'NSRequiredContext': {
                        'NSTextContent': 'FilePath',
                        'NSServiceCategory': 'public.item'
                    }
                }]
            }

            with open(self.info_plist_path, 'wb') as f:
                plistlib.dump(info_plist, f)

            # Create document.wflow with improved command handling and logging
            document_plist = {
                'AMApplicationBuild': "523",
                'AMApplicationVersion': "2.10",
                'AMDocumentVersion': "2",
                'actions': [{
                    'action': {
                        'AMAccepts': {
                            'container': ['List'],
                            'optional': True,
                            'types': ['public.item']
                        },
                        'AMActionVersion': "2.0.1",
                        'AMApplication': [],
                        'AMParameterProperties': {
                            'COMMAND_STRING': {
                                'isViewVisible': True,
                                'name': 'command',
                                'label': 'Command:'
                            },
                            'CheckedForUserDefaultShell': {
                                'isViewVisible': False,
                                'name': 'checkedForUserDefaultShell',
                                'label': 'Checked for User Default Shell:'
                            },
                            'inputMethod': {
                                'isViewVisible': False,
                                'name': 'inputMethod',
                                'label': 'Input Method:'
                            },
                            'source': {
                                'isViewVisible': True,
                                'name': 'source',
                                'label': 'Source:'
                            },
                            'shell': {
                                'isViewVisible': True,
                                'name': 'shell',
                                'label': 'Shell:'
                            },
                            'passinput': {
                                'isViewVisible': True,
                                'name': 'passinput',
                                'label': 'Pass Input:'
                            }
                        },
                        'AMProvides': {
                            'container': ['List'],
                            'types': ['public.item']
                        },
                        'AMRequiredResources': [],
                        'ActionBundlePath': '/System/Library/Automator/Run Shell Script.action',
                        'ActionName': 'Run Shell Script',
                        'ActionParameters': {
                            'COMMAND_STRING': self.command,
                            'CheckedForUserDefaultShell': True,
                            'inputMethod': 'as arguments',
                            'SOURCE_CODE': '',
                            'SHELL_PATH': '/bin/zsh',
                            'passinput': True
                        },
                        'BundleIdentifier': 'com.apple.Automator.RunShellScript',
                        'CFBundleVersion': '2.0.1',
                        'CanShowSelectedItemsWhenRun': True,
                        'CanShowWhenRun': True,
                        'Category': 'Files & Folders',
                        'Class': 'RunShellScriptAction',
                        'InputUUID': str(uuid.uuid4()).upper(),
                        'Keywords': ['Run', 'Shell', 'Script', 'Execute'],
                        'OutputUUID': str(uuid.uuid4()).upper(),
                        'UUID': str(uuid.uuid4()).upper(),
                        'ShowWhenRun': False,
                        'StartAsProcess': False,
                        'StartAsJob': True,
                        'CheckedForUserDefaultShell': True,
                        'RunInBackground': False,
                    }
                }]
            }

            with open(self.document_plist_path, 'wb') as f:
                plistlib.dump(document_plist, f)

            # Ensure correct permissions
            subprocess.run(['chmod', '-R', '755', str(self.service_dir)])

            # Force system to reload services
            subprocess.run(['/System/Library/CoreServices/pbs', '-update'])
            subprocess.run(['killall', 'Finder'])

            print(f"Successfully created Finder service: {self.service_name}")
            print("\nTo enable the service:")
            print("1. Open System Settings")
            print("2. Go to Keyboard > Keyboard Shortcuts > Services")
            print("3. Find and enable '{self.service_name}' under Files and Folders")
            print("\nNote: You may need to log out and back in for changes to take effect")
            return True

        except Exception as e:
            print(f"Error creating service: {e}", file=sys.stderr)
            return False

    def remove_service(self):
        """Remove the service"""
        try:
            if self.service_dir.exists():
                subprocess.run(['rm', '-rf', str(self.service_dir)])
                print(f"Successfully removed service: {self.service_name}")

                # Force system to reload services
                subprocess.run(['/System/Library/CoreServices/pbs', '-update'])
                subprocess.run(['killall', 'Finder'])
                return True
            else:
                print(f"Service not found: {self.service_name}")
                return False
        except Exception as e:
            print(f"Error removing service: {e}", file=sys.stderr)
            return False
            
def main():
    # Command that opens Terminal and runs the app with the selected file/folder
    command = """
#!/bin/zsh

# Log file for debugging
LOG_FILE="$HOME/aicodeprep_service.log"

# Log start time and arguments
echo "$(date): Service started" >> "$LOG_FILE"
echo "Current directory: $PWD" >> "$LOG_FILE"
echo "Arguments: $@" >> "$LOG_FILE"

# Function to handle paths with spaces
handle_path() {
    local path="$1"
    # Remove any file:// prefix and decode URL encoding
    path="${path#file://}"
    path="$(python3 -c 'import sys, urllib.parse; print(urllib.parse.unquote(sys.argv[1]))' "$path")"
    echo "$path"
}

# Process each input path
for filepath in "$@"; do
    path=$(handle_path "$filepath")
    echo "Processing path: $path" >> "$LOG_FILE"
    
    # Create AppleScript to open Terminal in the correct directory
    osascript <<EOF
tell application "Terminal"
    activate
    do script "cd \\"$(dirname "$path")\\" && /usr/bin/env python3 -m aicodeprep_gui_c \\"$path\\" 2>&1 | tee -a \\"$LOG_FILE\\"; exec /bin/zsh"
end tell
EOF
done
"""

    manager = FinderServiceManager("AI Code Prep", command)

    if len(sys.argv) > 1:
        if sys.argv[1] == '--remove':
            manager.remove_service()
        elif sys.argv[1] == '--add':
            manager.create_service()
        else:
            print("Usage: script.py --add|--remove")
    else:
        print("Usage: script.py --add|--remove")

if __name__ == "__main__":
    main()