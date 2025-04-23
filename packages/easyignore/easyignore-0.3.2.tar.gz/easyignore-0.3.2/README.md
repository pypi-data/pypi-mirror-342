# easyignore

<p align="left">
    <a href="https://opensource.org/licenses/MIT">
        <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg">
    </a>
    <a href="https://github.com/andrew-s28/easyignore/actions">
        <img alt="GitHub Actions Workflow Status" src="https://github.com/andrew-s28/easyignore/actions/workflows/ci.yaml/badge.svg">
    </a>
    <a href="https://pypi.python.org/pypi/easyignore">
        <img alt="PyPI Release" src="https://img.shields.io/pypi/v/easyignore.svg">
    </a>
    <a href="https://github.com/astral-sh/ruff">
        <img alt="Ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json">
    </a>
</p>

A simple CLI tool to easily create `.gitignore` and `.prettierignore` files for over 500 languages and frameworks.

## Features

- 🚀 Generate `.gitignore` and `.prettierignore` files with a single command
- 📚 500+ languages and frameworks via gitignore.io
- 📋 Shell auto-completion support

## Installation

Using uv (recommended):

```bash
uv tool install easyignore
```

Using pipx:

```bash
pipx install easyignore
```

Alternatively, run without an install using [uvx](https://docs.astral.sh/uv/guides/tools/) ([no auto-complete](#shell-completion)):

```bash
uvx easyignore
```

## Usage

### Basic Examples

Create a `.gitignore` file for Python:

```bash
easyignore python
```

Create a `.gitignore` file for multiple languages separated by a space:

```bash
easyignore python node react
```

Print the ignore file content to stdout without saving to a file:

```bash
easyignore python --print
```

List all available languages and frameworks:

```bash
easyignore --list
```

Create a file with a different name (e.g., `.prettierignore`):

```bash
easyignore react --file .prettierignore
```

### Controlling Output

Specify a file and/or a directory with:

```bash
easyignore python --file .prettierignore --directory .
```

If the directory does not exist, it will be created.

If the file already exists, either append or overwrite it:

```bash
easyignore java --append
```

```bash
easyignore go --overwrite
```

If you don't select an option and the file exists, you will be prompted to decide.

Instead of outputting to a file, you can print to stdout enabling piping to wherever you like:

```bash
easyignore python --print
```

Printing to stdout will disable printing to a file, regardless of what other options are entered.

### Shell Completion

One of the main advantages of **easyignore** is shell auto-completion, supported for bash, zsh, fish, and powershell, powered by [typer](https://typer.tiangolo.com/) auto-complete.

Automatically install the required scripts to your shell profile with:

```bash
easyignore --install-completion
```

Alternatively, you can print the shell completion script:

```bash
easyignore --show-completion
```

[!NOTE]
Auto-complete will only work when **easyignore** is called directly from the command line - `uvx` doesn't support autocomplete.

## Options

| Option | Description |
|--------|-------------|
| `-d, --directory DIRECTORY` | Directory for ignore file. (default: current directory) |
| `-f, --file TEXT` | File name for ignore file. (default: .gitignore) |
| `-a, --append` | Append to existing ignore file. |
| `-o, --overwrite` | Overwrite existing ignore file. |
| `-p, --print` | Print ignore file to stdout instead of saving to file. |
| `-l, --list` | List available languages/frameworks for ignore file. |
| `-i, --install-completion` | Install shell completion for easyignore. |
| `-s, --show-completion` | Show shell completion for easyignore. |
| `-h, --help` | Show help message and exit. |

## How It Works

**easyignore** currently uses the [gitignore.io](https://gitignore.io) API to fetch the latest ignore patterns for your selected languages and frameworks. However, **easyignore** is designed not to be locked into this decision - the specific APIs used to retrieve .gitignore may be expanded or swapped with no user functionality changes. This is particularly relevant since the [gitignore.io template repository](https://github.com/toptal/gitignore/tree/0a7fb01801c62ca53ab2dcd73ab96185e159e864) was recently archived and alternatives such as [donotcommit](https://github.com/brasilisclub/donotcommit) may be preferred in the future.

The command line interface for **easyignore** is built with [typer](https://typer.tiangolo.com/), with a modified shell completion solution that uses [shellingham](https://github.com/sarugaku/shellingham) to identify the shell. The templates are retrieved using [requests](https://requests.readthedocs.io/en/latest/) and printed to the console with [Rich](https://rich.readthedocs.io/en/stable/introduction.html).

## License

[MIT](LICENSE)
