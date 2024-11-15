from typing import Annotated

from arcade.sdk import ToolContext, tool
from arcade.sdk.auth import OAuth2

from ..services import create_page_with_parent, find_page_id


@tool(requires_auth=OAuth2(provider_id="notion"))
def create_page_by_parent_title(
    context: ToolContext,
    parent_title: Annotated[
        str,
        "Title of an existing page/database where the new page will be created, no need to include the page ID",
    ],
    title: Annotated[str, "Title for your new page"],
    content: Annotated[str, "Content in markdown format."],
) -> Annotated[str, "Confirmation message with the new page's ID or error message"]:
    """Creates a new page under an existing Notion page or database."""
    # First find the parent page
    parent_result = find_page_id(context, parent_title)
    if not parent_result.success:
        return f"Couldn't find parent page: {parent_result.message}"

    # Then create the new page
    create_result = create_page_with_parent(
        context, title, content, parent_result.data["id"]
    )

    if not create_result.success:
        return f"Found parent but failed to create page: {create_result.message}"

    return f"Created new page under '{parent_title}'! ID: {create_result.data['id']}"
