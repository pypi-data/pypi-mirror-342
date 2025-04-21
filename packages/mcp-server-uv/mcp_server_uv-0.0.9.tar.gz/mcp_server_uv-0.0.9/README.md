# MCP Server UV

A Model Context Protocol (MCP) server implementation for the UV package manager. This server provides MCP-compatible interfaces for managing Python packages and virtual environments using UV.

## Features

- **Package Management**
  - Install, uninstall, and upgrade Python packages
  - List installed packages
  - Add and remove project dependencies
  - Compile and sync requirements
  - View dependency trees

- **Project Management**
  - Initialize new Python projects
  - Create and update lockfiles
  - Build and publish packages
  - Run commands in project environment

## Installation

```bash
pip install mcp-server-uv
```

## Requirements

- Python >= 3.11
- UV >= 0.1.10
- mcp-python >= 0.1.0

## Usage

The server can be used as a Model Context Protocol server in compatible environments. It provides the following tools:

### Package Management Tools

- `uv_pip_list`: List installed packages
- `uv_pip_install`: Install Python packages
- `uv_pip_uninstall`: Remove packages from virtual environment
- `uv_pip_upgrade`: Upgrade Python packages
- `uv_pip_compile`: Generate requirements.txt with hashes
- `uv_pip_sync`: Sync virtual environment with requirements.txt

### Project Management Tools

- `uv_init`: Initialize a new Python project
- `uv_add`: Add project dependencies
- `uv_remove`: Remove project dependencies
- `uv_sync`: Sync project dependencies
- `uv_lock`: Update lockfile
- `uv_run`: Run commands in project environment
- `uv_tree`: View dependency tree
- `uv_build`: Build distribution archives
- `uv_publish`: Publish to package index

## Development

### Setup Development Environment

1. Clone the repository
2. Install development dependencies:
```bash
uv pip install -e ".[test]"
```

### Running Tests

```bash
pytest
```

### Test Coverage

The project uses pytest-cov for coverage reporting. Run tests with coverage:

```bash
pytest --cov=mcp_server_uv --cov-report=term-missing
```

## License

This project is open source and available under the MIT License.

## Author

- Liu Heng (liuheng@bonree.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.