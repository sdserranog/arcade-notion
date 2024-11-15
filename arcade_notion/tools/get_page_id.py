from typing import Annotated

from arcade.sdk import ToolContext, tool
from arcade.sdk.auth import OAuth2

from ..services import find_page_id


@tool(requires_auth=OAuth2(provider_id="notion"))
def get_page_id(
    context: ToolContext, title: Annotated[str, "Title of the page to find"]
) -> Annotated[str, "Success message with page ID or error message"]:
    """Finds and returns the ID of a Notion page by searching for its title. Only use when page ID is explicitly required."""
    result = find_page_id(context, title)
    return (
        result.message if not result.success else f"Found page! ID: {result.data['id']}"
    )
