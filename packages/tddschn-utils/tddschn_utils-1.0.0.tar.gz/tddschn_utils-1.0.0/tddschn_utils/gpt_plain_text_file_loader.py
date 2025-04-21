#!/usr/bin/env python3

import io
import os
import fnmatch
import argparse
from pathlib import Path
import sys
from typing import Iterable, Dict, List, Tuple

# Updated default preamble to be more general
DEFAULT_PREAMBLE_MULTI_DIR = "The following text contains files from one or more directories. For each directory, a structure section shows the included files, followed by the contents of those files. File content sections begin with ----, followed by the file path, then the content. The collection ends with --END--."
DEFAULT_PREAMBLE_GIT_REPO = "The following text is a Git repository with code. The structure of the text are sections that begin with ----, followed by a single line containing the file path and file name, followed by a variable amount of lines containing the file contents. The text representing the Git repository ends when the symbols --END-- are encounted. Any further text beyond --END-- are meant to be interpreted as instructions using the aforementioned Git repository as context."
DEFAULT_PREAMBLE_FILE_COLLECTION = "The following text is a collection of files. The structure of the text are sections that begin with ----, followed by a single line containing the file path and file name, followed by a variable amount of lines containing the file contents."

DEFAULT_EPILOGUE = """

--END--

reply 'ok' and only 'ok' if you read."""

# Heuristic to detect binary files: check for null bytes in the first chunk
CHUNK_SIZE = 1024
# Add common known text file extensions to prioritize including them even if they contain unusual bytes initially
# This list is not exhaustive and can be customized
KNOWN_TEXT_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml",
    ".xml", ".csv", ".log", ".sh", ".bash", ".zsh", ".c", ".cpp", ".h", ".hpp",
    ".java", ".go", ".rs", ".php", ".rb", ".pl", ".lua", ".sql", ".r", ".swift",
    ".kt", ".kts", ".scala", ".clj", ".hs", ".elm", ".diff", ".patch", ".rst",
    ".tex", ".gitignore", ".gitattributes", ".gptignore", ".dockerfile", "dockerfile",
    ".conf", ".cfg", ".ini", ".toml", ".tf", ".tfvars", ".hcl", ".gql", ".graphql",
    ".ps1", ".bat", ".cmd", ".jsx", ".tsx", ".vue", ".svelte"
}


def is_likely_binary(file_path: Path) -> bool:
    """
    Check if a file is likely binary by looking for null bytes in the first CHUNK_SIZE bytes.
    Also checks against known text file extensions. Returns False for empty files.
    """
    # Optimization: check known text extensions first
    if file_path.suffix.lower() in KNOWN_TEXT_EXTENSIONS:
        return False
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:  # Empty file is not binary
                return False
            # Simple heuristic: check for null bytes
            if b'\x00' in chunk:
                return True
            # Optional: More sophisticated check (e.g., ratio of non-printable chars)
            # try:
            #     chunk.decode('utf-8')
            # except UnicodeDecodeError:
            #     return True # If it doesn't decode as UTF-8, likely binary or wrong encoding

    except IOError:
        # File might not be readable, treat as potentially problematic (skip)
        return True
    return False


