# VisionFi Python Client

A Python client library for the VisionFi document analysis platform.

> **Note:** This package is a wrapper for the VisionFi API, which is a subscription service. A valid service account is required to use this package with the VisionFi API. Contact VisionFi for subscription details and to obtain your service account credentials.

## Installation

```bash
pip install visionfi-client
```

## Basic Usage

```python
from visionfi import VisionFi
import pathlib

# Initialize client
client = VisionFi(service_account_path='./service-account.json')

# Check authentication
auth_result = client.verify_auth()
print(f"Authentication successful: {auth_result.data}")

# Get client information
client_info = client.get_client_info()
if client_info.success:
    print(f"Client name: {client_info.data.name}")
    print(f"Client status: {client_info.data.status}")

# Analyze a document
with open('document.pdf', 'rb') as f:
    file_data = f.read()

job = client.analyze_document(file_data, {
    'file_name': 'document.pdf',
    'analysis_type': 'auto_loan_abstract'
})

print(f"Analysis job created: {job.uuid}")

# Get results (with polling)
results = client.get_results(
    job.uuid,
    poll_interval=5000,  # 5 seconds
    max_attempts=30,     # Up to 2.5 minutes
    early_warning_attempts=5
)

if results.status == 'processed':
    print("Analysis processed successfully!")
    print(f"Results: {results.results}")
```

## Features

- Authentication with Google service accounts
- Document analysis submission
- Results retrieval with polling
- Client information and workflow retrieval
- Comprehensive error handling

## License

MIT

## Acknowledgments

This package includes components licensed under Apache License 2.0 and MIT License. It builds on industry-standard libraries (requests, pydantic, google-auth) with hundreds of millions of monthly downloads.

See [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md) for statistics and [NOTICE.txt](NOTICE.txt) for licensing details.