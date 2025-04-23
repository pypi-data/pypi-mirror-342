import os
from google.oauth2 import service_account


def get_credentials():
    # Load credentials from the key file
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GCP_CREDENTIALS'),
        scopes=[
            'https://www.googleapis.com/auth/drive', # For Google Drive
            'https://www.googleapis.com/auth/spreadsheets',  # For Google Sheets
            'https://www.googleapis.com/auth/cloud-platform',  # For Vertex AI and Cloud Storage
        ]
    )
    return credentials