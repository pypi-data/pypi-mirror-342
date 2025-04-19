# SmolHub Download

A Python client library for uploading and downloading models from SmolHub.

## Installation

```bash
pip install smolhub_download
```

## Usage

```python
import sys
import os

# Add the parent directory of smolhub_download to the Python path
# This allows importing the package as if it were installed
current_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.join(current_dir, 'smolhub_download')
sys.path.insert(0, current_dir) 

try:
    # Correct the import path based on the nested structure
    from smolhub_download.client import download_model, download_dataset
    print("Successfully imported download functions from smolhub_download.client.")
except ImportError as e:
    print(f"Error importing smolhub_download.client: {e}")
    print("Please ensure the package structure is correct and dependencies (supabase, requests, tqdm) are installed.")
    sys.exit(1)

# Define the output directory
output_directory = "./smolhub_test_downloads" 
print(f"Attempting downloads to directory: {output_directory}")

# Test dataset download
dataset_name = 'Luis Suarez Handball Stance Detection'
print(f"\n--- Testing Dataset Download: {dataset_name} ---")
try:
    dataset_path = download_dataset(dataset_name, output_dir=output_directory)
    print(f"SUCCESS: Dataset '{dataset_name}' downloaded to {dataset_path}")
except Exception as e:
    print(f"FAILED: Error downloading dataset '{dataset_name}': {e}")

# Test model download
model_name = 'SmolLlama-130M-Pretrained' 
print(f"\n--- Testing Model Download: {model_name} ---")
try:
    model_path = download_model(model_name, output_dir=output_directory)
    print(f"SUCCESS: Model '{model_name}' downloaded to {model_path}")
except Exception as e:
    print(f"FAILED: Error downloading model '{model_name}': {e}")

print("\n--- Download Tests Complete ---")

```

## Features

- Upload PyTorch models to SmolHub
- Download models from SmolHub
- List available models
- Support for model descriptions
- Progress tracking for large uploads/downloads
- Automatic file handling

## Requirements

- Python >= 3.7
- requests >= 2.25.0
- torch >= 1.7.0

## License

MIT License