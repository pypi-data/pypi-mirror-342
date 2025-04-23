from . import gcp
from googleapiclient.discovery import build
from google.cloud import storage, aiplatform 

# Access Cloud Storage

def get_session(credentials=None):
    if credentials is None:
        credentials = gcp.get_credentials()
    storage_client = storage.Client(credentials=credentials)
    return storage_client
