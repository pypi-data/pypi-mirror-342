# Intercom MCP Server

A Model Context Protocol (MCP) server for Intercom integration. This server provides tools for interacting with Intercom, including managing conversations, contacts, companies, and help center articles.

## Features

- **Conversation Management**: List, view, and reply to customer conversations
- **Contact Management**: Create, search, and view user contacts
- **Company Management**: List and view companies
- **Help Center**: Access articles and content
- **Team Management**: View teams and admins
- **Resources**: Direct access to Intercom data
- **Prompts**: Templates for common Intercom workflows

## Installation

```bash
pip install mcp-intercom
```

## Configuration

Set the following environment variables:

```bash
export INTERCOM_BASE_URL="https://api.intercom.io"  # Default value, usually doesn't need changing
export INTERCOM_ACCESS_TOKEN="your_access_token"    # Preferred authentication method
# OR
export INTERCOM_API_KEY="your_api_key"              # Alternative authentication method
```

You'll need to create an Intercom access token with appropriate permissions from your Intercom Developer Hub.

## Usage

### Starting the server directly

```bash
mcp-intercom
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
"mcp-intercom": {
  "command": "uvx",
  "args": [
    "mcp-intercom"
  ],
  "env": {
    "INTERCOM_ACCESS_TOKEN": "your_access_token"
  }
}
```

Replace the environment variables with your actual Intercom credentials.

## Available Tools

* **list_conversations**: List recent conversations in Intercom
* **get_conversation**: Get details of a specific conversation
* **reply_to_conversation**: Reply to a conversation as a comment or note
* **list_contacts**: List contacts in Intercom
* **get_contact**: Get details of a specific contact
* **create_contact**: Create a new contact
* **list_companies**: List companies in Intercom
* **get_company**: Get details of a specific company
* **list_articles**: List help center articles
* **get_article**: Get details of a specific article
* **search_contacts**: Search for contacts with a query

## Available Resources

* **intercom://conversations**: List of recent conversations
* **intercom://contacts**: List of recent contacts
* **intercom://teams**: List of teams in your Intercom workspace
* **intercom://admins**: List of admin users in your Intercom workspace
* **intercom://companies**: List of recent companies

## Available Prompts

* **create_contact**: Template for creating a new contact
* **reply_to_conversation**: Template for replying to a conversation
* **search_knowledge_base**: Template for searching Intercom's knowledge base

## Example Usage

With Claude or another AI assistant, you can ask natural language questions like:

- "What are my recent Intercom conversations?"
- "Show me details for contact with email john@example.com"
- "Reply to conversation abc123 saying 'Thanks for reaching out!'"
- "Create a new contact with email jane@example.com and name Jane Smith"

## Development

To contribute to this project:

```bash
git clone https://github.com/yourusername/mcp-intercom.git
cd mcp-intercom
pip install -e .
```

## Version

0.0.1
