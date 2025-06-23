# Local Tokenizer

A Python CLI tool to count tokens in a local directory, respecting `.gitignore` files and providing detailed analysis of your codebase.

## Features

- 🔍 **Token counting** using OpenAI's tiktoken library (cl100k_base encoding)
- 📁 **Directory traversal** with intelligent filtering
- 🚫 **Gitignore support** - automatically respects `.gitignore` files
- 📊 **Rich output** with beautiful tables and progress bars
- 🎯 **Custom exclusion patterns** via glob patterns
- 📋 **Detailed reporting** with verbose mode
- 🔧 **Binary file detection** to skip non-text files
- ⚡ **Performance optimized** with progress tracking

## Installation

Install directly from the repository:

```bash
pip install git+https://github.com/kudziajaroslaw98/local-tokenizer.git
```

Or clone and install locally:

```bash
git clone https://github.com/kudziajaroslaw98/local-tokenizer.git
cd local-tokenizer
pip install -e .
```

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

- `-v, --verbose`: Show detailed table of all processed files
- `--exclude PATTERN`: Exclude files matching the glob pattern (can be used multiple times)

### Examples

**Verbose output with detailed file listing:**
```bash
localtokens . --verbose
```

**Exclude specific file patterns:**
```bash
localtokens . --exclude "*.log" --exclude "*.tmp"
```

**Analyze a Python project with verbose output:**
```bash
localtokens ~/my-python-project -v
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

1. **Directory Traversal**: Recursively walks through the specified directory
2. **Filtering**: Applies `.gitignore` rules and custom exclusion patterns
3. **Binary Detection**: Automatically skips binary files based on file extensions
4. **Token Counting**: Uses OpenAI's tiktoken library with cl100k_base encoding
5. **Reporting**: Provides detailed statistics and optional file-by-file breakdown

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

- **Code analysis**: Understand the size of your codebase in tokens
- **LLM preparation**: Estimate token counts before feeding code to language models
- **Project assessment**: Get insights into project complexity
- **Documentation**: Generate statistics for project documentation

---

Made with ❤️ by Jarosław Kudzia
