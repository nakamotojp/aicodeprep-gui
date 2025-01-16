import os
import sys
import plistlib
import subprocess
from pathlib import Path

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
            
            # Create Info.plist
            info_plist = {
                'NSServices': [{
                    'NSMenuItem': {'default': self.service_name},
                    'NSMessage': 'runWorkflowAsService',
                    'NSRequiredContext': {'NSTextContent': 'FilePath'},
                    'NSSendFileTypes': ['public.item']
                }]
            }
            
            with open(self.info_plist_path, 'wb') as f:
                plistlib.dump(info_plist, f)

            # Create document.wflow
            document_plist = {
                'AMApplicationBuild': "523",
                'AMApplicationVersion': "2.10",
                'AMDocumentVersion': "2",
                'actions': [{
                    'action': {
                        'AMAccepts': {
                            'container': ['List'],
                            'optional': False,
                            'types': ['com.apple.cocoa.path']
                        },
                        'AMActionVersion': "2.0.1",
                        'AMApplication': {
                            'type': 'file',
                            'bundleidentifier': 'com.apple.Terminal',
                            'name': 'Terminal',
                            'version': 'unknown'
                        },
                        'AMParameterProperties': {
                            'command': {
                                'isRequired': True,
                                'type': 'string'
                            }
                        },
                        'AMProvides': {
                            'container': ['List'],
                            'types': ['com.apple.cocoa.path']
                        },
                        'AMRequiredResources': [],
                        'ActionBundlePath': '/System/Library/Automator/Run Shell Script.action',
                        'ActionName': 'Run Shell Script',
                        'ActionParameters': {
                            'COMMAND_STRING': self.command,
                            'SHELL_PATH': '/bin/bash',
                            'SOURCE_CODE': ''
                        },
                        'BundleIdentifier': 'com.apple.Automator.RunShellScript',
                        'CFBundleVersion': '2.0.1',
                        'CanShowSelectedItemsWhenRun': True,
                        'CanShowWhenRun': True,
                        'Category': 'Utilities',
                        'Class': 'RunShellScriptAction',
                        'InputUUID': '{}',
                        'Keywords': ['Run', 'Shell', 'Script'],
                        'OutputUUID': '{}',
                        'ShowWhenRun': 1,
                        'StartsOnWorkspace': False,
                        'UUID': '{}',
                    }
                }]
            }
            
            with open(self.document_plist_path, 'wb') as f:
                plistlib.dump(document_plist, f)

            # Ensure correct permissions
            subprocess.run(['chmod', '-R', '755', str(self.service_dir)])
            
            # Restart Finder to load the new service
            subprocess.run(['killall', 'Finder'])
            
            print(f"Successfully created Finder service: {self.service_name}")
            print("Please check System Preferences > Keyboard > Shortcuts > Services")
            print("to ensure the service is enabled.")
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
                
                # Restart Finder to unload the service
                subprocess.run(['killall', 'Finder'])
                return True
            else:
                print(f"Service not found: {self.service_name}")
                return False
        except Exception as e:
            print(f"Error removing service: {e}", file=sys.stderr)
            return False

def main():
    # Example command that runs your Python module with the selected file
    command = """for f in "$@"
do
    /usr/bin/env python3 -m aicodeprep_gui_c "$f"
done"""

    manager = FinderServiceManager("AI Code Prep GUI", command)
    
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