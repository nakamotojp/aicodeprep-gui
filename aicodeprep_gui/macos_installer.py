import os
import shutil
import tempfile
import subprocess
import logging

# The workflow name, exactly as specified in the provided files.
WORKFLOW_NAME = "AICodePrep.workflow"
SERVICES_DIR = os.path.expanduser("~/Library/Services")

# This template is a direct copy of the provided `document.wflow` content.
# It calls 'aicp' directly, assuming it's in the PATH.
DOCUMENT_WFLOW_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>AMApplicationBuild</key>
	<string>528</string>
	<key>AMApplicationVersion</key>
	<string>2.10</string>
	<key>AMDocumentVersion</key>
	<string>2</string>
	<key>actions</key>
	<array>
		<dict>
			<key>action</key>
			<dict>
				<key>AMAccepts</key>
				<dict>
					<key>Container</key>
					<string>List</string>
					<key>Optional</key>
					<true/>
					<key>Types</key>
					<array>
						<string>com.apple.cocoa.string</string>
					</array>
				</dict>
				<key>AMActionVersion</key>
				<string>2.0.3</string>
				<key>AMApplication</key>
				<array>
					<string>Automator</string>
				</array>
				<key>AMParameterProperties</key>
				<dict>
					<key>COMMAND_STRING</key>
					<dict/>
					<key>CheckedForUserDefaultShell</key>
					<dict/>
					<key>inputMethod</key>
					<dict/>
					<key>shell</key>
					<dict/>
					<key>source</key>
					<dict/>
				</dict>
				<key>AMProvides</key>
				<dict>
					<key>Container</key>
					<string>List</string>
					<key>Types</key>
					<array>
						<string>com.apple.cocoa.string</string>
					</array>
				</dict>
				<key>ActionBundlePath</key>
				<string>/System/Library/Automator/Run Shell Script.action</string>
				<key>ActionName</key>
				<string>Run Shell Script</string>
				<key>ActionParameters</key>
				<dict>
					<key>COMMAND_STRING</key>
					<string>#!/bin/bash
# Ensure exactly one folder is selected
if [ "$#" -ne 1 ]; then
  osascript -e 'display dialog "Select exactly ONE folder." buttons {"OK"} default button 1'
  exit 1
fi

# Get the folder path
FOLDER_PATH="$1"

# Open Terminal and run the command visibly
osascript <<EOD
tell application "Terminal"
  activate
  do script "aicp '$FOLDER_PATH'"
end tell
EOD</string>
					<key>CheckedForUserDefaultShell</key>
					<true/>
					<key>inputMethod</key>
					<integer>1</integer>
					<key>shell</key>
					<string>/bin/bash</string>
					<key>source</key>
					<string></string>
				</dict>
				<key>BundleIdentifier</key>
				<string>com.apple.RunShellScript</string>
				<key>CFBundleVersion</key>
				<string>2.0.3</string>
				<key>CanShowSelectedItemsWhenRun</key>
				<false/>
				<key>CanShowWhenRun</key>
				<true/>
				<key>Category</key>
				<array>
					<string>AMCategoryUtilities</string>
				</array>
				<key>Class Name</key>
				<string>RunShellScriptAction</string>
				<key>InputUUID</key>
				<string>BD3EC33B-803C-414A-853D-C6C14C401602</string>
				<key>Keywords</key>
				<array>
					<string>Shell</string>
					<string>Script</string>
					<string>Command</string>
					<string>Run</string>
					<string>Unix</string>
				</array>
				<key>OutputUUID</key>
				<string>E67DCBB2-F6AF-4A82-8B48-5656193C9F2D</string>
				<key>UUID</key>
				<string>725FD07E-C1D8-4B66-8B0D-751256D26C99</string>
				<key>UnlocalizedApplications</key>
				<array>
					<string>Automator</string>
				</array>
				<key>arguments</key>
				<dict>
					<key>0</key>
					<dict>
						<key>default value</key>
						<integer>0</integer>
						<key>name</key>
						<string>inputMethod</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>0</string>
					</dict>
					<key>1</key>
					<dict>
						<key>default value</key>
						<false/>
						<key>name</key>
						<string>CheckedForUserDefaultShell</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>1</string>
					</dict>
					<key>2</key>
					<dict>
						<key>default value</key>
						<string></string>
						<key>name</key>
						<string>source</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>2</string>
					</dict>
					<key>3</key>
					<dict>
						<key>default value</key>
						<string></string>
						<key>name</key>
						<string>COMMAND_STRING</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>3</string>
					</dict>
					<key>4</key>
					<dict>
						<key>default value</key>
						<string>/bin/sh</string>
						<key>name</key>
						<string>shell</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>4</string>
					</dict>
				</dict>
				<key>isViewVisible</key>
				<integer>1</integer>
				<key>location</key>
				<string>332.000000:305.000000</string>
				<key>nibPath</key>
				<string>/System/Library/Automator/Run Shell Script.action/Contents/Resources/Base.lproj/main.nib</string>
			</dict>
			<key>isViewVisible</key>
			<integer>1</integer>
		</dict>
	</array>
	<key>connectors</key>
	<dict/>
	<key>workflowMetaData</key>
	<dict>
		<key>applicationBundleID</key>
		<string>com.apple.finder</string>
		<key>applicationBundleIDsByPath</key>
		<dict>
			<key>/System/Library/CoreServices/Finder.app</key>
			<string>com.apple.finder</string>
		</dict>
		<key>applicationPath</key>
		<string>/System/Library/CoreServices/Finder.app</string>
		<key>applicationPaths</key>
		<array>
			<string>/System/Library/CoreServices/Finder.app</string>
		</array>
		<key>inputTypeIdentifier</key>
		<string>com.apple.Automator.fileSystemObject.folder</string>
		<key>outputTypeIdentifier</key>
		<string>com.apple.Automator.nothing</string>
		<key>presentationMode</key>
		<integer>15</integer>
		<key>processesInput</key>
		<false/>
		<key>serviceApplicationBundleID</key>
		<string>com.apple.finder</string>
		<key>serviceApplicationPath</key>
		<string>/System/Library/CoreServices/Finder.app</string>
		<key>serviceInputTypeIdentifier</key>
		<string>com.apple.Automator.fileSystemObject.folder</string>
		<key>serviceOutputTypeIdentifier</key>
		<string>com.apple.Automator.nothing</string>
		<key>serviceProcessesInput</key>
		<false/>
		<key>systemImageName</key>
		<string>NSActionTemplate</string>
		<key>useAutomaticInputType</key>
		<false/>
		<key>workflowTypeIdentifier</key>
		<string>com.apple.Automator.servicesMenu</string>
	</dict>
