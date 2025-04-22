#!/usr/bin/env python3

import io
import os
import fnmatch
import argparse
from pathlib import Path
import sys
from typing import Iterable, Dict, List

# Updated default preamble to be more general
DEFAULT_PREAMBLE_MULTI_DIR = "The following text contains files from one or more directories. For each directory, a structure section shows the included files, followed by the contents of those files. File content sections begin with ----, followed by the file path, then the content. The collection ends with --END--."
DEFAULT_PREAMBLE_GIT_REPO = "The following text is a Git repository with code. The structure of the text are sections that begin with ----, followed by a single line containing the file path and file name, followed by a variable amount of lines containing the file contents. The text representing the Git repository ends when the symbols --END-- are encounted. Any further text beyond --END-- are meant to be interpreted as instructions using the aforementioned Git repository as context."
DEFAULT_PREAMBLE_FILE_COLLECTION = "The following text is a collection of files provided explicitly. The structure of the text are sections that begin with ----, followed by a single line containing the file path and file name, followed by a variable amount of lines containing the file contents. The collection ends with --END--." # Added for -L case

DEFAULT_EPILOGUE = """

--END--

reply 'ok' and only 'ok' if you read."""

# Heuristic to detect binary files: check for null bytes in the first chunk
CHUNK_SIZE = 1024
# Add common known text file extensions to prioritize including them even if they contain unusual bytes initially
KNOWN_TEXT_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml",
    ".xml", ".csv", ".log", ".sh", ".bash", ".zsh", ".c", ".cpp", ".h", ".hpp",
    ".java", ".go", ".rs", ".php", ".rb", ".pl", ".lua", ".sql", ".r", ".swift",
    ".kt", ".kts", ".scala", ".clj", ".hs", ".elm", ".diff", ".patch", ".rst",
    ".tex", ".gitignore", ".gitattributes", ".gptignore", ".dockerfile", "dockerfile",
    ".conf", ".cfg", ".ini", ".toml", ".tf", ".tfvars", ".hcl", ".gql", ".graphql",
    ".ps1", ".bat", ".cmd", ".jsx", ".tsx", ".vue", ".svelte"
}


def is_likely_binary(file_path: Path, verbose: bool = False) -> bool:
    """
    Check if a file is likely binary by looking for null bytes in the first CHUNK_SIZE bytes.
    Also checks against known text file extensions. Returns False for empty files.
    """
    if not file_path.is_file(): # Cannot check non-files
         if verbose: print(f"Skipping binary check for non-file path: {file_path}", file=sys.stderr)
         return True # Treat non-files as something to skip like binaries

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
                if verbose: print(f"Detected null byte, skipping likely binary file: {file_path}", file=sys.stderr)
                return True

    except IOError as e:
        # File might not be readable, treat as potentially problematic (skip)
        if verbose: print(f"IOError checking file type, skipping: {file_path} ({e})", file=sys.stderr)
        return True
    except Exception as e:
        if verbose: print(f"Unexpected error checking file type, skipping: {file_path} ({e})", file=sys.stderr)
        return True # Skip on unexpected errors
    return False


def get_args():
    parser = argparse.ArgumentParser(
        description="Process text files from specified directories or an explicit file list into a single text output. Skips likely binary files."
    )
    parser.add_argument(
        "source_paths",
        help="Paths to the source directories or files to include. Ignored if -L is used.",
        nargs='*',  # 0 or more allowed, ignored if -L present
        type=Path,
        default=None # Default to None to distinguish from empty list []
    )
    # Reintroduce -L
    parser.add_argument(
        "-L",
        "--file-list-file",
        help="Path to a file containing a list of file paths to include (one per line). If this is used, 'source_paths' arguments are ignored. Pass `-` to read the list from stdin.",
        default=None,
        type=str, # Read as string first to handle '-' easily
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
        help="Do not ignore .git directory (only applies when processing source_paths, not with -L)",
        action="store_true",
    )
    parser.add_argument(
        "-Z",
        "--no-ignore-gitignore-and-gitattributes",
        help="Do not ignore .gitignore and .gitattributes files (only applies when processing source_paths, not with -L)",
        action="store_true",
    )
    # cSpell:disable
    parser.add_argument(
        "-i",
        "--gptignore",
        help="Path to .gptignore file. If not specified, looks for .gptignore in the current working directory (only applies when processing source_paths, not with -L).",
        type=Path,
        default=Path(".gptignore") # Default to CWD
    )
    parser.add_argument(
        "-I", "--no-gptignore", help="Do not use any .gptignore file (only applies when processing source_paths, not with -L)", action="store_true"
    )
    # cSpell:enable
    parser.add_argument(
        "-n",
        "--dry-run",
        "--list-files-would-be-included",
        help="List files that would be included in the output (grouped by source directory/file or listed if -L is used)",
        action="store_true",
    )
    parser.add_argument(
        "--no-structure",
        help="Do not include the directory structure section for each source directory (only applies when processing source_paths, not with -L)",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print verbose output, including skipped binary files and ignored files/dirs.",
        action="store_true",
    )

    args = parser.parse_args()

    # Validate inputs: Need either source_paths or -L
    if not args.source_paths and args.file_list_file is None:
         parser.error("You must provide at least one source_path or use the -L option.")

    # Resolve source paths if they were provided (and might be used)
    if args.source_paths:
        args.source_paths = [p.resolve() for p in args.source_paths]

    # Convert file_list_file string to Path object if it's not '-'
    if args.file_list_file is not None and args.file_list_file != '-':
        args.file_list_file = Path(args.file_list_file)

    return args


