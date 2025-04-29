import os
import sys
import logging
import pyperclip
from typing import List

def process_files(selected_files: List[str], output_file: str) -> int:
    """Process selected files and write their contents to output_file"""
    try:
        # Get the directory passed from context menu (%V)
        target_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
        logging.info(f"Target directory from context menu: {target_dir}")
        logging.info(f"Current working directory: {os.getcwd()}")

        # Use the target directory for output
        output_path = os.path.join(target_dir, output_file)
        logging.info(f"Writing output to: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as outfile:
            for file_path in selected_files:
                relative_path = os.path.relpath(file_path, target_dir)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        outfile.write(f"{relative_path}:\n<code>\n")
                        outfile.write(infile.read())
                        outfile.write("\n</code>\n\n")
                        logging.info(f"Processed: {relative_path}")
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {str(e)}")
            
            # Add the note about skipped files
            outfile.write("\n<additional_information>Some files may have been skipped, to save tokens or because they didn't seem relevant. Ask about them if needed.</additional_information>\n")
        return len(selected_files)
    except Exception as e:
        logging.error(f"Error writing to output file: {str(e)}")
        return 0

def copy_to_clipboard(output_path: str) -> bool:
    """Copy the contents of output_path to clipboard"""
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            full_code = f.read()
        pyperclip.copy(full_code)
#        logging.info("Code copied to clipboard!")
        return True
    except Exception as e:
        logging.error(f"Error copying to clipboard: {str(e)}")
        return False