def get_args():
    parser = argparse.ArgumentParser(
        description="Process text files from specified directories into a single text output, optionally including directory structures. Skips likely binary files."
    )
    parser.add_argument(
        "source_paths",
        help="Paths to the source directories or files to include. If directories are specified, they are walked recursively.",
        nargs='+',  # Accept one or more paths
        type=Path,
    )
    parser.add_argument("-p", "--preamble", help="Preamble text", default=None)
    parser.add_argument(
        "-f", "--preamble-file", help="Path to preamble text file", default=None, type=Path
    )
    parser.add_argument("-e", "--epilogue", help="Epilogue text", default=None)
    parser.add_argument(
        "-F", "--epilogue-file", help="Path to epilogue text file", default=None, type=Path
    )
    parser.add_argument(
        "-E",
        "--no-epilogue",
        help="Do not include epilogue text",
        action="store_true",
    )
    parser.add_argument(
        "-o", "--output", help="Path to output text file", default="output.txt", type=Path
    )
    parser.add_argument(
        "-c",
        "--copy",
        help="Copy the output to the clipboard instead of writing to a file",
        action="store_true",
    )
    parser.add_argument(
        "-G",
        "--no-ignore-git",
        help="Do not ignore .git directory (if walking directories)",
        action="store_true",
    )
    parser.add_argument(
        "-Z",
        "--no-ignore-gitignore-and-gitattributes",
        help="Do not ignore .gitignore and .gitattributes files",
        action="store_true",
    )
    # cSpell:disable
    parser.add_argument(
        "-i",
        "--gptignore",
        help="Path to .gptignore file. If not specified, looks for .gptignore in the current working directory.",
        type=Path,
        default=Path(".gptignore") # Default to CWD
    )
    parser.add_argument(
        "-I", "--no-gptignore", help="Do not use any .gptignore file", action="store_true"
    )
    # cSpell:enable
    parser.add_argument(
        "-n",
        "--dry-run",
        "--list-files-would-be-included",
        help="List files that would be included in the output (grouped by source directory/file)",
        action="store_true",
    )
    parser.add_argument(
        "--no-structure",
        help="Do not include the directory structure section for each source directory",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print verbose output, including skipped binary files.",
        action="store_true",
    )

    args = parser.parse_args()

    # Resolve source paths to absolute paths for consistency
    args.source_paths = [p.resolve() for p in args.source_paths]

    return args


def get_ignore_list(ignore_file_path: Path) -> list[str]:
    ignore_list = []
    try:
        with open(ignore_file_path, "r", encoding='utf-8', errors='ignore') as ignore_file:
            for line in ignore_file:
                line = line.strip()
                if line and not line.startswith("#"):
                    # fnmatch expects forward slashes, even on Windows
                    ignore_list.append(line.replace("\\", "/"))
    except FileNotFoundError:
        print(f"Warning: Ignore file not found at {ignore_file_path}", file=sys.stderr)
    except IOError as e:
        print(f"Warning: Could not read ignore file {ignore_file_path}: {e}", file=sys.stderr)
    return ignore_list


def should_ignore(relative_file_path: Path, ignore_list: Iterable[str]) -> bool:
    # fnmatch needs string paths with forward slashes
    path_str = relative_file_path.as_posix()
    # Check against filename and full path relative to the base
    for pattern in ignore_list:
        if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(relative_file_path.name, pattern):
            return True
        # fnmatch pattern matching directories should end with /
        if pattern.endswith('/') and fnmatch.fnmatch(path_str + '/', pattern):
             return True
    return False


def get_included_files_for_path(
    source_path: Path,
    ignore_list: Iterable[str],
    verbose: bool = False
) -> List[Path]:
    """
    Finds all text files within or at the source_path that are not ignored.
    Skips likely binary files. Returns absolute paths.
    """
    included_files = []
    if source_path.is_file():
        base_path = source_path.parent
        relative_path = source_path.relative_to(base_path)
        if not should_ignore(relative_path, ignore_list):
            if not is_likely_binary(source_path):
                included_files.append(source_path)
            elif verbose:
                print(f"Skipping likely binary file: {source_path}", file=sys.stderr)
        elif verbose:
             print(f"Ignoring file due to rule: {source_path}", file=sys.stderr)

    elif source_path.is_dir():
        base_path = source_path
        for root, dirs, files in os.walk(source_path, topdown=True):
            root_path = Path(root)
            relative_root = root_path.relative_to(base_path)

            # Filter directories based on ignore list
            original_dirs = list(dirs) # Copy before modifying
            dirs[:] = [d for d in dirs if not should_ignore(relative_root / d, ignore_list)]
            if verbose:
                 skipped_dirs = set(original_dirs) - set(dirs)
                 for skipped in skipped_dirs:
                     print(f"Ignoring directory due to rule: {root_path / skipped}", file=sys.stderr)


            for file in files:
                file_path = root_path / file
                relative_file_path = file_path.relative_to(base_path)
                if not should_ignore(relative_file_path, ignore_list):
                    if not is_likely_binary(file_path):
                        included_files.append(file_path)
                    elif verbose:
                        print(f"Skipping likely binary file: {file_path}", file=sys.stderr)
                elif verbose:
                     print(f"Ignoring file due to rule: {file_path}", file=sys.stderr)

    else:
         print(f"Warning: Source path {source_path} is neither a file nor a directory. Skipping.", file=sys.stderr)

    return included_files


