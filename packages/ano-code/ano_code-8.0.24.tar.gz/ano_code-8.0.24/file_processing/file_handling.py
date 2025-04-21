import os
import requests
from yaspin import yaspin
from ai_assistant.llm_cli import groq_client
from ai_assistant.prompt_llm import AIAssistant
from ai_assistant.consts import COMMANDS
import tiktoken
import pathspec
import sys # <-- ADD THIS LINE AT THE TOP
import fnmatch
from pathlib import Path
import fnmatch

MAX_FILE_READ_BYTES = 10000 # Limit file size read to prevent memory issues and huge LLM prompts
BINARY_EXTENSIONS = { # Set of common binary file extensions to skip reading/commenting
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.tif', '.tiff',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.tar', '.gz', '.rar', '.7z',
    '.mp3', '.wav', '.ogg', '.mp4', '.avi', '.mov', '.wmv',
    '.exe', '.dll', '.so', '.dylib', '.class', '.jar',
    '.pyc', '.pyo', '.o', '.a', '.lib',
    '.sqlite', '.db', '.mdb',
    '.woff', '.woff2', '.ttf', '.otf', '.eot',
    '.lockb', # Example: bun.lockb
    '.lock', # Example: yarn.lock (often large, low info content for LLM)
    '.bin', '.dat',
}
DEFAULT_IGNORE_PATTERNS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build",
    "*.pyc", "*.pyo", "*.egg-info", ".DS_Store", "*.lock", "*.log", ".env*",
    "coverage", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".idea", ".vscode",
}


def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        return None


# Read folder content and respect .gitignore
def read_file_content(file_path: str):
    # gitignore_path = os.path.join(directory, '.gitignore')
    # spec = parse_gitignore(gitignore_path)

    # extensions = {".py", ".js", ".go", ".ts", ".tsx", ".jsx", ".dart", ".php", "Dockerfile", ".yml"}
    combined_content = ""

    # for root, dirs, files in os.walk(directory):
    #     if spec:
    #         dirs[:] = [d for d in dirs if not spec.match_file(os.path.join(root, d))]
    #     for filename in files:
    #         file_path = os.path.join(root, filename)
    #         if spec and spec.match_file(file_path):
    #             continue
    #         if not filename.endswith(tuple(extensions)):
    #             continue
    try:
        with open(file_path, 'r', encoding='utf-8') as f_content:
            f_c = f_content.read()
            # Check if the file is empty
            if not f_c.strip():
                print(f"Skipping empty file: {file_path}")
                pass
                # Check if the file is too large
            if os.path.getsize(file_path) > 10 * 1024 * 1024:  # 10 MB limit
                print(f"Skipping large file: {file_path}")
                pass
            # Check if the file is a binary file
            if b'\0' in f_c:
                print(f"Skipping binary file: {file_path}")
                pass
            # Check if the file is a symlink
            if os.path.islink(file_path):   
                print(f"Skipping symlink: {file_path}")
                pass
            # Check if the file is a directory
            if os.path.isdir(file_path):
                print(f"Skipping directory: {file_path}")
                pass
            # Check if the file is a socket
            if os.path.isfile(file_path) and os.path.is_socket(file_path):
                print(f"Skipping socket: {file_path}")
                pass
            # Check if the file is a FIFO
            if os.path.isfile(file_path) and os.path.is_fifo(file_path):
                print(f"Skipping FIFO: {file_path}")
                pass
            # Check if the file is a character device
            if os.path.isfile(file_path) and os.path.is_char_device(file_path):
                print(f"Skipping character device: {file_path}")
                pass
            # Check if the file is a block device
            if os.path.isfile(file_path) and os.path.is_block_device(file_path):
                print(f"Skipping block device: {file_path}")
                pass
            comment_dir(file_path, f_c)
    except Exception as e:
            print(f"Could not read file {file_path}: {e}")
    return combined_content


# Prompt the LLM
def prompt(path: str, cmd: str, m_tokens: int):
    loader = yaspin, 350,
    assistant = AIAssistant(groq_client)
    result = assistant.run_assistant(path, cmd)
    return result



