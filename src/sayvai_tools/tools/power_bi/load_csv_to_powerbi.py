import requests
import json
import pandas as pd

# Azure AD App information
client_id = "your_client_id"
client_secret = "your_client_secret"
tenant_id = "your_tenant_id"

# Power BI Workspace information
workspace_id = "your_workspace_id"

# Power BI REST API endpoints
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
datasets_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets"

# Get Access Token
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': 'https://graph.microsoft.com'
}

token_response = requests.post(token_url, data=token_data)
access_token = token_response.json().get('access_token')

# Load CSV data into a Pandas DataFrame
csv_file_path = "path/to/your/file.csv"
df = pd.read_csv(csv_file_path)

# Convert DataFrame to JSON
tables = []
for table_name, table_data in df.items():
    columns = [{'name': col} for col in table_data.columns]
    tables.append({'name': table_name, 'columns': columns})

# Publish Dataset to Power BI
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

dataset_payload = {
    'name': 'YourDatasetName',
    'tables': tables
}

response = requests.post(datasets_url, headers=headers, json=dataset_payload)

if response.status_code == 201:
    print("Dataset published successfully.")
else:
    print(f"Error publishing dataset. Status code: {response.status_code}, Response: {response.text}")