def generate_directory_tree(base_path: Path, file_paths: List[Path]) -> str:
    """Generates a string representation of the directory tree for the given files."""
    if not file_paths:
        return ""

    tree = io.StringIO()

    # Create relative paths for sorting and processing
    try:
        relative_paths = sorted([p.relative_to(base_path) for p in file_paths])
    except ValueError as e:
         print(f"Error creating relative paths for tree (base: {base_path}): {e}", file=sys.stderr)
         # Fallback: print simple list if tree fails
         tree.write(" (Error generating tree structure)\n")
         for p in sorted(file_paths):
              tree.write(f"- {p.name}\n")
         return tree.getvalue()


    tree_dict = {}

    for rel_path in relative_paths:
        current_level = tree_dict
        parts = rel_path.parts
        for i, part in enumerate(parts):
            if i == len(parts) - 1: # It's a file
                current_level[part] = None # Mark as file
            else: # It's a directory
                if part not in current_level:
                    current_level[part] = {}
                # Ensure we don't overwrite a directory entry with a file entry if names collide (rare)
                if current_level[part] is None:
                    print(f"Warning: Path conflict detected in tree generation near '{'/'.join(parts[:i+1])}'", file=sys.stderr)
                    break # Stop processing this path to avoid error
                current_level = current_level[part]


    def print_tree_level(level_dict, prefix=""):
        items = sorted(level_dict.items())
        for i, (name, content) in enumerate(items):
            connector = "└── " if i == len(items) - 1 else "├── "
            tree.write(f"{prefix}{connector}{name}\n")
            if content is not None: # It's a subdirectory
                new_prefix = prefix + ("    " if i == len(items) - 1 else "│   ")
                print_tree_level(content, new_prefix)

    print_tree_level(tree_dict)
    return tree.getvalue()


def write_files_to_output(base_path: Path, file_paths: List[Path], output_file):
    """Writes the content of each file to the output, prefixed with its relative path."""
    # Sort files by relative path for consistent output
    try:
        sorted_files = sorted(file_paths, key=lambda p: p.relative_to(base_path))
    except ValueError as e:
        print(f"Error creating relative paths for sorting output files (base: {base_path}): {e}", file=sys.stderr)
        print("Outputting files in potentially unsorted order.", file=sys.stderr)
        sorted_files = file_paths # Fallback


    for file_path in sorted_files:
        try:
            # Open in text mode, relying on the earlier binary check
            with open(file_path, "r", encoding='utf-8', errors="ignore") as file:
                contents = file.read()
            relative_path = file_path.relative_to(base_path)
            output_file.write("-" * 4 + "\n")
            # Use forward slashes for paths in the output for consistency
            output_file.write(f"{relative_path.as_posix()}\n")
            output_file.write(f"{contents}\n")
        except Exception as e:
            # Report error but continue with other files
            print(f"Error reading text file {file_path}: {e}", file=sys.stderr)
            output_file.write("-" * 4 + "\n")
            try:
                relative_path = file_path.relative_to(base_path)
                output_file.write(f"{relative_path.as_posix()} (Error reading content)\n")
            except ValueError: # Handle cases where relative_to might fail unexpectedly
                 output_file.write(f"{file_path.name} (Error reading content - path issue)\n")
            output_file.write(f"[Content could not be read due to error: {e}]\n")


