# SmolHub Download

A Python client library for uploading and downloading models from SmolHub.

## Installation

```bash
pip install smolhub_download
```

## Usage

```python
from smolhub_download import SmolHubClient

# Initialize the client
client = SmolHubClient()  # Default URL is http://localhost:5000
# Or specify a custom URL:
# client = SmolHubClient(base_url="https://your-smolhub-instance.com")

# Upload a model
result = client.upload_model(
    model_path="path/to/your/model.pt",
    name="my-model",
    description="My awesome model"  # Optional
)
print(f"Model uploaded: {result}")

# Download a model
model_path = client.download_model(
    model_name="my-model",
    output_path="downloaded_model.pt"  # Optional
)
print(f"Model downloaded to: {model_path}")

# List available models
models = client.list_models()
for model in models:
    print(f"Model: {model['name']}")
    print(f"Description: {model.get('description', 'No description')}")
    print(f"Size: {model['size']} bytes")
    print("---")
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