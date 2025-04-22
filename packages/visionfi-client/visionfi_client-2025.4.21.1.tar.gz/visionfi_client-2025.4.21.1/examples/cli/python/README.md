# VisionFi Python CLI

A command-line interface for interacting with the VisionFi document analysis API.

## Features

- Interactive mode with colorful menus
- Authentication with VisionFi API
- Document analysis with various workflows
- Results retrieval and display
- Configuration management
- Developer tools

## Requirements

- Python 3.7+
- colorama - Cross-platform colored terminal text library
  - ~233 million monthly downloads
  - 3.7k GitHub stars
  - BSD 3-Clause License
  - Industry standard for terminal colors in Python
- VisionFi client package

## Installation

1. Ensure you have the VisionFi client package installed:
   ```bash
   pip install visionfi-client
   ```
   
   For development, you can install from source:
   ```bash
   pip install -e /path/to/visionfi-pip-package
   ```

2. Install required dependencies:
   ```bash
   pip install colorama
   ```

## Usage

### Interactive Mode

The interactive mode provides a user-friendly interface with menus and options:

```bash
cd examples/cli/python
python visionfi_cli.py interactive
```

### Command-Line Mode

#### Authentication

Verify authentication with your service account:
```bash
python visionfi_cli.py auth verify
```

Get an authentication token:
```bash
python visionfi_cli.py auth token
```

#### Document Analysis

Analyze a document with a specific workflow:
```bash
python visionfi_cli.py analyze /path/to/document.pdf --workflow auto_loan_abstract
```

#### Results Retrieval

Retrieve results for a specific job UUID:
```bash
python visionfi_cli.py results 12345678-1234-1234-1234-123456789012
```

## Configuration

The CLI stores configuration in `~/.visionfi/config.json`. The configuration includes:
- Service account path
- API endpoint
- Recent job UUIDs
- Debug mode setting

You can manage these settings in the interactive mode under "Account & Configuration."

### Service Account Setup

The CLI provides several ways to configure your service account:

1. **Automatic Detection**:
   - Place your service account JSON file at `~/.visionfi/keys/visionfi_service_account.json`
   - The CLI will automatically detect and use it

2. **Guided Setup**:
   - The CLI will guide new users through the service account setup process
   - It offers options to copy an existing file or manually place the file in the default location

3. **Custom Path**:
   - You can specify a custom path to your service account file
   - This path will be saved in the configuration

## Developer Tools

The CLI includes developer tools for testing and debugging:
- Authentication testing
- Debug mode toggle
- Token retrieval

## License

Same license as the VisionFi package (MIT).

## Dependencies

The CLI example uses the following dependencies:

- **colorama** - Cross-platform colored terminal text library
  - BSD 3-Clause License
  - First released in 2010
  - ~233 million monthly downloads
  - 3.7k GitHub stars
  - Used by over 1.3 million projects
  - Makes ANSI color codes work consistently on all platforms including Windows

- **VisionFi client package** - The main package that builds on:
  - requests (~721 million monthly downloads)
  - pydantic (~348 million monthly downloads)
  - google-auth (~202 million monthly downloads)
  - google-auth-oauthlib (~71 million monthly downloads)