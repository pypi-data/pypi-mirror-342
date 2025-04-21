# QCMD - AI-powered Command Generator

QCMD is a powerful command-line tool that generates shell commands from natural language descriptions using Qwen2.5-Coder via Ollama. The tool now features a modular architecture for improved maintainability and extensibility.

## Features

- Generate shell commands from natural language descriptions
- Interactive shell with command history and autocompletion
- Auto-correction mode that fixes commands automatically
- Log analysis and monitoring with AI assistance
- System status monitoring and configuration management
- Safe command execution with dangerous command detection
- Highly customizable UI with color themes and display options

## Installation

### From PyPI

```bash
pip install ibrahimiq-qcmd
```

### From Source (Development Mode)

```bash
git clone https://github.com/aledanee/qcmd.git
cd qcmd
pip install -e .
```

Make sure you have [Ollama](https://ollama.ai/) installed and running with the Qwen2.5-Coder model:

```bash
ollama pull qwen2.5-coder:0.5b
ollama serve
```

## Usage

### Running QCMD

There are several ways to run QCMD:

1. Using the installed command:
```bash
qcmd "list all files in the current directory"
```

2. Using the Python module:
```bash
python -m qcmd_cli "list all files in the current directory"
```

3. Using the wrapper script (if in project directory):
```bash
./qcmd "list all files in the current directory"
```

4. Using the run_qcmd.py script (if in project directory):
```bash
./run_qcmd.py "list all files in the current directory"
```

### Basic Command Generation

```bash
qcmd "list all files in the current directory"
```

### Execute the Generated Command

```bash
qcmd --execute "check disk space"
```

### Interactive Shell

```bash
qcmd --shell
```

### Log Analysis

```bash
qcmd --logs
```

### System Status

```bash
qcmd --status
```

## Modular Architecture

QCMD has been refactored into a modular architecture for better maintainability and extensibility. The main components are:

### Core Modules

- `qcmd_cli.core.command_generator`: Generates and executes shell commands
- `qcmd_cli.core.interactive_shell`: Interactive shell functionality

### Utility Modules

- `qcmd_cli.utils.history`: Command history management
- `qcmd_cli.utils.session`: Session management
- `qcmd_cli.utils.system`: System status and monitoring

### Log Analysis

- `qcmd_cli.log_analysis.analyzer`: Log content analysis
- `qcmd_cli.log_analysis.log_files`: Log file discovery and selection
- `qcmd_cli.log_analysis.monitor`: Log file monitoring

### User Interface

- `qcmd_cli.ui.display`: UI elements and formatting

### Configuration

- `qcmd_cli.config.settings`: Configuration management

### Command Handling

- `qcmd_cli.commands.handler`: Command-line argument parsing and execution

See [MODULAR_ARCHITECTURE.md](MODULAR_ARCHITECTURE.md) for a detailed explanation of the modular design.

## Development

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/aledanee/qcmd.git
cd qcmd
```

2. Install in development mode:
```bash
pip install -e .
```

3. Install development dependencies:
```bash
pip install pytest
```

### Testing

Run the tests to verify the modular architecture:

```bash
python -m pytest tests/
```

### Directory Structure

```
qcmd/
├── qcmd_cli/                 # Main package
│   ├── commands/             # Command handlers
│   ├── config/               # Configuration management
│   ├── core/                 # Core functionality
│   ├── log_analysis/         # Log analysis modules
│   ├── ui/                   # User interface
│   └── utils/                # Utility modules
├── tests/                    # Test suite
└── run_qcmd.py               # Entry point script
```

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

Please make sure to update tests as appropriate and ensure all tests pass before submitting a pull request.

## Configuration

QCMD stores configuration in `~/.qcmd/config.json`. You can customize:

- Default model
- Temperature for generation
- UI settings (banner, colors, compact mode)
- Update checking behavior
- Maximum attempts for auto-correction

## License

MIT

## Credits

Powered by [Ollama](https://ollama.ai/) and [Qwen2.5-Coder](https://huggingface.co/Qwen/Qwen2.5-0.5B). 