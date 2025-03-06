import os
import json
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=r'C:\Users\wesho\Documents\my-api\.env')

# Get the credentials JSON string from the environment variable
creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
print(f"creds_json raw content: '{creds_json[:100]}'")

# Check if the environment variable is loaded
if not creds_json:
    raise ValueError("GOOGLE_SHEETS_CREDENTIALS environment variable not set.")

# Parse the JSON string and fix the private key formatting
try:
    creds_dict = json.loads(creds_json)  # Parse as JSON
    print("Parsed JSON successfully!")
    
    # Replace literal "\\n" with actual newlines in the private key
    if "private_key" in creds_dict:
        original_key = creds_dict["private_key"]
        # Remove any extra backslashes and ensure correct formatting
        creds_dict["private_key"] = original_key.replace("\\n", "\n")
        print("Reformatted private_key:", creds_dict["private_key"][:50])
    else:
        raise ValueError("No 'private_key' found in creds_dict")

except json.JSONDecodeError as e:
    raise ValueError(f"Failed to parse GOOGLE_SHEETS_CREDENTIALS as JSON: {e}")

print("Reformatted private_key full content:\n", creds_dict["private_key"])

# Authenticate with the modified credentials
try:
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=[
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    print("Credentials loaded successfully!")
except Exception as e:
    print(f"Error loading credentials: {e}")