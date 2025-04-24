# Google Cloud Billing MCP Server

A Model Context Protocol (MCP) server for Google Cloud Billing integration. This server provides tools for interacting with Google Cloud Billing API, enabling Claude and other AI assistants to help you analyze and understand your Google Cloud costs.

## Features

- **Billing Account Management**: View billing accounts and their details
- **Project Billing**: Retrieve billing information for specific projects
- **Services & SKUs**: List available services and their SKUs
- **Billing History**: Access billing history for accounts
- **Resources**: Access metadata about Google Cloud Billing objects
- **Prompts**: Templates for common Google Cloud Billing workflows

## Installation

```bash
pip install mcp-google_cloud_billing
```

## Configuration

### Obtaining API Credentials

To use this MCP server, you need to set up Google Cloud API credentials:

1. **Create a Google Cloud Project** (if you don't already have one):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click on "New Project" and follow the instructions

2. **Enable the Cloud Billing API**:
   - In your project, go to "APIs & Services" > "Library"
   - Search for "Cloud Billing API" and enable it

3. **Create a Service Account**:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Give it a name and description
   - Grant it the "Billing Account Viewer" role (or more permissions if needed)
   - Create a JSON key file and download it

4. **Set Environment Variables**:
   - `GOOGLE_CLOUD_BILLING_API_KEY`: The API key or access token (can be generated from the service account JSON)
   - `GOOGLE_CLOUD_BILLING_PROJECT_ID`: Your Google Cloud Project ID
   - `GOOGLE_CLOUD_BILLING_SERVICE_ACCOUNT`: Path to the service account JSON file (optional)

### Security Notes

- Keep your service account credentials secure and never commit them to version control
- Only grant the minimum necessary permissions to your service account
- Consider implementing credential rotation policies
- This MCP server is read-only for Google Cloud Billing to ensure safety

## Usage

### Starting the server directly

```bash
mcp-google_cloud_billing
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "google-cloud-billing": {
      "command": "uvx",
      "args": [
        "mcp-google_cloud_billing"
      ],
      "env": {
        "GOOGLE_CLOUD_BILLING_API_KEY": "your_api_key_or_token",
        "GOOGLE_CLOUD_BILLING_PROJECT_ID": "your-project-id",
        "GOOGLE_CLOUD_BILLING_SERVICE_ACCOUNT": "/path/to/service-account.json"
      }
    }
  }
}
```

Replace the environment variables with your actual Google Cloud Billing credentials.

## Available Tools

* **list_billing_accounts**: List all billing accounts the user has access to
* **get_billing_account**: Get details of a specific billing account
* **list_project_billing_info**: Get billing information for a project
* **list_billing_account_projects**: List all projects linked to a billing account
* **get_services_for_billing_account**: List all services available for a billing account
* **get_service_skus**: Get SKU information for a particular service
* **get_billing_history**: Get billing history for a specific account

## Available Resources

* **google_cloud_billing://accounts**: List of all Google Cloud Billing accounts
* **google_cloud_billing://account/{account_id}**: Details of a specific billing account
* **google_cloud_billing://project/{project_id}**: Billing information for a specific project
* **google_cloud_billing://services/{account_id}**: Services available for a billing account

## Available Prompts

* **analyze_billing**: Template for analyzing billing data
* **budget_planning**: Template for planning a Google Cloud budget
* **cost_optimization**: Template for optimizing costs of specific Google Cloud services

## Version

0.0.1
