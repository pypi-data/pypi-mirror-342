# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Google Cloud Billing MCP")

# Environment variables for Google Cloud Billing configuration
GOOGLE_CLOUD_BILLING_API_KEY = os.environ.get("GOOGLE_CLOUD_BILLING_API_KEY")
GOOGLE_CLOUD_BILLING_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_BILLING_PROJECT_ID")
GOOGLE_CLOUD_BILLING_SERVICE_ACCOUNT = os.environ.get("GOOGLE_CLOUD_BILLING_SERVICE_ACCOUNT")

# Base URL for Google Cloud Billing API
BILLING_API_BASE_URL = "https://cloudbilling.googleapis.com/v1"
GOOGLEAPIS_BASE_URL = "https://cloudresourcemanager.googleapis.com/v1"

# Check if environment variables are set
if not all([GOOGLE_CLOUD_BILLING_API_KEY, GOOGLE_CLOUD_BILLING_PROJECT_ID]):
    print("Warning: Google Cloud Billing environment variables not fully configured. Set GOOGLE_CLOUD_BILLING_API_KEY and GOOGLE_CLOUD_BILLING_PROJECT_ID.", file=sys.stderr)

# Helper function for API requests
async def make_google_cloud_billing_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Make a request to the Google Cloud Billing API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
    
    Returns:
        Response from Google Cloud Billing API as dictionary
    """
    # Determine if endpoint is for billing or another Google API
    if endpoint.startswith("/billing"):
        url = f"{BILLING_API_BASE_URL}{endpoint}"
    elif endpoint.startswith("/projects"):
        url = f"{GOOGLEAPIS_BASE_URL}{endpoint}"
    else:
        url = f"{BILLING_API_BASE_URL}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {GOOGLE_CLOUD_BILLING_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"HTTP Error: {e.response.status_code} - {e.response.text}"
            print(error_message, file=sys.stderr)
            return {
                "error": True,
                "status_code": e.response.status_code,
                "message": error_message
            }
        except httpx.RequestError as e:
            error_message = f"Request Error: {str(e)}"
            print(error_message, file=sys.stderr)
            return {
                "error": True,
                "message": error_message
            }

# === TOOLS ===

@mcp.tool()
async def list_billing_accounts() -> str:
    """
    List all billing accounts that the user has access to.
    """
    result = await make_google_cloud_billing_request("GET", "/billingAccounts")
    
    if "error" in result:
        return f"Error retrieving billing accounts: {result.get('message', 'Unknown error')}"
    
    accounts = result.get('billingAccounts', [])
    formatted_accounts = []
    
    for account in accounts:
        formatted_accounts.append({
            "name": account.get('name', '').split('/')[-1],
            "display_name": account.get('displayName', 'Unnamed Account'),
            "open": account.get('open', False),
            "master_billing_account": account.get('masterBillingAccount', 'None')
        })
    
    if not formatted_accounts:
        return "No billing accounts found or no access to billing accounts."
    
    return json.dumps(formatted_accounts, indent=2)

@mcp.tool()
async def get_billing_account(account_id: str) -> str:
    """
    Get details about a specific billing account.
    
    Args:
        account_id: The billing account ID (without 'billingAccounts/' prefix)
    """
    if not account_id:
        return "Error: Billing account ID is required."
    
    # Format the billing account ID if it doesn't have the prefix
    if not account_id.startswith("billingAccounts/"):
        account_id = f"billingAccounts/{account_id}"
    
    result = await make_google_cloud_billing_request("GET", f"/{account_id}")
    
    if "error" in result:
        return f"Error retrieving billing account: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    formatted_result = {
        "name": result.get('name', '').split('/')[-1],
        "display_name": result.get('displayName', 'Unnamed Account'),
        "open": result.get('open', False),
        "master_billing_account": result.get('masterBillingAccount', 'None')
    }
    
    return json.dumps(formatted_result, indent=2)

@mcp.tool()
async def list_project_billing_info(project_id: str = None) -> str:
    """
    List billing information for a project.
    
    Args:
        project_id: Optional project ID. If not provided, uses the default project ID from environment variables.
    """
    if not project_id:
        project_id = GOOGLE_CLOUD_BILLING_PROJECT_ID
        
    if not project_id:
        return "Error: Project ID is required but not provided and no default set in environment variables."
    
    result = await make_google_cloud_billing_request("GET", f"/projects/{project_id}/billingInfo")
    
    if "error" in result:
        return f"Error retrieving project billing info: {result.get('message', 'Unknown error')}"
    
    formatted_result = {
        "name": result.get('name', ''),
        "project_id": result.get('projectId', ''),
        "billing_account_name": result.get('billingAccountName', 'Not set'),
        "billing_enabled": result.get('billingEnabled', False)
    }
    
    return json.dumps(formatted_result, indent=2)

@mcp.tool()
async def list_billing_account_projects(account_id: str) -> str:
    """
    List all projects linked to a billing account.
    
    Args:
        account_id: The billing account ID (without 'billingAccounts/' prefix)
    """
    if not account_id:
        return "Error: Billing account ID is required."
    
    # Format the billing account ID if it doesn't have the prefix
    if not account_id.startswith("billingAccounts/"):
        account_id = f"billingAccounts/{account_id}"
    
    result = await make_google_cloud_billing_request("GET", f"/{account_id}/projects")
    
    if "error" in result:
        return f"Error retrieving projects for billing account: {result.get('message', 'Unknown error')}"
    
    projects = result.get('projectBillingInfo', [])
    formatted_projects = []
    
    for project in projects:
        formatted_projects.append({
            "name": project.get('name', ''),
            "project_id": project.get('projectId', ''),
            "billing_enabled": project.get('billingEnabled', False)
        })
    
    if not formatted_projects:
        return "No projects found linked to this billing account."
    
    return json.dumps(formatted_projects, indent=2)

@mcp.tool()
async def get_services_for_billing_account(account_id: str) -> str:
    """
    List all services that are available for a billing account.
    
    Args:
        account_id: The billing account ID (without 'billingAccounts/' prefix)
    """
    if not account_id:
        return "Error: Billing account ID is required."
    
    # Format the billing account ID if it doesn't have the prefix
    if not account_id.startswith("billingAccounts/"):
        account_id = f"billingAccounts/{account_id}"
    
    result = await make_google_cloud_billing_request("GET", f"/{account_id}/services")
    
    if "error" in result:
        return f"Error retrieving services: {result.get('message', 'Unknown error')}"
    
    services = result.get('services', [])
    formatted_services = []
    
    for service in services:
        formatted_services.append({
            "name": service.get('name', '').split('/')[-1],
            "display_name": service.get('displayName', ''),
            "service_id": service.get('serviceId', '')
        })
    
    if not formatted_services:
        return "No services found for this billing account."
    
    return json.dumps(formatted_services, indent=2)

@mcp.tool()
async def get_service_skus(service_id: str, account_id: str) -> str:
    """
    Get SKU information for a particular service.
    
    Args:
        service_id: The service ID (e.g., '6F81-5844-456A')
        account_id: The billing account ID (without 'billingAccounts/' prefix)
    """
    if not service_id or not account_id:
        return "Error: Both service ID and billing account ID are required."
    
    # Format the billing account ID if it doesn't have the prefix
    if not account_id.startswith("billingAccounts/"):
        account_id = f"billingAccounts/{account_id}"
    
    result = await make_google_cloud_billing_request("GET", f"/{account_id}/services/{service_id}/skus")
    
    if "error" in result:
        return f"Error retrieving SKUs: {result.get('message', 'Unknown error')}"
    
    skus = result.get('skus', [])
    formatted_skus = []
    
    for sku in skus:
        formatted_skus.append({
            "name": sku.get('name', ''),
            "sku_id": sku.get('skuId', ''),
            "description": sku.get('description', ''),
            "category": sku.get('category', {}).get('resourceFamily', '') + ' / ' + sku.get('category', {}).get('resourceGroup', ''),
            "pricing_info": "Available" if sku.get('pricingInfo', []) else "Not available"
        })
    
    if not formatted_skus:
        return "No SKUs found for this service."
    
    return json.dumps(formatted_skus, indent=2)

@mcp.tool()
async def get_billing_history(account_id: str, limit: int = 10) -> str:
    """
    Get the billing history for a specific account.
    
    Args:
        account_id: The billing account ID (without 'billingAccounts/' prefix)
        limit: Maximum number of history items to return (default: 10)
    """
    if not account_id:
        return "Error: Billing account ID is required."
    
    # Format the billing account ID if it doesn't have the prefix
    if not account_id.startswith("billingAccounts/"):
        account_id = f"billingAccounts/{account_id}"
    
    # The actual endpoint might vary based on the Google Cloud Billing API documentation
    # This is a hypothetical endpoint
    result = await make_google_cloud_billing_request("GET", f"/{account_id}/billingHistory?maxResults={limit}")
    
    if "error" in result:
        return f"Error retrieving billing history: {result.get('message', 'Unknown error')}"
    
    history_items = result.get('historyItems', [])
    formatted_history = []
    
    for item in history_items:
        formatted_history.append({
            "date": item.get('date', ''),
            "amount": item.get('amount', {}).get('units', 0),
            "currency": item.get('amount', {}).get('currencyCode', 'USD'),
            "description": item.get('description', '')
        })
    
    if not formatted_history:
        return "No billing history found for this account."
    
    return json.dumps(formatted_history, indent=2)

# === RESOURCES ===

@mcp.resource("https://google-cloud-billing/accounts")
async def get_all_billing_accounts() -> str:
    """Get a list of all Google Cloud Billing accounts."""
    result = await make_google_cloud_billing_request("GET", "/billingAccounts")
    
    if "error" in result:
        return f"Error retrieving billing accounts: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("https://google-cloud-billing/account/{account_id}")
async def get_billing_account_resource(account_id: str) -> str:
    """
    Get details of a specific billing account.
    
    Args:
        account_id: The billing account ID
    """
    # Format the billing account ID if it doesn't have the prefix
    if not account_id.startswith("billingAccounts/"):
        account_id = f"billingAccounts/{account_id}"
    
    result = await make_google_cloud_billing_request("GET", f"/{account_id}")
    
    if "error" in result:
        return f"Error retrieving billing account: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("https://google-cloud-billing/project/{project_id}")
async def get_project_billing_info_resource(project_id: str) -> str:
    """
    Get billing information for a specific project.
    
    Args:
        project_id: The project ID
    """
    result = await make_google_cloud_billing_request("GET", f"/projects/{project_id}/billingInfo")
    
    if "error" in result:
        return f"Error retrieving project billing info: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("https://google-cloud-billing/services/{account_id}")
async def get_services_resource(account_id: str) -> str:
    """
    Get all services available for a billing account.
    
    Args:
        account_id: The billing account ID
    """
    # Format the billing account ID if it doesn't have the prefix
    if not account_id.startswith("billingAccounts/"):
        account_id = f"billingAccounts/{account_id}"
    
    result = await make_google_cloud_billing_request("GET", f"/{account_id}/services")
    
    if "error" in result:
        return f"Error retrieving services: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("analyze_billing")
def analyze_billing_prompt(account_id: str = None, period: str = None):
    """
    A prompt template for analyzing Google Cloud Billing data.
    
    Args:
        account_id: ID of the billing account to analyze
        period: Time period to analyze (e.g., "last month", "last quarter")
    """
    if all([account_id, period]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please analyze my Google Cloud Billing data for account {account_id} over the {period} period. What are the main cost drivers and are there any recommendations for optimizing costs?"
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I'd like to analyze my Google Cloud Billing data. Can you help me understand my costs and provide optimization recommendations?"
                    }
                }
            ]
        }

@mcp.prompt("budget_planning")
def budget_planning_prompt(account_id: str = None, monthly_budget: str = None):
    """
    A prompt template for planning a Google Cloud Budget.
    
    Args:
        account_id: ID of the billing account
        monthly_budget: Target monthly budget amount
    """
    if all([account_id, monthly_budget]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"I need to set up a budget of {monthly_budget} for my Google Cloud account {account_id}. Can you help me understand how to allocate this budget across different services and set up proper alerts?"
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to plan a budget for my Google Cloud resources. Can you help me understand how to allocate the budget effectively and set up alerts?"
                    }
                }
            ]
        }

@mcp.prompt("cost_optimization")
def cost_optimization_prompt(service_name: str = None):
    """
    A prompt template for optimizing costs of a specific Google Cloud service.
    
    Args:
        service_name: Name of the service to optimize (e.g., "Compute Engine", "BigQuery")
    """
    if service_name:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"What are the best practices for optimizing costs for Google Cloud {service_name}? Please provide detailed recommendations that I can implement."
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "What are the best practices for optimizing costs in Google Cloud? Please provide general recommendations that can help reduce my cloud spending."
                    }
                }
            ]
        }

if __name__ == "__main__":
    print("Starting Google Cloud Billing MCP server...", file=sys.stderr)
    mcp.run()