def comment_dir(item_path: str):
    content = "No file content, this is not a file"
    
    more_details =""" \n\n Path: '${item_paths}'
    Brief Comment:"""
    cmd = COMMANDS["comment_path"]
    command = "${cmd} ${more_details}"
    prompt(item_path,command, 30)

def comment_file_content(item_path: str, file_content: str):
    content = "No file content, this is not a file"
    if file_content != "":
        content = file_content
    more_details =""" \n\n Path: '${item_paths}'
    File_content: '${file_content}'
    Brief Comment:"""
    cmd = COMMANDS["comment_path"]
    command = "${cmd} ${more_details}"
    prompt(item_path, 30, command)


# Send generated documentation to an API
def send_to_api(api_url, code_doc, repo_id):
    payload = {"code_doc": code_doc, "repo_id": repo_id}
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            print(f"Successfully sent documentation to API for repo_id '{repo_id}'.")
        else:
            print(f"Failed to send documentation for repo_id '{repo_id}'. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error sending to API: {e}")





def process_directory(directory, exclude_dirs)-> dict:
    tree = {}
    try:
        for entry in os.scandir(directory):
            if entry.is_dir(follow_symlinks=False):
                if entry.name in DEFAULT_IGNORE_PATTERNS.union(exclude_dirs):
                    # Skip this directory entirely
                    continue
                # Recurse into the directory
                tree[entry.name] = process_directory(entry.path, exclude_dirs)
            else:
                if entry.name not in DEFAULT_IGNORE_PATTERNS.union(exclude_dirs):
                    tree[entry.name] = None
                # Represent files with None
    except PermissionError:
        # Skip folders without permissions
        pass
    return tree



def find_gitignore(start_path):
    current_path = os.path.abspath(start_path)

    while True:
        gitignore_path = os.path.join(current_path, ".gitignore")
        if os.path.isfile(gitignore_path):
            return gitignore_path

        # Move up one directory
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            # Reached the filesystem root
            return None

        current_path = parent_path


# --- Core Recursive JSON Structure Generation ---
def parse_gitignore(current_path):
    try:
        gitignore_path = find_gitignore(current_path)
        if gitignore_path is None:
            return None
        with open(gitignore_path, 'r', encoding='utf-8') as gitignore_file:
            patterns = gitignore_file.read().splitlines()
            return patterns
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading .gitignore: {e}")
        return None


def is_ignored(path: Path, ignore_patterns):
    path_folders = path.root.split("/")
    print(path_folders)
    for folder in path_folders:
        if folder in ignore_patterns:
            return True
    return False


def generate_json_structure(root_path, ignore_patterns):
    def walk(dir_path):
        item = {
            "name": os.path.relpath(dir_path, root_path) if dir_path != root_path else ".",
            "type": "directory",
            "children": []
        }

        for entry in os.listdir(dir_path):
            full_path = os.path.join(dir_path, entry)
            if is_ignored(os.path.relpath(dir_path, root_path), ignore_patterns) != True:
                if os.path.isdir(full_path):
                    item["children"].append(walk(full_path))
                else:
                    item["children"].append({
                        "name": entry,
                        "type": "file"
                    })
        return item

    return walk(root_path)







def read_file_content(file_path: Path, encoding='utf-8'):
  try:
    # Use 'with' to ensure the file is automatically closed even if errors occur
    with open(file_path, 'r', encoding=encoding) as f:
      content = f.read() # Read the entire file content
      return content
  except FileNotFoundError:
    print(f"Error: File not found at '{file_path}'", file=sys.stderr)
    return None
  except PermissionError:
    print(f"Error: Permission denied to read file '{file_path}'", file=sys.stderr)
    return None
  except IsADirectoryError:
     print(f"Error: Expected a file path, but got a directory: '{file_path}'", file=sys.stderr)
     return None
  except UnicodeDecodeError:
    print(f"Error: Could not decode file '{file_path}' using encoding '{encoding}'. Try a different encoding.", file=sys.stderr)
    return None
  except Exception as e: # Catch any other potential file-related errors
    print(f"An unexpected error occurred while reading '{file_path}': {e}", file=sys.stderr)
    return None



