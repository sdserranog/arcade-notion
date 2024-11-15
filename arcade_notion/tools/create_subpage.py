from typing import Annotated

from arcade.sdk import ToolContext, tool
from arcade.sdk.auth import OAuth2

from ..services import create_page_with_parent


@tool(requires_auth=OAuth2(provider_id="notion"))
def create_subpage(
    context: ToolContext,
    parent_id: Annotated[str, "ID of the parent page"],
    title: Annotated[str, "Title for the new page"],
    content: Annotated[str, "Content in markdown format."],
) -> Annotated[str, "Success/error message"]:
    """Create a new page under a parent page using its ID."""
    result = create_page_with_parent(context, title, content, parent_id)
    return (
        result.message
        if not result.success
        else f"Created page! ID: {result.data['id']}"
    )
