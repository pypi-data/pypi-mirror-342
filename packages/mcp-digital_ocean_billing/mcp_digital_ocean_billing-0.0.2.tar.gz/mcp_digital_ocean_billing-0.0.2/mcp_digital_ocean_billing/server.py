# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Digital Ocean Billing MCP")

# Environment variables for Digital Ocean Billing configuration
DIGITAL_OCEAN_BILLING_BASE_URL = os.environ.get("DIGITAL_OCEAN_BILLING_BASE_URL", "https://api.digitalocean.com/v2")
DIGITAL_OCEAN_BILLING_API_KEY = os.environ.get("DIGITAL_OCEAN_BILLING_API_KEY")

# Check if environment variables are set
if not DIGITAL_OCEAN_BILLING_API_KEY:
    print("Warning: Digital Ocean Billing environment variables not fully configured. Set DIGITAL_OCEAN_BILLING_API_KEY.", file=sys.stderr)

# Helper function for API requests
async def make_digital_ocean_billing_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Make a request to the Digital Ocean Billing API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
    
    Returns:
        Response from Digital Ocean Billing API as dictionary
    """
    url = f"{DIGITAL_OCEAN_BILLING_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {DIGITAL_OCEAN_BILLING_API_KEY}",
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
            return {
                "error": True,
                "status_code": e.response.status_code,
                "message": e.response.text
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }

# === TOOLS ===

@mcp.tool()
async def get_account_balance() -> str:
    """
    Get the current account balance for your Digital Ocean account.
    """
    result = await make_digital_ocean_billing_request("GET", "/customers/my/balance")
    
    if "error" in result:
        return f"Error retrieving account balance: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    balance_info = result
    formatted_balance = f"""
Account Balance:
- Month-to-date Usage: ${balance_info.get('month_to_date_usage', 'N/A')}
- Account Balance: ${balance_info.get('account_balance', 'N/A')}
- Month-to-date Balance: ${balance_info.get('month_to_date_balance', 'N/A')}
- Generated At: {balance_info.get('generated_at', 'N/A')}
"""
    return formatted_balance

@mcp.tool()
async def get_billing_history(page: int = 1, per_page: int = 20) -> str:
    """
    Get the billing history for your Digital Ocean account.
    
    Args:
        page: Page number for pagination (default: 1)
        per_page: Number of items per page (default: 20)
    """
    result = await make_digital_ocean_billing_request("GET", f"/customers/my/billing_history?page={page}&per_page={per_page}")
    
    if "error" in result:
        return f"Error retrieving billing history: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    billing_history = result.get('billing_history', [])
    if not billing_history:
        return "No billing history found."
    
    formatted_history = "Billing History:\n\n"
    for item in billing_history:
        formatted_history += f"""
- Date: {item.get('date', 'N/A')}
  Type: {item.get('type', 'N/A')}
  Description: {item.get('description', 'N/A')}
  Amount: ${item.get('amount', 'N/A')}
"""
    
    # Add pagination info
    meta = result.get('meta', {})
    formatted_history += f"\nPage {page} of {meta.get('total_pages', 'unknown')} (Total items: {meta.get('total', 'unknown')})"
    
    return formatted_history

@mcp.tool()
async def get_invoice_list(page: int = 1, per_page: int = 20) -> str:
    """
    Get a list of invoices for your Digital Ocean account.
    
    Args:
        page: Page number for pagination (default: 1)
        per_page: Number of items per page (default: 20)
    """
    result = await make_digital_ocean_billing_request("GET", f"/customers/my/invoices?page={page}&per_page={per_page}")
    
    if "error" in result:
        return f"Error retrieving invoices: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    invoices = result.get('invoices', [])
    if not invoices:
        return "No invoices found."
    
    formatted_invoices = "Invoice List:\n\n"
    for invoice in invoices:
        formatted_invoices += f"""
- Invoice UUID: {invoice.get('invoice_uuid', 'N/A')}
  Amount: ${invoice.get('amount', 'N/A')}
  Date: {invoice.get('invoice_period', 'N/A')}
  Status: {invoice.get('status', 'N/A')}