def modify_file_content(file_path, new_content, encoding='utf-8', create_dirs=True):
    """
    Overwrites the content of a specified file with new content.

    Args:
        file_path (str): The full path to the file to modify.
        new_content (str): The new string content to write to the file.
        encoding (str): The encoding to use when writing the file. Defaults to 'utf-8'.
        create_dirs (bool): If True, automatically create parent directories
                            if they don't exist. Defaults to True.

    Returns:
        bool: True if the file was successfully written, False otherwise.

    Raises:
        TypeError: If new_content is not a string.
        # Specific OS/IO errors might still propagate if not caught explicitly below
    """
    if not isinstance(new_content, str):
        # Ensure content is a string, as required by f.write() in text mode
        print(f"Error: new_content for '{file_path}' must be a string, not {type(new_content)}.", file=sys.stderr)
        # Optionally raise TypeError("new_content must be a string") instead of returning False
        return False

    try:
        # Optional: Create parent directories if requested and needed
        if create_dirs:
            parent_dir = os.path.dirname(file_path)
            # Check if parent_dir is not empty (e.g., for files in the current dir)
            # and if it doesn't exist
            if parent_dir and not os.path.exists(parent_dir):
                try:
                    os.makedirs(parent_dir)
                    print(f"Info: Created directory '{parent_dir}' for file '{file_path}'.", file=sys.stderr)
                except OSError as e:
                    print(f"Error: Could not create directory '{parent_dir}' for file '{file_path}': {e}", file=sys.stderr)
                    return False # Cannot proceed if directory creation fails

        # Open the file in write mode ('w').
        # This TRUNCATES the file if it exists or CREATES it if it doesn't.
        # Use 'utf-8' encoding by default, crucial for non-ASCII text.
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(new_content)
        # print(f"Successfully wrote content to '{file_path}'.", file=sys.stderr) # Optional success message
        return True

    except PermissionError:
        print(f"Error: Permission denied when trying to write to '{file_path}'.", file=sys.stderr)
        return False
    except IsADirectoryError:
         print(f"Error: The path '{file_path}' points to a directory, not a file.", file=sys.stderr)
         return False
    except FileNotFoundError:
        # This typically happens if create_dirs is False and the directory doesn't exist,
        # or if the path is fundamentally invalid.
         print(f"Error: File or directory not found for path '{file_path}'. Check the path.", file=sys.stderr)
         return False
    except OSError as e:
        # Catch other potential OS-level errors (e.g., disk full, invalid argument)
        print(f"Error: An OS error occurred while writing to '{file_path}': {e}", file=sys.stderr)
        return False
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error: An unexpected error occurred while modifying '{file_path}': {e}", file=sys.stderr)
        return False



def delete_file(file_path):
    """
    Deletes a specified file.

    Args:
        file_path (str): The full path to the file to delete.

    Returns:
        bool: True if the file was successfully deleted, False otherwise.
              Returns False if the file didn't exist initially or if the
              path pointed to a directory.
    """
    # 1. Check if the path exists and is a file
    if not os.path.isfile(file_path):
        # Path doesn't exist or it's not a file (e.g., it's a directory)
        if os.path.exists(file_path):
            # It exists, but it's not a file
            print(f"Error: Path '{file_path}' exists but is not a regular file (likely a directory). Cannot delete.", file=sys.stderr)
        else:
            # It doesn't exist at all
            print(f"Error: File not found at '{file_path}'. Cannot delete.", file=sys.stderr)
        return False # Cannot proceed

    # 2. Attempt to delete the file
    try:
        os.remove(file_path)
        # print(f"Successfully deleted file: '{file_path}'", file=sys.stderr) # Optional success message
        return True # Deletion successful

    except PermissionError:
        print(f"Error: Permission denied. Cannot delete '{file_path}'.", file=sys.stderr)
        return False
    except OSError as e:
        # Catch other potential OS-level errors during removal
        # (e.g., file in use on Windows, filesystem errors)
        print(f"Error: OS error deleting file '{file_path}': {e}", file=sys.stderr)
        return False
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error: An unexpected error occurred deleting '{file_path}': {e}", file=sys.stderr)
        return False
