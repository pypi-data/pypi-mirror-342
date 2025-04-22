# VisionFi Python Package Examples

This directory contains example code and resources demonstrating how to use the VisionFi Python package.

## Contents

- **basic_usage.py** - Demonstrates the core functionality of the VisionFi client
- **cli/** - Command-line interface for interacting with the VisionFi API
- **files/invoices/** - Sample files for testing document analysis

## Dependencies

All examples use the VisionFi Python package, which relies on industry-standard dependencies:

- **requests** - ~721 million monthly downloads, 52k+ GitHub stars (Apache 2.0)
- **pydantic** - ~348 million monthly downloads, 23k+ GitHub stars (MIT)
- **google-auth** - ~202 million monthly downloads (Apache 2.0)
- **google-auth-oauthlib** - ~71 million monthly downloads (Apache 2.0)

The CLI example additionally uses:

- **colorama** - ~233 million monthly downloads, 3.7k GitHub stars (BSD 3-Clause)

## Getting Started

The easiest way to get started is to run the basic usage example:

```bash
# Install the VisionFi client package
pip install visionfi-client

# Run the basic example (you'll need to provide your own service account)
python basic_usage.py
```

For more advanced usage, explore the CLI examples under the `cli/` directory.

## License

All examples are provided under the MIT License, same as the VisionFi package.