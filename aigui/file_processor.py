import os
import sys
import logging
from typing import List, Literal

OutputFmt = Literal['xml', 'markdown']

def _write_one_file_xml(outfile, rel_path, abs_path):
    outfile.write(f"{rel_path}:\n<code>\n")
    if is_binary_file(abs_path):
        outfile.write(".. contents skipped (binary file) ..")
    else:
        try:
            with open(abs_path, "r", encoding="utf-8", errors="ignore") as infile:
                outfile.write(infile.read())
        except Exception:
            outfile.write(".. contents skipped (read error) ..")
    outfile.write("\n</code>\n\n")

from aigui.smart_logic import is_binary_file

def _write_one_file_md(outfile, rel_path, abs_path):
    outfile.write(f"### {rel_path}\n")
    if is_binary_file(abs_path):
        outfile.write(".. contents skipped (binary file) ..\n")
    else:
        try:
            with open(abs_path, "r", encoding="utf-8", errors="ignore") as infile:
                outfile.write(infile.read())
        except Exception:
            outfile.write(".. contents skipped (read error) ..\n")
    outfile.write(f"\n### END {rel_path}\n\n")

def process_files(selected_files: List[str], output_file: str, fmt: OutputFmt = 'xml', prompt: str = "") -> int:
    """
    Write the concatenation of `selected_files` into `output_file`.
    `fmt` is either 'xml' (default, uses <code> … </code>) or
    'markdown' (### path … ### END path).
    """
    try:
        output_path = os.path.join(os.getcwd(), output_file)
        logging.info(f"Writing output to: {output_path}")

        writer = _write_one_file_xml if fmt == 'xml' else _write_one_file_md

        with open(output_path, 'w', encoding='utf-8') as outfile:
            for file_path in selected_files:
                try:
                    try:
                        rel_path = os.path.relpath(file_path, os.getcwd())
                    except ValueError:
                        rel_path = file_path
                    writer(outfile, rel_path, file_path)
                    logging.info(f"Processed: {rel_path}")
                except Exception as exc:
                    logging.error(f"Error processing {file_path}: {exc}")

            if prompt:
                outfile.write("\n\n" + prompt.strip())

            # generic tail line – no XML tags any more
            outfile.write("\n\n.. some other files were skipped ..\n")

        return len(selected_files)
    except Exception as exc:
        logging.error(f"Error writing output file: {exc}")
        return 0
