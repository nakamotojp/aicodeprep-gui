from importlib import resources
import os
import sys
import pathlib
import yaml
import logging
from typing import List, Tuple
import fnmatch

def get_config_path():
    """Get the path to the default configuration file."""
    if getattr(sys, 'frozen', False):
        # If the application is frozen (e.g., PyInstaller), use the _MEIPASS directory.
        base_path = sys._MEIPASS
        config_path = os.path.join(base_path, 'aicodeprep_gui', 'data', 'default_config.yaml')
    else:
        # If running as a script, use importlib.resources.
        try:
            with resources.path('aicodeprep_gui.data', 'default_config.yaml') as config_file:
                config_path = str(config_file)
        except ModuleNotFoundError:
            # Fallback to a default path if the package structure is different.
            config_path = os.path.join(os.path.dirname(__file__), 'data', 'default_config.yaml')

    return config_path

def get_exe_directory():
    """Get the directory of the executable or script"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def load_default_config() -> dict:
    """Load the default configuration from YAML file"""
    try:
        config_path = get_config_path()
        logging.info(f"Looking for config at {config_path}")

        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            logging.warning("Default config file not found, using built-in defaults")
            config = {
                'code_extensions': ['.py', '.js', '.java', '.cpp', '.h', '.c', '.hpp', '.cs', '.php', '.rb', '.go',
                                   '.rs', '.swift', '.kt'],
                'exclude_extensions': ['.pyc', '.class', '.o', '.obj'],
                'exclude_patterns': ['__pycache__', '.git', 'node_modules', 'build', 'dist'],
                'exclude_dirs': ['__pycache__', '.git', 'node_modules', 'build', 'dist'],
                'include_dirs': [],
                'exclude_files': [],
                'include_files': [],
                'max_file_size': 1000000
            }

        if 'exclude_patterns' in config:
            config['exclude_patterns'] = [pattern.lstrip('.') for pattern in config['exclude_patterns']]

        if 'code_extensions' not in config or not config['code_extensions']:
            config['code_extensions'] = ['.py', '.js', '.java', '.cpp', '.h', '.c', '.hpp', '.cs', '.php', '.rb',
                                         '.go', '.rs', '.swift', '.kt']

        logging.info(f"Loaded configuration with {len(config.get('code_extensions', []))} code extensions")
        return config

    except Exception as e:
        logging.error(f"Error in configuration handling: {str(e)}")
        return {
            'code_extensions': ['.py', '.js', '.java', '.cpp', '.h', '.c', '.hpp', '.cs', '.php', '.rb', '.go',
                               '.rs', '.swift', '.kt'],
            'exclude_extensions': ['.pyc', '.class', '.o', '.obj'],
            'exclude_patterns': ['__pycache__', '.git', 'node_modules', 'build', 'dist'],
            'exclude_dirs': ['__pycache__', '.git', 'node_modules', 'build', 'dist'],
            'include_dirs': [],
            'exclude_files': [],
            'include_files': [],
            'max_file_size': 1000000
        }

def load_user_config() -> dict:
    """Load user-specific configuration from YAML file"""
    try:
        config_path = os.path.join(get_exe_directory(), 'aicodeprep_config.yaml')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                if config and 'exclude_patterns' in config:
                    config['exclude_patterns'] = [
                        pattern.lstrip('.') for pattern in config['exclude_patterns']
                    ]
                return config
    except Exception as e:
        logging.error(f"Error loading user configuration: {str(e)}")
    return {}

def matches_pattern(filename: str, pattern: str) -> bool:
    """Check if filename matches the given glob-style pattern (supports *, ?, [])"""
    return fnmatch.fnmatch(filename.lower(), pattern.lower())

def is_excluded_directory(path: str) -> bool:
    """Check if the directory should be excluded"""
    path_parts = pathlib.Path(path).parts
    return any(part in EXCLUDE_DIRS for part in path_parts)

def should_process_directory(dir_path: str) -> bool:
    """Determine if a directory should be processed"""
    if is_excluded_directory(dir_path):
        return False

    dir_name = os.path.basename(dir_path)
    if dir_name in INCLUDE_DIRS:
        return True
    if dir_name in EXCLUDE_DIRS:
        return False
    return True

def collect_all_files() -> List[Tuple[str, str, bool]]:
    """Collect all files in the target directory with inclusion flags"""
    all_files = []
    logging.info("Starting file collection...")

    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = os.getcwd()

    logging.info(f"Processing directory: {root_dir}")
    logging.info(f"Code extensions configured: {CODE_EXTENSIONS}")

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file == "aicp_FULLCODE.txt":
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_dir)

            if any(part.startswith('.') for part in pathlib.Path(file_path).parts):
                continue

            try:
                if os.path.getsize(file_path) > MAX_FILE_SIZE:
                    continue
            except (OSError, IOError):
                continue

            included = False

            if file in INCLUDE_FILES:
                included = True
            elif os.path.basename(root) in INCLUDE_DIRS:
                extension = pathlib.Path(file_path).suffix.lower()
                if extension in CODE_EXTENSIONS:
                    if (file not in EXCLUDE_FILES and
                            extension not in EXCLUDE_EXTENSIONS and
                            not any(matches_pattern(file, pattern) for pattern in EXCLUDE_PATTERNS)):
                        included = True
            else:
                extension = pathlib.Path(file_path).suffix.lower()
                if extension in CODE_EXTENSIONS:
                    if (file not in EXCLUDE_FILES and
                            extension not in EXCLUDE_EXTENSIONS and
                            not any(matches_pattern(file, pattern) for pattern in EXCLUDE_PATTERNS) and
                            not any(part in EXCLUDE_DIRS for part in pathlib.Path(root).parts)):
                        included = True

            all_files.append((file_path, relative_path, included))
            logging.info(f"Collected file: {relative_path}, Included by default: {included}")

    logging.info(f"Total files collected: {len(all_files)}")
    return all_files

# Load configurations
default_config = load_default_config()
user_config = load_user_config()
config = {**default_config, **user_config}

CODE_EXTENSIONS = set(config.get('code_extensions', []))
EXCLUDE_EXTENSIONS = set(config.get('exclude_extensions', []))
EXCLUDE_PATTERNS = set(config.get('exclude_patterns', []))
EXCLUDE_DIRS = set(config.get('exclude_dirs', []))
INCLUDE_DIRS = set(config.get('include_dirs', []))
EXCLUDE_FILES = set(config.get('exclude_files', []))
INCLUDE_FILES = set(config.get('include_files', []))
MAX_FILE_SIZE = config.get('max_file_size', 1000000)
