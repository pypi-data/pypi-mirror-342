import torch
from smolhub_download import SmolHubClient
import os



client = SmolHubClient()

# Upload the model
print('Uploading model...')
client.upload_model('../snapshot_6750.pt', name='snapshot_6750.pt', description='Test model for testing')
# List all models
print('Listing models...')
models = client.list_models()
print('Models:')
for model in models:
    print(f"Name: {model['name']}, Description: {model['description']}, Size: {model['size']} bytes")

# Download as test_model.pt
print('Downloading model...')
client.download_model('snapshot_6750.pt', 'test_model.pt')

# Load the model to GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Loading model to {device}...')
model = torch.load('test_model.pt', map_location=device)

print('Model loaded successfully!')

# Clean up
os.remove('test_model.pt')
print('Test model file removed')
