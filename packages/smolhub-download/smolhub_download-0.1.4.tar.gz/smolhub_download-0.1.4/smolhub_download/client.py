import os
import requests
# import torch # Keep if users might expect it, otherwise remove
from tqdm import tqdm
# from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor # No longer needed

# Supabase Constants
SUPABASE_URL = "https://uohiifugwkrermjjhjgz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVvaGlpZnVnd2tyZXJtampoamd6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ4ODQ2MzAsImV4cCI6MjA2MDQ2MDYzMH0.y5eQpHf9UTuKFIk3en4x_4Kudfm1XKVxw0IvVMsN0ho" # Use the public anon key

# Import Supabase client
try:
    from supabase import create_client, Client
except ImportError:
    # Provide a helpful error message if supabase is not installed
    raise ImportError("The 'supabase' library is required for download functionality. "
                      "Please install it using: pip install supabase")

class SmolHubClient:
    def __init__(self):
        """Initializes the SmolHubClient, focusing on download functionality via Supabase."""
        try:
            self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("Supabase client initialized successfully.")
        except Exception as e:
            print(f"Error initializing Supabase client: {e}")
            self.supabase = None # Ensure supabase is None if initialization fails

    # --- Upload Functions (Commented Out) ---

    # def _get_headers(self):
    #     """(Commented Out) Get headers for API requests."""
    #     pass

    # def upload_model(self, model_path, markdown_path=None, name=None, description=None):
    #     """(Commented Out) Upload a model file."""
    #     print("Upload functionality is disabled in this version.")
    #     pass

    # def list_models(self):
    #     """(Commented Out) Get a list of all available models."""
    #     print("Listing functionality is disabled in this version.")
    #     return []

    # def upload_dataset(self, dataset_path, markdown_path=None, name=None, description=None):
    #     """(Commented Out) Upload a dataset file."""
    #     print("Upload functionality is disabled in this version.")
    #     pass

    # def list_datasets(self):
    #     """(Commented Out) Get a list of all available datasets."""
    #     print("Listing functionality is disabled in this version.")
    #     return []

    # def upload_image(self, image_path, type_folder="models", name=None):
    #     """(Commented Out) Upload an image."""
    #     print("Upload functionality is disabled in this version.")
    #     pass

    # def upload_model_with_image(self, model_path, image_path=None, markdown_path=None, name=None, description=None):
    #     """(Commented Out) Upload a model with an image."""
    #     print("Upload functionality is disabled in this version.")
    #     pass

    # def upload_dataset_with_image(self, dataset_path, image_path=None, markdown_path=None, name=None, description=None):
    #     """(Commented Out) Upload a dataset with an image."""
    #     print("Upload functionality is disabled in this version.")
    #     pass

    # def upload_from_scratch_implementation(self, code_path, markdown_path=None, image_path=None, name=None, description=None):
    #     """(Commented Out) Upload a from-scratch implementation."""
    #     print("Upload functionality is disabled in this version.")
    #     pass

    # --- Download Functions (Modified) ---

    def _download_file_from_url(self, name, url, filename, output_dir):
        """Helper function to download a file from a URL with progress."""
        if not url:
            raise ValueError(f"No download link found for '{name}'.")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Determine the full output path
        output_path = os.path.join(output_dir, filename)

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status() # Raise an exception for bad status codes

            # Get total file size for progress bar
            total_size = int(response.headers.get('content-length', 0))

            print(f"Downloading '{name}' ({filename}) to {output_path}...")
            with open(output_path, 'wb') as f:
                with tqdm(
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    desc=f"Downloading {filename}"
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            size = f.write(chunk)
                            pbar.update(size)
            
            print(f"Successfully downloaded '{name}' to {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error downloading file for '{name}' from {url}: {e}")
        except Exception as e:
            # Clean up partial file if download fails
            if os.path.exists(output_path):
                os.remove(output_path)
            raise IOError(f"An error occurred during download or saving for '{name}': {e}")


    def download_model(self, model_name, output_dir="."):
        """
        Download a model by name using the download_link from Supabase.
        
        Args:
            model_name (str): Name of the model to download.
            output_dir (str, optional): Directory to save the downloaded model file. Defaults to current directory.
            
        Returns:
            str: Path to the downloaded model file.
        
        Raises:
            ValueError: If the model name is not found or has no download link.
            ConnectionError: If there's an issue connecting to Supabase or downloading.
            IOError: If there's an issue saving the file.
        """
        if not self.supabase:
            raise ConnectionError("Supabase client not initialized. Cannot download.")

        try:
            print(f"Querying Supabase for model: {model_name}")
            response = self.supabase.table('model_storage') \
                .select('filename, download_link') \
                .eq('name', model_name) \
                .limit(1) \
                .execute()

            if not response.data:
                raise ValueError(f"Model '{model_name}' not found in Supabase model_storage.")
            
            model_info = response.data[0]
            download_link = model_info.get('download_link')
            filename = model_info.get('filename')

            if not download_link:
                 raise ValueError(f"Model '{model_name}' found, but no 'download_link' is available in Supabase.")
            if not filename:
                 print(f"Warning: Model '{model_name}' has no filename in Supabase. Using model name as filename.")
                 filename = model_name # Fallback filename

            # Use the helper to download
            return self._download_file_from_url(model_name, download_link, filename, output_dir)

        except Exception as e:
            # Catch Supabase client errors or other unexpected issues
            raise ConnectionError(f"Error interacting with Supabase or downloading model '{model_name}': {e}")


    def download_dataset(self, dataset_name, output_dir="."):
        """
        Download a dataset by name using the download_link from Supabase.
        
        Args:
            dataset_name (str): Name of the dataset to download.
            output_dir (str, optional): Directory to save the downloaded dataset file. Defaults to current directory.
            
        Returns:
            str: Path to the downloaded dataset file.

        Raises:
            ValueError: If the dataset name is not found or has no download link.
            ConnectionError: If there's an issue connecting to Supabase or downloading.
            IOError: If there's an issue saving the file.
        """
        if not self.supabase:
            raise ConnectionError("Supabase client not initialized. Cannot download.")

        try:
            print(f"Querying Supabase for dataset: {dataset_name}")
            response = self.supabase.table('dataset_storage') \
                .select('filename, download_link') \
                .eq('name', dataset_name) \
                .limit(1) \
                .execute()

            if not response.data:
                raise ValueError(f"Dataset '{dataset_name}' not found in Supabase dataset_storage.")

            dataset_info = response.data[0]
            download_link = dataset_info.get('download_link')
            filename = dataset_info.get('filename')

            if not download_link:
                 raise ValueError(f"Dataset '{dataset_name}' found, but no 'download_link' is available in Supabase.")
            if not filename:
                 print(f"Warning: Dataset '{dataset_name}' has no filename in Supabase. Using dataset name as filename.")
                 filename = dataset_name # Fallback filename

            # Use the helper to download
            return self._download_file_from_url(dataset_name, download_link, filename, output_dir)

        except Exception as e:
            # Catch Supabase client errors or other unexpected issues
            raise ConnectionError(f"Error interacting with Supabase or downloading dataset '{dataset_name}': {e}")

# Helper functions (can be called directly if needed)
def download_model(model_name, output_dir="."):
    """Convenience function to download a model."""
    client = SmolHubClient()
    return client.download_model(model_name, output_dir)

def download_dataset(dataset_name, output_dir="."):
    """Convenience function to download a dataset."""
    client = SmolHubClient()
    return client.download_dataset(dataset_name, output_dir)

# Example Usage (Optional - can be removed or kept for testing)
if __name__ == '__main__':
    # Example: Download a model
    try:
        # Replace 'Your Model Name' with an actual model name from your Supabase table
        model_file_path = download_model('SmolLlama-130M-Instruct', output_dir='./downloaded_models') 
        print(f"Model downloaded to: {model_file_path}")
    except Exception as e:
        print(f"Error downloading model: {e}")

    # Example: Download a dataset
    try:
        # Replace 'Your Dataset Name' with an actual dataset name from your Supabase table
        dataset_file_path = download_dataset('Frank Lampard Ghost Goal Stance Detection', output_dir='./downloaded_datasets')
        print(f"Dataset downloaded to: {dataset_file_path}")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
