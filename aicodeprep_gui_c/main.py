import os
import sys
import argparse
import logging
from typing import List
from aicodeprep_gui_c.smart_logic import collect_all_files, load_default_config, load_user_config
from aicodeprep_gui_c.gui import show_file_selection_gui

# Configure logging with explicit console handler only
logger = logging.getLogger()

# Remove any existing handlers to prevent duplicate logging
for handler in logger.handlers:
    logger.removeHandler(handler)

logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add handler to root logger
logger.addHandler(console_handler)

def main():
    parser = argparse.ArgumentParser(description="Concatenate code files into a single text file.")
    parser.add_argument("-n", "--no-copy", action="store_true",
                        help="Do NOT copy output to clipboard (default: copy to clipboard)")
    parser.add_argument("-o", "--output", default="fullcode.txt",
                        help="Output file name (default: fullcode.txt)")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug logging")
    parser.add_argument("directory", nargs="?", default=".",
                        help="Directory to process (default: current directory)")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)

    # Get the target directory from command line argument (%V)
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    logger.info(f"Target directory: {target_dir}")

    # Change to the specified directory with error handling
    try:
        os.chdir(target_dir)
    except FileNotFoundError:
        logger.error(f"Directory not found: {target_dir}")
        return
    except Exception as e:
        logger.error(f"Error changing directory: {e}")
        return

    logger.info("Starting code concatenation...")

    all_files_with_flags = collect_all_files()

    if not all_files_with_flags:
        logger.warning("No files found to process!")
        return

    action, _ = show_file_selection_gui(all_files_with_flags)

    if action != 'quit':
        logger.info("Buy my cat a treat, comments, ideas for improvement appreciated: ")
        logger.info("https://wuu73.org/hello.html")

if __name__ == "__main__":
    main()