def main() -> None:
    args = get_args()

    # --- Ignore List Setup ---
    ignore_list = []
    # cSpell:disable
    gptignore_path = args.gptignore # Already defaults to Path(".gptignore")
    if not args.no_gptignore:
        # Look for .gptignore where specified or in CWD
        if gptignore_path.exists():
             if args.verbose: print(f"Using ignore file: {gptignore_path.resolve()}", file=sys.stderr)
             ignore_list.extend(get_ignore_list(gptignore_path))
        elif args.gptignore != Path(".gptignore"): # If user specified a non-default path but it doesn't exist
             print(f"Warning: Specified ignore file not found: {gptignore_path.resolve()}", file=sys.stderr)
        elif args.verbose:
             print("No .gptignore file found in current directory.", file=sys.stderr)

    # cSpell:enable
    if not args.no_ignore_git:
        ignore_list.append(".git") # Ignore the whole directory using simple name matching
        ignore_list.append(".git/*") # Ignore contents using wildcard matching
    if not args.no_ignore_gitignore_and_gitattributes:
        ignore_list.append(".gitignore")
        ignore_list.append(".gitattributes")

    if ignore_list and args.verbose:
        print(f"Effective ignore patterns: {ignore_list}", file=sys.stderr)

    # --- File Discovery ---
    all_included_files: Dict[Path, List[Path]] = {}
    total_files_count = 0

    for source_path in args.source_paths:
        if not source_path.exists():
             print(f"Warning: Source path '{source_path}' does not exist. Skipping.", file=sys.stderr)
             continue

        # get_included_files_for_path now handles binary skipping
        included = get_included_files_for_path(source_path, ignore_list, args.verbose)

        if included:
            all_included_files[source_path] = included
            total_files_count += len(included)
        elif source_path.is_dir() and args.verbose:
             print(f"No non-ignored text files found in directory: {source_path}", file=sys.stderr)
        elif source_path.is_file() and not included and args.verbose:
             # Message about skipping binary/ignored file is now inside get_included_files_for_path
             pass


    if not all_included_files:
        print("No text files to include found based on provided paths and ignore rules. Exiting.", file=sys.stderr)
        return

    # --- Dry Run ---
    if args.dry_run:
        print("--- Files that would be included: ---", file=sys.stderr)
        for source_path, files in all_included_files.items():
            # Determine base path correctly for display
            base_path = source_path if source_path.is_dir() else source_path.parent
            print(f"\n--- From source: {source_path} (base for paths: {base_path}) ---", file=sys.stderr)
            if not files:
                print("  (No files)", file=sys.stderr)
                continue

            # Show structure if it's a directory source and not disabled
            if source_path.is_dir() and not args.no_structure:
                 tree = generate_directory_tree(base_path, files)
                 print("--- Structure ---", file=sys.stderr)
                 print(tree, file=sys.stderr)
                 print("--- Files (relative to base) ---", file=sys.stderr)

            # Sort files relative to base path for display
            try:
                sorted_display_files = sorted(files, key=lambda p: p.relative_to(base_path))
            except ValueError:
                 print("  (Error generating relative paths for listing)", file=sys.stderr)
                 sorted_display_files = sorted(files) # Fallback sort

            for file_path in sorted_display_files:
                 try:
                     display_path = file_path.relative_to(base_path).as_posix()
                 except ValueError:
                     display_path = f"{file_path.name} (could not make relative)"
                 print(f"  {display_path}", file=sys.stderr)

        print(f"\nTotal text files: {total_files_count}", file=sys.stderr)
        return

    # --- Output Generation ---
    output_target = io.StringIO() if args.copy else open(args.output, "w", encoding='utf-8')

    try:
        # --- Preamble ---
        if args.preamble:
            preamble = args.preamble
        elif args.preamble_file:
            try:
                with open(args.preamble_file, "r", encoding='utf-8') as pf:
                    preamble = pf.read()
            except Exception as e:
                 print(f"Error reading preamble file {args.preamble_file}: {e}. Using default.", file=sys.stderr)
                 preamble = DEFAULT_PREAMBLE_MULTI_DIR
        else:
            preamble = DEFAULT_PREAMBLE_MULTI_DIR
        output_target.write(f"{preamble}\n\n")

        # --- Process Each Source Path ---
        first_section = True
        for source_path, included_files in all_included_files.items():
            if not included_files: continue

            if not first_section:
                output_target.write("\n")
            first_section = False

            base_path = source_path if source_path.is_dir() else source_path.parent
            resolved_source_display = source_path.resolve().as_posix() # Consistent display path

            # --- Directory Structure (Optional) ---
            if source_path.is_dir() and not args.no_structure:
                output_target.write("-" * 4 + " Structure for directory" + "\n")
                output_target.write(f"{resolved_source_display}\n")
                tree_str = generate_directory_tree(base_path, included_files)
                output_target.write(tree_str)
                output_target.write("\n")

            # --- File Contents ---
            output_target.write("-" * 4 + " Files from" + "\n")
            output_target.write(f"{resolved_source_display}\n") # Use resolved path

            # Write file contents, using base_path for relative paths
            write_files_to_output(base_path, included_files, output_target)


        # --- Epilogue ---
        if not args.no_epilogue:
            epilogue_content = None
            if args.epilogue:
                epilogue_content = args.epilogue
            elif args.epilogue_file:
                 try:
                     with open(args.epilogue_file, "r", encoding='utf-8') as ef:
                        epilogue_content = ef.read()
                 except Exception as e:
                     print(f"Error reading epilogue file {args.epilogue_file}: {e}. Using default.", file=sys.stderr)
                     # Fall back to default epilogue, which includes --END--
                     epilogue_content = DEFAULT_EPILOGUE
            else:
                epilogue_content = DEFAULT_EPILOGUE # Default includes --END--

            # Ensure --END-- is present, handling cases where custom epilogue might omit it
            # We add --END-- *before* the custom content if the default epilogue isn't used.
            if epilogue_content is None: # Should not happen with defaults, but belt-and-suspenders
                 output_target.write("\n\n--END--\n")
            elif epilogue_content is DEFAULT_EPILOGUE:
                 output_target.write(epilogue_content) # Default already has spacing and --END--
            else: # Custom epilogue provided
                 output_target.write("\n\n--END--\n\n") # Standard separator and end marker
                 output_target.write(epilogue_content) # Write custom content after the marker

        else:
             output_target.write("\n\n--END--\n") # Always write --END--


        # --- Final Output Handling ---
        if args.copy:
            import pyperclip
            content = output_target.getvalue()
            try:
                pyperclip.copy(content)
                print(f"Output copied to clipboard. Total text files: {total_files_count}. Total chars: {len(content)}", file=sys.stderr)
            except Exception as e:
                 # Try to inform user better about potential pyperclip issues
                 pyperclip_error = f"Error copying to clipboard: {e}. "
                 pyperclip_error += "Ensure 'pyperclip' is installed (`pip install pyperclip`). "
                 pyperclip_error += "On Linux, you might also need 'xclip' or 'xsel'. "
                 pyperclip_error += "On WSL, ensure host integration is working or install 'win32yank'."
                 print(pyperclip_error, file=sys.stderr)

        else:
            # For files, get size after writing is complete
            output_target.flush() # Ensure buffer is written
            try:
                 # os.path.getsize needs a filename, not a stream object
                 content_length = os.path.getsize(args.output)
            except OSError:
                 # If getting size fails, try getting stream position (might be less accurate after closing)
                 content_length = output_target.tell()

            print(f"Output written to {args.output}. Total text files: {total_files_count}. Total chars: {content_length}", file=sys.stderr)

    finally:
        if not args.copy and not isinstance(output_target, io.StringIO):
            if not output_target.closed:
                 output_target.close()


if __name__ == "__main__":
    main()