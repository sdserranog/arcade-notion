from dataclasses import dataclass
from typing import Optional, Dict, List, Literal

ParentType = Literal["page", "database"]


@dataclass
class Page:
    """Notion page or database information."""

    id: str
    title: str
    type: Literal["page", "database"]
    parent_type: Optional[ParentType] = None
    parent_id: Optional[str] = None
    url: Optional[str] = None
    last_edited_time: Optional[str] = None


@dataclass
class NotionResult:
    """Result object for Notion API operations."""

    success: bool
    message: str
    data: Optional[Dict] = None
    matches: Optional[List[Page]] = None
