from typing import Dict, List, Optional, Tuple

from arcade.sdk import ToolContext
from loguru import logger

from .markdown_processor import parse_markdown
from .notion_api import post_request
from .types import NotionResult, Page, ParentType


def parse_page_from_result(result: Dict) -> Optional[Page]:
    """Extract page information from Notion API result."""
    try:
        properties = result.get("properties", {})
        for field in ["title", "Title", "name", "Name"]:
            if title_field := properties.get(field, {}).get("title", []):
                title = title_field[0].get("text", {}).get("content", "Untitled")
                break
        else:
            title = "Untitled"

        parent = result.get("parent", {})
        parent_type = parent.get("type")

        return Page(
            id=result["id"],
            title=title,
            type=result["object"],
            parent_type=parent_type,
            parent_id=parent.get(parent_type),
            url=result.get("url"),
            last_edited_time=result.get("last_edited_time"),
        )
    except Exception as e:
        logger.error(f"Failed to parse page: {e}")
        return None


def find_best_match(pages: List[Page], query: str) -> Tuple[Page, str]:
    """Find the best matching page from a list."""
    query = query.lower()

    # Try exact match first
    if exact_matches := [p for p in pages if p.title.lower() == query]:
        return exact_matches[0], "exact match"

    # Try partial match next
    if partial_matches := [p for p in pages if query in p.title.lower()]:
        return partial_matches[0], "similar match"

    # Return most recent as fallback
    return pages[0], "potential match"


def find_page_id(
    context: ToolContext,
    title: str,
    get_all: bool = True,
    page_type: Optional[ParentType] = None,
) -> NotionResult:
    """
    Find Notion pages by title.
    Returns the best match and optionally all matching results.
    """
    response = post_request(
        "search",
        context.authorization.token,
        {
            "query": title,
            "sort": {"direction": "descending", "timestamp": "last_edited_time"},
            "page_size": 10,
        },
    )

    if response["error"]:
        return NotionResult(
            success=False, message=f"Search failed: {response['error']}"
        )

    # Get and filter valid pages
    pages = [
        page
        for result in response["data"].get("results", [])
        if (page := parse_page_from_result(result))
        and (not page_type or page.type == page_type)
    ]

    if not pages:
        type_msg = f" of type '{page_type}'" if page_type else ""
        return NotionResult(
            success=False, message=f"No pages{type_msg} found with title: {title}"
        )

    # Find best match
    best_match, match_type = find_best_match(pages, title)

    return NotionResult(
        success=True,
        message=(
            f"Found {match_type}: '{best_match.title}'"
            f"{f' ({len(pages)} total results)' if get_all else ''}"
        ),
        data={"id": best_match.id, "type": best_match.type},
        matches=pages if get_all else None,
    )


def create_page_with_parent(
    context: ToolContext,
    title: str,
    content: str,
    parent_id: str,
    parent_type: ParentType = "page",
) -> NotionResult:
    """Create a new Notion page under a parent page or database."""
    body = {
        "parent": {"database_id": parent_id}
        if parent_type == "database"
        else {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "children": parse_markdown(content),
    }

    response = post_request("pages", context.authorization.token, body)

    if response["error"]:
        logger.error(f"Page creation failed: {response['error']}")
        return NotionResult(
            success=False, message=f"Creation failed: {response['error']}"
        )

    if not (page_id := response["data"].get("id")):
        return NotionResult(success=False, message="No page ID received from Notion")

    return NotionResult(
        success=True, message="Page created successfully", data={"id": page_id}
    )
