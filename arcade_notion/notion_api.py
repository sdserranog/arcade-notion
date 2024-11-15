import requests
from typing import Dict, Any

NOTION_API_URL = "https://api.notion.com/v1/"
NOTION_VERSION = "2022-06-28"


def get_headers(token: str) -> Dict[str, str]:
    """Generate headers for Notion API requests."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def post_request(endpoint: str, token: str, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a POST request to a Notion API endpoint.

    Args:
        endpoint: API endpoint path
        token: Notion API token
        body: Request body data

    Returns:
        Dictionary with response data or error message
    """
    url = f"{NOTION_API_URL}{endpoint}"
    headers = get_headers(token)

    try:
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        return {"data": response.json(), "error": None}
    except requests.RequestException as e:
        return {"data": None, "error": str(e)}
