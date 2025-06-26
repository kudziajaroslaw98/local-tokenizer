# Local Tokenizer

A Python CLI tool to count tokens in a local directory, respecting `.gitignore` files and providing detailed analysis of your codebase.

## Features

- 🔍 **Token counting** using OpenAI's tiktoken library (`cl100k_base` encoding)
- 📝 **Context File Generation**: Create a single output file with a directory tree and all processed file contents, perfect for use with LLMs.
- 📁 **Directory traversal** with intelligent filtering and directory pruning
- 🚫 **Gitignore support** - automatically respects `.gitignore` files
- 📊 **Rich output** with beautiful tables and progress bars
- 🎯 **Custom exclusion patterns** via glob patterns
- 📋 **Detailed reporting** with verbose mode
- 🔧 **Binary file detection** to skip non-text files
- ⚡ **Performance optimized** with progress tracking

## Installation

There are two ways to install `localtokens`.

### Option 1: Direct Install (for Users)

Install the latest version directly from the GitHub repository.

```bash
pip install git+https://github.com/kudziajaroslaw98/local-tokenizer.git
```

This will install the command, but you will need to ensure `~/.local/bin` is in your `PATH`.

### Option 2: Local Development Setup (Recommended)

This method is recommended as it creates an isolated environment and is required for contributing.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/kudziajaroslaw98/local-tokenizer.git
    cd local-tokenizer
    ```

2.  **Create a virtual environment:**
    This is a crucial step to avoid conflicts with other Python packages.

    ```bash
    python3 -m venv .venv
    ```

3.  **Activate the virtual environment:**
    This tells your shell to use the tools installed inside `.venv`.

    ```bash
    source .venv/bin/activate
    ```

    Your terminal prompt should now start with `(.venv)`.

4.  **Install in editable mode:**
    This installs the tool and makes the `localtokens` command available.
    ```bash
    pip install -e .
    ```

## Troubleshooting

### `bash: localtokens: command not found...`

This almost always means **your virtual environment is not active.**

**Solution:**

1.  Navigate to the project directory: `cd /path/to/local-tokenizer`.
2.  Run the activation command: `source .venv/bin/activate`.
3.  Your prompt should now start with `(.venv)`. The command will now work.

**Note:** You must re-activate the environment every time you open a new terminal.

## Usage

### Basic Usage

Count tokens in the current directory:

```bash
localtokens .
```

Count tokens in a specific directory:

```bash
localtokens /path/to/your/project
```

### Options

- `-v, --verbose`: Show detailed table of all processed files.
- `-o, --create-output-file FILENAME`: Create a single output file with a directory tree and all processed file contents.
- `--exclude PATTERN`: Exclude files matching the glob pattern (can be used multiple times).

### Examples

**Verbose output with detailed file listing:**

```bash
localtokens . --verbose
```

**Create a context file for an LLM:**

```bash
localtokens . -o project_context.txt
```

**Exclude specific file patterns:**

```bash
localtokens . --exclude "*.log" --exclude "*.tmp"
```

## Output

The tool provides a comprehensive analysis summary including:

- **Total token count** across all processed files
- **Files processed** count
- **Files skipped** breakdown by reason:
  - Ignored by `.gitignore`
  - Excluded by custom patterns
  - Binary files
  - Decoding errors

### Sample Output

```
┌─────────────────── Analysis Summary ───────────────────┐
│ Total Tokens                                    12,547 │
│ Files Processed                                     42 │
│ Files Skipped (Ignored by .gitignore)               8 │
│ Files Skipped (Excluded by pattern)                 0 │
│ Files Skipped (Binary)                               3 │
│ Files with Errors (Decoding)                         0 │
└─────────────────────────────────────────────────────────┘
```

## How It Works

1. **Directory Traversal**: Recursively walks through the directory, intelligently pruning entire branches (like `node_modules`) that are ignored.
2. **Filtering**: Applies `.gitignore` rules and custom exclusion patterns.
3. **Binary Detection**: Automatically skips binary files based on file extensions.
4. **Token Counting**: Uses OpenAI's `tiktoken` library with `cl100k_base` encoding.
5. **Reporting**: Provides detailed statistics and optional file-by-file breakdown.

## Supported File Types

The tool processes all text files and automatically skips binary files including:

- Compiled files (`.so`, `.dll`, `.exe`)
- Archives (`.zip`, `.tar`, `.gz`)
- Images (`.png`, `.jpg`, `.gif`)
- Audio/Video files (`.mp3`, `.mp4`, `.avi`)
- Documents (`.pdf`, `.doc`, `.xls`)
- Fonts (`.woff`, `.ttf`)
- And many more...

## Requirements

- Python 3.9+
- Dependencies (automatically installed):
  - `click>=8.0` - CLI framework
  - `tiktoken>=0.5` - Token counting
  - `gitignore-parser>=0.1` - Gitignore parsing
  - `rich>=13.0` - Rich terminal output

## Development

### Project Structure

```
local-tokenizer/
├── src/
│   └── tokenizer/
│       ├── __init__.py
│       ├── main.py      # CLI interface
│       ├── engine.py    # Core processing logic
│       └── utils.py     # Utility functions
├── pyproject.toml       # Project configuration
└── README.md
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Use Cases

- **Code analysis**: Understand the size of your codebase in tokens.
- **LLM Context Preparation**: Generate a single, clean text file of your entire codebase to use as context for language models.
- **Project assessment**: Get insights into project complexity.
- **Documentation**: Generate statistics for project documentation.

---

Made with ❤️ by Jarosław Kudzia
