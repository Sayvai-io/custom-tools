import pandas as pd
import requests

# Azure AD App information
client_id = "your_client_id"
client_secret = "your_client_secret"
tenant_id = "your_tenant_id"

# Power BI Workspace and Report information
workspace_id = "your_workspace_id"
report_id = "your_report_id"

# Power BI REST API endpoints
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
report_visualizations_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}/pages"

# Get Access Token for retrieving visualizations
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "resource": "https://graph.microsoft.com",
}

token_response = requests.post(token_url, data=token_data)
access_token = token_response.json().get("access_token")

# Retrieve visualizations from the Power BI report
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

response = requests.get(report_visualizations_url, headers=headers)

if response.status_code == 200:
    visualizations_data = response.json()["value"]

    # Loop through each visualization and get the ID
    for visualization in visualizations_data:
        visualization_id = visualization["id"]
        visualization_name = visualization["displayName"]

        print(
            f"Visualization Name: {visualization_name}, Visualization ID: {visualization_id}"
        )

        # Get Access Token for retrieving visualization data
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "resource": "https://graph.microsoft.com",
        }

        token_response = requests.post(token_url, data=token_data)
        access_token = token_response.json().get("access_token")

        # Retrieve data from the Power BI visualization
        visualization_data_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}/visualizations/{visualization_id}/data"
        response = requests.get(
            visualization_data_url, headers={"Authorization": f"Bearer {access_token}"}
        )

        if response.status_code == 200:
            # Convert JSON data to Pandas DataFrame
            data = response.json()["dataPoints"]
            df = pd.DataFrame(data)

            # Save DataFrame to CSV
            df.to_csv(
                f"power_bi_visualization_data_{visualization_name}.csv", index=False
            )
            print(
                f"Visualization data for {visualization_name} exported to CSV successfully."
            )
        else:
            print(
                f"Error retrieving visualization data. Status code: {response.status_code}, Response: {response.text}"
            )
else:
    print(
        f"Error retrieving visualizations. Status code: {response.status_code}, Response: {response.text}"
    )
