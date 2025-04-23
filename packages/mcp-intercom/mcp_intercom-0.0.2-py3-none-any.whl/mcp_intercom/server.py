# server.py
import sys
import os
import json
import httpx
from typing import Dict, List, Optional, Any, Union
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Intercom MCP")

# Environment variables for Intercom configuration
INTERCOM_BASE_URL = os.environ.get("INTERCOM_BASE_URL", "https://api.intercom.io")
INTERCOM_API_KEY = os.environ.get("INTERCOM_API_KEY")
INTERCOM_ACCESS_TOKEN = os.environ.get("INTERCOM_ACCESS_TOKEN")

# Check if environment variables are set
if not INTERCOM_ACCESS_TOKEN and not INTERCOM_API_KEY:
    print("Warning: Intercom environment variables not fully configured. Set INTERCOM_ACCESS_TOKEN or INTERCOM_API_KEY.", file=sys.stderr)

# Helper function for API requests
async def make_intercom_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Make a request to the Intercom API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
    
    Returns:
        Response from Intercom API as dictionary
    """
    url = f"{INTERCOM_BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Use Access Token if available, otherwise use API Key
    if INTERCOM_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {INTERCOM_ACCESS_TOKEN}"
    elif INTERCOM_API_KEY:
        headers["Authorization"] = f"Bearer {INTERCOM_API_KEY}"
    else:
        return {
            "error": True,
            "message": "No authentication credentials provided"
        }
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, timeout=30.0)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data, timeout=30.0)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, timeout=30.0)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            try:
                error_data = e.response.json()
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": error_data.get("message", str(e))
                }
            except:
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": str(e)
                }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }

# === TOOLS ===

@mcp.tool()
async def list_conversations(page: int = 1, per_page: int = 10) -> str:
    """
    List recent conversations in Intercom.
    
    Args:
        page: Page number for pagination (starting at 1)
        per_page: Number of conversations per page (max 60)
    """
    result = await make_intercom_request("GET", f"/conversations?per_page={per_page}&page={page}")
    
    if "error" in result:
        return f"Error retrieving conversations: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_conversation(conversation_id: str) -> str:
    """
    Get details of a specific Intercom conversation.
    
    Args:
        conversation_id: The Intercom conversation ID
    """
    result = await make_intercom_request("GET", f"/conversations/{conversation_id}")
    
    if "error" in result:
        return f"Error retrieving conversation: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def reply_to_conversation(conversation_id: str, message_type: str, message_content: str, admin_id: str = None) -> str:
    """
    Reply to a specific Intercom conversation.
    
    Args:
        conversation_id: The Intercom conversation ID
        message_type: Type of message ('comment' or 'note')
        message_content: Content of the message
        admin_id: Optional admin ID sending the message
    """
    data = {
        "message_type": message_type,
        "body": message_content
    }
    
    if admin_id:
        data["admin_id"] = admin_id
    
    result = await make_intercom_request(
        "POST", 
        f"/conversations/{conversation_id}/reply",
        data
    )
    
    if "error" in result:
        return f"Error replying to conversation: {result.get('message', 'Unknown error')}"
    
    return f"Successfully replied to conversation {conversation_id}"

@mcp.tool()
async def list_contacts(page: int = 1, per_page: int = 10) -> str:
    """
    List contacts in Intercom.
    
    Args:
        page: Page number for pagination (starting at 1)
        per_page: Number of contacts per page (max 60)
    """
    result = await make_intercom_request("GET", f"/contacts?per_page={per_page}&page={page}")
    
    if "error" in result:
        return f"Error retrieving contacts: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_contact(contact_id: str) -> str:
    """
    Get details of a specific Intercom contact.
    
    Args:
        contact_id: The Intercom contact ID
    """
    result = await make_intercom_request("GET", f"/contacts/{contact_id}")
    
    if "error" in result:
        return f"Error retrieving contact: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_contact(email: str = None, phone: str = None, name: str = None, custom_attributes: str = None) -> str:
    """
    Create a new contact in Intercom.
    
    Args:
        email: Email address of the contact
        phone: Phone number of the contact
        name: Name of the contact
        custom_attributes: JSON string of custom attributes
    """
    if not (email or phone):
        return "Error: Either email or phone must be provided"
    
    data = {}
    
    if email:
        data["email"] = email
    
    if phone:
        data["phone"] = phone
    
    if name:
        data["name"] = name
    
    if custom_attributes:
        try:
            custom_attrs_dict = json.loads(custom_attributes)
            data["custom_attributes"] = custom_attrs_dict
        except json.JSONDecodeError:
            return "Error: custom_attributes must be a valid JSON string"
    
    result = await make_intercom_request("POST", "/contacts", data)
    
    if "error" in result:
        return f"Error creating contact: {result.get('message', 'Unknown error')}"
    
    return f"Successfully created contact: {json.dumps(result, indent=2)}"

@mcp.tool()
async def list_companies(page: int = 1, per_page: int = 10) -> str:
    """
    List companies in Intercom.
    
    Args:
        page: Page number for pagination (starting at 1)
        per_page: Number of companies per page (max 60)
    """
    result = await make_intercom_request("GET", f"/companies?per_page={per_page}&page={page}")
    
    if "error" in result:
        return f"Error retrieving companies: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_company(company_id: str) -> str:
    """
    Get details of a specific Intercom company.
    
    Args:
        company_id: The Intercom company ID
    """
    result = await make_intercom_request("GET", f"/companies/{company_id}")
    
    if "error" in result:
        return f"Error retrieving company: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def list_articles(page: int = 1, per_page: int = 10) -> str:
    """
    List help center articles in Intercom.
    
    Args:
        page: Page number for pagination (starting at 1)
        per_page: Number of articles per page (max 60)
    """
    result = await make_intercom_request("GET", f"/articles?per_page={per_page}&page={page}")
    
    if "error" in result:
        return f"Error retrieving articles: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_article(article_id: str) -> str:
    """
    Get details of a specific Intercom help center article.
    
    Args:
        article_id: The Intercom article ID
    """
    result = await make_intercom_request("GET", f"/articles/{article_id}")
    
    if "error" in result:
        return f"Error retrieving article: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def search_contacts(query: str, page: int = 1, per_page: int = 10) -> str:
    """
    Search for contacts in Intercom.
    
    Args:
        query: Search query string
        page: Page number for pagination (starting at 1)
        per_page: Number of results per page (max 60)
    """
    data = {
        "query": {
            "field": "email",
            "operator": "~",
            "value": query
        },
        "pagination": {
            "page": page,
            "per_page": per_page
        }
    }
    
    result = await make_intercom_request("POST", "/contacts/search", data)
    
    if "error" in result:
        return f"Error searching contacts: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === RESOURCES ===

@mcp.resource("intercom://conversations")
async def get_recent_conversations() -> str:
    """Get a list of recent Intercom conversations."""
    result = await make_intercom_request("GET", "/conversations?per_page=10")
    
    if "error" in result:
        return f"Error retrieving conversations: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("intercom://contacts")
async def get_recent_contacts() -> str:
    """Get a list of recent Intercom contacts."""
    result = await make_intercom_request("GET", "/contacts?per_page=10")
    
    if "error" in result:
        return f"Error retrieving contacts: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("intercom://teams")
async def get_teams() -> str:
    """Get a list of Intercom teams."""
    result = await make_intercom_request("GET", "/teams")
    
    if "error" in result:
        return f"Error retrieving teams: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("intercom://admins")
async def get_admins() -> str:
    """Get a list of Intercom admins."""
    result = await make_intercom_request("GET", "/admins")
    
    if "error" in result:
        return f"Error retrieving admins: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("intercom://companies")
async def get_recent_companies() -> str:
    """Get a list of recent Intercom companies."""
    result = await make_intercom_request("GET", "/companies?per_page=10")
    
    if "error" in result:
        return f"Error retrieving companies: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("create_contact")
def create_contact_prompt(email: str = None, name: str = None, phone: str = None):
    """
    A prompt template for creating a new contact in Intercom.
    
    Args:
        email: Email address of the contact
        name: Name of the contact
        phone: Phone number of the contact
    """
    if all([email, name]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me create a new Intercom contact with these details:\n\nName: {name}\nEmail: {email}" + (f"\nPhone: {phone}" if phone else "")
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
                        "text": f"I need to create a new contact in Intercom. Please help me with the required details."
                    }
                }
            ]
        }

@mcp.prompt("reply_to_conversation")
def reply_to_conversation_prompt(conversation_id: str = None, message_content: str = None):
    """
    A prompt template for replying to a conversation in Intercom.
    
    Args:
        conversation_id: ID of the conversation
        message_content: Content of the reply
    """
    if all([conversation_id, message_content]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me reply to Intercom conversation {conversation_id} with the following message:\n\n{message_content}"
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
                        "text": f"I need to reply to an Intercom conversation. Please help me with the required details."
                    }
                }
            ]
        }

@mcp.prompt("search_knowledge_base")
def search_knowledge_base_prompt(query: str = None):
    """
    A prompt template for searching Intercom's knowledge base.
    
    Args:
        query: Search query
    """
    if query:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me search Intercom's knowledge base for information about: {query}"
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
                        "text": f"I'd like to search Intercom's knowledge base. What would you like to know about?"
                    }
                }
            ]
        }

if __name__ == "__main__":
    print("Starting Intercom MCP server...", file=sys.stderr)
    mcp.run()
