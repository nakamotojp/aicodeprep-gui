import os
import sys
import logging
from typing import List

def process_files(selected_files: List[str], output_file: str) -> int:
    """Process selected files and write their contents to output_file"""
    try:
        output_path = os.path.join(os.getcwd(), output_file)
        logging.info(f"Writing output to: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as outfile:
            for file_path in selected_files:
                try:
                    try:
                        relative_path = os.path.relpath(file_path, os.getcwd())
                    except ValueError:
                        relative_path = file_path  # fallback to absolute path if unrelated
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        outfile.write(f"{relative_path}:\n<code>\n")
                        outfile.write(infile.read())
                        outfile.write("\n</code>\n\n")
                        logging.info(f"Processed: {relative_path}")
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {str(e)}")
            # Add the note about skipped files
            outfile.write("\n<notes>Some files may have been skipped, to save tokens or because they didn't seem relevant. Ask about them if needed.</notes>\n")
        return len(selected_files)
    except Exception as e:
        logging.error(f"Error writing to output file: {str(e)}")
        return 0