"""
    
    # Add pagination info
    meta = result.get('meta', {})
    formatted_invoices += f"\nPage {page} of {meta.get('total_pages', 'unknown')} (Total items: {meta.get('total', 'unknown')})"
    
    return formatted_invoices

@mcp.tool()
async def get_invoice_detail(invoice_uuid: str) -> str:
    """
    Get detailed information about a specific invoice.
    
    Args:
        invoice_uuid: The UUID of the invoice to retrieve
    """
    result = await make_digital_ocean_billing_request("GET", f"/customers/my/invoices/{invoice_uuid}")
    
    if "error" in result:
        return f"Error retrieving invoice details: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    invoice = result.get('invoice', {})
    if not invoice:
        return f"No invoice found with UUID: {invoice_uuid}"
    
    formatted_invoice = f"""
Invoice Details:
- Invoice UUID: {invoice.get('invoice_uuid', 'N/A')}
- Amount: ${invoice.get('amount', 'N/A')}
- Invoice Period: {invoice.get('invoice_period', 'N/A')}
- Status: {invoice.get('status', 'N/A')}
- Product Charges: ${invoice.get('product_charges', {}).get('amount', 'N/A')}
- Tax: ${invoice.get('tax', 'N/A')}
- Credits Applied: ${invoice.get('credits_applied', 'N/A')}

Line Items:
"""
    
    for item in invoice.get('product_charges', {}).get('items', []):
        formatted_invoice += f"""
  - Name: {item.get('name', 'N/A')}
    Amount: ${item.get('amount', 'N/A')}
    Count: {item.get('count', 'N/A')}
"""
    
    return formatted_invoice

# === RESOURCES ===

@mcp.resource("https://digital-ocean-billing/balance")
async def get_balance_resource() -> str:
    """Get the current account balance for your Digital Ocean account."""
    result = await make_digital_ocean_billing_request("GET", "/customers/my/balance")
    
    if "error" in result:
        return f"Error retrieving account balance: {result.get('message', 'Unknown error')}"
    
    # Return the raw JSON for the resource
    return json.dumps(result, indent=2)

@mcp.resource("https://digital-ocean-billing/billing_history")
async def get_billing_history_resource() -> str:
    """Get the billing history for your Digital Ocean account."""
    result = await make_digital_ocean_billing_request("GET", "/customers/my/billing_history")
    
    if "error" in result:
        return f"Error retrieving billing history: {result.get('message', 'Unknown error')}"
    
    # Return the raw JSON for the resource
    return json.dumps(result, indent=2)

@mcp.resource("https://digital-ocean-billing/invoices")
async def get_invoices_resource() -> str:
    """Get a list of invoices for your Digital Ocean account."""
    result = await make_digital_ocean_billing_request("GET", "/customers/my/invoices")
    
    if "error" in result:
        return f"Error retrieving invoices: {result.get('message', 'Unknown error')}"
    
    # Return the raw JSON for the resource
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("check_billing_summary")
def check_billing_summary_prompt():
    """
    A prompt template for checking Digital Ocean billing summary.
    """
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": "Please provide a summary of my current Digital Ocean billing status, including my current balance and recent charges."
                }
            }
        ]
    }

@mcp.prompt("analyze_invoice")
def analyze_invoice_prompt(invoice_uuid: str = None):
    """
    A prompt template for analyzing a specific Digital Ocean invoice.
    
    Args:
        invoice_uuid: UUID of the invoice to analyze
    """
    if invoice_uuid:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please analyze my Digital Ocean invoice with UUID {invoice_uuid} and explain the charges in detail."
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
                        "text": "I'd like to analyze one of my Digital Ocean invoices. Please help me understand the charges and if there are any ways to optimize my spending."
                    }
                }
            ]
        }

@mcp.prompt("cost_optimization")
def cost_optimization_prompt():
    """
    A prompt template for getting Digital Ocean cost optimization recommendations.
    """
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": "Based on my Digital Ocean billing history, can you suggest ways to optimize my costs and reduce unnecessary spending?"
                }
            }
        ]
    }

if __name__ == "__main__":
    print("Starting Digital Ocean Billing MCP server...", file=sys.stderr)
    mcp.run()
