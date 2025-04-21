import os
import argparse
import fnmatch

# --- Configuration ---

# Default patterns/names to ignore
DEFAULT_IGNORE_PATTERNS = [
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    "*.pyc",
    "*.pyo",
    "*.egg-info",
    ".DS_Store",
    "*.lock",        # e.g., package-lock.json, yarn.lock, bun.lockb
    "*.log",
    ".env*",         # .env, .env.local, etc.
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",          # JetBrains IDE metadata
    ".vscode",        # VS Code metadata
    "target",         # Rust build directory
    "*.o",            # Compiled object files
    "*.a",            # Static libraries
    "*.so",           # Shared libraries (Linux)
    "*.dll",          # Shared libraries (Windows)
    "*.dylib",        # Shared libraries (macOS)
]

# --- Helper Functions ---

def should_ignore(name: str, ignore_patterns: list[str]) -> bool:
    """Checks if a file/folder name matches any ignore pattern."""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    # Also ignore hidden files/folders starting with '.' unless explicitly allowed
    # (e.g. .github is often kept, but handled by topdown=True filtering)
    # Note: .git is already explicitly ignored above.
    # if name.startswith('.'):
    #     return True # Uncomment this line if you want to ignore ALL hidden items
    return False

# --- Core Structure Generation ---

def generate_structure_lines(root_dir: str, ignore_patterns: list[str]) -> list[str]:
    """
    Generates the project structure as a list of formatted strings.
    """
    structure_lines = []
    root_dir_abs = os.path.abspath(root_dir)
    root_name = os.path.basename(root_dir_abs)

    # Add the root directory name itself
    structure_lines.append(f"{root_name}/")

    print(f"Ignoring patterns: {ignore_patterns}", flush=True)

    item_count = 0

    for dirpath, dirnames, filenames in os.walk(root_dir_abs, topdown=True):
        # --- Filtering ---
        # Filter ignored directories *in place*. This prevents os.walk from descending
        # into them because we are using topdown=True.
        dirnames[:] = [d for d in dirnames if not should_ignore(d, ignore_patterns)]
        # Filter ignored files
        filenames = [f for f in filenames if not should_ignore(f, ignore_patterns)]

        # Sort for consistent order
        dirnames.sort()
        filenames.sort()

        # --- Calculate Level and Indentation ---
        # Get the path relative to the starting root directory
        relative_dirpath = os.path.relpath(dirpath, root_dir_abs)
        # Calculate depth level
        level = 0 if relative_dirpath == '.' else relative_dirpath.count(os.sep) + 1
        # Indentation uses '│  ' for levels, but not for the connector part
        indent = '│  ' * (level - 1) if level > 0 else ''

        # Combine directories and files for processing
        entries = dirnames + filenames

        for i, name in enumerate(entries):
            item_count += 1
            is_last = (i == len(entries) - 1)
            # Determine connector based on position
            connector = '└── ' if is_last else '├── '

            # Check if it's a directory (we know this because it's in dirnames)
            is_dir = name in dirnames

            # Format the display name (add '/' suffix for directories)
            display_name = name + ('/' if is_dir else '')

            # Construct the line
            line = f"{indent}{connector}{display_name}"
            structure_lines.append(line)


    return structure_lines

# --- Main Execution ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and print a project directory structure.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "root_dir",
        nargs='?',  # Make the argument optional
        default='.', # Default to current directory if not provided
        help="The root directory of the project to analyze (defaults to current directory)."
    )
    parser.add_argument(
        "-i", "--ignore",
        action="append",
        help="Glob pattern or name to ignore (can be used multiple times). "
             f"Defaults include common patterns like: {', '.join(DEFAULT_IGNORE_PATTERNS[:5])}..."
             # Showing only a few defaults for brevity in help message
    )
    parser.add_argument(
        "-o", "--output",
        help="Optional file path to save the output structure."
    )

    args = parser.parse_args()

    # Combine default and user-provided ignore patterns
    ignore_patterns = DEFAULT_IGNORE_PATTERNS + (args.ignore if args.ignore else [])
    # Remove duplicates if any
    ignore_patterns = list(set(ignore_patterns))

    target_dir = args.root_dir
    if not os.path.isdir(target_dir):
        print(f"Error: Directory '{target_dir}' not found or is not a valid directory.")
        exit(1)

    try:
        structure_output_lines = generate_structure_lines(target_dir, ignore_patterns)
        full_output = "\n".join(structure_output_lines)

        if args.output:
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(full_output)
                print(f"Project structure saved to '{args.output}'")
            except IOError as e:
                print(f"\nError writing to output file '{args.output}': {e}")
                print("\n--- Generated Structure ---")
                print(full_output) # Print to console if file write fails
        else:
            print("\n--- Generated Structure ---")
            print(full_output)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