def get_ignore_list(ignore_file_path: Path, verbose: bool = False) -> list[str]:
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
    (Used when NOT using -L)
    Finds all text files within or at the source_path that are not ignored.
    Skips likely binary files. Returns absolute paths.
    """
    included_files = []
    if source_path.is_file():
        base_path = source_path.parent
        try:
            relative_path = source_path.relative_to(base_path)
        except ValueError:
             if verbose: print(f"Warning: Could not determine relative path for {source_path} based on {base_path}", file=sys.stderr)
             relative_path = source_path # Fallback for should_ignore check, might not work as expected

        if not should_ignore(relative_path, ignore_list):
            if not is_likely_binary(source_path, verbose):
                included_files.append(source_path)
            # Verbose message for binary skip is in is_likely_binary
        elif verbose:
             print(f"Ignoring file due to rule: {source_path}", file=sys.stderr)

    elif source_path.is_dir():
        base_path = source_path
        for root, dirs, files in os.walk(source_path, topdown=True):
            root_path = Path(root)
            try:
                 relative_root = root_path.relative_to(base_path)
            except ValueError:
                 if verbose: print(f"Warning: Could not determine relative path for {root_path} based on {base_path}", file=sys.stderr)
                 continue # Skip this directory if path calculation fails

            # Filter directories based on ignore list
            original_dirs = list(dirs) # Copy before modifying
            dirs[:] = [d for d in dirs if not should_ignore(relative_root / d, ignore_list)]
            if verbose:
                 skipped_dirs = set(original_dirs) - set(dirs)
                 for skipped in skipped_dirs:
                     print(f"Ignoring directory due to rule: {root_path / skipped}", file=sys.stderr)


            for file in files:
                file_path = root_path / file
                try:
                    relative_file_path = file_path.relative_to(base_path)
                except ValueError:
                     if verbose: print(f"Warning: Could not determine relative path for {file_path} based on {base_path}", file=sys.stderr)
                     continue # Skip this file if path calculation fails

                if not should_ignore(relative_file_path, ignore_list):
                    if not is_likely_binary(file_path, verbose):
                        included_files.append(file_path)
                    # Verbose message for binary skip is in is_likely_binary
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
    relative_paths_dict = {}
    for p in file_paths:
        try:
             relative_paths_dict[p.relative_to(base_path)] = p
        except ValueError:
             print(f"Error creating relative path for tree item {p} (base: {base_path})", file=sys.stderr)
             # Include with absolute path as fallback? Or just skip from tree? Skip for now.

    if not relative_paths_dict:
        return " (No files relative to base path found for tree)\n"

    sorted_relative_paths = sorted(relative_paths_dict.keys())

    tree_dict = {}
    for rel_path in sorted_relative_paths:
        current_level = tree_dict
        parts = rel_path.parts
        for i, part in enumerate(parts):
            if i == len(parts) - 1: # It's a file
                current_level[part] = None # Mark as file
            else: # It's a directory
                if part not in current_level:
                    current_level[part] = {}
                # Ensure we don't overwrite a directory entry with a file entry if names collide (rare)
                if current_level.get(part) is None: # Check if it exists and is None (a file)
                    print(f"Warning: Path conflict detected in tree generation near '{'/'.join(parts[:i+1])}'", file=sys.stderr)
                    # Decide how to handle: skip, overwrite, mark differently? For now, just warn.
                # Allow overwriting a file entry with a dir entry if needed (e.g. file 'foo', dir 'foo/bar')
                if current_level.get(part) is None: # Check if it's marked as a file
                     current_level[part] = {} # Upgrade to directory
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


def write_files_to_output(base_path: Path, file_paths: List[Path], output_file, verbose: bool = False):
    """
    Writes the content of each file to the output, prefixed with its relative path to base_path.
    If relative path fails, uses the filename.
    """
    # Sort files for consistent output. Try relative sort first.
    sorted_files = []
    try:
        # Use a tuple for sorting: (directory parts, filename)
        sorted_files = sorted(file_paths, key=lambda p: (p.relative_to(base_path).parts[:-1], p.relative_to(base_path).name))
    except ValueError:
        if verbose: print(f"Warning: Could not sort files relative to {base_path}. Using absolute path sort.", file=sys.stderr)
        sorted_files = sorted(file_paths) # Fallback to absolute path sort

    for file_path in sorted_files:
        try:
            # Open in text mode, relying on the earlier binary check
            with open(file_path, "r", encoding='utf-8', errors="ignore") as file:
                contents = file.read()

            # Determine display path: relative to base_path if possible, else just name
            try:
                display_path = file_path.relative_to(base_path).as_posix()
            except ValueError:
                display_path = file_path.name # Fallback

            output_file.write("-" * 4 + "\n")
            output_file.write(f"{display_path}\n")
            output_file.write(f"{contents}\n")
        except Exception as e:
            # Report error but continue with other files
            print(f"Error reading text file {file_path}: {e}", file=sys.stderr)
            output_file.write("-" * 4 + "\n")
            try: # Try to get display path again for error message
                display_path = file_path.relative_to(base_path).as_posix()
            except ValueError:
                display_path = file_path.name
            output_file.write(f"{display_path} (Error reading content)\n")
            output_file.write(f"[Content could not be read due to error: {e}]\n")


def main() -> None:
    args = get_args()
    verbose = args.verbose

    # --- Mode Determination: Explicit List (-L) or Source Paths ---
    explicit_list_mode = args.file_list_file is not None
    final_files_to_process: List[Path] = []
    files_base_path: Path = Path.cwd() # Default base for relative paths, especially for -L

    if explicit_list_mode:
        if verbose: print(f"Mode: Explicit file list (-L '{args.file_list_file}')", file=sys.stderr)
        raw_file_paths: List[str] = []
        try:
            if args.file_list_file == '-':
                if verbose: print("Reading file list from stdin...", file=sys.stderr)
                raw_file_paths = [line.strip() for line in sys.stdin if line.strip()]
            else:
                file_list_path : Path = args.file_list_file # Already converted to Path if not '-'
                if verbose: print(f"Reading file list from {file_list_path}...", file=sys.stderr)
                if not file_list_path.is_file():
                     raise FileNotFoundError(f"File list not found: {file_list_path}")
                with open(file_list_path, "r", encoding='utf-8', errors='ignore') as f:
                    raw_file_paths = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading file list from '{args.file_list_file}': {e}", file=sys.stderr)
            sys.exit(1)

        if not raw_file_paths:
            print("No file paths provided in the list via -L. Exiting.", file=sys.stderr)
            sys.exit(0)

        # Process the explicit list
        for file_str in raw_file_paths:
            # Try resolving relative to CWD first, then treat as absolute if needed
            path = Path(file_str)
            if not path.is_absolute():
                path = Path.cwd() / path
            # Resolve to clean up ".." etc. but catch errors for non-existent files
            try:
                 resolved_path = path.resolve(strict=True) # strict=True requires file exists
            except FileNotFoundError:
                 print(f"Warning: File specified in list not found: {path}", file=sys.stderr)
                 continue
            except Exception as e: # Catch other potential resolution errors
                 print(f"Warning: Could not resolve path '{path}': {e}", file=sys.stderr)
                 continue

            # Check if it's a text file (binary check happens here)
            # Ignore rules (-i, -I, -G, -Z) are NOT applied in -L mode
            if not is_likely_binary(resolved_path, verbose):
                final_files_to_process.append(resolved_path)
            # Verbose message for binary skip is now inside is_likely_binary

        # Base path for output remains CWD for -L mode

    else:
        # --- Source Paths Mode (Original Logic) ---
        if verbose: print(f"Mode: Processing source paths: {args.source_paths}", file=sys.stderr)
        # --- Ignore List Setup ---
        ignore_list = []
        gptignore_path = args.gptignore
        if not args.no_gptignore:
            if gptignore_path.exists():
                 if verbose: print(f"Using ignore file: {gptignore_path.resolve()}", file=sys.stderr)
                 ignore_list.extend(get_ignore_list(gptignore_path, verbose))
            elif args.gptignore != Path(".gptignore"):
                 print(f"Warning: Specified ignore file not found: {gptignore_path.resolve()}", file=sys.stderr)
            elif verbose:
                 print("No .gptignore file found in current directory.", file=sys.stderr)

        if not args.no_ignore_git:
            ignore_list.append(".git")
            ignore_list.append(".git/*")
        if not args.no_ignore_gitignore_and_gitattributes:
            ignore_list.append(".gitignore")
            ignore_list.append(".gitattributes")

        if ignore_list and verbose:
            print(f"Effective ignore patterns: {ignore_list}", file=sys.stderr)

        # --- File Discovery ---
        # Dictionary to hold {source_path: [included_files]} - for structure generation
        source_path_files: Dict[Path, List[Path]] = {}
        for source_path in args.source_paths:
            if not source_path.exists():
                 print(f"Warning: Source path '{source_path}' does not exist. Skipping.", file=sys.stderr)
                 continue

            included = get_included_files_for_path(source_path, ignore_list, verbose)

            if included:
                source_path_files[source_path] = included
                final_files_to_process.extend(included) # Also add to the flat list
            elif source_path.is_dir() and verbose:
                 print(f"No non-ignored text files found in directory: {source_path}", file=sys.stderr)
            # Verbose message for skipped files now inside get_included_files_for_path / is_likely_binary

        # Remove duplicates if a file ended up being included via multiple source paths
        final_files_to_process = sorted(list(set(final_files_to_process)))

        # Base path for relative paths in output: For source_paths mode, this will be handled per-group later.


    # --- Exit if no files found ---
    if not final_files_to_process:
        print("No text files to include found based on provided paths/list and filters. Exiting.", file=sys.stderr)
        return

    total_files_count = len(final_files_to_process)

    # --- Dry Run ---
    if args.dry_run:
        print("--- Files that would be included: ---", file=sys.stderr)
        if explicit_list_mode:
            print(f"(From explicit list: {args.file_list_file})")
            # Use CWD as base for display paths
            base_path_display = Path.cwd()
            print(f"(Paths relative to: {base_path_display})")
            for file_path in final_files_to_process: # Already filtered and resolved
                 try:
                     display_path = file_path.relative_to(base_path_display).as_posix()
                 except ValueError:
                     display_path = file_path.as_posix() # Fallback to absolute if not relative
                 print(f"  {display_path}", file=sys.stderr)
        else: # Source Paths Mode
            # Print grouped by source path as before
            for source_path, files in source_path_files.items():
                 base_path = source_path if source_path.is_dir() else source_path.parent
                 print(f"\n--- From source: {source_path} (base for paths: {base_path}) ---", file=sys.stderr)
                 if not files:
                    print("  (No files)", file=sys.stderr)
                    continue

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
                 # Choose default based on mode
                 preamble = DEFAULT_PREAMBLE_FILE_COLLECTION if explicit_list_mode else DEFAULT_PREAMBLE_MULTI_DIR
        else:
             # Choose default based on mode
             preamble = DEFAULT_PREAMBLE_FILE_COLLECTION if explicit_list_mode else DEFAULT_PREAMBLE_MULTI_DIR
        output_target.write(f"{preamble}\n\n")

        # --- Process Files ---
        if explicit_list_mode:
            # Write a single header and then all files relative to CWD
            output_target.write("-" * 4 + " Files from explicit list" + "\n")
            output_target.write(f"({args.file_list_file})\n") # Indicate source list
            write_files_to_output(files_base_path, final_files_to_process, output_target, verbose)
        else:
            # Source Paths Mode: Iterate through groups found earlier
            first_section = True
            for source_path, included_files in source_path_files.items():
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

                 # Write file contents, using the correct base_path for this group
                 write_files_to_output(base_path, included_files, output_target, verbose)


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
                     epilogue_content = DEFAULT_EPILOGUE
            else:
                epilogue_content = DEFAULT_EPILOGUE

            if epilogue_content is None:
                 output_target.write("\n\n--END--\n")
            elif epilogue_content is DEFAULT_EPILOGUE:
                 output_target.write(epilogue_content) # Default already has spacing and --END--
            else: # Custom epilogue
                 output_target.write("\n\n--END--\n\n") # Standard separator and end marker
                 output_target.write(epilogue_content)
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
                 pyperclip_error = f"Error copying to clipboard: {e}. "
                 pyperclip_error += "Ensure 'pyperclip' is installed (`pip install pyperclip`). "
                 pyperclip_error += "On Linux, you might also need 'xclip' or 'xsel'. "
                 pyperclip_error += "On WSL, ensure host integration is working or install 'win32yank'."
                 print(pyperclip_error, file=sys.stderr)
        else:
            output_target.flush()
            content_length = 0
            try:
                 content_length = os.path.getsize(args.output)
            except OSError as e:
                 print(f"Warning: Could not get output file size: {e}", file=sys.stderr)
                 # Try stream position as fallback
                 try:
                      content_length = output_target.tell()
                 except (OSError, ValueError):
                      pass # Give up trying to get size

            print(f"Output written to {args.output}. Total text files: {total_files_count}. Total chars: {content_length or 'unknown'}", file=sys.stderr)

    finally:
        if not args.copy and not isinstance(output_target, io.StringIO):
            if not output_target.closed:
                 output_target.close()


if __name__ == "__main__":
    main()