</dict>
</plist>
"""

# This template is a direct copy of the provided `Info.plist` content.
INFO_PLIST_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>NSServices</key>
	<array>
		<dict>
			<key>NSBackgroundColorName</key>
			<string>background</string>
			<key>NSIconName</key>
			<string>NSActionTemplate</string>
			<key>NSMenuItem</key>
			<dict>
				<key>default</key>
				<string>AICodePrep</string>
			</dict>
			<key>NSMessage</key>
			<string>runWorkflowAsService</string>
			<key>NSRequiredContext</key>
			<dict>
				<key>NSApplicationIdentifier</key>
				<string>com.apple.finder</string>
			</dict>
			<key>NSSendFileTypes</key>
			<array>
				<string>public.folder</string>
			</array>
		</dict>
	</array>
</dict>
</plist>
"""

def install_quick_action():
    """Generates and installs the macOS Quick Action by creating the workflow files directly."""
    try:
        # Create the .workflow bundle structure in a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            workflow_path = os.path.join(temp_dir, WORKFLOW_NAME)
            contents_path = os.path.join(workflow_path, "Contents")
            os.makedirs(contents_path, exist_ok=True)

            # Write the static `document.wflow` file. No path formatting is needed.
            with open(os.path.join(contents_path, "document.wflow"), "w", encoding="utf-8") as f:
                f.write(DOCUMENT_WFLOW_TEMPLATE)

            # Write the static `Info.plist` file.
            with open(os.path.join(contents_path, "Info.plist"), "w", encoding="utf-8") as f:
                f.write(INFO_PLIST_TEMPLATE)
            
            # Ensure the destination directory exists
            os.makedirs(SERVICES_DIR, exist_ok=True)
            
            # Move the generated workflow to the user's Services directory
            dest_path = os.path.join(SERVICES_DIR, WORKFLOW_NAME)
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)  # Remove old version if it exists
            
            shutil.move(workflow_path, SERVICES_DIR)

        # Refresh system services to make the Quick Action appear immediately.
        # This is a best-effort attempt. A logout/login cycle is the most reliable way.
        try:
            subprocess.run(["/System/Library/CoreServices/pbs", "-flush"], check=False, timeout=5)
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logging.warning(f"Could not flush services cache with 'pbs': {e}. A restart may be required.")
        
        subprocess.run(["/usr/bin/killall", "Finder"], check=False)

        msg = (f"Quick Action '{WORKFLOW_NAME}' installed successfully.\n\n"
               "It should now appear when you right-click a folder in Finder (under 'Quick Actions' or 'Services').")
        logging.info(msg)
        return True, msg

    except Exception as e:
        msg = f"Failed to install Quick Action: {e}"
        logging.error(msg)
        return False, msg

def uninstall_quick_action():
    """Removes the macOS Quick Action from the user's Library."""
    dest_path = os.path.join(SERVICES_DIR, WORKFLOW_NAME)
    if os.path.exists(dest_path):
        try:
            shutil.rmtree(dest_path)
            # Attempt to refresh services to make the change immediate
            try:
                subprocess.run(["/System/Library/CoreServices/pbs", "-flush"], check=False, timeout=5)
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                 logging.warning(f"Could not flush services cache during uninstall: {e}")
            msg = f"Quick Action '{WORKFLOW_NAME}' has been uninstalled."
            logging.info(msg)
            return True, msg
        except Exception as e:
            msg = f"Failed to uninstall Quick Action: {e}"
            logging.error(msg)
            return False, msg
    else:
        msg = "Quick Action was not found (already uninstalled)."
        logging.info(msg)
        return True, msg