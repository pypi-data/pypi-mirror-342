import os
import sys
import pytest
import torch
from smolhub_download import SmolHubClient

# Ensure using conda environment and GPU is available
if not os.environ.get('CONDA_DEFAULT_ENV'):
    pytest.skip("Tests must be run in conda environment", allow_module_level=True)

if not torch.cuda.is_available():
    pytest.skip("CUDA is not available", allow_module_level=True)

@pytest.fixture
def client():
    return SmolHubClient()

@pytest.fixture
def test_model():
    # Create a simple test model
    model = torch.nn.Linear(10, 1)
    model = model.cuda()  # Move to GPU
    path = "test_model.pt"
    torch.save(model.state_dict(), path)
    yield path
    # Cleanup
    if os.path.exists(path):
        os.remove(path)

def test_upload_model(client, test_model):
    result = client.upload_model(
        model_path=test_model,
        name="test-model",
        description="Test model for testing"
    )
    assert isinstance(result, dict)
    assert 'model' in result
    assert result['model']['name'] == "test-model"

def test_list_models(client):
    models = client.list_models()
    assert isinstance(models, list)
    if len(models) > 0:
        assert 'name' in models[0]

def test_download_model(client, test_model):
    # First upload a model
    client.upload_model(
        model_path=test_model,
        name="test-download-model"
    )
    
    # Then download it
    output_path = "downloaded_test_model.pt"
    downloaded_path = client.download_model(
        model_name="test-download-model",
        output_path=output_path
    )
    
    assert os.path.exists(downloaded_path)
    assert os.path.getsize(downloaded_path) > 0
    
    # Load and verify on GPU
    loaded_state = torch.load(downloaded_path, map_location='cuda')
    assert all(t.is_cuda for t in loaded_state.values())
    
    # Cleanup
    os.remove(downloaded_path)

def test_snapshot_workflow(client):
    """Test uploading snapshot_6750.pt and downloading as download_model.pt"""
    snapshot_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "snapshot_6750.pt")
    download_path = "download_model.pt"
    
    try:
        # Verify snapshot exists
        assert os.path.exists(snapshot_path), f"Snapshot file not found at {snapshot_path}"
        original_size = os.path.getsize(snapshot_path)
        
        # Upload the snapshot model
        result = client.upload_model(
            model_path=snapshot_path,
            name="snapshot-6750",
            description="Snapshot model from training"
        )
        assert isinstance(result, dict)
        assert 'model' in result
        assert result['model']['name'] == "snapshot-6750"
        
        # Download the model with new name
        downloaded_path = client.download_model(
            model_name="snapshot-6750",
            output_path=download_path
        )
        
        assert os.path.exists(downloaded_path)
        downloaded_size = os.path.getsize(downloaded_path)
        assert downloaded_size == original_size, f"Downloaded file size {downloaded_size} doesn't match original {original_size}"
        
        # Load just the metadata to verify it's a valid PyTorch file
        # This avoids loading the entire model into memory but loads on GPU
        loaded = torch.load(downloaded_path, map_location='cuda')
        assert loaded is not None
        
    finally:
        # Cleanup downloaded file
        if os.path.exists(download_path):
            os.remove(download_path)







