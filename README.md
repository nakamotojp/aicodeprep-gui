This is NOT ready so this readme is for the older exe installer which is at wuu73.org/aicp 
But you can still get it working by downloading this, cd into the folder, type:
"pip install -e ."
After package is installed, cd into the aicodeprep_gui_c folder, type:
"python regmenu_gui.py"
if that doesn't work for some reason try looking at the other regmenu-win.py file, 
enabling classic menu gets rid of the usual "extra step" you would need to do to get to the AI Code Prep actual menu. The default Windows 11 menu is the annoying one that doesn't show every option. You should enable classic menu then add context menu, if having issues just paste the whole script into ChatGPT and ask it how to do it.

Most people say this works fine but one person said the menu won't install for them and I have no idea why, can't replicate it, so can't figure out why that would happen but feel free to let me know if it does!

aicodeprep-gui (AI Code Prep GUI)

aicodeprep is now a GUI application designed to streamline the process of sharing your project's code with AI chatbots. It allows you to quickly gather code files into a single text file and copy the content to your clipboard, making it easy to paste into AI chatbots for coding assistance.

Purpose

The main goal of aicodeprep is to expedite the process of preparing and sharing your project code with AI chatbots. With the new GUI, you can effortlessly select and manage files to include, simplifying your workflow.

Features

Right-Click Context Menu: After installation, you can right-click in any Windows folder to open the GUI.
Pre-Checked Files: The GUI automatically checks relevant files, with options to modify selections.
Easy Processing: Click "Process Selected" to compile code into fullcode.txt and copy it to the clipboard.
Installation

Windows Installation

Double Click install file and follow instructions, standard type of Windows install wizard.

Usage

Once installed, right-click in a folder that has code or subfolders with code, project folder etc window to run aicodeprep-gui. The GUI will launch, showing pre-checked files. Adjust selections as needed, then click "Process Selected" to generate fullcode.txt and copy to clipboard.

Optional Configuration (rarely needed)

Customize behavior by modifying default_config.yaml or create an aicodeprep_config.yaml which is in the data folder in the folder where you installed aicodeprep-gui (usually Program Files/AICodePrep-GUI/data)

Donations/Tips:

Bitcoin: bc1qkuwhujaxhzk7e3g4f3vekpzjad2rwlh9usagy6
Litecoin: ltc1q3z327a3ea22mlhtawmdjxmwn69n65a32fek2s4
Monero: 46FzbFckBy9bbExzwAifMPBheYFb37k8ghGWSHqc6wE1BiEz6rQc2f665JmqUdtv1baRmuUEcDoJ2dpqY6Msa3uCKArszQZ
Cashapp: $lightweb73

Share any bugs, improvement ideas! wuu73@yahoo.com
